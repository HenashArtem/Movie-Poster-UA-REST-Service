import json
import pytest
import shutil
import os
from app import app


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile('data/screenings.json', 'data/screenings_copy.json')
    yield
    shutil.copyfile('data/screenings_copy.json', 'data/screenings.json')
    os.remove('data/screenings_copy.json')


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_screenings(client):
    response = client.get('/screenings')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'screenings' in data
    assert len(data['screenings']) == 10


def test_get_screening(client):
    response = client.get('/screenings/1')
    assert response.status_code == 200
    screening = json.loads(response.data)
    assert screening['movie_id'] == 1


def test_get_nonexistent_screening(client):
    response = client.get('/screenings/100')
    assert response.status_code == 404


def test_update_screening(client):
    updated_screening = {
        "movie_id": 1,
        "cinema_id": 1,
        "time": "2024-03-25T20:00:00"
    }
    response = client.put('/screenings/1', json=updated_screening)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Screening updated successfully"


def test_delete_screening(client):
    response = client.delete('/screenings/1')
    assert response.status_code == 200


def test_add_screening(client):
    new_screening = {
        "movie_id": 2,
        "cinema_id": 2,
        "time": "2024-03-27T14:00:00"
    }
    response = client.post('/screenings', json=new_screening)
    assert response.status_code == 201
    response = client.get('/screenings')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['screenings']) == 11


def test_delete_nonexistent_screening(client):
    response = client.delete('/screenings/100')
    assert response.status_code == 404
