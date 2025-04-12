# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for storing experiment data, metadata, and transformers. See ExperimentStore for details."""
import tempfile
from typing import cast, Any, Dict, List, Mapping, MutableMapping, Optional, Tuple, Union, Sequence
from abc import abstractmethod, ABC
import logging
import pathlib
import pickle
import gc
import os

import numpy as np
import pandas as pd
from scipy import sparse
from collections import defaultdict

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.inference import inference
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.runtime._data_definition import MaterializedTabularData
from azureml.automl.runtime.shared._cache_constants import Keys
from azureml.automl.runtime.shared.utilities import issparse
from azureml.core import Dataset, Run, Workspace

from azureml.automl.core.constants import SupportedTransformersInternal
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import AutoMLInternalLogSafe
from azureml.automl.core.shared.constants import MLTableDataLabel
from azureml.automl.core.shared.exceptions import ClientException, ValidationException
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.constants import FeaturizationConfigMode

from azureml.automl.runtime.shared._cv_splits import FeaturizedCVSplit
from azureml.automl.runtime.shared.file_dataset_cache import FileDatasetCache
from azureml.automl.runtime.shared.run_backed_cache_store import RunBackedCacheStore
from azureml.automl.runtime.shared.model_wrappers import DropColumnsTransformer
from azureml.core.datastore import Datastore
from azureml.core.run import LinkOutput
from azureml.data.dataset_factory import TabularDatasetFactory
from azureml.data import DataType
from azureml.training.tabular.featurization.timeseries._distributed.timeseries_data_profile import \
    AggregatedTimeSeriesDataProfile


_READ_ONLY_ERROR_MESSAGE = "Unable to set attributes on read only store."
_CV_NOT_FOUND_MESSAGE = "CV split '{}' not found."

logger = logging.getLogger(__name__)

try:
    import mlflow
    has_mlflow = True
except ImportError:
    has_mlflow = False


class _CacheableStoreABC(ABC):
    """The abstract object for a cacheable object in an ExperimentStore."""

    @abstractmethod
    def _load(self):
        ...

    @abstractmethod
    def _unload(self):
        ...


class _CacheableStoreBase(_CacheableStoreABC):
    """The base object for any part of an ExperimentStore."""

    def __init__(self, cache, read_only):
        self._cache = cache
        self._read_only = read_only

    def __getstate__(self):
        state = self.__dict__.copy()
        # These entries should always be set on the ExperimentStore.
        del state["_cache"]
        del state["_read_only"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


class _CVSplitsCollection(MutableMapping[Union[str, int], FeaturizedCVSplit]):
    """
    Object for storing featurized CV splits.

    This object is only be used by ExperimentData.

    This object handles custom read/writes to a mutable mapping allowing
    for caching without need to load/unload by users. All key/value pairs
    are stored in the Cache. A read from the collection results in a two
    cache look ups - 1 to check if the key is in the dictionary, 1 to
    retrieve the value. A write to the collection results in 1 read and
    2 writes - the first read is required to update the keys in the dictionary,
    while the 2 writes handle the added key and value.
    """

    split_keys = Keys.SPLIT_KEYS

    def __init__(self, cache, read_only):
        self._cache = cache
        self._read_only = read_only

    def __getitem__(self, key):
        if key in self._cache.get([self.split_keys])[self.split_keys]:
            return self._cache.get([key])[key]
        else:
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe,
                    target="get_cv_split",
                    error_message=_CV_NOT_FOUND_MESSAGE.format(key),
                    error_details=_CV_NOT_FOUND_MESSAGE.format(key),
                )
            )

    def __setitem__(self, key, value):
        if self._read_only:
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe,
                    target="set_cv_split",
                    error_message=_READ_ONLY_ERROR_MESSAGE,
                    error_details=_READ_ONLY_ERROR_MESSAGE,
                )
            )
        else:
            # Only check split keys from cache if we know the split_keys are
            # in the cache. If the split_keys key is not yet cached, we know we
            # are on the first item in the list.
            if self.split_keys in self._cache.cache_items:
                splits = self._cache.get([self.split_keys])[self.split_keys]
            else:
                splits = []

            if key not in splits:
                splits.append(key)
                self._cache.set(self.split_keys, splits)
            self._cache.set(key, value)

    def __iter__(self):
        keys = self._cache.get([self.split_keys])[self.split_keys]
        self._cur_key = 0
        self._keys = keys
        return self

    def __next__(self):
        if self._keys and self._cur_key < len(self._keys):
            res = self._cache.get([self._keys[self._cur_key]])[self._keys[self._cur_key]]
            self._cur_key += 1
            return res
        else:
            raise StopIteration

    def __len__(self):
        keys = self._cache.get([self.split_keys])[self.split_keys]
        return len(keys) if keys else 0

    def __delitem__(self, item: Union[str, int]) -> None:
        if self._read_only:
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe,
                    target="del_cv_split",
                    error_message=_READ_ONLY_ERROR_MESSAGE,
                    error_details=_READ_ONLY_ERROR_MESSAGE,
                )
            )
        else:
            keys = self._cache.get([self.split_keys])[self.split_keys]
            if item in keys:
                keys.remove(item)
                self._cache.remove(item)
                self._cache.set(self.split_keys, keys)
            else:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternalLogSafe,
                        target="del_cv_split",
                        error_message=_CV_NOT_FOUND_MESSAGE.format(item),
                        error_details=_CV_NOT_FOUND_MESSAGE.format(item),
                    )
                )


