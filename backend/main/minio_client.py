from minio import Minio
from django.conf import settings
from io import BytesIO
from minio.error import S3Error

minio_client = Minio(
    settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def upload_to_minio(file_data, file_name):
    try:
        file_data.seek(0)
        file_bytes = BytesIO(file_data.read())
        
        minio_client.put_object(
            settings.MINIO_BUCKET,
            file_name,
            file_bytes,
            length=len(file_bytes.getvalue()),
            content_type=file_data.content_type
        )
        print("File uploaded to MinIO")
        return True
    except IOError as e:
        print(f"IOError during MinIO upload: {e}")
        return False
    except Exception as e:
        print(f"Error during MinIO upload: {e}")
        return False

def generate_presigned_url(file_name):
    try:
        return minio_client.presigned_get_object(settings.MINIO_BUCKET, file_name)
    except S3Error as e:
        print(f"Error generating presigned URL: {e}")
        return None