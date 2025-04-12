# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import pathlib
import tempfile
from typing import Any, Iterable, Optional, List

from azure.core.exceptions import ResourceExistsError
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import CacheException
from azureml.automl.runtime.shared._cache_constants import Keys
from azureml.automl.runtime.shared.lazy_file_cache_store import DirCachedValueMetadata, LazyFileCacheStore
from azureml.core import Run as AzureMLRun

logger = logging.getLogger(__name__)

# Default timeout for uploading / downloading the files
DEFAULT_IO_TIMEOUT_SECONDS = 3600


class RunBackedCacheStore(LazyFileCacheStore):
    """
    Cache store that is backed by the Run's default artifact storage. Note that this cache store does not allow
    key overwrites, the behavior is non-deterministic (as Run based storage does not allow deleting or
    overwriting files)

    All objects added to this cache store will be available on the Run under the `artifact_path` specified during
    the initialization of this class.
    The files are uploaded to the run on demand, via. a call to `flush()` - until then, all serialized files are only
    available on the local file system, yet available to query (i.e. via. get()). Only new files are uploaded
    on the run, i.e., overwrites

    Ensure that flush() is the last operation on this cache store, subsequent key retrievals will require re-loading
    the cache contents (via. call to load()), as files locally may be deleted.

    Note: Cache Stores are currently serialized / deserialized (e.g. when spawning processes). Please ensure any new
        attributes added at the class level are handled in the get_state and set_state dunder methods.
    """

    def __init__(
        self, run: AzureMLRun, artifact_path: Optional[str] = None, temp_dir_path: Optional[str] = None
    ) -> None:
        """
        Construct an instance of RunBackedCacheStore

        :param run:  An instance of AzureML Run on which to create / read objects
        :param artifact_path: The root directory from which to create / read objects
        """
        self._temp_dir_path = temp_dir_path or tempfile.mkdtemp()
        self._run = run
        self._artifact_path = artifact_path or "outputs"

        super().__init__(os.path.join(self._temp_dir_path, self._artifact_path))

    def _download_cache(self) -> None:
        """
        Download files from the Run to the _root directory and return the list of files downloaded.
        """
        try:
            local_path = str(pathlib.Path(self._root).parent)
            local_files = set(self.get_available_keys(local_path).keys())
            if len(local_files) > 0:  # we have some files already downloaded locally
                run_files = self._get_keys_available_on_run()
                # calculate the delta b/w what's available locally and what's currently on the Run
                files_to_download = run_files - local_files
                if len(files_to_download) > 0:
                    logger.info(f"Downloading {len(files_to_download)} files locally.")
                    for f in files_to_download:
                        f_name = "{}/{}".format(self._artifact_path, f)
                        f_output_path = os.path.join(local_path, f_name)
                        self._run.download_file(name=f_name, output_file_path=f_output_path)
            else:
                logger.info("No files are available for the cache store locally, downloading files from the Run.")
                self._run.download_files(
                    prefix=self._artifact_path,
                    output_directory=local_path,
                    batch_size=500,
                    timeout_seconds=DEFAULT_IO_TIMEOUT_SECONDS,
                )
        except Exception as ex:
            logging_utilities.log_traceback(ex, logger, is_critical=False)
            msg = f"Failed to download files from the data store. Error type: {ex.__class__.__name__}"
            raise CacheException.from_exception(ex, msg=msg).with_generic_msg(msg)

    def load(self) -> None:
        """
        Read the contents of the blob at the path and store keys, data references to them
        in memory. This will hydrate `cached_items` field of this.
        """
        self._download_cache()
        # load the files as items available on the cache
        super(RunBackedCacheStore, self).load()
        self._sanitize_cache_items()

    def add(self, keys: Iterable[str], values: Iterable[Any]) -> None:
        """
        Serialize the values and add them to cache and upload to the azure blob container.

        :param keys: List of keys.
        :param values: Corresponding values to be cached.
        """
        Contract.assert_value(value=keys, name="keys", log_safe=True)
        super(RunBackedCacheStore, self).add(keys, values)

    def flush(self, _batch_upload: bool = True) -> None:
        """
        Uploads the contents of the cache store to the Run as artifacts and clean up the local directory

        :return: None
        """
        try:
            with self.log_activity():
                local_paths = []
                remote_paths = []

                run_files = self._get_keys_available_on_run()
                logger.info(f"Files available on the run: {run_files}")
                run_files_with_dirs = set(run_files)
                # add all possible parent dirs for run files, inorder to filter dir keys
                for p in run_files:
                    path = pathlib.Path(p)
                    run_files_with_dirs.update(
                        [
                            p.as_posix()
                            for p in path.parents
                            if p.as_posix() != "." and p.as_posix() not in run_files_with_dirs
                        ]
                    )

                for key, item in self.cache_items.items():
                    item.update_remote_path(key, self._artifact_path)
                    rel_path = pathlib.Path(item.remote_path).relative_to(self._artifact_path).as_posix()
                    if rel_path not in run_files_with_dirs:
                        if isinstance(item, DirCachedValueMetadata):
                            for _, dir_item in item.dir_items.items():
                                local_paths.append(dir_item.local_path)
                                remote_paths.append(dir_item.remote_path)
                        else:
                            local_paths.append(item.local_path)
                            remote_paths.append(item.remote_path)

                if len(local_paths) > 0:
                    logger.info(f"flush: Uploading keys: {remote_paths}")
                    self._update_index_file()
                    # Add index file for upload
                    upload_path = (
                        (pathlib.Path(self._artifact_path) / Keys.DEFAULT_NAMESPACE / Keys.INDICES_DIR)
                        .joinpath(self._index_file_name)
                        .as_posix()
                    )
                    local_paths.append(self._index_file_path)
                    remote_paths.append(upload_path)
                    if _batch_upload:
                        self._batch_upload_to_run(remote_paths, local_paths)
                    else:
                        # upload files individually
                        for r, l in zip(remote_paths, local_paths):
                            try:
                                self._run.upload_file(r, l)
                            except Exception as ex:
                                if isinstance(ex, ResourceExistsError) or "Resource conflict" in str(ex):
                                    logger.warning(f"File {r} already exists on the run. Ignoring.")
                                else:
                                    raise
                    logger.info("flush: Uploaded {} files to cache store".format(len(local_paths)))
        except Exception as ex:
            logging_utilities.log_traceback(ex, logger, is_critical=False)
            msg = f"flush: Failed to upload local files to the Run. Error type: {ex.__class__.__name__}"
            raise CacheException.from_exception(ex, msg=msg).with_generic_msg(msg)

        # Delete files available locally
        super(RunBackedCacheStore, self).remove_all()

    def _batch_upload_to_run(self, remote_paths: List[str], local_paths: List[str]) -> None:
        try:
            # attempt to batch upload the files
            self._run.upload_files(names=remote_paths, paths=local_paths, timeout_seconds=DEFAULT_IO_TIMEOUT_SECONDS)
        except Exception as ex:
            logging_utilities.log_traceback(ex, logger, is_critical=False)
            if isinstance(ex, ResourceExistsError) or "Resource conflict" in str(ex):
                logger.warning(
                    "Batch upload of files to the run failed. "
                    "Fallback to uploading files individually, this may take some time..."
                )
                return self.flush(_batch_upload=False)
            raise

    def _get_keys_available_on_run(self):
        """Retrieve the keys that are available on the Run"""
        run_paths = [f for f in self._run.get_file_names() if f.startswith(self._artifact_path)]
        run_files = set([pathlib.Path(p).relative_to(self._artifact_path).as_posix() for p in run_paths])
        return run_files

    def __getstate__(self):
        return super().__getstate__(), {
            "run_id": self._run.id,
            "artifact_path": self._artifact_path,
            "temp_dir_path": self._temp_dir_path,
        }

    def __setstate__(self, state):
        super_state, my_state = state
        curr_run = AzureMLRun.get_context()  # to get the current experiment
        self._run = AzureMLRun(experiment=curr_run.experiment, run_id=my_state.get("run_id"))  # restore original run
        self._artifact_path = my_state.get("artifact_path")
        self._temp_dir_path = my_state.get("temp_dir_path")
        super().__setstate__(super_state)
