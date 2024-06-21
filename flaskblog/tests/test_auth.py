import pytest
from flaskblog import create_app
from flaskblog.models import db as sqlalchemy_db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.app_context():
        sqlalchemy_db.create_all()  # Create all tables before testing
        yield app
        sqlalchemy_db.session.remove()  # Remove session after testing
        sqlalchemy_db.drop_all()  # Drop all tables after testing

def test_register(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert 'User registered successfully' in response.json['message']

def test_login(client):
    client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'Login successful' in response.json['message']

def test_logout(client):
    client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert 'Logout successful' in response.json['message']
