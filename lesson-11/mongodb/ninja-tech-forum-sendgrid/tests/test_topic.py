import pytest
from main import app
from models.database import mongo_db
from utils.csrf_helper import get_csrf_token


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    cleanup()  # clean up before every test

    yield client


@pytest.fixture
def client_logged_in():
    app.config['TESTING'] = True
    client = app.test_client()

    cleanup()  # clean up before every test

    # SIGNUP
    password = "password123"
    client.post('/signup', data={"username": "ramuta", "password": password, "repeat": password}, follow_redirects=True)

    yield client


def cleanup():
    # clean up the DB
    mongo_db.tinydb.purge_tables()


def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Welcome to Ninja Tech Forum, stranger' in response.data


def test_index_logged_in(client_logged_in):
    response = client_logged_in.get('/')
    assert b'Welcome to Ninja Tech Forum, ramuta' in response.data


def test_topic_create(client_logged_in):
    # GET
    response_get = client_logged_in.get('/create-topic')
    assert b'Create a new topic' in response_get.data

    # POST
    response_post = client_logged_in.post('/create-topic', data={"csrf": get_csrf_token(username="ramuta"),
                                                                 "title": "My topic",
                                                                 "text": "Some text"}, follow_redirects=True)

    assert b'My topic' in response_post.data  # topic title on the index page
