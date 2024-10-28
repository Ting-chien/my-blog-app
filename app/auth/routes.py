from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user

from . import blueprint
from .forms import LoginForm
from .models import User


@blueprint.route("/")
def index():
    return "Hello login"


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # get user from db
        if user and user.verify_password(form.password.data):
            # load user in session
            login_user(user, form.remember_me) 
            # check if user came from protected page
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("base.index")
            print(next)
            return redirect(next)
        flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)