import json
import pytest
import shutil
import os
from app import app


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile('data/cinemas.json', 'data/cinemas_copy.json')
    yield
    shutil.copyfile('data/cinemas_copy.json', 'data/cinemas.json')
    os.remove('data/cinemas_copy.json')


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_cinemas(client):
    response = client.get('/cinemas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'cinemas' in data
    assert len(data['cinemas']) == 10


def test_get_cinema(client):
    response = client.get('/cinemas/1')
    assert response.status_code == 200
    cinema = json.loads(response.data)
    assert cinema['name'] == "Планета кіно"


def test_get_nonexistent_cinema(client):
    response = client.get('/cinemas/100')
    assert response.status_code == 404


def test_update_cinema(client):
    updated_cinema = {
        "name": "Оновлений кінотеатр",
        "location": "Нове розташування",
        "movies_playing": [1, 2, 3]
    }
    response = client.put('/cinemas/1', json=updated_cinema)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Cinema updated successfully"


def test_delete_cinema(client):
    response = client.delete('/cinemas/1')
    assert response.status_code == 200


def test_add_cinema(client):
    new_cinema = {
        "name": "Новий кінотеатр",
        "location": "Нове місце",
        "movies_playing": [4, 5]
    }
    response = client.post('/cinemas', json=new_cinema)
    assert response.status_code == 201
    response = client.get('/cinemas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['cinemas']) == 11


def test_delete_nonexistent_cinema(client):
    response = client.delete('/cinemas/100')
    assert response.status_code == 404
