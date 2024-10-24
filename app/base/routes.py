from flask import render_template, request, redirect, url_for, session, flash

from app import db
from app.base import blueprint
from app.base.models import User


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["user"] = username
            session["id"] = user.id
            return redirect(url_for("blog_blueprint.index"))
        flash("Wrong input username or password")
        return render_template('login.html', 
                                msg='Username not exist or wrong password.')

    return render_template("login.html")


@blueprint.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("base_blueprint.login"))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exist
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', 
                                   msg='Username already registered')
        
        # Insert new user
        user = User(username=username,
                    password=password)
        db.session.add(user)
        db.session.commit()

        # Login to profile page
        session["user"] = username
        session["id"] = user.id
        return redirect(url_for("blog_blueprint.index"))

    return render_template("register.html")


@blueprint.route('/profile', methods=['GET'])
def profile():
    if "user" in session:
        user = session["user"]
        return render_template("profile.html", user=user)
    return redirect(url_for("base_blueprint.login"))


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404