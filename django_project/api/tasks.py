import time
from celery import shared_task as celery_shared_task

from api.models import File


@celery_shared_task
def process_file(file_id: int):
    try:
        orm_file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return False

    if orm_file.type == File.FileTypeChoices.NA:
        process_na_file(orm_file)
    elif orm_file.type == File.FileTypeChoices.IMG:
        process_image_file(orm_file)
    elif orm_file.type == File.FileTypeChoices.TXT:
        process_text_file(orm_file)
    elif orm_file.type == File.FileTypeChoices.PDF:
        process_pdf_file(orm_file)

    orm_file.processed = True
    orm_file.save()

    return True

def process_na_file(orm_file: File):
    # File processing
    time.sleep(10)

def process_image_file(orm_file: File):
    # File processing
    time.sleep(10)

def process_text_file(orm_file: File):
    # File processing
    time.sleep(10)

def process_pdf_file(orm_file: File):
    # File processing
    time.sleep(10)