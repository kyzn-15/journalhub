from flask import Blueprint, render_template, flash, redirect, url_for, session
from app.models.db import get_db_connection
from app.models.journal import Journal
from .decorators import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required('admin')
def admin_dashboard():
    conn = get_db_connection()
    
    total_users = conn.execute('SELECT COUNT(*) as count FROM users WHERE role != "admin"').fetchone()['count']
    total_journals = conn.execute('SELECT COUNT(*) as count FROM journals').fetchone()['count']
    pending_journals = conn.execute('SELECT COUNT(*) as count FROM journals WHERE status = "pending"').fetchone()['count']
    
    recent_journals = conn.execute('''
        SELECT j.*, u.full_name as uploader_name 
        FROM journals j 
        LEFT JOIN users u ON j.uploaded_by = u.id 
        ORDER BY j.created_at DESC 
        LIMIT 10
    ''').fetchall()
    
    users = conn.execute('SELECT * FROM users WHERE role != "admin" ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_journals=total_journals,
                         pending_journals=pending_journals,
                         recent_journals=recent_journals,
                         users=users)

@admin_bp.route('/admin/approve/<int:journal_id>')
@login_required('admin')
def approve_journal(journal_id):
    Journal.update_status(journal_id, 'approved')
    flash('Jurnal berhasil disetujui', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/reject/<int:journal_id>')
@login_required('admin')
def reject_journal(journal_id):
    Journal.update_status(journal_id, 'rejected')
    flash('Jurnal ditolak', 'info')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/delete_journal/<int:journal_id>')
@login_required('admin')
def delete_journal(journal_id):
    Journal.delete(journal_id)
    flash('Jurnal berhasil dihapus', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/delete_user/<int:user_id>')
@login_required('admin')
def delete_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user and user['role'] != 'admin':
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        flash('User berhasil dihapus', 'success')
    else:
        flash('Tidak dapat menghapus admin', 'error')
    conn.close()
    return redirect(url_for('admin.admin_dashboard'))