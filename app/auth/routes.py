from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from .. import db
from ..email import send_email
from . import blueprint
from .forms import LoginForm, RegistrationForm
from .models import User


@blueprint.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('base.index'))
    return render_template('auth/unconfirmed.html')


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


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # 寄送認證信
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        print("Already confirmed")
        return redirect(url_for('base.index'))
    if current_user.confirm(token):
        print("Confirmed")
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        print("")
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('base.index'))