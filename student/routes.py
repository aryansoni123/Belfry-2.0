"""
Student routes for viewing and solving quizzes.
Uses LeetCode-style server-side execution engine.
"""
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from student import student_bp
from models import db, Quiz, Testcase, Submission
from judge import OnlineJudge
import json

# Initialize online judge
judge = OnlineJudge()

@student_bp.route('/dashboard')
@login_required
def dashboard():
    """Student dashboard showing available quizzes."""
    quizzes = Quiz.query.filter_by(is_active=True).order_by(Quiz.created_at.desc()).all()
    
    # Get submission status for each quiz
    quiz_status = []
    for quiz in quizzes:
        submission = Submission.query.filter_by(
            user_id=current_user.id,
            quiz_id=quiz.id
        ).order_by(Submission.submitted_at.desc()).first()
        
        quiz_status.append({
            'quiz': quiz,
            'submission': submission,
            'status': submission.status if submission else 'not_attempted'
        })
    
    return render_template('student_dashboard.html', quiz_status=quiz_status)

@student_bp.route('/quiz/<int:quiz_id>')
@login_required
def solve_quiz(quiz_id):
    """Solve a quiz (Skillrack-style interface)."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if not quiz.is_active:
        flash('This quiz is not available.', 'error')
        return redirect(url_for('student.dashboard'))
    
    # Get sample testcases only
    sample_testcases = Testcase.query.filter_by(quiz_id=quiz_id, is_sample=True).all()
    
    # Convert testcases to JSON-serializable format
    # For function-based problems, input_data and expected_output are JSON strings
    sample_testcases_json = [
        {
            'input_data': tc.input_data,
            'expected_output': tc.expected_output
        }
        for tc in sample_testcases
    ]
    
    # Get previous submission if any
    previous_submission = Submission.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz_id
    ).order_by(Submission.submitted_at.desc()).first()
    
    return render_template('solve_quiz.html', 
                         quiz=quiz, 
                         sample_testcases=sample_testcases,
                         sample_testcases_json=json.dumps(sample_testcases_json),
                         previous_submission=previous_submission)

@student_bp.route('/quiz/<int:quiz_id>/run', methods=['POST'])
@login_required
def run_code(quiz_id):
    """Run code against sample test cases only (LeetCode-style)."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if not quiz.is_active:
        return jsonify({'error': 'Quiz is not available'}), 400
    
    code = request.json.get('code', '').strip()
    language = request.json.get('language', 'python')
    
    if not code:
        return jsonify({'error': 'Code cannot be empty'}), 400
    
    # Get only sample testcases
    testcases = Testcase.query.filter_by(quiz_id=quiz_id, is_sample=True).all()
    
    if not testcases:
        return jsonify({'error': 'No sample test cases found for this quiz'}), 400
    
    # Prepare test cases for judge
    testcase_data = [
        {
            'input_data': tc.input_data,
            'expected_output': tc.expected_output
        }
        for tc in testcases
    ]
    
    # Execute using online judge (LeetCode-style)
    function_signature = quiz.function_signature or 'def solution():'
    results = judge.execute_submission(
        user_code=code,
        function_signature=function_signature,
        testcases=testcase_data,
        language=language,
        timeout=2.0,
        memory_limit='256m'
    )
    
    return jsonify({
        'status': 'success' if results['status'] == 'pass' else 'fail',
        'passed_testcases': results['passed_count'],
        'total_testcases': results['total_count'],
        'testcase_results': results.get('testcase_results', []),
        'error_message': results.get('error_message'),
        'error_type': results.get('error_type'),
        'total_execution_time': results.get('execution_time', 0)
    })

@student_bp.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit code for final evaluation against all test cases (LeetCode-style)."""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if not quiz.is_active:
        return jsonify({'error': 'Quiz is not available'}), 400
    
    code = request.json.get('code', '').strip()
    language = request.json.get('language', 'python')
    
    if not code:
        return jsonify({'error': 'Code cannot be empty'}), 400
    
    # Get all testcases (including hidden ones)
    testcases = Testcase.query.filter_by(quiz_id=quiz_id).all()
    
    if not testcases:
        return jsonify({'error': 'No test cases found for this quiz'}), 400
    
    # Prepare test cases for judge
    testcase_data = [
        {
            'input_data': tc.input_data,
            'expected_output': tc.expected_output
        }
        for tc in testcases
    ]
    
    # Execute using online judge (LeetCode-style)
    function_signature = quiz.function_signature or 'def solution():'
    results = judge.execute_submission(
        user_code=code,
        function_signature=function_signature,
        testcases=testcase_data,
        language=language,
        timeout=2.0,
        memory_limit='256m'
    )
    
    # Create submission record
    submission = Submission(
        user_id=current_user.id,
        quiz_id=quiz_id,
        code=code,
        language=language,
        status=results['status'],
        error_message=results.get('error_message'),
        error_type=results.get('error_type'),
        passed_testcases=results['passed_count'],
        total_testcases=results['total_count'],
        execution_time=results.get('execution_time', 0)
    )
    db.session.add(submission)
    db.session.commit()
    
    return jsonify({
        'status': submission.status,
        'passed_testcases': submission.passed_testcases,
        'total_testcases': submission.total_testcases,
        'error_message': submission.error_message,
        'error_type': submission.error_type,
        'execution_time': submission.execution_time,
        'testcase_results': results.get('testcase_results', [])
    })

# Legacy evaluate_code function removed - now using OnlineJudge

@student_bp.route('/submissions')
@login_required
def my_submissions():
    """View all submissions by the current student with scores."""
    submissions = Submission.query.filter_by(
        user_id=current_user.id
    ).order_by(Submission.submitted_at.desc()).all()
    
    return render_template('my_submissions.html', submissions=submissions)

