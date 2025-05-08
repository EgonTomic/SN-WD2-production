import uuid
from smartninja_mongo.bson import ObjectId
from smartninja_mongo.odm import Model
from utils.email_helper import send_email_to_one_recipient
from models.database import mongo_db


collection = mongo_db.users


class User(Model):
    def __init__(self, username, password_hash, email_address=None, verified=False, verification_token=None, **kwargs):
        self.username = username
        self.password_hash = password_hash
        self.email_address = email_address
        self.verified = verified
        self.verification_token = verification_token

        super().__init__(**kwargs)

    def insert(self):
        self.session_token = str(uuid.uuid4())
        user_id = collection.insert_one(self.__dict__).inserted_id
        self._id = user_id  # save id from MongoDB into the User object

        # send email verification message
        subject = "Please verify your email address"
        domain = "https://ninja-tech-forum.herokuapp.com"  # TODO: enter your own Heroku domain here!
        message = "Hi! Please click on this link to verify your email address: {0}/verify-email/{1}".format(domain, self.verification_token)
        send_email_to_one_recipient(recipient_email=self.email_address, subject=subject, message=message)

        return True

    @classmethod
    def get_by_username(cls, username):
        user_dict = collection.find_one({"username": username})
        user_obj = cls.convert_dict_to_object(data_dict=user_dict)
        return user_obj

    @classmethod
    def get_by_session_token(cls, session_token):
        user_dict = collection.find_one({"session_token": session_token})
        user_obj = cls.convert_dict_to_object(data_dict=user_dict)
        return user_obj

    @classmethod
    def email_verification(cls, verification_token):
        user_dict = collection.find_one({"verification_token": verification_token})

        if user_dict:
            collection.update_one({"_id": user_dict["_id"]}, {"$set": {"verified": True}})
            return True
        else:
            return False

    def set_new_session_token(self):
        self.session_token = str(uuid.uuid4())
        collection.update_one({"_id": ObjectId(self._id)}, {"$set": {"session_token": self.session_token}})

        return True
