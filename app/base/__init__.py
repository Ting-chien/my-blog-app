from flask import Blueprint

blueprint = Blueprint('base', __name__)

from ..auth.models import Permission


@blueprint.app_context_processor
def inject_permissions():
    """
    透過 app_context_processor 裝飾器，可以將變數全域
    的載入模板中被使用。
    """
    return dict(Permission=Permission)
