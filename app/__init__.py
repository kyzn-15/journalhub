from flask import Flask
from .models.db import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'
    app.config['UPLOAD_FOLDER'] = 'uploads/journals'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    from .controllers.auth_controller import auth_bp
    from .controllers.dashboard_controller import dashboard_bp
    from .controllers.journal_controller import journal_bp
    from .controllers.admin_controller import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        init_db()
    
    return app