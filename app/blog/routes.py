from flask import render_template, request, redirect, url_for, session, flash, jsonify

from app import db, socket_io
from app.blog import blueprint
from app.blog.models import Post, Message
from app.base.models import User


@socket_io.on('send')
def send_message(data):
    print("calling in socket send")
    socket_io.emit('get', data)


@blueprint.route("/")
def index():
    posts = Post.query.order_by(Post.created_at)
    return render_template("index.html", posts=posts)


@blueprint.route("/post/<int:id>")
def get_post(id):
    post = Post.query.filter(Post.id == id).first()
    messages = Message.query.filter(Message.post_id == id).all()
    return render_template("get_post.html", post=post, messages=messages)


@blueprint.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if request.method == "POST":
        author = session["user"]
        title = request.form["title"]
        content = request.form["content"]

        # Check if the author exist
        user = User.query.filter_by(username=author).first()
        if not user:
            return redirect(url_for("base_blueprint.login"))
        
        # Check if title and content exist
        if not title or not content:
            flash("Please add title and content.")
            render_template("add_post.html")

        # Save post to database
        post = Post(
            user_id=user.id,
            title=title,
            content=content
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("blog_blueprint.index"))

    return render_template("add_post.html")


@blueprint.route('/get-messages', methods=['POST'])
def get_messages():

    id = session["id"]
    user = session["user"]

    # Select posts belong to user
    posts = Post.query.filter(Post.user_id == id).all()
    messages = Message.query.filter(Message.post_id.in_([p.id for p in posts])).order_by(Message.created_at).all()

    result = []
    for m in messages:
        result.append({
            "content": m.content
        })


    return jsonify({
        "data": result
    })


@blueprint.route('/add-message/<int:post_id>', methods=['GET', 'POST'])
def add_message(post_id):
    
    username = session["user"]
    user = User.query.filter(User.username == username).first()

    if request.method == "POST":
        content = request.form["content"]
        
        if content:
            message = Message(
                user_id=user.id,
                post_id=post_id,
                content=content
            )
            db.session.add(message)
            db.session.commit()

            send_message(f"{message.content} - {message.user.username}")

        return redirect(url_for("blog_blueprint.get_post", id=post_id))