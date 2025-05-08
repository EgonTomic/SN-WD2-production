import os
from smartninja_mongo.connection import MongoClient
import smartninja_redis


# mongoDB
client = MongoClient(os.getenv("MONGODB_URI", "localhost"))  # Find MONGODB_URI env var (Heroku). If not found, use "localhost"
mongo_db = client.heroku_dt0wvt4m  # change the database name when you deploy on Heroku

# redis
redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))
