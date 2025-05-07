from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models.user import User
from models.settings import db

profile_handlers = Blueprint("profile", __name__)

@profile_handlers.route("/profile", methods=["GET"])
def profile():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()

    if user:
        return render_template("profile/profile.html", user=user)

@profile_handlers.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    session_token = request.cookies.get("session_token")

    # get user from database based on session_token
    user = db.query(User).filter_by(session_token=session_token).first()

    if request.method == "GET":
        if user:
            return render_template("profile/edit_profile.html", user=user)
        else:
            return redirect(url_for("topic.index"))
    elif request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email_adress")

        # update user object
        user.username = name
        user.email_adress = email

        db.add(user)
        db.commit()
        return redirect(url_for("profile.profile"))
    
@profile_handlers.route("/delete-profile", methods=["GET", "POST"])
def delete_profile():
    session_token = request.cookies.get("session_token")

    # get user from database based on session_token
    user = db.query(User).filter_by(session_token=session_token).first()

    if request.method == "GET":
        return render_template("profile/delete_profile.html", user=user)
    elif request.method == "POST":
        db.delete(user)
        db.commit()
        return redirect(url_for("topic.index"))