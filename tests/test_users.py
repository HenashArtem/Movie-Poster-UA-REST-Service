import json
import pytest
import shutil
import os
from app import app


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    shutil.copyfile('data/users.json', 'data/users_copy.json')
    yield
    shutil.copyfile('data/users_copy.json', 'data/users.json')
    os.remove('data/users_copy.json')


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'users' in data
    assert len(data['users']) == 10


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == 200
    user = json.loads(response.data)
    assert user['username'] == "user1"


def test_get_nonexistent_user(client):
    response = client.get('/users/100')
    assert response.status_code == 404


def test_update_user(client):
    updated_user = {
        "username": "updated_user",
        "email": "updated_user@example.com"
    }
    response = client.put('/users/1', json=updated_user)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == "User updated successfully"


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == 200


def test_add_user(client):
    new_user = {
        "username": "new_user",
        "email": "new_user@example.com"
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['users']) == 11


def test_delete_nonexistent_user(client):
    response = client.delete('/users/100')
    assert response.status_code == 404
