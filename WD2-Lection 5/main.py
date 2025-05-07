from flask import Flask
from handlers.auth import auth_handlers
from models.user import User
from models.topic import Topic
from models.settings import db
from handlers.topic import topic_handlers
from handlers.comment import comment_handlers
from handlers.profile import profile_handlers

app = Flask(__name__)
app.register_blueprint(auth_handlers)
app.register_blueprint(topic_handlers)
app.register_blueprint(comment_handlers)
app.register_blueprint(profile_handlers)

# Create tables in database
db.create_all()

if __name__ == "__main__":
    app.run()