"""
Main Flask application file for Belfry.
Enterprise-grade coding assessment platform.
"""
from flask import Flask
from config import Config
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Import and initialize db BEFORE importing models
from models import db
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Import models AFTER db.init_app
from models import User, Quiz, Testcase, Submission

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    return User.query.get(int(user_id))

# Register blueprints AFTER everything is initialized
from auth import auth_bp
from teacher import teacher_bp
from student import student_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(teacher_bp, url_prefix='/teacher')
app.register_blueprint(student_bp, url_prefix='/student')

@app.route('/')
def index():
    """Root route - redirects to appropriate dashboard."""
    from flask import redirect, url_for
    from flask_login import current_user
    
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        else:
            return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

