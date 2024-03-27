import json
import pytest
import shutil
import os
from app import app


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile('data/movies.json', 'data/movies_copy.json')
    yield
    shutil.copyfile('data/movies_copy.json', 'data/movies.json')
    os.remove('data/movies_copy.json')


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_movies(client):
    response = client.get('/movies')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'movies' in data
    assert len(data['movies']) == 10


def test_get_movie(client):
    response = client.get('/movies/1')
    assert response.status_code == 200
    movie = json.loads(response.data)
    assert movie['title'] == "Месники: Завершення"


def test_get_nonexistent_movie(client):
    response = client.get('/movies/100')
    assert response.status_code == 404


def test_update_movie(client):
    updated_movie = {
        "title": "Оновлений фільм",
        "genre": "Драма",
        "duration": "2 год"
    }
    response = client.put('/movies/1', json=updated_movie)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "Movie updated successfully"


def test_delete_movie(client):
    response = client.delete('/movies/1')
    assert response.status_code == 200


def test_add_movie(client):
    new_movie = {
        "title": "Новий фільм",
        "genre": "Комедія",
        "duration": "1 година"
    }
    response = client.post('/movies', json=new_movie)
    assert response.status_code == 201
    response = client.get('/movies')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['movies']) == 11


def test_delete_nonexistent_movie(client):
    response = client.delete('/movies/100')
    assert response.status_code == 404
