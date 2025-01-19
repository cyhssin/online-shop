import boto3
import os
from django.conf import settings


class Bucket:
    """
        CDN Bucket manager
        init method creates connection.
    """

    def __init__(self):
        self.connection = boto3.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        objects = self.connection.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME
        )
        return objects

    def delete_object(self, key):
        self.connection.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True


    def download_object(self, key):
        try:
            local_path = os.path.join(settings.AWS_LOCAL_STORAGE, key)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(settings.AWS_LOCAL_STORAGE + key, "wb") as f:
                self.connection.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)
                print(f"Object with key {key} downloaded to {local_path}.")
        except Exception as e:
            print(f"Error downloading object with key {key}: {e}")

bucket = Bucket()