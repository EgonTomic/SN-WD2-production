from flask import render_template, request, redirect, url_for, Blueprint
from models.user import User
from models.comment import Comment
from utils.csrf_helper import set_csrf_token, get_csrf_token

comment_handlers = Blueprint("comment", __name__)


@comment_handlers.route("/topic/<topic_id>/create-comment", methods=["POST"])
def comment_create(topic_id):
    # get current user (comment author)
    session_token = request.cookies.get("session_token")
    user = User.get_by_session_token(session_token=session_token)

    # only logged in users can create a comment
    if not user:
        return redirect(url_for('auth.login'))

    csrf = request.form.get("csrf")  # csrf from HTML
    redis_csrf = get_csrf_token(username=user.username)

    # if they match, allow user to create a comment
    if csrf and csrf == redis_csrf:
        text = request.form.get("text")

        # create a Comment object
        comment = Comment(topic_id=topic_id, text=text, author_id=user._id, author_username=user.username)
        comment.insert()

        return redirect(url_for('topic.topic_details', topic_id=topic_id, csrf_token=set_csrf_token(username=user.username)))
    else:
        return "CSRF token is not valid!"


@comment_handlers.route("/comment/<comment_id>/edit", methods=["GET", "POST"])
def comment_edit(comment_id):
    comment = Comment.get_by_id(comment_id=comment_id)

    # get current user
    session_token = request.cookies.get("session_token")
    user = User.get_by_session_token(session_token=session_token)

    # check if user logged in & if user is author
    if not user:
        return redirect(url_for('auth.login'))
    elif comment.author_id != user._id:
        return "You can only edit your own comments!"

    # GET request
    if request.method == "GET":
        csrf_token = set_csrf_token(username=user.username)
        return render_template("comment/comment_edit.html", comment=comment, csrf_token=csrf_token)

    # POST request
    elif request.method == "POST":
        text = request.form.get("text")

        # check CSRF tokens
        csrf = request.form.get("csrf")
        redis_csrf = get_csrf_token(username=user.username)

        # if they match, allow user to edit the comment
        if csrf and csrf == redis_csrf:
            Comment.edit_comment(comment_id=comment_id, updates_dict={"text": text})
            return redirect(url_for('topic.topic_details', topic_id=comment.topic_id))
        else:
            return "CSRF error: tokens don't match!"


@comment_handlers.route("/comment/<comment_id>/delete", methods=["POST"])
def comment_delete(comment_id):
    comment = Comment.get_by_id(comment_id=comment_id)

    # get current user
    session_token = request.cookies.get("session_token")
    user = User.get_by_session_token(session_token=session_token)

    # check if user logged in & if user is author
    if not user:
        return redirect(url_for('auth.login'))
    elif comment.author_id != user._id:
        return "You can only delete your own comments!"

    # check CSRF tokens
    csrf = request.form.get("csrf")
    redis_csrf = get_csrf_token(username=user.username)

    # if they match, allow user to delete the comment
    if csrf and csrf == redis_csrf:
        Comment.delete_comment(comment_id=comment_id)
        return redirect(url_for('topic.topic_details', topic_id=comment.topic_id))
    else:
        return "CSRF error: tokens don't match!"
