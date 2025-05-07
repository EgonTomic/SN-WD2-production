import os
from sqla_wrapper import SQLAlchemy

db_url = os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite?check_same_thread=False")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)