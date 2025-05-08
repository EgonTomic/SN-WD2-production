import datetime
from smartninja_mongo.odm import Model
from smartninja_mongo.bson import ObjectId
from models.database import mongo_db
from models.user import User
from models.topic import Topic
from utils.email_helper import send_email_to_one_recipient


collection = mongo_db.comments


class Comment(Model):
    def __init__(self, topic_id, author_id, text, author_username, **kwargs):
        self.topic_id = topic_id
        self.author_id = author_id
        self.author_username = author_username
        self.text = text
        self.created = datetime.datetime.now()

        super().__init__(**kwargs)

    def insert(self):
        comment_id = collection.insert_one(self.__dict__).inserted_id
        self._id = comment_id  # save id from MongoDB into the Topic object

        # get topic and topic author
        topic = Topic.get_by_id(topic_id=self.topic_id)
        topic_author = User.get_by_username(username=topic.author_username)

        # send message data
        message = "A new comment was posted in your topic {}.".format(topic.title)
        subject = "New comment!"
        send_email_to_one_recipient(recipient_email=topic_author.email_address, subject=subject, message=message)

        return comment_id

    @classmethod
    def get_by_id(cls, comment_id):
        comment_dict = collection.find_one({"_id": ObjectId(comment_id)})

        # convert topic dictionary into topic object
        comment_obj = cls.convert_dict_to_object(data_dict=comment_dict)

        return comment_obj

    @classmethod
    def get_comments(cls, topic_id):
        comment_dicts = collection.find({"topic_id": topic_id})  # we don't use ObjectId() because we didn't save topic_id like this

        """
        # Uncomment this if you want to convert dicts into objects
        comments = []
        for comm_dict in comment_dicts:
            comments.append(cls.convert_dict_to_object(data_dict=comm_dict))
        """

        return comment_dicts

    @classmethod
    def edit_comment(cls, comment_id, updates_dict):
        result = collection.update_one({"_id": ObjectId(comment_id)}, {"$set": updates_dict})

        return result

    @classmethod
    def delete_comment(cls, comment_id):
        result = collection.delete_one({"_id": ObjectId(comment_id)})

        return result
