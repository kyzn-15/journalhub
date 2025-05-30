from .db import get_db_connection
import os

class Journal:
    @staticmethod
    def get_all_approved():
        conn = get_db_connection()
        journals = conn.execute('''
            SELECT j.*, u.full_name as uploader_name 
            FROM journals j 
            LEFT JOIN users u ON j.uploaded_by = u.id 
            WHERE j.status = 'approved'
            ORDER BY j.created_at DESC
        ''').fetchall()
        conn.close()
        return journals

    @staticmethod
    def create(title, abstract, author_name, author_email, category, filename, file_path, uploaded_by):
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO journals (title, abstract, author_name, author_email, 
                                category, filename, file_path, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, abstract, author_name, author_email, category, 
              filename, file_path, uploaded_by))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(journal_id):
        conn = get_db_connection()
        journal = conn.execute('''
            SELECT j.*, u.full_name as uploader_name 
            FROM journals j 
            LEFT JOIN users u ON j.uploaded_by = u.id 
            WHERE j.id = ?
        ''', (journal_id,)).fetchone()
        conn.close()
        return journal

    @staticmethod
    def update_status(journal_id, status):
        conn = get_db_connection()
        conn.execute('UPDATE journals SET status = ? WHERE id = ?', (status, journal_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(journal_id):
        conn = get_db_connection()
        journal = conn.execute('SELECT * FROM journals WHERE id = ?', (journal_id,)).fetchone()
        if journal:
            try:
                os.remove(journal['file_path'])
            except:
                pass
            conn.execute('DELETE FROM journals WHERE id = ?', (journal_id,))
            conn.commit()
        conn.close()