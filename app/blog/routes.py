from flask import render_template, request, redirect, url_for, session, flash

from app import db
from app.blog import blueprint
from app.blog.models import Post
from app.base.models import User


@blueprint.route("/")
def index():
    posts = Post.query.order_by(Post.created_at)
    return render_template("index.html", posts=posts)


@blueprint.route("/post/<int:id>")
def get_post(id):
    post = Post.query.filter(Post.id == id).first()
    return render_template("get_post.html", post=post)


@blueprint.route('add-post', methods=['GET', 'POST'])
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
            author=author,
            title=title,
            content=content
        )
        db.session.add(post)
        db.session.commit()

        redirect(url_for("blog_blueprint.index"))

    return render_template("add_post.html")
