# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for data transformation."""
import copy
import json
import logging
from typing import List, Union, Any, Optional, Dict, Mapping, Tuple, cast

import numpy as np
import pandas as pd
import scipy
from azureml.dataprep import Dataflow
from scipy import sparse
from sklearn_pandas import DataFrameMapper

from azureml._common._error_definition import AzureMLError
from azureml._common.exceptions import AzureMLException
from azureml.automl.core.constants import FeatureType, FeaturizationRunConstants
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.shared import logging_utilities, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ArtifactUploadFailed, InvalidArgumentType
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.constants import TimeSeriesInternal
from azureml.automl.core.shared.exceptions import CacheException, ClientException, ValidationException
from azureml.automl.core.shared.pickler import DefaultPickler
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime._data_definition import RawExperimentData
from azureml.automl.runtime._engineered_feature_names import _GenerateEngineeredFeatureNames
from azureml.automl.runtime.column_purpose_detection import _time_series_column_helper
from azureml.automl.runtime.column_purpose_detection._time_series_column_helper import infer_objects_safe
from azureml.automl.runtime.column_purpose_detection.types import StatsAndColumnPurposeType
from azureml.automl.runtime.data_cleaning import _remove_nan_rows_in_X_y
from azureml.automl.runtime.data_context import DataContextParams
from azureml.automl.runtime.distributed.utilities import get_unique_download_path
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.types import CoreDataInputType, DataInputType
from azureml.automl.runtime.stats_computation import RawFeatureStats
from azureml.core import Run
from azureml.exceptions import ServiceException as AzureMLServiceException, AzureMLAggregatedException
from .featurization import DataTransformer, data_transformer_utils, TransformerAndMapper
from .featurization._featurizer_container import FeaturizerContainer
from .featurization._unprocessed_featurizer import FeaturizerFactory
from .featurizer.transformer.featurization_utilities import get_transform_names, does_property_hold_for_featurizer

logger = logging.getLogger(__name__)
_PICKLER = DefaultPickler()

_DUMMY_VALUES_FOR_TYPE = {
    "bytes": "example_value",
    "bool": False,
    "datetime": "2000-1-1",
    "float": 0.0,
    "int": 0,
    "object": "example_value",
    "str": "example_value",
    "timedelta": "1000"
}

_DUMMY_VALUES_FOR_FEATURE = {
    FeatureType.DateTime: (_DUMMY_VALUES_FOR_TYPE["datetime"], np.dtype('datetime64[ns]'))
}


def _upload_pickle(obj: Any, run_obj: Run, file_name: str) -> None:
    """
    Helper function for pickling and uploading object to storage with specified file name.

    :param obj: The object to be uploaded.
    :param run_obj: The run through which we upload the file.
    :param file_name: The name of the file to be created in storage.
    :return: None
    """
    _PICKLER.dump(obj, file_name)
    try:
        run_obj.upload_file(file_name, file_name)
    except AzureMLAggregatedException as error:
        if "Resource Conflict: ArtifactId" in error.message:
            logger.warning("Artifact upload failed with conflict. The file already exists")
        else:
            raise


def _download_pickle(file_name: str) -> Any:
    """
    Helper function for downloading file from storage.

    :param file_name: The name of the file to be downloaded.
    :return: The downloaded, unpickled object.
    """
    return _PICKLER.load(file_name)


def load_and_update_from_sweeping(data_transformer: DataTransformer,
                                  df: DataInputType) -> None:
    """
    Function called in the featurization run for updating the newly-instantiated data transformer
    with values from the setup iteration's data transformer that are necessary for full featurization.

    :param data_transformer: The data transformer to update.
    :param df: The input data used for recreating the column types mapping.
    :return: None.
    """

    run = Run.get_context()
    property_dict = run.get_properties()

    with logging_utilities.log_activity(logger=logger, activity_name="FeatureConfigDownload"):
        try:
            downloaded_path = get_unique_download_path(property_dict.get(FeaturizationRunConstants.CONFIG_PROP,
                                                                         FeaturizationRunConstants.CONFIG_PATH))
            feature_config = _download_pickle(downloaded_path)
        except Exception as e:
            logging_utilities.log_traceback(
                exception=e,
                logger=logger,
                override_error_msg="Error when retrieving feature config from local node storage.")
            raise e

    data_transformer.transformer_and_mapper_list = feature_config

    with logging_utilities.log_activity(logger=logger, activity_name="EngineeredFeatureNamesDownload"):
        try:
            downloaded_path = get_unique_download_path(property_dict.get(FeaturizationRunConstants.NAMES_PROP,
                                                                         FeaturizationRunConstants.NAMES_PATH))
            data_transformer._engineered_feature_names_class = \
                _download_pickle(downloaded_path)
        except Exception as e:
            logging_utilities.log_traceback(
                exception=e,
                logger=logger,
                override_error_msg="Error when retrieving feature names from local node storage.")
            raise e

    if data_transformer._columns_types_mapping is None:
        if isinstance(df, np.ndarray):
            df = pd.DataFrame(df)

        data_transformer._columns_types_mapping = data_transformer_utils.get_pandas_columns_types_mapping(df)

    data_transformer._feature_sweeped = True


