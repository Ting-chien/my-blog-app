from flask import render_template
from flask_login import login_required

from . import blueprint
from ..decorators import admin_required, permission_required
from ..auth.models import Permission



@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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
