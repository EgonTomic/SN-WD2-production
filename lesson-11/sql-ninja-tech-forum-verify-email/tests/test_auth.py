import os
import pytest
from main import app
from models.settings import db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client


@pytest.fixture
def client_logged_in():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    # SIGNUP
    password = "password123"
    client.post('/signup', data={"username": "ramuta", "password": password, "repeat": password}, follow_redirects=True)

    yield client


def cleanup():
    # clean up the DB (drop all tables)
    db.drop_all()


def test_signup_login(client):
    # SIGNUP
    password = "password123"
    response_1 = client.post('/signup', data={"username": "ramuta", "password": password,
                                              "repeat": password}, follow_redirects=True)

    assert b'Welcome to Ninja Tech Forum, ramuta' in response_1.data

    # LOGIN
    response_2 = client.post('/login', data={"username": "ramuta", "password": password}, follow_redirects=True)
    assert b'Welcome to Ninja Tech Forum, ramuta' in response_2.data