def save_feature_config(feature_config: Union[List[TransformerAndMapper], DataFrameMapper]) -> None:
    """
    Logic for saving the transformer_and_mapper_list or mapper from the setup run's data transformer.

    :param feature_config: The feature config to be downloaded and used in the featurization run.
    :return: None.
    """
    run = Run.get_context()
    error = AzureMLError.create(ArtifactUploadFailed, target="feature_config")
    with logging_utilities.log_activity(logger=logger, activity_name="FeatureConfigUpload"):
        try:
            _upload_pickle(feature_config, run, FeaturizationRunConstants.CONFIG_PATH)
        except AzureMLServiceException:
            raise
        except AzureMLException as e:
            if hasattr(e, '_azureml_error') and e._azureml_error is None:
                e._azureml_error = error
            raise e


def save_engineered_feature_names(engineered_feature_names: _GenerateEngineeredFeatureNames) -> None:
    """
    Logic for saving the engineered feature names from the setup run's data transformer.

    :param engineered_feature_names: The feature names to be downloaded and used in the featurization run.
    :return: None.
    """
    run = Run.get_context()
    error = AzureMLError.create(ArtifactUploadFailed, target="feature_names")
    with logging_utilities.log_activity(logger=logger, activity_name="EngineeredFeatureNamesUpload"):
        try:
            _upload_pickle(engineered_feature_names, run, FeaturizationRunConstants.NAMES_PATH)
        except AzureMLServiceException:
            raise
        except AzureMLException as e:
            if hasattr(e, '_azureml_error') and e._azureml_error is None:
                e._azureml_error = error
            raise e


def pull_fitted_featurizers_from_cache(cache_store: Optional[CacheStore],
                                       featurizer_container: FeaturizerContainer) -> Mapping[int, Any]:
    """
    Pull any featurizers that were already fitted and cached in their own independent runs back
    into the DataTransformer. If missing from the cache, raise an exception.

    :param cache_store: The CacheStore.
    :param featurizer_container: Object containing featurizers and other relevant settings.
    :return: The featurizer index mapping that will be used to mutate the DataTransformer object.
    """
    cache_keys = [get_cache_key_from_index(featurizer.index) for featurizer
                  in featurizer_container if featurizer.is_cached]
    if cache_store is None:
        if len(cache_keys) > 0:
            raise ClientException("Cannot pull cached featurizers from null cache.", has_pii=False)
        return {}

    fitted_featurizers = cache_store.get(cache_keys)
    featurizer_index_mapping = {}
    for featurizer_cache_key in cache_keys:
        index = get_data_transformer_index_from_cache_key_string(featurizer_cache_key)
        if fitted_featurizers[featurizer_cache_key] is None:  # cache lookup failed and a default value was returned
            raise CacheException("Cached entry for featurizer index {} unexpectedly missing.".format(index),
                                 has_pii=False)
        featurizer_index_mapping[index] = fitted_featurizers[featurizer_cache_key]
    return featurizer_index_mapping


def get_data_transformer_index_from_cache_key_string(key_name: str) -> int:
    """
    Given the key string used to store a fitted featurizer in the cache, extract the index.

    :param key_name: The cache key string.
    :return: The index.
    """
    return int(key_name.split('_')[-1])


