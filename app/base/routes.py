from flask import render_template, request, redirect, url_for, session

from app import db
from app.base import blueprint


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        session["user"] = username
        return redirect(url_for("base_blueprint.profile"))

    return render_template("login.html")


@blueprint.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("base_blueprint.login"))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")


@blueprint.route('/profile', methods=['GET'])
def profile():
    if "user" in session:
        user = session["user"]
        return render_template("profile.html", user=user)
    return render_template("login.html")


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404