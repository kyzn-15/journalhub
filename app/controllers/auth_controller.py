from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    from app.models.journal import Journal
    journals = Journal.get_all_approved()[:10]
    return render_template('index.html', journals=journals)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            flash(f'Selamat datang, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Username atau password salah', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        full_name = request.form['full_name']
        
        if role not in ['user', 'researcher']:
            flash('Role tidak valid', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        existing = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        if existing:
            flash('Username atau email sudah digunakan', 'error')
            conn.close()
            return render_template('register.html')
        
        User.create(username, email, password, role, full_name)
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout', 'info')
    return redirect(url_for('auth.index'))