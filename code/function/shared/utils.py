import logging

from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob import BlobProperties
from azure.storage.blob.aio import BlobServiceClient


def get_azure_credential(
    managed_identity_client_id: str = None,
) -> DefaultAzureCredential:
    """Creates a default azure crendetial used for authentication.

    managed_identity_client_id (str): Specifies the client id of a managed identity.
    RETURNS (str): Returns a default azure credential.
    """
    if managed_identity_client_id is None:
        return DefaultAzureCredential()
    else:
        return DefaultAzureCredential(
            managed_identity_client_id=managed_identity_client_id,
        )


async def get_blob_properties(
    storage_domain_name: str,
    storage_container_name: str,
    storage_blob_name: str,
    managed_identity_client_id: str = None,
) -> BlobProperties:
    """Copy file from source blob storage container async to sink blob storage container.

    storage_domain_name (str): The domain name of the storage account to which the file will be copied.
    storage_container_name (str): The container name of the storage account.
    storage_blob_name (str): The blob name of the storage account.
    managed_identity_client_id (str): Specifies the managed identity client id used for auth.
    RETURNS (BlobProperties): Returns the properties of the blob.
    """
    logging.info(
        f"Get properties for blob: 'https://{storage_domain_name}/{storage_container_name}/{storage_blob_name}'."
    )

    # Create credentials
    credential = get_azure_credential(
        managed_identity_client_id=managed_identity_client_id
    )

    # Copy blob file
    async with BlobServiceClient(
        account_url=f"https://{storage_domain_name}",
        credential=credential,
    ) as blob_service_client:
        blob_client = blob_service_client.get_blob_client(
            container=storage_container_name,
            blob=storage_blob_name,
        )
        blob_properties = await blob_client.get_blob_properties()

    return blob_properties
