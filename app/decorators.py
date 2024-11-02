from functools import wraps
from flask import abort
from flask_login import current_user
from .auth.models import Permission


def permission_required(permission):
    """
    權限檢查裝飾器，會比對用戶是否有 permission
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    因為 admin 權限較常被單獨比較，因此獨立建立一函數
    """
    return permission_required(Permission.ADMIN)(f)