def get_cache_key_from_index(index: int) -> str:
    """
    Given a featurizer's index in the DataTransformer featurizer collection, generate the cache key.

    :param index: The index.
    :return: The cache key string.
    """
    return FeaturizationRunConstants.FEATURIZER_CACHE_PREFIX + str(index)


def count_nans_in_data(data: CoreDataInputType) -> int:
    """
    Count number of NaNs in the given data

    :param data: np.ndarray, pd.DataFrame, or scipy.sparse.spmatrix
    :return:
    """
    if data is None:
        return 0

    if isinstance(data, pd.DataFrame):
        return int(data.isna().sum().sum())

    if isinstance(data, np.ndarray):
        return int(pd.isna(data).sum().sum())

    return 0


def should_convert_data_to_sparse(data: CoreDataInputType, count_nans: Optional[int] = None) -> bool:
    """
    Check if input data needs to be converted into sparse matrix
    If already scipy.sparse.spmatrix, we don't need to convert.
    Else, check if data contains 50 percent or more NaNs.

    There are some models that take in sparse matrix but not NaNs (fails on assert_all_finite validation).
    In order to avoid this failure, we need to convert the data into sparse matrix.

    :param data: np.ndarray, pd.DataFrame, or scipy.sparse.spmatrix
    :param count_nans: count of nans in data
    :return:
    """
    if data is None:
        return False

    limit = int(data.size * 0.5)

    if count_nans is None:
        return count_nans_in_data(data) >= limit

    return count_nans >= limit


def convert_data_to_sparse(data: Optional[CoreDataInputType]) -> Optional[CoreDataInputType]:
    """
    Convert data into sparse matrix.

    :param data: np.ndarray, pd.DataFrame, or scipy.sparse.spmatrix
    :return: sparse matrix if converted, otherwise original data
    """
    if data is None or scipy.sparse.issparse(data):
        return data

    try:
        # Convert data to sparse matrix
        if isinstance(data, pd.DataFrame):
            csrmatrix = scipy.sparse.csr_matrix(data.values)
        else:
            csrmatrix = scipy.sparse.csr_matrix(data)

        # At this point, csrmatrix still contains np.nan, these need to be converted to appropriate numbers
        csrmatrix.data = np.nan_to_num(csrmatrix.data)
        # Afterwards, eliminate those nans explicitly converted to zeros so that it is not used for training
        csrmatrix.eliminate_zeros()

        logger.info("Converting data to sparse matrix succeeded.")
        return csrmatrix
    except Exception:
        logger.warning("Converting data to sparse matrix failed. Proceeding with original data.")
        return data


def remove_nans_in_raw_experiment_data(
        raw_experiment_data: RawExperimentData, automl_settings_obj: AutoMLBaseSettings
) -> RawExperimentData:
    """
    Clean raw data.
    This step is needed before any data processing or training as nan labels are omitted from training.

    :param raw_experiment_data: Original RawExperimentData
    :param automl_settings_obj: AutoML settings
    :return: Updated RawExperimentData that are cleared of nans
    """

    # Log original raw data info
    _log_data_info('X_raw', raw_experiment_data.X)
    _log_data_info('X_valid_raw', raw_experiment_data.X_valid)
    _log_data_info('X_test_raw', raw_experiment_data.X_test)
    _log_data_info('y_raw', raw_experiment_data.y)
    _log_data_info('y_valid_raw', raw_experiment_data.y_valid)
    _log_data_info('y_test_raw', raw_experiment_data.y_test)

    # Clean training data
    featurization = DataContextParams(automl_settings_obj).control_params.featurization
    X, y, sample_weight = _remove_nan_rows_in_X_y(
        raw_experiment_data.X, raw_experiment_data.y,
        sample_weight=raw_experiment_data.weights,
        is_timeseries=automl_settings_obj.is_timeseries,
        target_column=raw_experiment_data.target_column_name,
        featurization_config=featurization
    )

    # Clean validation data
    X_valid, y_valid, sample_weight_valid = _remove_nan_rows_in_X_y(
        raw_experiment_data.X_valid, raw_experiment_data.y_valid,
        sample_weight=raw_experiment_data.weights_valid,
        is_timeseries=automl_settings_obj.is_timeseries,
        target_column=raw_experiment_data.target_column_name,
        featurization_config=featurization
    )

    # Clean test data
    X_test, y_test, _ = _remove_nan_rows_in_X_y(
        raw_experiment_data.X_test, raw_experiment_data.y_test,
        is_timeseries=automl_settings_obj.is_timeseries,
        target_column=raw_experiment_data.target_column_name,
        featurization_config=featurization
    )

    raw_experiment_data.X = X
    raw_experiment_data.y = y
    raw_experiment_data.weights = sample_weight
    raw_experiment_data.X_valid = X_valid
    raw_experiment_data.y_valid = y_valid
    raw_experiment_data.weights_valid = sample_weight_valid
    raw_experiment_data.X_test = X_test
    raw_experiment_data.y_test = y_test

    # Log cleaned raw data info
    _log_data_info('X_raw_cleaned', raw_experiment_data.X)
    _log_data_info('X_valid_raw_cleaned', raw_experiment_data.X_valid)
    _log_data_info('X_test_raw_cleaned', raw_experiment_data.X_test)
    _log_data_info('y_raw_cleaned', raw_experiment_data.y)
    _log_data_info('y_valid_raw_cleaned', raw_experiment_data.y_valid)
    _log_data_info('y_test_raw_cleaned', raw_experiment_data.y_test)

    return raw_experiment_data


