from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from . import blueprint
from .forms import LoginForm
from .models import User


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
            return redirect(next)
        flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user() # 透過 flask-login 的函數來將使用者從 session 中移除
    flash("You have been logged out.")
    return redirect(url_for("base.index"))