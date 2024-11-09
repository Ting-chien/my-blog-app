from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from . import blueprint
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..decorators import admin_required, permission_required
from ..auth.models import Permission, User, Role



@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@blueprint.route("/user/<username>")
def user(username):
    # 透過username來向資料庫查詢符合的用戶，入查無使用者則返回404頁面
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@blueprint.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """編輯個人資訊頁的資訊"""
    form = EditProfileForm()
    # 若有送出表單，則會更新個人資訊，並從新跳轉到此頁
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    # 若表單位送出，則會帶入current_user的資訊
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@blueprint.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    """提供管理者編輯用戶的資料、權限"""
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@blueprint.route("/admin")
@login_required
@admin_required
def for_admins_only():
    """
    檢查是否有 admin 權限
    """
    return "For administrators!"


@blueprint.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    """
    檢查是否有 moderate 權限
    """
    return "For comment moderators!"