class ExperimentData(_CacheableStoreBase):
    """
    The object containing data for a given Experiment.

    This object should only be used by the ExperimentStore.

    Information stored in this object can be memory- or cache-backed.

    ExperimentData represents any data which may be used throughout a job. There are two types of
    data formats which can be accessed - materialized and lazy. Materialized data represents data
    which can be materialized entirely in memory. Materialized data is typically stored as a pandas
    dataframe. Lazy data represents data which is too large to fit into memory and must be streamed
    as it is used. Lazy data is typically stored as a TabularDataset. Materialized data will always
    be cache-backed data.
    """

    class MaterializedData(_CacheableStoreBase):
        """
        Object containing materialized data within the ExperimentStore.

        materialized data is any data which can be stored in memory
        (typically pandas dataframes or numpy arrays). As this data is
        always stored in memory, all attributes are cache-backed. If
        the ExperimentStore is loaded as read-only, writes to these attributes
        will raise an exception.

        Data stored here is stored in the form X, y, sample_weight.
        Available data groups are - train, valid, test, raw, cv_splits.

        CV splits are implemented through the _CVSplitsCollection object
        which is a cache-backed mutable mapping.
        """

        def __init__(self, cache, read_only):
            super().__init__(cache, read_only)
            self.cv_splits = _CVSplitsCollection(cache, read_only)
            self._dataset_paths = defaultdict(str)

        def get_test(self):
            """
            Retrieves test data stored in the cache store.

            We first try to retrieve the merged dataframe
            that would have been stored with the key `Keys.FULL_TEST`. If that fails, we attempt to retrieve
            using individual keys `Keys.X_TEST`, `Keys.Y_TEST`, `Keys.SW_TEST`.

            :return: A tuple of X_test, y_test, sample_weight_test
            """
            path = self._dataset_paths['test']
            key = path + Keys.FULL_TEST

            ret = self._cache.get([key])  # type: Dict[str, pd.DataFrame]
            if ret is not None:
                merged_df = ret.get(key, None)  # type: pd.DataFrame
                if merged_df is not None:
                    return get_x_y_sample_weight_from_merged_df(merged_df)
                else:
                    separate_keys = [path + Keys.X_TEST,
                                     path + Keys.Y_TEST,
                                     path + Keys.SW_TEST]
                    ret = self._cache.get(separate_keys)
                    return ret[separate_keys[0]], ret[separate_keys[1]], ret[separate_keys[2]]

        def set_test(
            self,
            X: Union[np.ndarray, pd.DataFrame, sparse.spmatrix],
            y: Union[np.ndarray, pd.Series],
            sample_weight: Optional[Union[np.ndarray, pd.Series]],
            featurization: Union[str, FeaturizationConfig] = FeaturizationConfigMode.Off,
        ) -> None:
            if self._read_only:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternalLogSafe,
                        target="set_test",
                        error_message=_READ_ONLY_ERROR_MESSAGE,
                        error_details=_READ_ONLY_ERROR_MESSAGE,
                    )
                )
            else:
                key_list = [Keys.X_TEST, Keys.Y_TEST, Keys.SW_TEST, Keys.FULL_TEST]

                if featurization != FeaturizationConfigMode.Off:
                    self._dataset_paths['test'] = Keys.FEATURIZATION_DATA_NAMESPACE
                    key_list = [Keys.FEATURIZATION_DATA_NAMESPACE + key for key in key_list]

                merged_df = None
                if issparse(X) is False:
                    merged_df = _create_merged_x_y_sample_weight(X, y, sample_weight)

                if merged_df is None:
                    self._cache.add([key_list[0], key_list[1], key_list[2]], [X, y, sample_weight])
                else:
                    self._cache.set(key_list[3], merged_df)

        def get_train(self):
            """
            Retrieves train data stored in the cache store.

            We first try to retrieve the merged dataframe
            that would have been stored with the key `Keys.FULL_TRAIN`. If that fails, we attempt to retrieve
            using individual keys `Keys.X_TRAIN`, `Keys.Y_TRAIN`, `Keys.SW_TRAIN`.

            :return: A tuple of X_train, y_train, sample_weight_train
            """
            path = self._dataset_paths['train']
            key = path + Keys.FULL_TRAIN
            ret = self._cache.get([key])
            if ret is not None:
                merged_df = ret.get(key, None)  # type: pd.DataFrame
                if merged_df is not None:
                    return get_x_y_sample_weight_from_merged_df(merged_df)
                else:
                    separate_keys = [path + Keys.X_TRAIN,
                                     path + Keys.Y_TRAIN,
                                     path + Keys.SW_TRAIN]
                    ret = self._cache.get(separate_keys)
                    return ret[separate_keys[0]], ret[separate_keys[1]], ret[separate_keys[2]]

        def set_train(
            self,
            X: Union[pd.DataFrame, np.ndarray, sparse.spmatrix],
            y: Union[pd.Series, np.ndarray],
            sample_weight: Optional[Union[pd.Series, np.ndarray]],
            featurization: Union[str, FeaturizationConfig] = FeaturizationConfigMode.Off,
        ) -> None:
            """
            Writes the training data to the cache.

            If the data is not sparse and can be merged into a single dataframe, we attempt to do it. If successful,
            the merged dataframe is written to a single file in the cache with the key `Keys.FULL_TRAIN`.
            If the merge fails, we store the training data as three different datasets with keys `Keys.X_TRAIN`,
            `Keys.Y_TRAIN`, `Keys.SW_TRAIN`.

            :param X: Training features.
            :param y: Training labels or target values.
            :param sample_weight: Sample weight.
            :param featurization: Featurization mode selected
            """
            if self._read_only:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternalLogSafe,
                        target="set_train",
                        error_message=_READ_ONLY_ERROR_MESSAGE,
                        error_details=_READ_ONLY_ERROR_MESSAGE,
                    )
                )
            else:
                key_list = [Keys.X_TRAIN, Keys.Y_TRAIN, Keys.SW_TRAIN, Keys.FULL_TRAIN]

                if featurization != FeaturizationConfigMode.Off:
                    self._dataset_paths['train'] = Keys.FEATURIZATION_DATA_NAMESPACE
                    key_list = [Keys.FEATURIZATION_DATA_NAMESPACE + key for key in key_list]

                merged_df = None
                if issparse(X) is False:
                    merged_df = _create_merged_x_y_sample_weight(X, y, sample_weight)

                if merged_df is None:
                    self._cache.add([key_list[0], key_list[1], key_list[2]], [X, y, sample_weight])
                else:
                    self._cache.set(key_list[3], merged_df)

        def get_raw(self) -> Tuple[Any, Any, Any, Any]:
            keys = [Keys.X_RAW, Keys.Y_RAW, Keys.X_RAW_VALID, Keys.Y_RAW_VALID]
            ret = self._cache.get(keys)
            return ret[keys[0]], ret[keys[1]], ret[keys[2]], ret[keys[3]]

        def set_raw(self, X, y, X_valid, y_valid):
            if self._read_only:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternalLogSafe,
                        target="set_raw",
                        error_message=_READ_ONLY_ERROR_MESSAGE,
                        error_details=_READ_ONLY_ERROR_MESSAGE,
                    )
                )
            else:
                self._cache.add(
                    [Keys.X_RAW, Keys.Y_RAW, Keys.X_RAW_VALID, Keys.Y_RAW_VALID],
                    [X, y, X_valid, y_valid]
                )

        def get_valid(self):
            """
            Retrieves validation data stored in the cache store.

            We first try to retrieve the merged dataframe
            that would have been stored with the key `Keys.FULL_VALIDATION`. If that fails, we attempt to retrieve
            using individual keys `Keys.X_VALIDATION`, `Keys.Y_VALIDATION`, `Keys.SW_VALIDATION`.

            :return: A tuple of X_validation, y_validation, sample_weight_validation
            """
            path = self._dataset_paths['valid']
            key = path + Keys.FULL_VALIDATION
            ret = self._cache.get([key])    # type: Dict[str, pd.DataFrame]
            if ret is not None:
                merged_df = ret.get(key, None)  # type: pd.DataFrame
                if merged_df is not None:
                    return get_x_y_sample_weight_from_merged_df(merged_df)
                else:
                    separate_keys = [path + Keys.X_VALID,
                                     path + Keys.Y_VALID,
                                     path + Keys.SW_VALID]
                    ret = self._cache.get(separate_keys)
                    return ret[separate_keys[0]], ret[separate_keys[1]], ret[separate_keys[2]]

        def set_valid(
            self,
            X: Union[pd.DataFrame, np.ndarray, sparse.spmatrix],
            y: Union[pd.Series, np.ndarray],
            sample_weight: Optional[Union[pd.Series, np.ndarray]],
            featurization: Union[str, FeaturizationConfig] = FeaturizationConfigMode.Off,
        ) -> None:
            """
            Writes the validation data to the cache.
            """
            if self._read_only:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternalLogSafe,
                        target="set_valid",
                        error_message=_READ_ONLY_ERROR_MESSAGE,
                        error_details=_READ_ONLY_ERROR_MESSAGE,
                    )
                )
            else:
                key_list = [Keys.X_VALID, Keys.Y_VALID, Keys.SW_VALID, Keys.FULL_VALIDATION]
                if featurization != FeaturizationConfigMode.Off:
                    self._dataset_paths['valid'] = Keys.FEATURIZATION_DATA_NAMESPACE
                    key_list = [Keys.FEATURIZATION_DATA_NAMESPACE + key for key in key_list]

                merged_df = None
                if issparse(X) is False:
                    merged_df = _create_merged_x_y_sample_weight(X, y, sample_weight)

                if merged_df is None:
                    self._cache.add([key_list[0], key_list[1], key_list[2]], [X, y, sample_weight])
                else:
                    self._cache.set(key_list[3], merged_df)

        def get_CV_splits(self):
            for split in self.cv_splits:
                yield (split)

        def _load(self):
            materialized_data_bytes = cast(
                bytes, self._cache.get([Keys.EXPERIMENT_DATA_MATERIALIZED])[Keys.EXPERIMENT_DATA_MATERIALIZED]
            )
            self._dataset_paths = pickle.loads(materialized_data_bytes)

        def _unload(self):
            self._cache.set(Keys.EXPERIMENT_DATA_MATERIALIZED, pickle.dumps(self._dataset_paths))

    class LazyData(_CacheableStoreBase):
        """
        Object containing lazy data within the ExperimentStore.

        Lazy data is any data which need be loaded into memory prior to
        use (typically dataset objects). As this data is only materialized
        on demand, these attributes are all memory-backed.

        Data stored here is stored in the form Data, label_column_name,
        sample_weight_column_name. This object supports retrieval of data
        in the form X, y, sw and data, label_name, sw_name.
        """

        def __init__(self, cache, read_only):
            super().__init__(cache, read_only)
            self._training_dataset = None
            self._validation_dataset = None
            self._label_column_name = ""
            self._weight_column_name = None

        def get_training_dataset(self):
            """
            Get the training dataset.

            Returns the data in the from dataset, label column name, sample weight column name.
            """
            return (
                self._training_dataset,
                self._label_column_name,
                self._weight_column_name,
            )

        def set_training_dataset(self, dataset, label_column_name, weight_column_name):
            """
            Set the training data.

            Sets the values for training dataset, label column name, and optionally weight column name.
            :param dataset: The TabularDataset to be stored.
            :param label_column_name: The label column name from the dataset.
            :param weight_column_name: If present, the name of the sample weight column from the dataset.
            """
            if self._read_only:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternalLogSafe,
                        target="set_training_dataset",
                        error_message=_READ_ONLY_ERROR_MESSAGE,
                        error_details=_READ_ONLY_ERROR_MESSAGE,
                    )
                )
            else:
                self._training_dataset = dataset
                self._label_column_name = label_column_name
                if weight_column_name:
                    self._weight_column_name = weight_column_name

        def _get_X_train(self):
            columns_to_drop = []
            if self._label_column_name is not None:
                columns_to_drop.append(self._label_column_name)
            if self._weight_column_name is not None:
                columns_to_drop.append(self._weight_column_name)

            if self._training_dataset is not None:
                return self._training_dataset.drop_columns(columns_to_drop)
            else:
                return None

        def _get_y_train(self):
            if self._label_column_name and self._training_dataset is not None:
                return self._training_dataset.keep_columns([self._label_column_name])
            else:
                return None

        def _get_sw_train(self):
            if self._weight_column_name and self._training_dataset is not None:
                return self._training_dataset.keep_columns([self._weight_column_name])
            else:
                return None

        def _get_X_valid(self):
            columns_to_drop = []
            if self._label_column_name is not None:
                columns_to_drop.append(self._label_column_name)
            if self._weight_column_name is not None:
                columns_to_drop.append(self._weight_column_name)

            if self._validation_dataset is not None:
                return self._validation_dataset.drop_columns(columns_to_drop)
            else:
                return None

        def _get_y_valid(self):
            if self._label_column_name and self._validation_dataset is not None:
                return self._validation_dataset.keep_columns([self._label_column_name])
            else:
                return None

        def _get_sw_valid(self):
            if self._weight_column_name and self._validation_dataset is not None:
                return self._validation_dataset.keep_columns([self._weight_column_name])
            else:
                return None

        def get_train(self):
            """
            Get the training data.

            Returns the training data in the form X, y, sw.
            """
            return self._get_X_train(), self._get_y_train(), self._get_sw_train()

        def get_valid(self):
            """
            Get the validation data.

            Returns the validation data in the for X_valid, y_valid, sw_valid.
            """
            return self._get_X_valid(), self._get_y_valid(), self._get_sw_valid()

        def get_raw(self):
            """
            Get the raw data.

            Returns the raw data for training and validation (if applicable, else returns None).
            """
            return (
                self._get_X_train(),
                self._get_y_train(),
                self._get_X_valid(),
                self._get_y_valid(),
            )

        def get_validation_dataset(self):
            """
            Get the validation dataset.

            Returns the validation dataset along with the label and sample weight column names
            """
            return (
                self._training_dataset,
                self._label_column_name,
                self._weight_column_name,
            )

        def set_validation_dataset(self, dataset):
            """
            Set the validation dataset.

            Assumes the same label column name and sample weight column name from training
            set also also present in validation dataset.
            """
            if self._read_only:
                raise ClientException._with_error(
                    AzureMLError.create(
                        AutoMLInternalLogSafe,
                        target="set_validation_dataset",
                        error_message=_READ_ONLY_ERROR_MESSAGE,
                        error_details=_READ_ONLY_ERROR_MESSAGE,
                    )
                )
            else:
                self._validation_dataset = dataset

        def _load(self):
            cache = self._cache
            read_only = self._read_only
            lazy_experiment_data = self._cache.get([Keys.EXPERIMENT_DATA_LAZY])[Keys.EXPERIMENT_DATA_LAZY]
            self.__dict__ = pickle.loads(lazy_experiment_data).__dict__
            self._cache = cache
            self._read_only = read_only

        def _unload(self):
            self._cache.set(Keys.EXPERIMENT_DATA_LAZY, pickle.dumps(self))

    class PartitionData(_CacheableStoreBase):
        """
        Prepared data = Raw data modified by dropping rows with invalid frequency, aggregation, padding and splitting.
        Featurized data = Prepared data modified using featurization
        """

        def __init__(self, cache, read_only):
            super().__init__(cache, read_only)
            self._featurized_train_dataset_id = None  # type: Optional[str]
            self._featurized_valid_dataset_id = None  # type: Optional[str]
            self._prepared_train_dataset_id = None  # type: Optional[str]
            self._prepared_valid_dataset_id = None  # type: Optional[str]
            self._prepared_test_dataset_id = None  # type: Optional[str]
            self._raw_train_dataset_id = None  # type: Optional[str]
            self._raw_valid_dataset_id = None  # type: Optional[str]
            self._raw_partitioned_dataset = {}  # type: MutableMapping[MLTableDataLabel, str]

        def write_file(self, src, dest):
            dest = "data/" + dest
            if isinstance(self._cache, FileDatasetCache):
                # FileDatasetCache only supports uploading folders - not files.
                end = src.rfind("/")
                if end == -1:
                    raise ClientException._with_error(
                        AzureMLError.create(
                            AutoMLInternalLogSafe,
                            target="write_file",
                            error_message="write_file requires a path when a FileDatasetCache is used.",
                            error_details="write_file requires a path when a FileDatasetCache is used."
                        )
                    )
                src = src[:end]
                self._cache.upload_folder(src, dest)
            else:
                self._cache.upload_file(src, dest)

        def save_raw_partitioned_dataset(
            self,
            workspace: Workspace,
            path_to_dataset: str,
            dataset_type: MLTableDataLabel,
            partition_keys: Sequence[str],
            set_column_types: Optional[Mapping[str, DataType]] = None,
        ) -> None:
            self._raw_partitioned_dataset[dataset_type] = \
                self._save_dataset(workspace, path_to_dataset, partition_keys, set_column_types, root_dir=None)

        def save_featurized_train_dataset(
            self,
            workspace: Workspace,
            path_to_dataset: str,
            partition_keys: Sequence[str],
            set_column_types: Optional[Mapping[str, DataType]] = None,
        ) -> None:
            self._featurized_train_dataset_id = \
                self._save_dataset(workspace, path_to_dataset, partition_keys, set_column_types)

        def save_featurized_valid_dataset(
            self,
            workspace: Workspace,
            path_to_dataset: str,
            partition_keys: Sequence[str],
            set_column_types: Optional[Mapping[str, DataType]] = None,
        ) -> None:
            self._featurized_valid_dataset_id = \
                self._save_dataset(workspace, path_to_dataset, partition_keys, set_column_types)

        def save_prepared_train_dataset(
            self,
            workspace: Workspace,
            path_to_dataset: str,
            partition_keys: Sequence[str],
            set_column_types: Optional[Mapping[str, DataType]] = None,
        ) -> None:
            self._prepared_train_dataset_id = \
                self._save_dataset(workspace, path_to_dataset, partition_keys, set_column_types)

        def save_prepared_valid_dataset(
            self,
            workspace: Workspace,
            path_to_dataset: str,
            partition_keys: Sequence[str],
            set_column_types: Optional[Mapping[str, DataType]] = None,
        ) -> None:
            self._prepared_valid_dataset_id = \
                self._save_dataset(workspace, path_to_dataset, partition_keys, set_column_types)

        def save_prepared_test_dataset(
            self,
            workspace: Workspace,
            path_to_dataset: str,
            partition_keys: Sequence[str],
            set_column_types: Optional[Mapping[str, DataType]] = None,
        ) -> None:
            self._prepared_test_dataset_id = \
                self._save_dataset(workspace, path_to_dataset, partition_keys, set_column_types)

        def get_raw_partitioned_dataset(self, workspace, dataset_type):
            return Dataset.get_by_id(workspace, self._raw_partitioned_dataset[dataset_type])

        def get_featurized_train_dataset(self, workspace):
            return Dataset.get_by_id(workspace, self._featurized_train_dataset_id)

        def get_featurized_valid_dataset(self, workspace):
            return Dataset.get_by_id(workspace, self._featurized_valid_dataset_id)

        def get_prepared_train_dataset(self, workspace):
            return Dataset.get_by_id(workspace, self._prepared_train_dataset_id)

        def get_prepared_test_dataset(self, workspace):
            return Dataset.get_by_id(workspace, self._prepared_test_dataset_id)

        def get_prepared_valid_dataset(self, workspace):
            return Dataset.get_by_id(workspace, self._prepared_valid_dataset_id)

        def get_raw_train_dataset(self, workspace):
            return Dataset.get_by_id(workspace, self._raw_train_dataset_id)

        def get_raw_valid_dataset(self, workspace):
            return Dataset.get_by_id(workspace, self._raw_valid_dataset_id)

        def save_raw_train_dataset(self, dataset):
            self._raw_train_dataset_id = dataset.id

        def save_raw_valid_dataset(self, dataset):
            self._raw_valid_dataset_id = dataset.id

        def _save_dataset(
            self,
            workspace: Workspace,
            path_to_dataset: str,
            partition_keys: Sequence[str],
            set_column_types: Optional[Mapping[str, DataType]] = None,
            root_dir: Optional[str] = "data"
        ) -> str:
            partition_string = None
            if partition_keys:
                partition_string = ""
                for key in partition_keys:
                    partition_string += "{"
                    partition_string += str(key)
                    partition_string += "}/"

                partition_string += "*.parquet"

            if root_dir is not None and len(root_dir) != 0:
                path_to_dataset = "data/" + path_to_dataset
            dataset = Dataset.Tabular.from_parquet_files(
                path=(self._cache._data_store, path_to_dataset),
                validate=False,
                partition_format=partition_string,
                set_column_types=set_column_types
            )
            return cast(str, dataset._ensure_saved(workspace))

        def _load(self):
            cache = self._cache
            read_only = self._read_only
            partitioned_data_bytes = cast(
                bytes, self._cache.get([Keys.EXPERIMENT_DATA_PARTITIONED])[Keys.EXPERIMENT_DATA_PARTITIONED]
            )
            self.__dict__ = pickle.loads(partitioned_data_bytes).__dict__
            self._cache = cache
            self._read_only = read_only

        def _unload(self):
            self._cache.set(Keys.EXPERIMENT_DATA_PARTITIONED, pickle.dumps(self))

    def __init__(self, cache, read_only):
        super().__init__(cache, read_only)
        self.materialized = self.MaterializedData(cache, read_only)
        self.lazy = self.LazyData(cache, read_only)
        self.cv_splits = _CVSplitsCollection(cache, read_only)
        self.partitioned = self.PartitionData(cache, read_only)

    def _load(self):
        self.materialized._load()
        self.lazy._load()
        self.partitioned._load()

    def _unload(self):
        self.materialized._unload()
        self.lazy._unload()
        self.partitioned._unload()