def log_raw_data_characteristics(raw_experiment_data: RawExperimentData) -> None:
    """
    Log raw data stat.

    :param raw_experiment_data: RawExperimentData to use for logging data stats
    :return:
    """
    y_df = raw_experiment_data.y
    Validation.validate_value(y_df, "y", reference_code=ReferenceCodes._DATA_TRANSFORMATION_INVALID_Y)

    if not isinstance(y_df, pd.DataFrame):
        try:
            y_df = pd.DataFrame(y_df)
        except ValueError as ve:
            raise ValidationException._with_error(
                AzureMLError.create(InvalidArgumentType, target="y", argument="y", actual_type=type(y_df),
                                    expected_types="pandas.DataFrame"),
                inner_exception=ve
            ) from ve

    y_raw_stats = RawFeatureStats(y_df.iloc[:, 0])
    utilities._log_raw_data_stat(
        y_raw_stats,
        prefix_message="[YCol]"
    )

    # log the data characteristics
    if sparse.issparse(raw_experiment_data.X):
        logger.info("The sparse matrix is not supported for getting col characteristics.")
    else:
        x_df = raw_experiment_data.X
        if not isinstance(x_df, pd.DataFrame):
            x_df = pd.DataFrame(raw_experiment_data.X)
        for column in x_df.columns:
            raw_stats = RawFeatureStats(x_df[column])
            utilities._log_raw_data_stat(
                raw_stats,
                prefix_message="[XColNum:{}]".format(x_df.columns.get_loc(column))
            )


def _add_raw_column_names_to_X(X: DataInputType, x_raw_column_names: Optional[np.ndarray] = None,
                               time_column_name: Optional[str] = None) -> pd.DataFrame:
    """
    Add raw column names to X.

    :param x_raw_column_names: List of raw column names
    :param X: dataframe / array
    :raise ValueError if number of raw column names is not same as the number of columns in X
    :return: Dataframe with column names
    """
    # If X is already a DataFrame, then return X. Assumption here is that raw column names
    # are already present in the data frame header. The passed x_raw_column_names are not needed.
    if isinstance(X, pd.DataFrame):
        X = infer_objects_safe(X)
        if time_column_name is not None:
            try:
                X = _time_series_column_helper.convert_to_datetime(X, time_column_name)
            except Exception:
                pass
        return X

    # If x_raw_column_names is passed, check whether it is valid
    if x_raw_column_names is not None:
        # Combine the raw feature names with X
        number_of_columns = 1 if len(X.shape) == 1 else X.shape[1]
        Contract.assert_true(
            x_raw_column_names.shape[0] == number_of_columns,
            "Number of raw column names {} and number of columns in input data {} do not match".format(
                x_raw_column_names.shape[0], number_of_columns)
        )

    if not scipy.sparse.issparse(X):
        X_with_raw_columns = pd.DataFrame(
            data=X, columns=x_raw_column_names.tolist() if x_raw_column_names is not None else None)
        X_with_raw_columns = infer_objects_safe(X_with_raw_columns)
        # Do our best to convert time_column_name to datetime.
        if time_column_name is not None:
            try:
                X_with_raw_columns = _time_series_column_helper.convert_to_datetime(
                    X_with_raw_columns, time_column_name)
            except Exception:
                pass
        return X_with_raw_columns
    else:

        # pd.SparseDataFrame was deprecated since pandas 0.25.1.
        X_sparce = pd.DataFrame.sparse.from_spmatrix(
            data=X, columns=x_raw_column_names.tolist() if x_raw_column_names is not None else None)
        # In the new implementation of sparse data frame, pandas replaces missing values in the sparse
        # matrix by zeroes instead of np.NaN-s. Here we make sure that we fill the data as before.
        for col in X_sparce.columns:
            if isinstance(X_sparce[col].dtype, pd.SparseDtype):
                X_sparce[col].values.fill_value = np.NaN
        return X_sparce


