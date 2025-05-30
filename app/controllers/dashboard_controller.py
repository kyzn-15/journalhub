from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.models.db import get_db_connection
from app.models.journal import Journal
from .decorators import login_required  

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(role=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Silakan login terlebih dahulu', 'error')
                return redirect(url_for('auth.login'))
            if role and session.get('role') != role:
                flash('Akses ditolak', 'error')
                return redirect(url_for('dashboard.dashboard'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@dashboard_bp.route('/dashboard')
@login_required()
def dashboard():
    if session['role'] == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    
    if session['role'] == 'researcher':
        conn = get_db_connection()
        my_journals = conn.execute('SELECT * FROM journals WHERE uploaded_by = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
        conn.close()
        return render_template('dashboard.html', my_journals=my_journals)
    else:
        journals = Journal.get_all_approved()
        return render_template('dashboard.html', journals=journals)