class ExperimentMetadata(_CacheableStoreBase):
    """
    The object containing metadata for a given Experiment.

    This object should only be used by the ExperimentStore.

    Any information stored in this object will be memory-backed and should
    be unloaded (saved) to the CacheStore prior to usage in subsequent runs
    or subprocesses.

    ExperimentMetadata represents any metadata used throughout a job. ExperimentMetadata is split between
    common metadata attributes used across jobs - things like task, is_sparse, data_snapshot, etc. - and
    things specific to a given job. Specific attributes are stored under their prospective tasks:
    Classification, Regression, and Timeseries. If something is not a generic piece of metadata used across
    tasks it should be put in the correct task's metadata.
    """

    class _ClassificationMetadata(_CacheableStoreBase):
        """Metadata related to classification tasks."""

        def __init__(self, cache, read_only):
            super().__init__(cache, read_only)
            self.num_classes = None
            self.class_labels = None

        def _load(self):
            cache = self._cache
            read_only = self._read_only
            self.__dict__ = pickle.loads(
                self._cache.get(["ExperimentMetadata_Classification"])["ExperimentMetadata_Classification"]).__dict__
            self._cache = cache
            self._read_only = read_only

        def _unload(self):
            self._cache.set("ExperimentMetadata_Classification", pickle.dumps(self))

    class _RegressionMetadata(_CacheableStoreBase):
        """Metadata related to regression tasks."""

        def __init__(self, cache, read_only):
            super().__init__(cache, read_only)
            self.bin_info = {}
            self.y_min = None
            self.y_max = None
            self.y_std = None

        def get_y_range(self):
            return self.y_min, self.y_max

        def _load(self):
            cache = self._cache
            read_only = self._read_only
            self.__dict__ = pickle.loads(
                self._cache.get(["ExperimentMetadata_Regression"])["ExperimentMetadata_Regression"]).__dict__
            self._cache = cache
            self._read_only = read_only

        def _unload(self):
            self._cache.set("ExperimentMetadata_Regression", pickle.dumps(self))

    class _TimeseriesMetadata(_CacheableStoreBase):
        """Metadata related to timeseries tasks."""

        INDICATOR_KEY = "indicator_cols"
        TIMESERIES_DATA_PROFILE_KEY = "timeseries_data_profile"

        def __init__(self, cache, read_only):
            super().__init__(cache, read_only)
            self.timeseries_param_dict = {}
            self.global_series_start = None
            self.global_series_end = None
            self.series_stats = None
            self.apply_log_transform_for_label = False
            self.min_points_per_grain = 0
            self.raw_input_data_snapshot_str_with_quantiles = ""
            self.output_data_snapshot_str_with_quantiles = ""
            self.short_grain_names = []

        def get_featurized_data_profile(self) -> AggregatedTimeSeriesDataProfile:
            """
            Get the featurized data profile.

            :return: The dataprofile for the training and validation timeseries dataset.
            """
            data_profile = self._cache.get([
                ExperimentMetadata._TimeseriesMetadata.TIMESERIES_DATA_PROFILE_KEY
            ])[ExperimentMetadata._TimeseriesMetadata.TIMESERIES_DATA_PROFILE_KEY]
            return cast(AggregatedTimeSeriesDataProfile, data_profile)

        def set_featurized_data_profile(self, data_profile: AggregatedTimeSeriesDataProfile) -> None:
            """
            Set the data profile.

            :param data_profile: The dataprofile for the training and validation timeseries dataset.
            """
            self._cache.set(ExperimentMetadata._TimeseriesMetadata.TIMESERIES_DATA_PROFILE_KEY, data_profile)

        def get_indicator_columns_data(self) -> Dict[str, bool]:
            """
            Get the dictionary showing if the column is an indicator, consisting of zeroes and
            ones.

            :return: The dictionary column -> is indicator if it was set or empty dictionary.
            """
            indicator_columns_data = self._cache.get(
                [
                    ExperimentMetadata._TimeseriesMetadata.INDICATOR_KEY
                ])[
                ExperimentMetadata._TimeseriesMetadata.INDICATOR_KEY
            ]
            return cast(
                Dict[str, bool],
                indicator_columns_data if indicator_columns_data else {},
            )

        def set_indicator_columns_data(self, indicator_columns_data: Dict[str, bool]) -> None:
            """
            Set the dictionary showing if the column is an indicator, consisting of zeroes and
            ones.

            :param indicator_columns_data: The dictionary column -> is indicator.
            """
            self._cache.set(ExperimentMetadata._TimeseriesMetadata.INDICATOR_KEY, indicator_columns_data)

        def _load(self):
            cache = self._cache
            read_only = self._read_only
            self.__dict__ = pickle.loads(
                self._cache.get(["ExperimentMetadata_Timeseries"])["ExperimentMetadata_Timeseries"]).__dict__
            self._cache = cache
            self._read_only = read_only

        def _unload(self):
            self._cache.set("ExperimentMetadata_Timeseries", pickle.dumps(self))

    def __init__(self, cache, read_only):
        super().__init__(cache, read_only)
        self.is_sparse = False
        self.nimbus = None
        self.num_samples = None
        self.problem_info = None
        self.raw_data_snapshot_str = ""
        self.output_snapshot_str = ""
        self.raw_data_type = None
        self.task = ""
        self.training_type = ""
        self.X_raw_column_names = None
        self._timeseries = self._TimeseriesMetadata(cache, read_only)
        self._regression = self._RegressionMetadata(cache, read_only)
        self._classification = self._ClassificationMetadata(cache, read_only)

        # This is the dataset_categoricals for the whole uber transformed dataset
        # This contains both label encoder and one hot encoder data. The keys will be different
        # types - forex:  X,  featurized_cv_split_0, featurized_cv_split_1 etc. The values will be list of
        # zero and non zero. 0 will indicate non categorical column and non zero will indicate label encoder
        # columns with the unqiue value count.

        self.dataset_categoricals_dict = {}  # type: Dict[str, List[int]]

        # This is the mapping of learner types to the list of columns. This information is used
        # by the dropcolumnstransformer only. The keys are 'DefaultLearners' and 'CatIndicatorLearners'.
        # The inner dictionary keys are data types for ex - X, featurized_cv_split_0, featurized_cv_split_1 etc and the
        # values in the dictionary is the list of the columns that need to be considered.
        self.learner_columns_mapping = {}  # type: Dict[str, Dict[str, List[int]]]

    @property
    def is_timeseries(self) -> bool:
        """
        Get the older version of automl timeseries.

        Previously AutoML only supported classification/regression tasks. When
        forecasting was added, the task was converted to regression and is_timeseries
        was set to `True`. This property is added to support the old workflows where
        task is expected to be only Classification/Regression and is_timeseries is needed.
        In new workflows, task_type should be used.
        """
        return self.task == constants.Tasks.FORECASTING

    @property
    def task_type(self) -> str:
        """
        Get the older version of automl tasks.

        Previously AutoML only supported classification/regression tasks. When
        forecasting was added, the task was converted to regression and is_timeseries
        was set to `True`. This property is added to support the old workflows where
        task is expected to be only Classification/Regression. In new workflows,
        task_type should be used.
        """
        if self.task == constants.Tasks.FORECASTING:
            return constants.Tasks.REGRESSION
        else:
            return self.task

    @property
    def classification(self) -> '_ClassificationMetadata':
        return self._classification

    @property
    def regression(self) -> '_RegressionMetadata':
        return self._regression

    @property
    def timeseries(self) -> '_TimeseriesMetadata':
        return self._timeseries

    def _load(self):
        cache = self._cache
        read_only = self._read_only
        timeseries = self._timeseries
        regression = self._regression
        classification = self._classification

        self.__dict__ = pickle.loads(self._cache.get(["ExperimentMetadata"])["ExperimentMetadata"]).__dict__
        timeseries._load()
        regression._load()
        classification._load()

        self._cache = cache
        self._read_only = read_only
        self._timeseries = timeseries
        self._regression = regression
        self._classification = classification

    def _unload(self):
        self._timeseries._unload()
        self._regression._unload()
        self._classification._unload()

        timeseries = self._timeseries
        regression = self._regression
        classification = self._classification

        del self._timeseries
        del self._regression
        del self._classification

        self._cache.set("ExperimentMetadata", pickle.dumps(self))

        self._timeseries = timeseries
        self._regression = regression
        self._classification = classification


