from flask import Blueprint, render_template, request, flash, redirect, url_for, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.models.journal import Journal
from .decorators import login_required
import os
import uuid

journal_bp = Blueprint('journal', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@journal_bp.route('/upload', methods=['GET', 'POST'])
@login_required('researcher')
def upload_journal():
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        author_name = request.form['author_name']
        author_email = request.form['author_email']
        category = request.form['category']
        file = request.files['file']
        
        if file.filename == '':
            flash('Tidak ada file yang dipilih', 'error')
            return render_template('upload_journal.html')
        
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{original_filename}"
            
            upload_dir = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            os.makedirs(upload_dir, exist_ok=True)
            
            save_path = os.path.join(upload_dir, unique_filename)
            try:
                file.save(save_path)
                Journal.create(
                    title=title,
                    abstract=abstract,
                    author_name=author_name,
                    author_email=author_email,
                    category=category,
                    filename=original_filename,
                    file_path=unique_filename,
                    uploaded_by=session['user_id']
                )
                flash('Jurnal berhasil diupload dan menunggu persetujuan admin', 'success')
                return redirect(url_for('dashboard.dashboard'))
            except Exception:
                flash('Terjadi kesalahan saat mengupload file', 'error')
        else:
            flash('File harus berformat PDF, DOC, atau DOCX', 'error')
    
    return render_template('upload_journal.html')


@journal_bp.route('/journal/<int:journal_id>')
def view_journal(journal_id):
    journal = Journal.get_by_id(journal_id)
    if not journal:
        flash('Jurnal tidak ditemukan', 'error')
        return redirect(url_for('auth.index'))
    
    # Hak akses
    if journal['status'] != 'approved':
        if 'role' not in session:
            flash('Jurnal belum disetujui', 'error')
            return redirect(url_for('auth.index'))
        if session['role']=='researcher' and journal['uploaded_by']!=session['user_id']:
            flash('Anda tidak memiliki akses ke jurnal ini', 'error')
            return redirect(url_for('dashboard.dashboard'))
    
    return render_template('view_journal.html', journal=journal)


@journal_bp.route('/download/<int:journal_id>')
def download_journal(journal_id):
    journal = Journal.get_by_id(journal_id)
    if not journal:
        flash('Jurnal tidak ditemukan', 'error')
        return redirect(url_for('auth.index'))
    
    if journal['status'] != 'approved':
        if 'role' not in session:
            flash('Jurnal belum disetujui', 'error')
            return redirect(url_for('auth.index'))
        if session['role']=='researcher' and journal['uploaded_by']!=session['user_id']:
            flash('Anda tidak memiliki akses ke jurnal ini', 'error')
            return redirect(url_for('dashboard.dashboard'))

    upload_dir = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    unique_filename = journal['file_path']

    file_path = os.path.join(upload_dir, unique_filename)
    if not os.path.exists(file_path):
        flash('File jurnal tidak ditemukan di server', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    return send_from_directory(upload_dir, unique_filename, as_attachment=True,
                               download_name=journal['filename'])
