from typing import Union
from pathlib import Path
import logging

from . import core
from . import buckets

BUCKET_NAME = buckets.ASSETS

logger = logging.getLogger(__name__)


def download_plugins(
    local_dir: Union[str, Path],
    bucket: str = BUCKET_NAME,
    plugin_name: str = "",
) -> Path:
    """
    Download the plugins folder from the s3 assets bucket.
    args:
        local_dir: The local directory. Contents will be downloaded and placed into this directory.
        plugin_name: The name of the ,
    used to download specific plugins/folders.
    """
    local_dir = str(local_dir)
    plugins_root_dir = "plugins"
    remote_file_path = plugins_root_dir
    if plugin_name:
        remote_file_path += f"/{plugin_name}"
    if not Path(local_dir).exists():
        logger.warning(f"Creating dir: {Path(local_dir)}")
        Path(local_dir).mkdir(parents=True, exist_ok=True)
    result = core.download.folder(
        bucket_name=bucket, s3_folder=remote_file_path, local_dir=local_dir
    )
    # result = core.download.file(
    #     bucket_name=bucket,
    #     remote_file_path=remote_file_path,
    #     local_file_path=local_file_path,
    # )
    logger.warning(f"Assets downloaded result: {result}")
    return Path(result)


def download_plugin(
    local_dir: Union[str, Path],
    plugin_name: str,
    bucket: str = BUCKET_NAME,
) -> Path:
    """
    Download a single plugin (.zip file) form the plugins folder.
    args:
        local_dir: The local directory to place the zipfile into.
        plugin_name: The name of the plugin to download, without file extension.
    """
    local_dir = str(local_dir)
    plugins_root_dir = "plugins"
    remote_file_path = plugins_root_dir + f"/{plugin_name}.zip"
    local_file_path = f"{local_dir}/{Path(remote_file_path).name}"
    if not Path(local_dir).exists():
        logger.warning(f"Creating dir: {Path(local_dir)}")
        Path(local_dir).mkdir(parents=True, exist_ok=True)
    result = core.download.file(
        local_file_path=local_file_path,
        remote_file_path=remote_file_path,
        bucket_name=bucket,
    )
    logger.warning(f"Assets downloaded result: {result}")
    return Path(result)


# def upload_file(
#     submission_id: Union[str, UUID],
#     local_file_path: str,
#     remote_dir: str = "",
#     file_rename: Optional[str] = None,
#     bucket: str = BUCKET_NAME,
# ) -> str:
#     """
#     Upload a single file from the local filesystem into the target remote dir.
#     local_file_path: A path to the file in the local filesystem
#     remote_dir: The remote dir to place the file into, relative to the submission's root dir
#     file_rename: If provided, rename the file when uploading to s3.
#     Returns: The s3 file key relative to the submissioin root dir
#     """
#     submission_root_dir = str(submission_id)
#     file_name = file_rename if file_rename else Path(local_file_path).name
#     # Convert to path to handle double backslashes in case remote_dir is empty
#     remote_file_path = Path(f"{submission_root_dir}/{remote_dir}/{file_name}")
#     # If no remote_dir is specified, avoid leading '/'
#     submission_rel_file_path = (
#         Path(f"{remote_dir}/{file_name}") if remote_dir else Path(file_name)
#     )
#     core.upload.file(
#         bucket_name=bucket,
#         local_file=local_file_path,
#         remote_file=str(remote_file_path),
#     )
#     return str(submission_rel_file_path)
