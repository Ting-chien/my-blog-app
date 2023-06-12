from flask import render_template, request, redirect, url_for, session

from app import db
from app.blog import blueprint
from app.blog.models import Blog
from app.base.models import User


@blueprint.route('', methods=['GET', 'POST'])
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
            render_template
            
    return render_template("add_post.html")
