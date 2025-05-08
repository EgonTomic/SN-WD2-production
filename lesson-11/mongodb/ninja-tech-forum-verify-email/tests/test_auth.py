import pytest
from main import app
from models.database import mongo_db


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


def test_signup_login(client):
    # SIGNUP
    password = "password123"
    response_1 = client.post('/signup', data={"username": "ramuta", "password": password,
                                              "email-address": "matt@smartninja.org", "repeat": password},
                             follow_redirects=True)

    assert b'Welcome to Ninja Tech Forum, ramuta' in response_1.data

    # LOGIN
    response_2 = client.post('/login', data={"username": "ramuta", "password": password}, follow_redirects=True)
    assert b'Welcome to Ninja Tech Forum, ramuta' in response_2.data
