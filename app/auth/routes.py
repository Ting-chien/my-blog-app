from flask import render_template

from . import blueprint


@blueprint.route("/login")
def login():
    return render_template("auth/login.html")