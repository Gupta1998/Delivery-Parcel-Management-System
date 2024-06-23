from flask import flash, redirect, url_for
from flask_login import current_user
from . import login_manager
from functools import wraps

def role_required(role_name):
    def decorator(func):
        print(current_user)
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role != role_name:
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('index'))
            return func(*args, **kwargs)
        return decorated_function
    return decorator