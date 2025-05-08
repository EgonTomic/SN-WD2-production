import hashlib
import uuid

from flask import render_template, request, redirect, url_for, make_response, Blueprint
from models.user import User


auth_handlers = Blueprint("auth", __name__)


@auth_handlers.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = User.get_by_username(username=username)

        if not user:
            return "This user does not exist"
        else:
            # if user exists, check if password hashes match
            if password_hash == user.password_hash:
                user.set_new_session_token()

                # save user's session token into a cookie
                response = make_response(redirect(url_for('topic.index')))
                response.set_cookie("session_token", user.session_token)

                return response
            else:
                return "Your password is incorrect!"


@auth_handlers.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")

    elif request.method == "POST":
        username = request.form.get("username")
        email_address = request.form.get("email-address")
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        if password != repeat:
            return "Passwords do not match! Go back and try again."

        # check if username already exists
        user_exists = User.get_by_username(username=username)
        if user_exists:
            return "A user with this username already exists. Try a more unique username."

        verification_token = str(uuid.uuid4())

        user = User(username=username, password_hash=hashlib.sha256(password.encode()).hexdigest(),
                    email_address=email_address, verified=False, verification_token=verification_token)
        user.insert()

        # save user's session token into a cookie
        response = make_response(redirect(url_for('topic.index')))
        response.set_cookie("session_token", user.session_token)

        return response


@auth_handlers.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    result = User.email_verification(verification_token=token)
    return render_template("auth/email_verification_result.html", verified=result)