class ExperimentTansformers(_CacheableStoreBase):
    """
    The object containing transformers for a given Experiment.

    This object should only be used by the ExperimentStore.

    Any information stored in this object will be memory-backed and should
    be unloaded (saved) to the CacheStore prior to usage in subsequent runs
    or subprocesses.
    """

    def __init__(self, cache, read_only):
        super().__init__(cache, read_only)
        self._transformers = {}  # type: Dict[str, Any]

    def get_column_transformer_pipeline_step(self, columns_to_keep: List[int]) -> Tuple[str, DropColumnsTransformer]:
        return (
            SupportedTransformersInternal.DropColumnsTransformer,
            DropColumnsTransformer(columns_to_keep),
        )

    def set_transformers(self, transformers):
        if self._read_only:
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe,
                    target="set_transformers",
                    error_message=_READ_ONLY_ERROR_MESSAGE,
                    error_details=_READ_ONLY_ERROR_MESSAGE,
                )
            )
        else:
            self._transformers = transformers

    def get_transformers(self):
        return self._transformers

    def get_timeseries_transformer(self):
        return self._transformers.get(constants.Transformers.TIMESERIES_TRANSFORMER)

    def get_y_transformer(self):
        return self._transformers.get(constants.Transformers.Y_TRANSFORMER)

    def _load(self):
        cache = self._cache
        read_only = self._read_only
        if has_mlflow and cache.get_dir(Keys.EXP_TRANSFORMERS_CACHE_DIR) is not None:
            try:
                transformer = mlflow.sklearn.load_model(
                    cache.get_dir(Keys.EXP_TRANSFORMERS_CACHE_DIR)
                )
            except Exception as e:
                raise ClientException.from_exception(
                    e, msg="Could not load transformers model via mlflow.",
                )
        else:
            transformer = pickle.loads(
                cast(bytes, self._cache.get([Keys.EXP_TRANSFORMERS])[Keys.EXP_TRANSFORMERS])
            )

        self.__dict__ = transformer.__dict__
        self._cache = cache
        self._read_only = read_only

    def _unload(self):
        cache = self._cache
        save_as_mlflow = has_mlflow
        if save_as_mlflow:
            try:
                td = tempfile.mkdtemp()
                mlflow_dir = Keys.EXP_TRANSFORMERS_CACHE_DIR
                output_dir = os.path.join(td, *mlflow_dir.split("/"))

                cd = inference.get_conda_deps_as_dict(True)
                logger.info("Saving data transformer as ML model to {}.".format(output_dir))
                mlflow.sklearn.save_model(
                    sk_model=self,
                    path=output_dir,
                    conda_env=cd,
                    serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_PICKLE)

                cache.add_dir(Keys.EXP_TRANSFORMERS_CACHE_DIR, output_dir)
            except Exception as e:
                save_as_mlflow = False
                logging_utilities.log_traceback(e, logger, is_critical=False)
                logger.info("Exception occurred while saving transformers as mlflow model.")

        if not save_as_mlflow:
            logger.info("Saving data transformer as pickle file")
            cache.set(Keys.EXP_TRANSFORMERS, pickle.dumps(self))


