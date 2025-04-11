import boto3
import uuid
import os
import io
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class S3FileUploadHandler:
    """Utility for handling file uploads to AWS S3 with dynamic configuration"""

    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str,
        bucket_name: str,
    ):
        """
        Initialize the S3 file uploader with AWS credentials and configuration.

        Args:
            aws_access_key_id (str): AWS Access Key ID.
            aws_secret_access_key (str): AWS Secret Access Key.
            region_name (str): AWS region.
            bucket_name (str): S3 bucket name.
        """
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.bucket_name = bucket_name

    def _get_s3_key(
        self, user_id: str, file_type: str, custom_folder: Optional[str] = None
    ) -> str:
        """
        Construct the S3 key (path) based on user ID, file type, and optional custom folder.

        Args:
            user_id (str): ID of the user uploading the file.
            file_type (str): Type of the file (e.g., "image", "document").
            custom_folder (Optional[str]): An optional custom folder name.

        Returns:
            str: The constructed S3 key (path).
        """
        unique_filename = f"{uuid.uuid4()}"
        if custom_folder:
            s3_key = f"{user_id}/{custom_folder}/{unique_filename}"
        else:
            s3_key = f"{user_id}/{file_type}/{unique_filename}"

        return s3_key

    def _validate_file(
        self, file: io.BytesIO, allowed_extensions: List[str], max_size_mb: float
    ) -> bool:
        """
        Validate the file type and size.

        Args:
            file (io.BytesIO): The file to be validated.
            allowed_extensions (List[str]): List of allowed file extensions.
            max_size_mb (float): The maximum allowed file size in megabytes.

        Returns:
            bool: True if the file is valid, False otherwise.
        """
        # Check file extension
        file_ext = os.path.splitext(file.name)[1].lower()
        if allowed_extensions and file_ext not in allowed_extensions:
            raise ValueError(
                f"File type not allowed. Accepted types: {', '.join(allowed_extensions)}"
            )

        # Check file size
        max_size_bytes = max_size_mb * 1024 * 1024
        if len(file.getvalue()) > max_size_bytes:
            raise ValueError(
                f"File size exceeds maximum allowed size of {max_size_mb} MB"
            )

        return True

    def upload_file(
        self,
        file: io.BytesIO,
        user_id: str,
        file_type: str,
        allowed_extensions: Optional[List[str]] = None,
        max_size_mb: float = 10.0,
        custom_folder: Optional[str] = None,
    ) -> Optional[str]:
        """
        Upload a file to S3 with validation and dynamic path construction.

        Args:
            file (io.BytesIO): The file to be uploaded.
            user_id (str): ID of the user uploading the file.
            file_type (str): The type of file (image, document, etc.)
            allowed_extensions (Optional[List[str]]): List of allowed file extensions.
            max_size_mb (float): Maximum allowed file size in MB.
            custom_folder (Optional[str]): Custom folder to organize the files.

        Returns:
            str: The S3 URL of the uploaded file or None if the upload failed.
        """
        try:
            # Validate the file
            if not self._validate_file(file, allowed_extensions, max_size_mb):
                return None

            # Generate the S3 key (path)
            s3_key = self._get_s3_key(user_id, file_type, custom_folder)

            # Upload the file to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                s3_key,
                ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"},
            )

            # Return the S3 URL
            s3_url = f"https://{self.bucket_name}.s3.{os.getenv('AWS_REGION', 'ap-southeast-1')}.amazonaws.com/{s3_key}"
            return s3_url

        except Exception as e:
            raise ValueError(f"Error uploading file: {str(e)}")
