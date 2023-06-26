import os
import json
from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_socketio import join_room, leave_room
from werkzeug.utils import secure_filename
from psycopg2 import Binary

from app import db, socket_io
from app.blog import blueprint
from app.blog.models import Post, Message
from app.base.models import User


@socket_io.on('connect')
def handle_connect():
    sid = session["id"]
    join_room(sid)


@socket_io.on('disconnect')
def handle_disconnect():
    sid = session["id"]
    leave_room(sid)


@socket_io.on('send')
def send_message(data):
    recipient = data["recipient"]
    message = data["message"]
    socket_io.emit('get-message', message, room=[recipient])
    socket_io.emit('alert', message, room=[recipient])


@blueprint.route("/")
def index():
    posts = Post.query.order_by(Post.created_at)
    return render_template("index.html", posts=posts)


@blueprint.route("/post/<int:id>")
def get_post(id):
    post = Post.query.filter(Post.id == id).first()
    messages = Message.query.filter(Message.post_id == id).all()
    return render_template("get_post.html", post=post, messages=messages, img=json.loads(post.image.decode()))


@blueprint.route('/add-post', methods=['GET', 'POST'])
def add_post():

    if request.method == "POST":
        data = request.json
        author = session["user"]
        title = data["title"]
        content = data["content"]
        image = data["img"]

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
            content=content,
            image=json.dumps(image).encode()
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

            send_message({
                "recipient": message.post.user_id,
                "message": f"{message.content} - {message.user.username}"
            })

        return redirect(url_for("blog_blueprint.get_post", id=post_id))
    

@blueprint.route("/upload-file", methods=["POST"])
def upload_file():

    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        filepath = "app/static/img"
        file.save(os.path.join(filepath, filename))
        return redirect(url_for("blog_blueprint.uploaded_file", filename=filename))

    return redirect(url_for("blog_blueprint.add_post"))


@blueprint.route("/files/<filename>")
def uploaded_file(filename):
    return f"""
    <img src="/static/img/{filename}">
    """


@blueprint.route("/upload-file-with-blob", methods=["POST"])
def upload_file_with_blob():

    print(request.form)

    return jsonify({
        "img": None
    })


@blueprint.route("/upload-file-with-buffer", methods=["POST"])
def upload_file_with_buffer():

    json_data = request.json

    # insert new image
    img = Image(data=json.dumps(json_data["img"]).encode())
    db.session.add(img)
    db.session.commit()

    # return image object
    return jsonify({
        "img": json.loads(img.data.decode())
    })