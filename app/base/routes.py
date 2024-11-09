from flask import render_template
from flask_login import login_required

from . import blueprint
from ..decorators import admin_required, permission_required
from ..auth.models import Permission, User



@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@blueprint.route("/user/<username>")
def user(username):
    # 透過username來向資料庫查詢符合的用戶，入查無使用者則返回404頁面
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


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
