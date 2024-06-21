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

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_post_success(client):
    response = client.post('/blog/posts', json={
        'title': 'Test Post',
        'content': 'This is a test post.'
    })
    assert response.status_code == 201  # Expecting 201 for successful creation
    assert 'Post created successfully' in response.json['message']
    
    
def test_create_post_missing_title(client):
    response = client.post('/blog/posts', json={
        'content': 'This is a test post without a title.'
    })
    assert response.status_code == 400
    assert 'Title' in response.json['message']


def test_create_post_missing_body(client):
    response = client.post('/blog/posts', json={
        'title': 'Test Post'
    })
    assert response.status_code == 400
    assert 'content' in response.json['message']


def test_get_posts(client):
    # Create posts first
    client.post('/blog/posts', json={
        'title': 'First Post',
        'content': 'This is the first test post.'
    })
    client.post('/blog/posts', json={
        'title': 'Second Post',
        'content': 'This is the second test post.'
    })

    # Get posts
    response = client.get('/blog/posts')
    assert response.status_code == 200
    posts = response.json
    assert len(posts) == 2
    assert posts[0]['title'] == 'First Post'
    assert posts[1]['title'] == 'Second Post'
