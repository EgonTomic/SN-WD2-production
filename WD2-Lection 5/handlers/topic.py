from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models.topic import Topic
from models.user import User
from models.settings import db
import math
from models.comment import Comment
from utils.redis_helper import create_csrf_token, validate_csrf_token

topic_handlers = Blueprint("topic", __name__)

@topic_handlers.route("/")
def index():
    # Check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    # Get number of page from URL argument
    try:
        page_number = int(request.args.get("page", 1))
    except ValueError: 
        page_number = 1
    page_number = max(1, page_number)

    # Basic query
    base_query = db.query(Topic)
    total_topics = base_query.count()

    # Adding ordering
    topic_query = base_query.order_by(Topic.id.desc())

    # Parameters pagination
    per_page = 5
    num_pages = math.ceil(total_topics / per_page)
    
    offset = (page_number - 1) * per_page
    
    topics = topic_query.limit(per_page).offset(offset).all()

    page_obj = type("PageObj", (), {})()  # Creating empty object
    page_obj.number = page_number
    page_obj.object_list = topics
    page_obj.has_previous = page_number > 1
    page_obj.has_next = page_number < num_pages
    page_obj.previous_page_number = page_number - 1 if page_obj.has_previous else 1
    page_obj.next_page_number = page_number + 1 if page_obj.has_next else num_pages

    return render_template("topic/index.html", user=user, topics=topics, page_obj=page_obj,num_pages=num_pages, total_topics=total_topics)
    
@topic_handlers.route("/create-topic", methods=["GET", "POST"])
def topic_create():
    # Check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()
    
    if not user:
        return redirect(url_for("auth.login"))
    
    if request.method == "GET":
        csrf_token = create_csrf_token(user.username)

        return render_template("topic/topic_create.html", user=user, csrf_token=csrf_token)
    elif request.method == "POST":
        csrf_token = request.form.get('csrf_token')
        title = request.form.get('title')
        text = request.form.get('text')

        if validate_csrf_token(csrf_token, user.username):
            # Create new topic object
            user = db.query(User).filter_by(session_token=session_token).first()
            topic = Topic.create(title=title, text=text, author=user)
            return redirect(url_for("topic.index"))
        else:
            return redirect(url_for("auth.login"))
    
@topic_handlers.route("/topic/<topic_id>", methods=["GET"])
def topic_details(topic_id):
    # Check if user is authenticated based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    topic = db.query(Topic).get(int(topic_id))
    comments = db.query(Comment).filter_by(topic=topic).all()

    return render_template("topic/topic_details.html", topic=topic, user=user, comments=comments, csrf_token=create_csrf_token(user.username))

@topic_handlers.route("/topic/<topic_id>/edit", methods=["GET", "POST"])
def topic_edit(topic_id):
    # Check if user is autheticaed based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    if not user:
        return redirect(url_for("topic.index"))
    
    topic = db.query(Topic).get(int(topic_id))

    if user.id != topic.author.id:
        return redirect(url_for("topic.index"))
    
    if request.method == "GET":
        return render_template("topic/topic_edit.html", topic=topic, user=user)
    elif request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        topic.title = title
        topic.text = text
        db.add(topic)
        db.commit()
        return redirect(url_for("topic.topic_details", topic_id=topic_id))

@topic_handlers.route("/topic/<topic_id>/delete", methods=["GET", "POST"])
def topic_delete(topic_id):
    # Check if user is autheticaed based on session_token
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    if not user:
        return redirect(url_for("topic.index"))
    
    topic = db.query(Topic).get(int(topic_id))

    if user.id != topic.author.id:
        return redirect(url_for("topic.index"))
    
    if request.method == "GET":
        return render_template("topic/topic_delete.html", topic=topic, user=user)
    
    elif request.method == "POST":
        db.delete(topic)
        db.commit()
        return redirect(url_for("topic.index"))