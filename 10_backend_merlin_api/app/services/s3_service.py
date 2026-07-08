"""S3 Audio file storage service for practitioner profiles."""

import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class S3AudioService:
    """Manages audio file uploads, presigned URLs, and deletions."""
    
    def __init__(self):
        """Initialize S3 client with OVH configuration."""
        self.client = boto3.client(
            's3',
            endpoint_url=settings.OVH_S3_ENDPOINT,
            region_name=settings.OVH_S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = settings.OVH_S3_BUCKET
    
    def upload_audio(
        self,
        practitioner_id: str,
        file_bytes: bytes,
        filename: str,
        content_type: str = 'audio/webm'
    ) -> str:
        """
        Upload audio file to S3.
        
        Args:
            practitioner_id: UUID of practitioner
            file_bytes: Audio file content (bytes)
            filename: Original filename with extension
            content_type: MIME type (default: audio/webm)
        
        Returns:
            S3 object key (e.g., "audio-profiles/prat-001/audio.webm")
        
        Raises:
            Exception: If upload fails
        """
        key = f"audio-profiles/{practitioner_id}/{filename}"
        
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_bytes,
                ContentType=content_type,
                ServerSideEncryption='AES256',
                StorageClass='STANDARD'  # OVH Object Storage
            )
            logger.info(f"Uploaded audio to S3: {key} ({len(file_bytes)} bytes)")
            return key
        except ClientError as e:
            logger.error(f"S3 upload failed for {key}: {e}")
            raise Exception(f"Failed to upload audio to S3: {str(e)}")
    
    def get_presigned_url(
        self,
        key: str,
        expiration_seconds: int = 604800  # 7 days
    ) -> tuple[str, datetime]:
        """
        Generate presigned URL for temporary download access.
        
        Args:
            key: S3 object key
            expiration_seconds: URL validity period (default: 7 days)
        
        Returns:
            Tuple of (presigned_url, expires_at datetime)
        
        Raises:
            Exception: If URL generation fails
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expiration_seconds
            )
            expires_at = datetime.utcnow() + timedelta(seconds=expiration_seconds)
            logger.info(f"Generated presigned URL for {key}, expires at {expires_at}")
            return url, expires_at
        except ClientError as e:
            logger.error(f"Presigned URL generation failed for {key}: {e}")
            raise Exception(f"Failed to generate presigned URL: {str(e)}")
    
    def delete_audio(self, key: str) -> None:
        """
        Delete audio file from S3.
        
        Args:
            key: S3 object key
        
        Raises:
            Exception: If deletion fails
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"Deleted audio from S3: {key}")
        except ClientError as e:
            logger.error(f"S3 deletion failed for {key}: {e}")
            raise Exception(f"Failed to delete audio from S3: {str(e)}")
    
    def refresh_presigned_url_if_needed(
        self,
        key: str,
        presigned_url: Optional[str],
        expires_at: Optional[datetime],
        refresh_buffer_hours: int = 24
    ) -> tuple[str, datetime]:
        """
        Check if presigned URL is expired or expiring soon, refresh if needed.
        
        Args:
            key: S3 object key
            presigned_url: Current presigned URL (may be None)
            expires_at: Current expiration time
            refresh_buffer_hours: Refresh if < N hours until expiry
        
        Returns:
            Tuple of (fresh_presigned_url, new_expires_at)
        """
        now = datetime.utcnow()
        
        # If no URL or expired, generate new one
        if not presigned_url or not expires_at or expires_at <= now:
            logger.info(f"Presigned URL expired or missing for {key}, regenerating...")
            return self.get_presigned_url(key)
        
        # If expiring within buffer period, refresh
        refresh_time = now + timedelta(hours=refresh_buffer_hours)
        if expires_at <= refresh_time:
            logger.info(f"Presigned URL expiring soon for {key}, regenerating...")
            return self.get_presigned_url(key)
        
        # URL still valid
        return presigned_url, expires_at
