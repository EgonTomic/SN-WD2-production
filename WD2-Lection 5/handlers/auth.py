import hashlib
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models.user import User
from models.settings import db

auth_handlers = Blueprint("auth", __name__)

@auth_handlers.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Calculate hashed password based on plan text input from login form
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Get user from database base on username from login form
        user = db.query(User).filter_by(username=username).first()

        if not user:
            return "Username or password is incorrect."
        else:
            # If user exists, check if password hashes match
            if password_hash == user.password_hash:
                user.session_token = str(uuid.uuid4())
                db.add(user)
                db.commit()

                # Save user session token into cookie
                response = make_response(redirect(url_for("topic.index")))
                response.set_cookie("session_token", user.session_token)

                return response
            else:
                return "Username or password is incorrect."
            

@auth_handlers.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")
    elif request.method == "POST":
        username = request.form.get("username")
        email_address = request.form.get("email_adress")
        password = request.form.get("password")
        repeated_password = request.form.get("repeatpassword")

        if password != repeated_password:
            return "Passwords don't match. Please try again."

        print("New user username: " + username)
        print("New user email: " + email_address)
        print("New user password: " + password)
        print("New user repeat password: " + repeated_password)

        user = User(username=username, email_adress=email_address,  password_hash=hashlib.sha256(password.encode()).hexdigest(), 
                    session_token=str(uuid.uuid4()))
        
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for("topic.index")))
        response.set_cookie("session_token", user.session_token)
 
        return response