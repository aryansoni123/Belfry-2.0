"""
Database models for Belfry application.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and role management."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'teacher' or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = db.relationship('Submission', backref='user', lazy=True)
    created_quizzes = db.relationship('Quiz', backref='creator', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Quiz(db.Model):
    """Quiz model representing a coding problem (LeetCode-style function-based)."""
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    problem_statement = db.Column(db.Text, nullable=False)
    function_signature = db.Column(db.Text, nullable=True)  # e.g., "def twoSum(nums: List[int], target: int) -> List[int]:"
    sample_input = db.Column(db.Text, nullable=True)
    sample_output = db.Column(db.Text, nullable=True)
    constraints = db.Column(db.Text, nullable=True)
    problem_type = db.Column(db.String(20), default='function')  # 'function' (LeetCode-style) or 'stdin' (legacy)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    testcases = db.relationship('Testcase', backref='quiz', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='quiz', lazy=True)
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class Testcase(db.Model):
    """Testcase model for quiz evaluation (LeetCode-style)."""
    __tablename__ = 'testcases'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    input_data = db.Column(db.Text, nullable=False)  # JSON string of function arguments
    expected_output = db.Column(db.Text, nullable=False)  # JSON string of expected return value
    is_sample = db.Column(db.Boolean, default=False)  # True for sample, False for hidden
    testcase_type = db.Column(db.String(20), default='normal')  # 'normal', 'boundary', 'random'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Testcase {self.id} for Quiz {self.quiz_id}>'

class Submission(db.Model):
    """Submission model for student code submissions."""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(20), default='python')
    status = db.Column(db.String(20), default='pending')  # 'pending', 'pass', 'fail'
    error_message = db.Column(db.Text, nullable=True)
    error_type = db.Column(db.String(50), nullable=True)  # 'runtime_error', 'timeout', 'wrong_answer', 'syntax_error'
    passed_testcases = db.Column(db.Integer, default=0)
    total_testcases = db.Column(db.Integer, default=0)
    execution_time = db.Column(db.Float, nullable=True)  # Total execution time in seconds
    memory_used = db.Column(db.Integer, nullable=True)  # Memory used in KB
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Submission {self.id} by User {self.user_id}>'