def _get_dummy_value_by_purpose_or_dtype(purpose: Optional[FeatureType] = None,
                                         npdtype: Optional[np.dtype] = None) -> Tuple[Any, np.dtype]:
    """
    Get dummy values by either purpose or dtype of the column. If purpose is provided, it will get preference
    over dtype since column purpose can be overridden by user. Numeric FeatureTypes fall back to using dtype to
    differentiate between int and float types. If neither purpose nor dtype is provided, a dummy value is picked
    based on the assumption that featurization was turned off.

    :param purpose: The FeatureType of the column
    :param npdtype: The dtype of the column
    :return: The dummy value
    """
    if purpose and purpose != FeatureType.Numeric:
        return _DUMMY_VALUES_FOR_FEATURE.get(str(purpose), (_DUMMY_VALUES_FOR_TYPE['str'], np.dtype('object')))

    if npdtype:
        for dtype_substring in _DUMMY_VALUES_FOR_TYPE.keys():
            if dtype_substring in npdtype.name:
                return _DUMMY_VALUES_FOR_TYPE[dtype_substring], npdtype

    # If neither the dtype nor column purpose is known, it means featurization was turned off and
    # the user passed a numpy array or a sparse matrix. We can safely return a numeric value.
    return _DUMMY_VALUES_FOR_TYPE['int'], np.dtype('int64')


def get_data_snapshot(data: pd.DataFrame) -> str:
    """
    Get the snapshot of the data.

    :param data: The data frame to be used as a template.
    :return: The data snapshot string.
    """
    first_row = data.head(1)
    column_names_and_types = data.dtypes.to_dict()
    df_str = _get_data_snapshot_helper(
        first_row,
        column_names_and_types=column_names_and_types,
        column_purposes=None)
    return _format_pandas_snapshot_str(df_str)


def _get_data_snapshot_helper(data: Union[pd.DataFrame, pd.Series],
                              column_names_and_types: Optional[Dict[str, np.dtype]] = None,
                              column_purposes: Optional[List[StatsAndColumnPurposeType]] = None) -> str:
    Contract.assert_type(data, "data", (pd.DataFrame, pd.Series))
    if isinstance(data, pd.DataFrame):
        Contract.assert_value(column_names_and_types, "column_names_and_types")
        col_str_list = []
        column_names_and_types = cast(Dict[str, np.dtype], column_names_and_types)
        if not column_purposes:
            # if column_purposes is not set, construct the column purpose array
            # and set the purpose and raw_stats set to None
            column_purposes = [(None, None, col) for col in column_names_and_types.keys()]  # type:ignore
        for rawstats, purpose, col in column_purposes:
            dtype = column_names_and_types[col]
            col_val, col_type = _get_dummy_value_by_purpose_or_dtype(npdtype=dtype, purpose=purpose)  # type:ignore
            col_val = json.dumps([col_val]) if isinstance(col_val, str) else [col_val]
            col_str = "{0}: pd.Series({1}, dtype={2})".format(
                json.dumps(col), col_val, json.dumps(str(col_type)))
            col_str_list.append(col_str)
        snapshot_str = "{" + ", ".join(col_str_list) + "}"
    else:
        # data is of type pd.Series
        if not column_purposes:
            # if column_purposes is not set, featurization was turned off
            # construct the column purpose array and set the purpose and raw_stats set to None
            column_purposes = [(None, None, col) for col in range(len(data))]  # type:ignore
        dummy_data = pd.Series([_get_dummy_value_by_purpose_or_dtype(purpose=purpose)[0]  # type:ignore
                                for rawstats, purpose, col in column_purposes])
        snapshot_json_str = dummy_data.to_json(orient='values', date_format='iso')
        snapshot_str = str(json.loads(snapshot_json_str))
    return snapshot_str


