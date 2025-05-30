from functools import wraps
from flask import flash, redirect, url_for, session

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Silakan login terlebih dahulu', 'error')
                return redirect(url_for('auth.login'))
            if role and session.get('role') != role:
                flash('Akses ditolak', 'error')
                return redirect(url_for('dashboard.dashboard'))
            return f(*args, **kwargs)
        return wrapper
    return decorator