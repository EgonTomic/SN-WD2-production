from models.settings import db
from datetime import datetime
from utils.mail_helper import send_email

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User")

    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"))
    topic = db.relationship("Topic")

    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def create(cls, text, author, topic):
        comment = cls(text=text, topic=topic, author=author)
        db.add(comment)
        db.commit()

        # Only send mail to topic author if his mail is in database

        if topic.author.email_adress:
            send_email(receiver_email=topic.author.email_adress, subject="New comment for your topic", text="Your topic {0} has a new comment".format(topic.title))

        return comment