import logging

import azure.functions as func
import azurefunctions.extensions.bindings.blob as blob
from shared.config import settings
from shared.utils import get_blob_properties

bp = func.Blueprint()


@bp.function_name("VideoUpload")
@bp.blob_trigger(
    arg_name="client",
    path="upload-newsvideos/{name}",
    connection="BlobTrigger",
    # source="LogsAndContainerScan",
)
async def upload_video(client: blob.BlobClient):
    logging.info("File upload detected.")

    # Initialize
    logging.info("Initialize")
    _ = await get_blob_properties(
        storage_domain_name=f"{client.account_name}.blob.core.windows.net",
        storage_container_name=client.container_name,
        storage_blob_name=client.blob_name,
        managed_identity_client_id=settings.MANAGED_IDENTITY_CLIENT_ID,
    )
    logging.info(f"Completed Function run successfully.")
