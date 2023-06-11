from flask import render_template, request, redirect, url_for, session

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
            return redirect(url_for("base_blueprint.profile"))
        return render_template('login.html', 
                                msg='Username not exist or wrong password.', 
                                is_login=True)

    return render_template("login.html", is_login=True)


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
                                   msg='Username already registered', 
                                   is_register=True)
        
        # Insert new user
        user = User(username=username,
                    password=password)
        db.session.add(user)
        db.session.commit()

        # Login to profile page
        session["user"] = username
        return redirect(url_for("base_blueprint.profile"))

    return render_template("register.html", is_register=True)


@blueprint.route('/profile', methods=['GET'])
def profile():
    if "user" in session:
        user = session["user"]
        return render_template("profile.html", user=user)
    return render_template("login.html")


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404