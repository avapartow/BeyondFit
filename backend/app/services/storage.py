"""
Storage service for handling photo uploads with privacy-first approach
Photos are deleted by default after processing
"""
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime, timedelta
from typing import Optional
import hashlib
from PIL import Image
import io
from app.config import get_settings

settings = get_settings()


class StorageService:
    """S3-compatible storage service for photos"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
            endpoint_url=settings.s3_endpoint_url if settings.s3_endpoint_url else None
        )
        self.bucket_name = settings.s3_bucket_name
        self.delete_after_processing = settings.delete_photos_after_processing
    
    def _generate_filename(self, user_id: int, photo_type: str, extension: str = "jpg") -> str:
        """Generate unique filename for photo"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        hash_part = hashlib.md5(f"{user_id}{timestamp}".encode()).hexdigest()[:8]
        return f"users/{user_id}/{photo_type}_{timestamp}_{hash_part}.{extension}"
    
    def _strip_exif(self, image_bytes: bytes) -> bytes:
        """Remove EXIF metadata from image for privacy"""
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Create new image without EXIF
            data = list(image.getdata())
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(data)
            
            # Convert back to bytes
            output = io.BytesIO()
            image_without_exif.save(output, format=image.format or 'JPEG')
            return output.getvalue()
        except Exception as e:
            print(f"Error stripping EXIF: {e}")
            return image_bytes
    
    def upload_photo(
        self,
        user_id: int,
        photo_bytes: bytes,
        photo_type: str,  # 'front' or 'side'
        store_permanently: bool = False
    ) -> str:
        """
        Upload photo to S3
        
        Args:
            user_id: User ID
            photo_bytes: Photo file bytes
            photo_type: Type of photo ('front' or 'side')
            store_permanently: If True, don't auto-delete
            
        Returns:
            S3 URL or local file path
        """
        # Strip EXIF metadata
        clean_bytes = self._strip_exif(photo_bytes)
        
        # Generate filename
        filename = self._generate_filename(user_id, photo_type)
        
        try:
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=clean_bytes,
                ContentType='image/jpeg'
            )
            
            # If auto-delete is enabled and user didn't opt-in to storage
            if self.delete_after_processing and not store_permanently:
                # Set lifecycle/expiration (or we'll delete after analysis)
                # For now, we'll handle deletion in the analysis endpoint
                pass
            
            # Return URL
            url = f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{filename}"
            return url
            
        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            raise
    
    def download_photo(self, photo_url: str) -> bytes:
        """Download photo from S3"""
        # Extract key from URL
        key = photo_url.split(f"{self.bucket_name}.s3.")[1].split("/", 1)[1]
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return response['Body'].read()
        except ClientError as e:
            print(f"Error downloading from S3: {e}")
            raise
    
    def delete_photo(self, photo_url: str) -> bool:
        """Delete photo from S3"""
        # Extract key from URL
        try:
            key = photo_url.split(f"{self.bucket_name}.s3.")[1].split("/", 1)[1]
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True
        except Exception as e:
            print(f"Error deleting from S3: {e}")
            return False
    
    def save_locally(self, photo_bytes: bytes, filename: str) -> str:
        """
        Save photo locally (fallback if S3 not configured)
        Returns local file path
        """
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, filename)
        
        # Strip EXIF
        clean_bytes = self._strip_exif(photo_bytes)
        
        with open(filepath, 'wb') as f:
            f.write(clean_bytes)
        
        return filepath
    
    def delete_user_photos(self, user_id: int) -> bool:
        """Delete all photos for a user (privacy/GDPR)"""
        try:
            prefix = f"users/{user_id}/"
            
            # List all objects with prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' not in response:
                return True
            
            # Delete all objects
            objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
            
            self.s3_client.delete_objects(
                Bucket=self.bucket_name,
                Delete={'Objects': objects_to_delete}
            )
            
            return True
        except Exception as e:
            print(f"Error deleting user photos: {e}")
            return False


_storage_instance = None

def get_storage_service() -> StorageService:
    """Get or create StorageService singleton"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = StorageService()
    return _storage_instance
