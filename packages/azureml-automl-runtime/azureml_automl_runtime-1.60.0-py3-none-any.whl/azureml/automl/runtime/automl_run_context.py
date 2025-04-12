# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Context manager that wraps an AutoML run context."""
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory
import json
import logging
import os
import pickle
import platform
import re
import sklearn

from .onnx_convert import OnnxConverter
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml._common._error_definition import AzureMLError
from azureml.automl.core import package_utilities
from azureml.automl.core.shared import constants, exceptions, logging_utilities, reference_codes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import AutoMLInternal
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared.pickler import DefaultPickler
from azureml.automl.core._run import RunType
import azureml.automl.core.inference as inference
import azureml.automl.core._exception_utilities as exception_utilities
from azureml.training.tabular.models.mlflow import timeseries as ts_mlflow

# Timeout in seconds for artifact upload
ARTIFACT_UPLOAD_TIMEOUT_SECONDS = 1200

logger = logging.getLogger(__name__)

try:
    import mlflow
    from mlflow.tracking import MlflowClient

    has_mlflow = True
except ImportError:
    has_mlflow = False

logger = logging.getLogger(__name__)


class AutoMLAbstractRunContext(ABC):
    """Wrapper class for an AutoML run context."""

    def __init__(self):
        """Initialize the run context wrapper."""
        self._run_id = None  # type: Optional[str]
        self._uploaded_artifacts = None  # type: Optional[Dict[str, Any]]
        self._model_sizes = {}  # type: Dict[str, int]
        self._pickler = DefaultPickler()

    @abstractmethod
    def _get_run_internal(self) -> RunType:
        """Retrieve the run context. Must be overridden by subclasses."""
        raise NotImplementedError  # PII safe to raise directly

    def set_local(self, local: bool) -> None:
        """
        Set whether this run is local or not.

        :param local: Whether this run is local or not
        """
        with self.get_run() as run:
            run._is_local_run = local

    @property
    def parent_run_id(self) -> str:
        """
        Get the parent run id for this execution context, or the run id if this is a parent run.

        :return: the parent run id
        """
        match = re.fullmatch(r'(.*?)_(?:setup|[0-9]+)', self.run_id)
        if match is None:
            return self.run_id
        return match.group(1)

    @property
    def run_id(self) -> str:
        """
        Get the run id associated with the run wrapped by this run context. The run id is assumed to be immutable.

        :return: the run id
        """
        if self._run_id is None:
            with self.get_run() as run:
                self._run_id = run.id
        return cast(str, self._run_id)

    @contextmanager
    def get_run(self):
        """
        Yield a run context.

        Wrapped by contextlib to convert it to a context manager. Nested invocations will return the same run context.
        """
        yield self._get_run_internal()

    def save_model_output(self, fitted_pipeline: Any, remote_path: str, working_dir: str) -> None:
        """
        Save the given fitted model to the given path using this run context.

        :param fitted_pipeline: the fitted model to save
        :param remote_path: the path to save to
        """
        logger.info("Saving models.")
        self._save_model(fitted_pipeline, remote_path, self._save_python_model, working_dir, save_model_path=True)

    def save_onnx_model_output(self, onnx_model: object, remote_path: str, working_dir: str) -> None:
        """
        Save the given onnx model to the given remote path using this run context.

        :param onnx_model: the onnx model to save
        :param remote_path: the path to save to
        """
        self._save_model(onnx_model, remote_path, self._save_onnx_model, working_dir)

    def save_onnx_model_resource(self, onnx_resource: Dict[Any, Any], remote_path: str, working_dir: str) \
            -> None:
        """
        Save the given onnx model resource to the given remote path using this run context.

        :param onnx_resource: the onnx model resource dict to save
        :param remote_path: the path to save to
        """
        self._save_file(onnx_resource, remote_path, False, self._save_dict_to_json_output, working_dir)

    def _save_model(self, model_object: Any, remote_path: str,
                    serialization_method: "Callable[[Any], None]",
                    working_directory: Optional[str],
                    save_model_path: bool = False) -> None:
        self._save_file(model_object, remote_path, binary_mode=True, serialization_method=serialization_method,
                        working_directory=working_directory, save_model_path=save_model_path)

    def _save_file(self, save_object: Any, remote_path: str, binary_mode: bool,
                   serialization_method: "Callable[[Any], None]",
                   working_directory: str,
                   save_model_path: bool = False) -> None:
        if binary_mode:
            write_mode = "wb+"
        else:
            write_mode = "w+"
        output = None
        try:
            # Get the suffix of the model path, e.g. 'outputs/model.pt' will get '.pt'.
            _, suffix = os.path.splitext(remote_path)
            # Init the temp file with correct suffix.
            output = NamedTemporaryFile(mode=write_mode, suffix=suffix, delete=False, dir=working_directory)
            serialization_method(save_object, output)
            with self.get_run() as run_object:
                if save_model_path:
                    # Save the property of the remote model path.
                    run_object.add_properties({
                        constants.PROPERTY_KEY_OF_MODEL_PATH: remote_path
                    })
                artifact_response = run_object.upload_file(remote_path, output.name)
                if artifact_response:
                    self._uploaded_artifacts = artifact_response.artifacts
        finally:
            if output is not None:
                output.close()
                try:
                    os.unlink(output.name)
                except PermissionError as e:
                    DeleteFileException = exceptions.DeleteFileException.from_exception(
                        e,
                        target="_save_file",
                        reference_code=reference_codes.ReferenceCodes._DELETE_FILE_PERMISSION_ERROR
                    ).with_generic_msg("PermissionError while cleaning up temp file.")
                    logging_utilities.log_traceback(DeleteFileException, logger)

    def _get_artifact_id(self, artifact_path: str) -> str:
        """
        Parse the run history response message to get the artifact ID.

        :param artifact_path: the path to artifact
        :return: the composed artifact ID string
        """
        try:
            if self._uploaded_artifacts and self._uploaded_artifacts.get(artifact_path) is not None:
                return cast(str, inference.AMLArtifactIDHeader
                            + self._uploaded_artifacts[artifact_path].artifact_id)
            else:
                return ""
        except Exception:
            return ""

    def _get_artifact_id_run_properties(self):
        properties = {
            inference.AutoMLInferenceArtifactIDs.CondaEnvDataLocation:
                self._get_artifact_id(constants.CONDA_ENV_FILE_PATH),
            inference.AutoMLInferenceArtifactIDs.ModelDataLocation:
                self._get_artifact_id(constants.MODEL_PATH),
            inference.AutoMLInferenceArtifactIDs.ModelSizeOnDisk:
                str(self._model_sizes.get(constants.MODEL_PATH, '')),
            inference.AutoMLInferenceArtifactIDs.ScoringDataLocation:
                self._get_artifact_id(constants.SCORING_FILE_PATH),
            inference.AutoMLInferenceArtifactIDs.ScoringDataLocationV2:
                self._get_artifact_id(constants.SCORING_FILE_V2_PATH),
            inference.AutoMLInferenceArtifactIDs.ScoringDataLocationPBI:
                self._get_artifact_id(constants.SCORING_FILE_PBI_V1_PATH)
        }
        return properties

    def _save_onnx_model(self, model_object: Any, model_output) -> None:
        OnnxConverter.save_onnx_model(model_object, model_output.name)

    def _save_python_model(self, model_object: Any, model_output) -> None:
        with (open(model_output.name, 'wb')):
            _, ext = os.path.splitext(model_output.name)
            if ext == '.pt' or ext == '.pth':
                try:
                    import torch
                    torch.save(model_object, model_output)
                except Exception:
                    self._pickler.dump(model_object, model_output.name, model_output)
            else:
                self._pickler.dump(model_object, model_output.name, model_output)
            model_output.flush()

    def _save_mlflow_model(self,
                           fitted_pipeline: Any,
                           working_dir: str,
                           options: Dict[str, Any],
                           inference_deps: Optional[CondaDependencies] = None,
                           model_name: Optional[str] = None,
                           metadata: Optional[Dict[str, Any]] = None):
        """
        Save the model in mlflow format and upload it to the tracking store.

        :param fitted_pipeline: The model to be saved.
        :param working_dir: The local working directory to save the models in before uploading.
        :param options: The MLflow options to be used when saving the model.
        :param model_name: The file name of the model, needed if we want to directly serialize it first
        before MLflow conversion.
        :param metadata: Dictionary of meta info to be dumped in MLmodel file.
        """
        try:
            import torch
            is_torch = isinstance(fitted_pipeline, torch.nn.Module)
        except Exception:
            is_torch = False

        remote_path = constants.MLFLOW_OUTPUT_PATH

        # for nlp models, only take base dependencies.
        if inference_deps is not None:
            conda_deps = inference_deps
        else:
            all_pip_dependencies, all_conda_dependencies, channels = \
                package_utilities._get_curated_environment_conda_list_packages()

            python_version = platform.python_version()
            conda_deps = CondaDependencies.create(conda_packages=all_conda_dependencies,
                                                  python_version=python_version,
                                                  pip_packages=all_pip_dependencies,
                                                  pin_sdk_version=False)

            # some mlflow deployments require conda-forge to be first in the list of channels
            for channel in conda_deps.conda_channels:
                if channel != "conda-forge":
                    conda_deps.remove_channel(channel)
            for channel in channels:
                conda_deps.add_channel(channel)
            conda_deps.add_channel("anaconda")

        cd = conda_deps.as_dict()

        metadata = {} if not metadata else metadata
        _metadata = self._get_env_metadata()
        if _metadata:
            metadata.update(_metadata)
        logger.info("Logging MLFlow model to tracking store.")
        if options.get(constants.MLFlowLiterals.FLAVOR_FORECASTING, False) is True:
            # For the forecasting models, we need to use forecasting mlflow flavor to log/save the mlflow model.
            logger.info("Saving forecasting model to {}.".format(remote_path))
            ts_mlflow.log_model(
                fc_model=fitted_pipeline,
                artifact_path=remote_path,
                conda_env=cd,
                signature=options.get(constants.MLFlowLiterals.SCHEMA_SIGNATURE),
                serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_PICKLE,
                pickle_module=pickle,
                metadata=metadata)
        elif isinstance(fitted_pipeline, sklearn.pipeline.Pipeline):
            logger.info("Saving sklearn model to {}.".format(remote_path))
            mlflow.sklearn.log_model(
                sk_model=fitted_pipeline,
                artifact_path=remote_path,
                conda_env=cd,
                signature=options.get(constants.MLFlowLiterals.SCHEMA_SIGNATURE),
                serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_PICKLE,
                metadata=metadata)
            logger.info('Saved mlflow model successfully.')
        elif is_torch:
            logger.info("Saving pytorch model to {}.".format(remote_path))
            mlflow.pytorch.log_model(
                pytorch_model=fitted_pipeline,
                artifact_path=remote_path,
                conda_env=cd,
                signature=options.get(constants.MLFlowLiterals.SCHEMA_SIGNATURE),
                pickle_module=pickle,
                metadata=metadata)
        elif self._mlflow_custom_pyfunc_flavor_workflow(options) == constants.MLFlowLiterals.LOADER:
            if constants.MLFlowLiterals.DATA_PATH not in options:
                options[constants.MLFlowLiterals.DATA_PATH] = model_name
            logger.info("Saving model resources to {}.".format(remote_path))
            mlflow.pyfunc.log_model(
                artifact_path=remote_path,
                loader_module=options[constants.MLFlowLiterals.LOADER],
                data_path=options[constants.MLFlowLiterals.DATA_PATH],
                signature=options.get(constants.MLFlowLiterals.SCHEMA_SIGNATURE, None),
                input_example=options.get(constants.MLFlowLiterals.INPUT_EXAMPLE, None),
                conda_env=cd,
                metadata=metadata)

        elif self._mlflow_custom_pyfunc_flavor_workflow(options) == constants.MLFlowLiterals.WRAPPER:
            logger.info("Saving mlflow pyfunc model to {}.".format(remote_path))
            with open(os.path.join(working_dir,
                      constants.MLFlowLiterals.MODEL_SETTINGS_FILENAME), 'w') as settings_file:
                self._save_dict_to_json_output(options[constants.MLFlowLiterals.WRAPPER]._model_settings,
                                               settings_file)
            mlflow.pyfunc.log_model(artifact_path=remote_path,
                                    python_model=options[constants.MLFlowLiterals.WRAPPER],
                                    artifacts={"model": model_name, "settings": settings_file.name},
                                    conda_env=cd,
                                    signature=options[constants.MLFlowLiterals.SCHEMA_SIGNATURE],
                                    metadata=metadata)
            logger.info('Saved mlflow model successfully.')
        else:
            message = "Unknown model type could not be saved with mlflow."
            raise ClientException._with_error(
                AzureMLError.create(AutoMLInternal, target="save_mlflow", error_details=message)
            )

    @exception_utilities.ignore_exceptions
    def _get_env_metadata(self) -> Dict[str, Any]:
        metadata = None
        if os.getenv("ENABLE_METADATA") == "true":
            run = self._get_run_internal()
            # Improving this behavior with 1440665
            env = run.get_environment()

            # training CE image metadata details
            # this is hacky in response to iCM
            # https://portal.microsofticm.com/imp/v3/incidents/details/401023866/home
            # TODO to fix this and move into environments.py DockerImageDetails
            # https://msdata.visualstudio.com/Vienna/_workitems/edit/2508089
            img_details = env.get_image_details(run.experiment.workspace)
            docker_url = img_details.repository
            if img_details.registry and not docker_url.startswith(img_details.registry):
                docker_url = img_details.registry + "/" + docker_url

            metadata = {'azureml.base_image': docker_url, 'azureml.engine': 'automl'}
            logger.info("mlflow metadata base_image: {}".format(metadata))
        return metadata

    def _mlflow_custom_pyfunc_flavor_workflow(self, options: Dict[str, Any]) -> str:
        """
        Helper function to get the workflow type for mlflow custom pyfunc flavor.

        :param options: Related MLflow settings.
        :return: Returns the mlflow custom pyfunc flavor workflow type.
        """
        if constants.MLFlowLiterals.LOADER in options:
            return constants.MLFlowLiterals.LOADER
        elif constants.MLFlowLiterals.WRAPPER in options:
            return constants.MLFlowLiterals.WRAPPER

    def _save_str_output(self, str_object: Any, output) -> None:
        with open(output.name, "w") as f:
            f.write(str_object)

    def _save_dict_to_json_output(self, dict_object: Dict[Any, Any], output) -> None:
        with open(output.name, 'w') as f:
            json.dump(dict_object, f)

    def save_str_output(self, input_str: str, remote_path: str,
                        overwrite_mode: bool = False,
                        working_directory: Optional[str] = None) -> None:
        """
        Save the str file as a txt into the Artifacts.

        :param input_str: the input string.
        :param remote_path: the file name in the Artifacts.
        """
        self._save_file(input_str, remote_path, binary_mode=False,
                        serialization_method=self._save_str_output, working_directory=working_directory)

    def batch_save_artifacts(self,
                             working_directory: Optional[str],
                             input_strs: Dict[str, str],
                             model_outputs: Dict[str, Any],
                             save_as_mlflow: bool = False,
                             mlflow_options: Optional[Dict[str, Any]] = None,
                             metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Save a batch of text files and models into the Artifacts.
        This is more efficient than saving individual artifacts.

        :param working_directory: Directory to use for temporary storage.
        :param input_strs: Dictionary of strings. The key is the artifact name and the value is the content.
        :param model_outputs: Dictionary of models. The key is the artifact name and the value is the model.
        :param mlflow_options: Dictionary of MLflow settings/wrappers for model saving process.
        :param save_as_mlflow: Flag for whether to save using MLFlow to save the model.
        :param metadata: Dictionary of meta info to be dumped in MLmodel file.
        """
        temp_resources = []
        file_keys = []
        file_paths = []

        try:
            if save_as_mlflow and not has_mlflow:
                logger.warning("MLFlow is not present in the current environment. Can't save MLFlow models and "
                               "defaulting back to pickle.")
                save_as_mlflow = False

            inference_deps = None
            if constants.INFERENCE_DEPENDENCIES in input_strs.keys():
                inference_deps = input_strs.pop(constants.INFERENCE_DEPENDENCIES)

            for name, contents in input_strs.items():
                text_file = NamedTemporaryFile(mode="w", delete=False, dir=working_directory)
                self._save_str_output(contents, text_file)
                temp_resources.append(text_file)
                file_keys.append(name)
                file_paths.append(text_file.name)

            for name, model in model_outputs.items():
                # Get the suffix of the model path, e.g. 'outputs/model.pt' will get '.pt'.
                _, suffix = os.path.splitext(name)

                # Support legacy model save methodology for all scenarios to maintain SDK v1 compatibility.
                # Note that prefix only matters for MLflow code paths, for the file name may be surfaced
                # depending on the flavor.
                model_file = NamedTemporaryFile(mode="wb", prefix=constants.MLFlowLiterals.MODEL_IMPL_PREFIX,
                                                suffix=suffix, delete=False, dir=working_directory)
                self._save_python_model(model, model_file)
                self._model_sizes[name] = os.path.getsize(model_file.name)
                temp_resources.append(model_file)
                file_keys.append(name)
                file_paths.append(model_file.name)

                if save_as_mlflow and not isinstance(model, list):
                    try:
                        td = TemporaryDirectory(dir=working_directory)
                        temp_resources.append(td)

                        self._save_mlflow_model(fitted_pipeline=model,
                                                working_dir=td.name,
                                                options=mlflow_options or {},
                                                inference_deps=inference_deps,
                                                model_name=model_file.name,
                                                metadata=metadata)
                    except Exception as e:
                        logging_utilities.log_traceback(e, logger)
                        logger.warn("Failed when saving mlflow model with {}.".format(str(e)))

            self._batch_save_artifact_files(file_keys, file_paths)

        finally:
            for f in temp_resources:
                if isinstance(f, TemporaryDirectory):
                    f.cleanup()
                else:
                    f.close()
                    try:
                        os.unlink(f.name)
                    except PermissionError as e:
                        delete_file_exception = exceptions.DeleteFileException.from_exception(
                            e,
                            target="batch_save_artifacts",
                            reference_code=reference_codes.ReferenceCodes._DELETE_FILE_BATCH_PERMISSION_ERROR
                        ).with_generic_msg("PermissionError while cleaning up temp file.")
                        logging_utilities.log_traceback(delete_file_exception, logger)

    def _batch_save_artifact_files(self, file_keys: List[str], file_paths: List[str]) -> None:
        """
        Save a batch of files in artifact store.
        Batch uploading files is more efficient than uploading files one by one.
        """
        with self.get_run() as run_object:
            # Save the property of the remote model path.
            remote_model_path = ''
            if constants.MODEL_PATH in file_keys:
                # Save the model.pkl file
                remote_model_path = constants.MODEL_PATH
            elif constants.PT_MODEL_PATH in file_keys:
                # Save the model.pt file
                remote_model_path = constants.PT_MODEL_PATH
            run_object.add_properties({
                constants.PROPERTY_KEY_OF_MODEL_PATH: remote_model_path
            })

            upload_response = run_object.upload_files(file_keys, file_paths, return_artifacts=True,
                                                      timeout_seconds=ARTIFACT_UPLOAD_TIMEOUT_SECONDS)
            if upload_response:
                self._uploaded_artifacts = upload_response[0]

    def _register_mlflow_model(self):
        """
        Register the manually saved model so that we can use models:/ URI to fetch it.

        :return: ModelVersion
        """
        client = MlflowClient()
        child_run = self._get_run_internal()
        mlflow_run = client.get_run(child_run.id)

        model_name = child_run.id
        model_desc = "AutoML trained model."
        model_source_uri = '{}/outputs'.format(mlflow_run.info.artifact_uri)

        logger.info("Registering model found at {}.".format(model_source_uri))
        client.create_registered_model(model_name)
        model = client.create_model_version(model_name, model_source_uri, child_run.id, description=model_desc)
        logger.info("Registered model to models:/{}/{}".format(model.name, model.version))
        return model
