from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db_connection

class User:
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def create(username, email, password, role, full_name):
        conn = get_db_connection()
        password_hash = generate_password_hash(password)
        try:
            conn.execute('''
                INSERT INTO users (username, email, password_hash, role, full_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, role, full_name))
            conn.commit()
        finally:
            conn.close()