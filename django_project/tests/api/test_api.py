import os
import time
import pytest
from rest_framework import status as http_status
from rest_framework.test import APIClient
from model_bakery import baker

from api.models import File


@pytest.fixture(scope='module')
def file_factory():
    def return_function(**kwargs):
        return baker.make(File, **kwargs)
    return return_function

@pytest.fixture(scope='module')
def api_client():
    return APIClient()

@pytest.fixture(scope='module')
def api_base_route():
    return '/api/'

@pytest.fixture(scope='module')
def files_route(api_base_route):
    return f'{api_base_route}files/'

@pytest.fixture(scope='module')
def upload_route(api_base_route):
    return f'{api_base_route}upload/'

@pytest.fixture
def delete_file(scope='module'):
    def return_function(file: File):
        os.remove(file.file.path)
    return return_function

@pytest.fixture
def create_file(scope='module'):
    def return_function(ext: str) -> str:
        file_name = f'temp_test_file.{ext}'
        file_path = os.path.join(os.path.abspath('.'), file_name)
        with open(file_path, 'w') as file:
            file.write('temp test file')
        return file_path
    return return_function

@pytest.mark.django_db
def test_get_files_list(api_client, file_factory, files_route, delete_file):
    FILES_AMT = 10
    
    # Arrange
    files = file_factory(_create_files=True, _quantity=FILES_AMT)

    # Act
    resp = api_client.get(files_route)
    
    # Assert
    assert resp.status_code == http_status.HTTP_200_OK
    
    data = resp.data
    assert isinstance(data, list)

    assert len(data) == FILES_AMT

    # Deleting files
    for file in files:
        delete_file(file)

@pytest.mark.django_db
def test_get_file_by_id(api_client, file_factory, files_route, delete_file):
    # Arrange
    file = file_factory(_create_files=True)

    # Act
    resp = api_client.get(f'{files_route}{file.id}/')
    
    # Assert
    assert resp.status_code == http_status.HTTP_200_OK
    
    data = resp.data
    assert isinstance(data, dict)

    assert data['id'] == file.id
    assert data['file'] == file.file.url
    assert data['type'] == file.type
    assert 'processed' in data.keys()
    assert 'uploaded_at' in data.keys()

    # Deleting files
    delete_file(file)

@pytest.mark.parametrize(
    'file_ext, file_type, http_status_code',
    [
        (File.VALID_FILES_EXTENSIONS[File.FileTypeChoices.IMG][0],
         File.FileTypeChoices.IMG, http_status.HTTP_201_CREATED),
        ('xxx',
         File.FileTypeChoices.IMG, http_status.HTTP_400_BAD_REQUEST),
    ]
)
@pytest.mark.django_db
def test_post_file(api_client, upload_route, create_file, file_ext, file_type,
                   http_status_code):
    # Arrange
    file_path = create_file(ext=file_ext)

    # Act
    with open(file_path) as file:
        resp = api_client.post(
            upload_route,
            data={
                'file': file,
                'type': file_type
            }

        )
    
    # Assert
    assert resp.status_code == http_status_code

    # Deleting files
    os.remove(file_path)

@pytest.mark.parametrize(
    'file_ext, file_type, check_delay_sec, checks_max',
    [
        ('xxx',
         File.FileTypeChoices.NA, 1, 7),
        (File.VALID_FILES_EXTENSIONS[File.FileTypeChoices.IMG][0],
         File.FileTypeChoices.IMG, 1, 7),
        (File.VALID_FILES_EXTENSIONS[File.FileTypeChoices.TXT][0],
         File.FileTypeChoices.TXT, 1, 7),
        (File.VALID_FILES_EXTENSIONS[File.FileTypeChoices.PDF][0],
         File.FileTypeChoices.PDF, 1, 7),
    ]
)
@pytest.mark.django_db(transaction=True)
def test_process_file(api_client, upload_route, create_file, file_ext,
                      file_type, check_delay_sec, checks_max):
    # Arrange
    file_path = create_file(ext=file_ext)

    # Act
    with open(file_path) as file:
        resp = api_client.post(
            upload_route,
            data={
                'file': file,
                'type': file_type
            }
        )

    # Assert
    assert resp.status_code == http_status.HTTP_201_CREATED

    file_id = resp.data['id']
    checks_count = 0
    while File.objects.get(id=file_id).processed != True:
        checks_count += 1
        assert checks_count < checks_max
        time.sleep(check_delay_sec)

    # Deleting files
    os.remove(file_path)