class FeaturizationJsonParser:
    """
    Class for constructing and deconstructing the featurization JSON. Builds and saves it in the setup run for
    JOS to interpret, and processes the returned JSON from JOS in the featurization run.

    Example JSON:
    {
        "featurizers": [
            {
                "index": 0,
                "transformers": [
                    "StringCastTransformer",
                    "TfidfVectorizer"
                ]
            },
            {
                "index": 1,
                "transformers": [
                    "StringCastTransformer",
                    "TfidfVectorizer"
                ]
            },
            {
                "index": 2,
                "transformers": [
                    "StringCastTransformer",
                    "TfidfVectorizer",
                    "PretrainedTextDNNTransformer"
                ],
                "is_distributable": True,
                "is_separable": True
            }
        ]
    }
    """
    @staticmethod
    def _build_jsonifiable_featurization_props(feature_config: Union[List[TransformerAndMapper], DataFrameMapper]) \
            -> Dict[str, Union[List[Dict[str, Any]], bool]]:
        """
        Function encapsulating the JSON construction logic. Given the feature config, extracts the
        transformer names for each featurizer, notes that featurizer's index in the config, and
        associates any necessary flags (e.g. distributed) with the entry.

        :param feature_config: The feature_config generated in the setup run's data transformer.
        :return: A jsonifiable featurizer dict.
        """
        if isinstance(feature_config, DataFrameMapper):
            featurizers = [feature_config.features[i][1] for i in range(len(feature_config.features))]
        else:
            featurizers = [feature_config[i].transformers for i in range(len(feature_config))]

        featurizer_properties_list = []  # type: List[Dict[str, Any]]
        for index, featurizer in enumerate(featurizers):
            featurizer_properties_list.append({
                FeaturizationRunConstants.INDEX_KEY: index,
                FeaturizationRunConstants.TRANSFORMERS_KEY: get_transform_names(featurizer),
                FeaturizationRunConstants.IS_DISTRIBUTABLE:
                    does_property_hold_for_featurizer(featurizer, FeaturizationRunConstants.IS_DISTRIBUTABLE),
                FeaturizationRunConstants.IS_SEPARABLE:
                    does_property_hold_for_featurizer(featurizer, FeaturizationRunConstants.IS_SEPARABLE)
            })
        return {FeaturizationRunConstants.FEATURIZERS_KEY: featurizer_properties_list}

    @staticmethod
    def save_featurization_json(featurization_props: Dict[str, Union[List[Dict[str, Any]], bool]]) -> None:
        """
        Builds featurization json and saves it to the run's artifact store.

        :param featurization_props: The featurization properties distilled from the feature_config
        to be json serialized.
        :return: None.
        """
        run = Run.get_context()
        with logging_utilities.log_activity(logger=logger, activity_name="FeaturizationJsonUpload"):
            with open(FeaturizationRunConstants.FEATURIZATION_JSON_PATH, 'w') as file_obj:
                json.dump(featurization_props, file_obj)
            try:
                run.upload_file(FeaturizationRunConstants.FEATURIZATION_JSON_PATH,
                                FeaturizationRunConstants.FEATURIZATION_JSON_PATH)
            except AzureMLAggregatedException as error:
                # don't fail when run upload results in conflict
                if "Resource Conflict: ArtifactId" in error.message:
                    logger.warning("Artifact upload failed with conflict. The file already exists.")
                else:
                    raise

    @staticmethod
    def parse_featurizer_container(json_props: str,
                                   is_onnx_compatible: bool = False) -> "FeaturizerContainer":
        """
        Given the fragment of the featurization JSON string corresponding to to the featurizer list,
        return the corresponding featurizer list object with the correct properties.

        :param json_props: The json fragment, containing the properties for the featurizers and featurizer list.
        :param is_onnx_compatible: Boolean flag for whether onnx is enabled or not.
        :return: The featurizer list object.
        """
        try:
            featurizer_container_properties = json.loads(json_props)
            list_of_featurizers = \
                [FeaturizerFactory.get_featurizer(featurizer_props, is_onnx_compatible=is_onnx_compatible)
                 for featurizer_props in featurizer_container_properties.pop(
                    FeaturizationRunConstants.FEATURIZERS_KEY)]
            return FeaturizerContainer(featurizer_list=list_of_featurizers, **featurizer_container_properties)
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            logger.exception("Malformed JSON provided to independent featurizer run.")
            logging_utilities.log_traceback(e, logger)
            raise


