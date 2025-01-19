from bucket import bucket
from celery import shared_task

def all_bucket_objects_task():
    """
    Get all objects from the bucket
    """
    objects = bucket.get_objects().get("Contents", [])
    return objects

@shared_task
def delete_object_task(key):
    """
    Task to delete an object from the bucket asynchronously.
    Args: key (str): The key of the object to be deleted.
    """

    bucket.delete_object(key)

@shared_task
def download_object_task(key):
    """
    Task to download an object from the bucket asynchronously.
    Args: key (str): The key of the object to be downloaded.
    """

    bucket.download_object(key)