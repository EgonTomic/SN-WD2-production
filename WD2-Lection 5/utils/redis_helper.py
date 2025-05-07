import os
import smartninja_redis
import uuid

# Create redis database caching purposes
redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))

def create_csrf_token(username):
    csrf_token = str(uuid.uuid4())
    redis.set(name=csrf_token, value=username)

    return csrf_token

def validate_csrf_token(csrf_token, username):
    redis_csrf_username = redis.get(name=csrf_token)

    if redis_csrf_username and redis_csrf_username.decode() == username:
        return True
    else:
        return False