def _add_new_numeric_column_in_data(
        data: DataInputType,
        column_names_and_types: Optional[Dict[str, np.dtype]],
        column_names: List[str]
) -> pd.DataFrame:
    """Add the column in column_names as numeric columns to the copy of the data."""
    if isinstance(data, Dataflow) and not column_names_and_types:
        # We need some data to figure out pandas dtypes.
        data = data.take(1000).to_pandas_dataframe()

    # Forecasting quantiles only support pd.DataFrame
    Validation.validate_type(data, "data", pd.DataFrame)
    data = data.copy()
    for col_name in column_names:
        data[col_name] = 0.

    return data


def _add_new_numeric_column_purposes(
        data: pd.DataFrame,
        column_purposes: Optional[List[StatsAndColumnPurposeType]],
        column_names: List[str]
) -> None:
    """Add numeric columns into column purposes."""
    if column_purposes is None:
        return
    for col_name in column_names:
        column_purposes.append((RawFeatureStats(data[col_name]), FeatureType.Numeric, col_name))


def _format_pandas_snapshot_str(raw_snapshot_str: str) -> str:
    return 'pd.DataFrame(' + raw_snapshot_str + ')'


def _get_data_snapshot_with_quantiles(
        data: DataInputType, column_names_and_types: Optional[Dict[str, np.dtype]] = None,
        column_purposes: Optional[List[StatsAndColumnPurposeType]] = None,
        is_forecasting: bool = False,
        is_raw: bool = True,
        include_cols: Optional[List[str]] = None
) -> Any:
    """
    Get the data snapshot with quantiles for the input data. If raw data, then the lower and upper quantile column
    names will be added and if it is prediction data, the lower, mid and upper quantile prediction columns will
    be added.
    """
    Contract.assert_true(is_forecasting, "Only forecasting jobs support quantiles in the input and output.")
    if is_raw:
        quantile_columns = [
            TimeSeriesInternal.QUANTILE_LOWER_COLUMN_NAME, TimeSeriesInternal.QUANTILE_UPPER_COLUMN_NAME]
    else:
        quantile_columns = [
            TimeSeriesInternal.QUANTILE_LOWER_FORECAST_COLUMN_NAME,
            TimeSeriesInternal.QUANTILE_UPPER_FORECAST_COLUMN_NAME,
            TimeSeriesInternal.QUANTILE_MID_FORECAST_COLUMN_NAME
        ]

    data = _add_new_numeric_column_in_data(data, column_names_and_types, quantile_columns)
    if include_cols:
        include_cols.extend(quantile_columns)
        # some column may not present in the dataset when wrong config is passing in.
        col_in_data = [col for col in include_cols if col in data.columns]
        data = data[col_in_data]
    column_names_and_types = copy.deepcopy(column_names_and_types)

    new_column_names_and_types = data.dtypes.to_dict()
    if not column_names_and_types:
        column_names_and_types = new_column_names_and_types
    else:
        for c, dtypes in new_column_names_and_types.items():
            if c in quantile_columns:
                column_names_and_types[c] = dtypes

    column_purposes = copy.deepcopy(column_purposes)
    _add_new_numeric_column_purposes(data, column_purposes, quantile_columns)

    return _format_pandas_snapshot_str(
        _get_data_snapshot_helper(data, column_names_and_types, column_purposes))


def _log_data_info(data_name: str,
                   data: Optional[np.ndarray]) -> None:
    """
    Log details about the data.

    :param data_name: Name of data to inspect.
    :param data: Data to inspect.
    """
    if data is not None:
        message_format = "{} datatype is {}, shape is {}, datasize is {}."
        memory_size = memory_utilities.get_data_memory_size(data)
        logger.info(message_format.format(data_name, type(data), data.shape, memory_size))
    else:
        message_format = "{} is None, no data details to log."
        logger.info(message_format.format(data_name))