class ExperimentStore:
    """
    The place to store data, metadata, transformers, and other information necessary
    complete a task within AutoML.

    This object replaces the ClientDatasets object. The purpose of this object is to
    store any information which is necessary across the set of tasks within AutoML.
    Example jobs currently supported include: AutoML Featurize, Train, Explain, & Test.
    This object should never do any work related to creating, modifying, or splitting
    data/metadata, it acts simply as a place to store and marshall information between
    runs.

    This object is represented as a singleton object instantiated once at the entrypoint of
    of a run and retrieved at use time. Attempts to recreate the singleton, or to retrieve the
    singleton prior to initial creation will both result in exceptions. The data is marshalled
    across runs or processes via the CacheStore. The ExperimentStore can unload (write) data
    to the underlying cache or load (read) data from the cache depending on the requirements
    of the run. Additionally, a read-only flag is included to ensure the ExperimentStore is
    only written to when the entrypoint expects such writes.

    Attributes within the ExperimentStore have two modes of storage - memory-backed and cached-backed.
    Attributes which are typically large, things like training data or cv-splits, are stored as
    cache-backed attributes. All other attributes, like transformers and metadata, are memory-backed.
    Reading from or writing to cache-backed attributes will result in a read or write to the underlying
    cache store. Reading from or writing to memory-backed attributes results in a read or write to the
    in memory object. The only way to ensure memory-backed attributes are persisted accross runs or processes
    is to unload (write) and load (read) the ExperimentStore to the cache. Once a run is finished, it should
    always reset its ExperimentStore state to ensure no undesired elements of a previous job persist within
    a future job in the same environment. This reset is done via ExperimentStore.reset().

    .. code-block:: python

        # Create a read/write ExperimentStore
        expr_store = ExperimentStore(cache, read_only=False)

        # Retreive an ExperimentStore
        expr_store = ExperimentStore.get_instance()

        # Write the ExperimentStore to the cache
        expr_store.unload()

        # Create a read-only ExperimentStore and load the information from the cache
        exp = ExperimentStore(cache, read_only=True)
        expr_store.load()

        # Retrieve and ExperimentStore
        expr_store = ExperimentStore.get_instance()

    The ExperimentStore has three major components for compartmentalizing data - ExperimentData,
    ExperimentMetadata, and ExperimentTransformers. These attributes provide access to their
    respective data components: data, metadata, transformers.

    ExperimentData represents any data which may be used throughout a job. There are two types of
    data formats which can be accessed - materialized and lazy. Materialized data represents data
    which can be materialized entirely in memory. Materialized data is typically stored as a pandas
    dataframe. Lazy data represents data which is too large to fit into memory and must be streamed
    as it is used. Lazy data is typically stored as a TabularDataset. Materialized data will always
    be cache-backed data.

    ExperimentMetadata represents any metadata used throughout a job. ExperimentMetadata is split between
    common metadata attributes used across jobs - things like task, is_sparse, data_snapshot, etc. - and
    things specific to a given job. Specific attributes are stored under their prospective tasks:
    Classification, Regression, and Timeseries. If something is not a generic piece of metadata used across
    tasks it should be put in the correct task's metadata. All ExperimentMetadata is memory-backed.

    ExperimentTransformers represents any transformers used to featurize data during an AutoML job.
    ExperimentTransformers is memory-backed.
    """

    __instance = None

    def __init__(self, cache, read_only):
        logger.info("Requested a new ExperimentStore instance.")
        if ExperimentStore.__instance:
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe,
                    target="ExperimentStore.__init__",
                    error_message="ExperimentStore singleton has already been created.",
                    error_details="ExperimentStore singleton has already been created.",
                )
            )
        else:
            self._data = ExperimentData(cache, read_only)
            self._metadata = ExperimentMetadata(cache, read_only)
            self._transformers = ExperimentTansformers(cache, read_only)
            self._read_only = read_only
            self._cache = cache
            ExperimentStore.__instance = self
        logger.info("Created ExperimentStore with ID: {}.".format(id(self)))

    @staticmethod
    def has_instance() -> bool:
        return ExperimentStore.__instance is not None

    @staticmethod
    def get_instance() -> "ExperimentStore":
        if not ExperimentStore.__instance:
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe,
                    target="ExperimentStore.get_instance",
                    error_message="ExperimentStore singleton has not been created.",
                    error_details="ExperimentStore singleton has not been created.",
                )
            )
        return ExperimentStore.__instance

    @classmethod
    def reset(cls) -> None:
        logger.info("Resetting ExperimentStore ID: {}".format(id(cls.__instance)))
        cls.__instance = None

    @property
    def data(self) -> ExperimentData:
        return self._data

    @data.setter
    def data(self, data):
        raise ClientException._with_error(
            AzureMLError.create(
                AutoMLInternalLogSafe,
                target="ExperimentStore.set_data",
                error_message="Setting data is not supported.",
                error_details="Setting data is not supported.",
            )
        )

    @property
    def metadata(self) -> ExperimentMetadata:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        raise ClientException._with_error(
            AzureMLError.create(
                AutoMLInternalLogSafe,
                target="ExperimentStore.set_metadata",
                error_message="Setting metadata is not supported.",
                error_details="Setting metadata is not supported.",
            )
        )

    @property
    def transformers(self) -> ExperimentTansformers:
        return self._transformers

    @transformers.setter
    def transformers(self, transformers):
        raise ClientException._with_error(
            AzureMLError.create(
                AutoMLInternalLogSafe,
                target="ExperimentStore.set_transformers",
                error_message="Setting transformers is not supported.",
                error_details="Setting transformers is not supported.",
            )
        )

    def update_output_dataset_lineage(
        self,
        parent_run: Run,
        featurization: Union[str, FeaturizationConfig] = FeaturizationConfigMode.Off
    ) -> None:
        """
        Update output lineage in experiment's parent run.

        :param parent_run: parent run of experiment
        """

        # Skip if parent run is StepRun as its causing service error.
        # Tracking WI:1827170
        if parent_run.type == "azureml.StepRun":
            logger.info("skipping if parent run is a StepRun")
            return

        cache = self._cache
        cache_items = cache.cache_items

        if not isinstance(cache, RunBackedCacheStore):
            logger.info("Not updating for cache store of type " + str(type(cache)))
            return

        logger.info("update output lineage for run id : " + parent_run.id)
        ws = parent_run.experiment.workspace
        datastore = Datastore.get(ws, "workspaceartifactstore")

        # TODO: 1561974 handle un-merged training/validation data in cache store
        keys = (
            Keys.FULL_TRAIN,
            Keys.FULL_VALIDATION
        )

        try:
            for key in keys:
                # prepend key based on featurized data logic
                run_key = key
                if featurization != FeaturizationConfigMode.Off:
                    run_key = Keys.FEATURIZATION_DATA_NAMESPACE + key

                if cache_items.get(run_key):
                    # Get remote path of cached item
                    path = cache_items.get(run_key).remote_path

                    # Prepend to relative artifact path, as retreiving from underlying blob store.
                    datastore_path = (pathlib.Path("ExperimentRun")) / \
                        ".".join(["dcid", parent_run.id])
                    datastore_path = datastore_path.joinpath(path)
                    path = datastore_path.as_posix()

                    dataset = TabularDatasetFactory.from_parquet_files((
                        datastore, path))
                    link_output = LinkOutput(workspace=ws, name=key)
                    link_output.link(dataset, parent_run)
        except Exception as e:
            logging_utilities.log_traceback(e, logger, is_critical=False)
            logger.info("caught exception while fetching and linking output dataset")

    def load(self) -> None:
        """Load the ExperimentStore state from cache."""
        self._data._cache.load()
        self._data._load()
        self._metadata._load()
        self._transformers._load()

    def unload(self) -> None:
        """Unload the ExperimentStore state to cache."""
        if self._read_only:
            raise ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe,
                    target="ExperimentStore.unload",
                    error_message=_READ_ONLY_ERROR_MESSAGE,
                    error_details=_READ_ONLY_ERROR_MESSAGE,
                )
            )
        else:
            self._data._unload()
            self._metadata._unload()
            self._transformers._unload()
            self._cache.flush()
            gc.collect()

    def clear(self) -> bool:
        """
        Clear experiment data from cache store.

        This method will delete any underlying cached data. Once deleted, it cannot be recovered.

        If call was successful returns True, otherwise False.
        """
        try:
            self._data._cache.unload()
            return True
        except IOError:
            return False


