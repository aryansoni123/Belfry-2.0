"""
Teacher routes for quiz management.
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from teacher import teacher_bp
from models import db, Quiz, Testcase, User, Submission
from testcase_generator import TestcaseGenerator, generate_function_testcases
from functools import wraps
import json

def teacher_required(f):
    """Decorator to ensure user is a teacher."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'teacher':
            flash('Access denied. Teacher privileges required.', 'error')
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    """Teacher dashboard showing all quizzes."""
    quizzes = Quiz.query.filter_by(created_by=current_user.id).order_by(Quiz.created_at.desc()).all()
    
    # Get statistics for each quiz
    quiz_stats = []
    for quiz in quizzes:
        total_submissions = Submission.query.filter_by(quiz_id=quiz.id).count()
        passed_submissions = Submission.query.filter_by(quiz_id=quiz.id, status='pass').count()
        quiz_stats.append({
            'quiz': quiz,
            'total_submissions': total_submissions,
            'passed_submissions': passed_submissions
        })
    
    return render_template('teacher_dashboard.html', quiz_stats=quiz_stats)

@teacher_bp.route('/create_quiz', methods=['GET', 'POST'])
@teacher_required
def create_quiz():
    """Create a new quiz (LeetCode-style function-based)."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        problem_statement = request.form.get('problem_statement')
        function_signature = request.form.get('function_signature', '').strip()
        sample_input = request.form.get('sample_input', '').strip()
        sample_output = request.form.get('sample_output', '').strip()
        constraints = request.form.get('constraints', '').strip()
        problem_type = request.form.get('problem_type', 'function')  # 'function' or 'stdin'
        
        if not title or not problem_statement:
            flash('Title and problem statement are required.', 'error')
            return render_template('create_quiz.html')
        
        # For function-based problems, function_signature is required
        if problem_type == 'function' and not function_signature:
            flash('Function signature is required for function-based problems.', 'error')
            return render_template('create_quiz.html')
        
        # Create quiz
        quiz = Quiz(
            title=title,
            description=description or '',
            problem_statement=problem_statement,
            function_signature=function_signature if problem_type == 'function' else None,
            sample_input=sample_input,
            sample_output=sample_output,
            constraints=constraints,
            problem_type=problem_type,
            created_by=current_user.id
        )
        db.session.add(quiz)
        db.session.flush()  # Get quiz.id
        
        # Generate test cases
        if problem_type == 'function':
            # Function-based: Generate test cases with JSON input/output
            testcases = generate_function_testcases(
                function_signature=function_signature,
                sample_input=sample_input,
                sample_output=sample_output,
                constraints=constraints
            )
        else:
            # Legacy stdin-based: Use old generator
            testcases = TestcaseGenerator.generate_testcases(
                problem_statement=problem_statement,
                sample_input=sample_input,
                sample_output=sample_output,
                constraints=constraints
            )
        
        # Add test cases in batches for better performance
        batch_size = 100
        total_testcases = len(testcases)
        
        for i in range(0, total_testcases, batch_size):
            batch = testcases[i:i+batch_size]
            for tc in batch:
                testcase = Testcase(
                    quiz_id=quiz.id,
                    input_data=tc['input_data'],
                    expected_output=tc['expected_output'],
                    is_sample=tc['is_sample'],
                    testcase_type=tc['testcase_type']
                )
                db.session.add(testcase)
            # Commit in batches to avoid memory issues
            db.session.flush()
        
        db.session.commit()
        flash(f'Quiz "{title}" created successfully with {total_testcases} test cases!', 'success')
        return redirect(url_for('teacher.dashboard'))
    
    return render_template('create_quiz.html')

@teacher_bp.route('/quiz/<int:quiz_id>')
@teacher_required
def view_quiz(quiz_id):
    """View quiz details and submissions."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Verify ownership
    if quiz.created_by != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('teacher.dashboard'))
    
    # Get testcases
    testcases = Testcase.query.filter_by(quiz_id=quiz_id).all()
    
    # Get submissions
    submissions = Submission.query.filter_by(quiz_id=quiz_id).order_by(Submission.submitted_at.desc()).all()
    
    return render_template('view_quiz.html', quiz=quiz, testcases=testcases, submissions=submissions)

@teacher_bp.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
@teacher_required
def edit_quiz(quiz_id):
    """Edit an existing quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Verify ownership
    if quiz.created_by != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('teacher.dashboard'))
    
    if request.method == 'POST':
        quiz.title = request.form.get('title')
        quiz.description = request.form.get('description')
        quiz.problem_statement = request.form.get('problem_statement')
        quiz.sample_input = request.form.get('sample_input', '').strip()
        quiz.sample_output = request.form.get('sample_output', '').strip()
        quiz.constraints = request.form.get('constraints', '').strip()
        
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('teacher.view_quiz', quiz_id=quiz_id))
    
    return render_template('edit_quiz.html', quiz=quiz)

@teacher_bp.route('/quiz/<int:quiz_id>/regenerate_testcases', methods=['POST'])
@teacher_required
def regenerate_testcases(quiz_id):
    """Regenerate test cases for a quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Verify ownership
    if quiz.created_by != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Delete existing testcases
    Testcase.query.filter_by(quiz_id=quiz_id).delete()
    db.session.flush()
    
    # Generate new testcases based on problem type
    if quiz.problem_type == 'function':
        testcases = generate_function_testcases(
            function_signature=quiz.function_signature or '',
            sample_input=quiz.sample_input,
            sample_output=quiz.sample_output,
            constraints=quiz.constraints
        )
    else:
        testcases = TestcaseGenerator.generate_testcases(
            problem_statement=quiz.problem_statement,
            sample_input=quiz.sample_input,
            sample_output=quiz.sample_output,
            constraints=quiz.constraints
        )
    
    # Add test cases in batches for better performance
    batch_size = 100
    total_testcases = len(testcases)
    
    for i in range(0, total_testcases, batch_size):
        batch = testcases[i:i+batch_size]
        for tc in batch:
            testcase = Testcase(
                quiz_id=quiz.id,
                input_data=tc['input_data'],
                expected_output=tc['expected_output'],
                is_sample=tc['is_sample'],
                testcase_type=tc['testcase_type']
            )
            db.session.add(testcase)
        db.session.flush()
    
    db.session.commit()
    return jsonify({'success': True, 'count': total_testcases})

