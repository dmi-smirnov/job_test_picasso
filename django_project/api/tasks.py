import time
from celery import shared_task as celery_shared_task

from api.models import File


@celery_shared_task
def process_file(file_id: int):
    try:
        orm_file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return False

    # File processing
    time.sleep(10)

    orm_file.processed = True
    orm_file.save()

    return True