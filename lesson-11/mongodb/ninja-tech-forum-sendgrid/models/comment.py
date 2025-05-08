import datetime
import json
import os
import requests
from smartninja_mongo.odm import Model
from smartninja_mongo.bson import ObjectId
from models.database import mongo_db
from models.user import User
from models.topic import Topic


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

        # SENDGRID
        sender_email = os.getenv("MY_SENDER_EMAIL")
        api_key = os.getenv('SENDGRID_API_KEY')
        topic = Topic.get_by_id(topic_id=self.topic_id)
        author = User.get_by_username(username=topic.author_username)

        if sender_email and api_key and author.email_address:
            url = "https://api.sendgrid.com/v3/mail/send"

            data = {"personalizations": [{
                        "to": [{"email": author.email_address}],
                        "subject": "New comment!"
                    }],

                    "from": {"email": sender_email},

                    "content": [{
                        "type": "text/plain",
                        "value": "A new comment was posted in your topic {}".format(topic.title)
                    }]
            }

            headers = {
                'authorization': "Bearer {0}".format(api_key),
                'content-type': "application/json"
            }

            response = requests.request("POST", url=url, data=json.dumps(data), headers=headers)

            print("Sent to SendGrid")
            print(response.text)
        else:
            print("No env vars or no email address")

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
