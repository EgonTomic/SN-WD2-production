import uuid

from models.database import redis


def set_csrf_token(username):
    csrf_token = str(uuid.uuid4())  # create CSRF token
    redis.set(name=username, value=csrf_token)  # store CSRF token into Redis for that specific user

    return csrf_token


def get_csrf_token(username):
    try:
        csrf = redis.get(name=username).decode()  # csrf from Redis (needs to be decoded from byte string)
    except:
        csrf = None

    return csrf