def _create_merged_x_y_sample_weight(
    X: Optional[Union[np.ndarray, pd.DataFrame]],
    y: Optional[Union[np.ndarray, pd.Series]],
    sample_weight: Optional[Union[np.ndarray, pd.Series]],
) -> Optional[pd.DataFrame]:
    """
    Create a combined dataframe containing X, y, sample weight.

    :param X: The X.
    :param y: The y.
    :param sample_weight: The sample weight.
    :return: A combined dataframe if the merge is successful. `None` otherwise.
    """
    if X is None or y is None:
        return None

    num_rows = X.shape[0]
    expected_num_cols = X.shape[1] if X.ndim == 2 else 1
    try:
        # We create MaterializedTabularData as it has validations.
        mtd = MaterializedTabularData(X, y, weights=sample_weight)
        combined_df = mtd.X.copy()                                  # Call by reference FTW.
        combined_df[Keys.Y_COLUMN] = y
        expected_num_cols = expected_num_cols + 1
        if sample_weight is not None:
            combined_df[Keys.SW_COLUMN] = sample_weight
            expected_num_cols = expected_num_cols + 1

        logger.info(f'Shape of X: {X.shape}, shape of y: {y.shape}, shape of combined df: {combined_df.shape}')
        actual_cols = combined_df.shape[1]
        actual_rows = combined_df.shape[0]
        Contract.assert_true(X.shape[0] == actual_rows, f'Expected same number of rows in X {num_rows} '
                                                        f'and combined_df {actual_rows}.')
        Contract.assert_true(actual_cols == expected_num_cols, f'Expected combined df to have {expected_num_cols} but'
                                                               f'it has only {actual_cols}.')
        return combined_df
    except MemoryError as me:
        # MemoryError here should be logged and ignored as we could be failing due to the copy we are making.
        logger.warning('MemoryError occurred while trying to create a combined dataframe.')
        logging_utilities.log_traceback(me, logger, is_critical=False)
        return None
    except ValidationException as ve:
        logger.warning(ve.message)
        logging_utilities.log_traceback(ve, logger, is_critical=False)
        return None
    except Exception as ex:
        logger.info(f"Failed to merge dataset with exception of type: {type(ex)}")
        logging_utilities.log_traceback(ex, logger, is_critical=False)
        return None


def get_x_y_sample_weight_from_merged_df(merged_df: Optional[pd.DataFrame]) -> Tuple[
    Optional[Union[np.ndarray, pd.DataFrame]],
    Optional[Union[np.ndarray, pd.DataFrame]],
    Optional[Union[np.ndarray, pd.DataFrame]]
]:
    if merged_df is None:
        return None, None, None

    y = merged_df.pop(Keys.Y_COLUMN)
    array_y = y.values
    sw = None
    if Keys.SW_COLUMN in merged_df.columns:
        sw = merged_df.pop(Keys.SW_COLUMN).values

    return merged_df, array_y, sw
