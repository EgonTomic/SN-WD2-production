from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models.topic import Topic
from models.user import User
from models.comment import Comment
from models.settings import db
from utils.redis_helper import create_csrf_token, validate_csrf_token

comment_handlers = Blueprint("comment", __name__)

@comment_handlers.route("/topic/<topic_id>/create_comment", methods=["POST"])
def comment_create(topic_id):

    # Check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    if not user:
        return redirect(url_for("auth.login"))
    
    csrf_token = request.form.get("csrf_token")
    text = request.form.get("text")

    topic = db.query(Topic).get(int(topic_id))

    if validate_csrf_token(csrf_token, user.username):
        comment = Comment.create(topic=topic, text=text, author=user)

    return redirect(url_for("topic.topic_details", topic_id=topic_id, csrf_token=create_csrf_token(user.username)))

@comment_handlers.route("/comment/<comment_id>/edit", methods=["GET", "POST"])
def comment_edit(comment_id):
    
    # Check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    if not user:
        return redirect(url_for("auth.login"))
    
    text = request.form.get("text")

    comment = db.query(Comment).get(int(comment_id))

    if user.id != comment.author.id:
        return redirect(url_for("topic.index"))
    
    if request.method == "GET":
        return render_template("topic/comment_edit.html", comment=comment, user=user)
    elif request.method == "POST":
        text = request.form.get("text")
        comment.text = text
        db.add(comment)
        db.commit()
        return redirect(url_for("topic.topic_details", topic_id=comment.topic.id))
    
@comment_handlers.route("/comment/<comment_id>/delete", methods=["GET", "POST"])
def comment_delete(comment_id):

    # Check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    if not user:
        return redirect(url_for("auth.login"))
    
    comment = db.query(Comment).get(int(comment_id))
    
    if user.id != comment.author.id:
        return redirect(url_for("topic.index"))
    
    if request.method == "GET":
        return render_template("topic/comment_delete.html", comment=comment, user=user, topic=comment.topic)
    elif request.method == "POST":
        db.delete(comment)
        db.commit()
        return redirect(url_for("topic.index"))