"""
Database initialization script for Belfry.
Creates all tables and optionally seeds initial data.
"""
from app import app, db
from models import User, Quiz, Testcase, Submission
from werkzeug.security import generate_password_hash

def init_db():
    """Initialize the database with all tables."""
    with app.app_context():
        # WARNING: This will delete ALL data!
        import sys
        print("=" * 60)
        print("WARNING: This will DELETE ALL existing data!")
        print("=" * 60)
        response = input("Type 'DELETE ALL DATA' to confirm: ")
        if response != 'DELETE ALL DATA':
            print("Aborted. Database was NOT modified.")
            return
        
        # Drop all tables (for fresh start)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")

def seed_data():
    """Seed the database with initial teacher and student accounts."""
    with app.app_context():
        # Create teacher account
        teacher = User(
            username='teacher',
            email='teacher@belfry.edu',
            password_hash=generate_password_hash('teacher123'),
            role='teacher'
        )
        db.session.add(teacher)
        
        # Create student account
        student = User(
            username='student',
            email='student@belfry.edu',
            password_hash=generate_password_hash('student123'),
            role='student'
        )
        db.session.add(student)
        
        # Create another student
        student2 = User(
            username='student2',
            email='student2@belfry.edu',
            password_hash=generate_password_hash('student123'),
            role='student'
        )
        db.session.add(student2)
        
        db.session.commit()
        
        print("Seed data created successfully!")
        print("\nDefault accounts:")
        print("Teacher - Username: teacher, Password: teacher123")
        print("Student - Username: student, Password: student123")
        print("Student - Username: student2, Password: student123")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--seed':
        init_db()
        seed_data()
    else:
        init_db()
        print("\nTo seed initial accounts, run: python init_db.py --seed")

