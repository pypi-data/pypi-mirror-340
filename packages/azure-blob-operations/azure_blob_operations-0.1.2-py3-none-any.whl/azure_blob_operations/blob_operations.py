import io
import time
import os
from typing import Optional, Union, Any
from datetime import datetime, timedelta
from functools import lru_cache
from azure.storage.blob import (
    BlobServiceClient,
    ContentSettings,
    BlobSasPermissions,
    generate_blob_sas,
)
from werkzeug.datastructures import FileStorage
from .config import CONFIG
from .utils import validate_params

class BlobOperations:
    """Generic Azure Blob Storage operations."""

    @staticmethod
    @lru_cache(maxsize=32)
    def _get_blob_service_client(connection_string: str) -> BlobServiceClient:
        """Initialize and cache a BlobServiceClient for a given connection string."""
        validate_params(connection_string=connection_string)
        return BlobServiceClient.from_connection_string(connection_string)

    @staticmethod
    def download_blob(
        connection_string: str,
        container_name: str,
        blob_path: str,
        delete_after: Optional[bool] = None,
    ) -> io.BytesIO:
        """
        Download a blob to a BytesIO object.

        Args:
            connection_string: Azure Storage connection string.
            container_name: Name of the container.
            blob_path: Path to the blob.
            delete_after: Whether to delete the blob after downloading (default: None, treated as False).

        Returns:
            BytesIO object containing the blob content.

        Raises:
            Exception: If the blob is not found or download fails.
        """
        validate_params(
            connection_string=connection_string,
            container_name=container_name,
            blob_path=blob_path,
        )
        try:
            blob_client = BlobOperations._get_blob_service_client(connection_string).get_blob_client(
                container=container_name, blob=blob_path
            )
            blob_data = blob_client.download_blob().readall()
            if delete_after is True:  # Explicitly check for True, treat None as False
                blob_client.delete_blob()
            return blob_data
        except Exception as e:
            raise Exception(f"Blob not found: {blob_path}", 404)
        

    @staticmethod
    def upload_blob(
        connection_string: str,
        container_name: str,
        blob_path: str,
        data: Any,
        content_type: Optional[str] = None,
        overwrite: bool = True,
    ) -> None:
        """
        Upload data to a blob, supporting various data types.

        Args:
            connection_string: Azure Storage connection string.
            container_name: Name of the container.
            blob_path: Path to the blob.
            data: Data to upload (bytes, BytesIO, file object, FileStorage, str, or path to file).
            content_type: MIME type for the blob (default: None, auto-detected if possible).
            overwrite: Whether to overwrite an existing blob (default: True).

        Raises:
            Exception: If upload fails or data type is unsupported.
        """
        validate_params(
            connection_string=connection_string,
            container_name=container_name,
            blob_path=blob_path,
        )

        # Determine content type if not provided
        if not content_type:
            content_type = BlobOperations._infer_content_type(blob_path, data)

        # Process the data based on its type
        try:
            if isinstance(data, (bytes, bytearray)):
                upload_data = data
            elif isinstance(data, io.BytesIO):
                data.seek(0)
                upload_data = data.read()
            elif isinstance(data, str) and os.path.isfile(data):
                # Handle file paths
                with open(data, 'rb') as f:
                    upload_data = f.read()
            elif isinstance(data, FileStorage):
                # Handle Werkzeug FileStorage (e.g., Flask uploads)
                upload_data = data.read()
                if not content_type:
                    content_type = data.content_type or BlobOperations._infer_content_type(blob_path, data)
            elif hasattr(data, 'read') and callable(data.read):
                # Handle file-like objects (e.g., open file handles)
                upload_data = data.read()
            elif isinstance(data, str):
                # Handle string data (encode to bytes)
                upload_data = data.encode('utf-8')
                content_type = content_type or 'text/plain'
            else:
                raise Exception(f"Unsupported data type: {type(data)}", 400)

            # Upload the processed data
            blob_client = BlobOperations._get_blob_service_client(connection_string).get_blob_client(
                container=container_name, blob=blob_path
            )
            blob_client.upload_blob(
                upload_data,
                overwrite=overwrite,
                content_settings=ContentSettings(content_type=content_type),
            )
        except Exception as e:
            raise Exception(f"Upload failed: {blob_path}", 400)

    @staticmethod
    def move_blob(
        source_connection_string: str,
        source_container: str,
        source_blob_path: str,
        dest_connection_string: str,
        dest_container: str,
        dest_blob_path: Optional[str] = None,
    ) -> None:
        """
        Move a blob between containers or storage accounts.

        Args:
            source_connection_string: Connection string for the source storage account.
            source_container: Source container name.
            source_blob_path: Source blob path.
            dest_connection_string: Connection string for the destination storage account.
            dest_container: Destination container name.
            dest_blob_path: Destination blob path (defaults to source_blob_path).

        Raises:
            Exception: If move fails.
        """
        validate_params(
            source_connection_string=source_connection_string,
            source_container=source_container,
            source_blob_path=source_blob_path,
            dest_connection_string=dest_connection_string,
            dest_container=dest_container,
        )
        dest_blob_path = dest_blob_path or source_blob_path

        try:
            source_service_client = BlobOperations._get_blob_service_client(source_connection_string)
            dest_service_client = BlobOperations._get_blob_service_client(dest_connection_string)

            source_blob_client = source_service_client.get_blob_client(
                container=source_container, blob=source_blob_path
            )
            dest_blob_client = dest_service_client.get_blob_client(
                container=dest_container, blob=dest_blob_path
            )

            sas_token = generate_blob_sas(
                account_name=source_service_client.account_name,
                container_name=source_container,
                blob_name=source_blob_path,
                account_key=source_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=CONFIG.sas_expiry_hours),
            )
            source_url = f"{source_blob_client.url}?{sas_token}"

            dest_blob_client.start_copy_from_url(source_url)
            BlobOperations._wait_for_copy(dest_blob_client)
            source_blob_client.delete_blob()
        except Exception as e:
            raise Exception(f"Move failed: {source_blob_path}", 400)

    @staticmethod
    def delete_blob(
        connection_string: str,
        container_name: str,
        blob_path: str,
    ) -> None:
        """
        Delete a blob or blobs with a prefix.

        Args:
            connection_string: Azure Storage connection string.
            container_name: Name of the container.
            blob_path: Path to the blob or prefix.

        Raises:
            Exception: If deletion fails.
        """
        validate_params(
            connection_string=connection_string,
            container_name=container_name,
            blob_path=blob_path,
        )
        try:
            container_client = BlobOperations._get_blob_service_client(connection_string).get_container_client(
                container_name
            )
            blobs = container_client.list_blobs(name_starts_with=blob_path)
            for blob in sorted(blobs, key=lambda x: x.name, reverse=True):
                container_client.get_blob_client(blob.name).delete_blob()
        except Exception as e:
            raise Exception(f"Deletion failed: {blob_path}", 400)

    @staticmethod
    def _wait_for_copy(blob_client, max_retries: int = CONFIG.max_retries) -> None:
        """Wait for a blob copy operation to complete."""
        retry_count = 0
        properties = blob_client.get_blob_properties()
        while properties.copy.status == "pending" and retry_count < max_retries:
            time.sleep(CONFIG.retry_delay)
            properties = blob_client.get_blob_properties()
            retry_count += 1
        if properties.copy.status != "success":
            raise Exception(f"Copy operation failed: {properties.copy.status}", 400)

    @staticmethod
    def _infer_content_type(blob_path: str, data: Any) -> str:
        """
        Infer the content type based on blob path or data.

        Args:
            blob_path: Path to the blob.
            data: Data being uploaded.

        Returns:
            Inferred content type (MIME type).
        """
        import mimetypes

        # Initialize MIME types
        mimetypes.init()

        # Check for FileStorage content type
        if isinstance(data, FileStorage) and data.content_type:
            return data.content_type

        # Infer from file extension
        extension = os.path.splitext(blob_path)[1].lower()
        content_type, _ = mimetypes.guess_type(blob_path)
        if content_type:
            return content_type

        # Default content types for common extensions
        defaults = {
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.zip': 'application/zip',
            '.jpg': 'image/jpeg',
            '.png': 'image/png',
        }
        return defaults.get(extension, CONFIG.default_content_type)