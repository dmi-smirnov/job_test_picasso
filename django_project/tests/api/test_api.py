import os
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

@pytest.fixture
def delete_file(scope='module'):
    def return_function(file: File):
        os.remove(file.file.path)
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
def test_get_file_by_id(api_client, file_factory, files_route):
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
    