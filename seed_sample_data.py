"""
Seed script to populate Belfry with sample quizzes and submissions.
Creates:
- Multiple function-based quizzes (LeetCode-style)
- Test cases for each quiz
- Some submissions (passed/failed) for some quizzes
- Some quizzes ready to submit (no submissions yet)
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Quiz, Testcase, Submission
from config import Config
from datetime import datetime, timedelta, timezone
import json

# Create app without importing routes (to avoid docker dependency)
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def seed_sample_data():
    """Seed database with sample quizzes and submissions."""
    
    with app.app_context():
        # Check if database tables exist, create if not
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            print("Creating database with latest schema...")
            db.create_all()
            print("Database created.")
        else:
            print("Database already exists. Checking for updates...")
            # Only create missing tables
            db.create_all()
        
        # Check if users exist, if not create them
        if not User.query.filter_by(username='teacher').first():
            from werkzeug.security import generate_password_hash
            teacher = User(
                username='teacher',
                email='teacher@belfry.edu',
                password_hash=generate_password_hash('teacher123'),
                role='teacher'
            )
            db.session.add(teacher)
            
            student1 = User(
                username='student',
                email='student@belfry.edu',
                password_hash=generate_password_hash('student123'),
                role='student'
            )
            db.session.add(student1)
            
            student2 = User(
                username='student2',
                email='student2@belfry.edu',
                password_hash=generate_password_hash('student123'),
                role='student'
            )
            db.session.add(student2)
            db.session.commit()
            print("Created default users.")
        # Get teacher user
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            print("ERROR: Teacher user not found. Please run 'python init_db.py --seed' first.")
            return
        
        # Get student users
        student1 = User.query.filter_by(username='student').first()
        student2 = User.query.filter_by(username='student2').first()
        
        if not student1 or not student2:
            print("ERROR: Student users not found. Please run 'python init_db.py --seed' first.")
            return
        
        # Check if quizzes already exist
        existing_quizzes = Quiz.query.all()
        if existing_quizzes:
            print(f"Found {len(existing_quizzes)} existing quiz(es) in database.")
            print("To avoid data loss, this script will NOT drop existing quizzes.")
            print("Use restore_quizzes_safe.py to add missing quizzes without dropping data.")
            return
        
        print("Creating sample quizzes and submissions...")
        
        # Quiz 1: Two Sum (with submissions - some passed, some failed)
        quiz1 = Quiz(
            title="Two Sum",
            description="Find two numbers in an array that add up to a target value.",
            problem_statement="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]""",
            function_signature="def twoSum(nums: List[int], target: int) -> List[int]:",
            sample_input=json.dumps([[2, 7, 11, 15], 9]),
            sample_output=json.dumps([0, 1]),
            constraints="""2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9
Only one valid answer exists.""",
            problem_type='function',
            created_by=teacher.id,
            is_active=True
        )
        db.session.add(quiz1)
        db.session.flush()
        
        # Test cases for Two Sum
        two_sum_testcases = [
            {'input': [[2, 7, 11, 15], 9], 'output': [0, 1], 'is_sample': True, 'type': 'normal'},
            {'input': [[3, 2, 4], 6], 'output': [1, 2], 'is_sample': False, 'type': 'normal'},
            {'input': [[3, 3], 6], 'output': [0, 1], 'is_sample': False, 'type': 'boundary'},
            {'input': [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19], 'output': [8, 9], 'is_sample': False, 'type': 'random'},
            {'input': [[-1, -2, -3, -4, -5], -8], 'output': [2, 4], 'is_sample': False, 'type': 'boundary'},
        ]
        
        for tc in two_sum_testcases:
            testcase = Testcase(
                quiz_id=quiz1.id,
                input_data=json.dumps(tc['input']),
                expected_output=json.dumps(tc['output']),
                is_sample=tc['is_sample'],
                testcase_type=tc['type']
            )
            db.session.add(testcase)
        
        # Submissions for Two Sum
        # Student1: Passed submission
        submission1 = Submission(
            user_id=student1.id,
            quiz_id=quiz1.id,
            code="""from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []""",
            language='python',
            status='pass',
            passed_testcases=5,
            total_testcases=5,
            execution_time=0.05,
            submitted_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        db.session.add(submission1)
        
        # Student2: Failed submission (wrong algorithm)
        submission2 = Submission(
            user_id=student2.id,
            quiz_id=quiz1.id,
            code="""from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    # Wrong approach - returns first two numbers that sum to target
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []""",
            language='python',
            status='fail',
            error_type='wrong_answer',
            error_message='Failed 1 out of 5 test cases.',
            passed_testcases=4,
            total_testcases=5,
            execution_time=0.12,
            submitted_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
        db.session.add(submission2)
        
        # Quiz 2: Reverse String (with one passed submission)
        quiz2 = Quiz(
            title="Reverse String",
            description="Reverse a string in-place.",
            problem_statement="""Write a function that reverses a string. The input string is given as an array of characters s.

You must do this by modifying the input array in-place with O(1) extra memory.

Example 1:
Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]

Example 2:
Input: s = ["H","a","n","n","a","h"]
Output: ["h","a","n","n","a","H"]""",
            function_signature="def reverseString(s: List[str]) -> None:",
            sample_input=json.dumps([["h", "e", "l", "l", "o"]]),
            sample_output=json.dumps(["o", "l", "l", "e", "h"]),
            constraints="""1 <= s.length <= 10^5
s[i] is a printable ascii character.""",
            problem_type='function',
            created_by=teacher.id,
            is_active=True
        )
        db.session.add(quiz2)
        db.session.flush()
        
        # Test cases for Reverse String
        # Note: For in-place modification, we check the modified array
        reverse_testcases = [
            {'input': [["h", "e", "l", "l", "o"]], 'output': ["o", "l", "l", "e", "h"], 'is_sample': True, 'type': 'normal'},
            {'input': [["H", "a", "n", "n", "a", "h"]], 'output': ["h", "a", "n", "n", "a", "H"], 'is_sample': False, 'type': 'normal'},
            {'input': [["a"]], 'output': ["a"], 'is_sample': False, 'type': 'boundary'},
            {'input': [["A", "B", "C"]], 'output': ["C", "B", "A"], 'is_sample': False, 'type': 'random'},
        ]
        
        for tc in reverse_testcases:
            testcase = Testcase(
                quiz_id=quiz2.id,
                input_data=json.dumps(tc['input']),
                expected_output=json.dumps(tc['output']),
                is_sample=tc['is_sample'],
                testcase_type=tc['type']
            )
            db.session.add(testcase)
        
        # Submission for Reverse String (Student1 passed)
        submission3 = Submission(
            user_id=student1.id,
            quiz_id=quiz2.id,
            code="""from typing import List

def reverseString(s: List[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1""",
            language='python',
            status='pass',
            passed_testcases=4,
            total_testcases=4,
            execution_time=0.03,
            submitted_at=datetime.now(timezone.utc) - timedelta(hours=5)
        )
        db.session.add(submission3)
        
        # Quiz 3: Valid Parentheses (ready to submit - no submissions)
        quiz3 = Quiz(
            title="Valid Parentheses",
            description="Check if parentheses are valid.",
            problem_statement="""Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: True

Example 2:
Input: s = "()[]{}"
Output: True

Example 3:
Input: s = "(]"
Output: False

Example 4:
Input: s = "([)]"
Output: False

Example 5:
Input: s = "{[]}"
Output: True""",
            function_signature="def isValid(s: str) -> bool:",
            sample_input=json.dumps(["()"]),
            sample_output=json.dumps(True),
            constraints="""1 <= s.length <= 10^4
s consists of parentheses only '()[]{}'.""",
            problem_type='function',
            created_by=teacher.id,
            is_active=True
        )
        db.session.add(quiz3)
        db.session.flush()
        
        # Test cases for Valid Parentheses
        valid_paren_testcases = [
            {'input': ["()"], 'output': True, 'is_sample': True, 'type': 'normal'},
            {'input': ["()[]{}"], 'output': True, 'is_sample': False, 'type': 'normal'},
            {'input': ["(]"], 'output': False, 'is_sample': False, 'type': 'normal'},
            {'input': ["([)]"], 'output': False, 'is_sample': False, 'type': 'normal'},
            {'input': ["{[]}"], 'output': True, 'is_sample': False, 'type': 'normal'},
            {'input': ["["], 'output': False, 'is_sample': False, 'type': 'boundary'},
        ]
        
        for tc in valid_paren_testcases:
            testcase = Testcase(
                quiz_id=quiz3.id,
                input_data=json.dumps(tc['input']),
                expected_output=json.dumps(tc['output']),
                is_sample=tc['is_sample'],
                testcase_type=tc['type']
            )
            db.session.add(testcase)
        
        # Quiz 4: Maximum Subarray (ready to submit - no submissions)
        quiz4 = Quiz(
            title="Maximum Subarray",
            description="Find the maximum sum of a contiguous subarray.",
            problem_statement="""Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.

Example 2:
Input: nums = [1]
Output: 1

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23""",
            function_signature="def maxSubArray(nums: List[int]) -> int:",
            sample_input=json.dumps([[-2, 1, -3, 4, -1, 2, 1, -5, 4]]),
            sample_output=json.dumps(6),
            constraints="""1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4""",
            problem_type='function',
            created_by=teacher.id,
            is_active=True
        )
        db.session.add(quiz4)
        db.session.flush()
        
        # Test cases for Maximum Subarray
        max_subarray_testcases = [
            {'input': [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], 'output': 6, 'is_sample': True, 'type': 'normal'},
            {'input': [[1]], 'output': 1, 'is_sample': False, 'type': 'boundary'},
            {'input': [[5, 4, -1, 7, 8]], 'output': 23, 'is_sample': False, 'type': 'normal'},
            {'input': [[-1]], 'output': -1, 'is_sample': False, 'type': 'boundary'},
            {'input': [[-2, -1]], 'output': -1, 'is_sample': False, 'type': 'boundary'},
        ]
        
        for tc in max_subarray_testcases:
            testcase = Testcase(
                quiz_id=quiz4.id,
                input_data=json.dumps(tc['input']),
                expected_output=json.dumps(tc['output']),
                is_sample=tc['is_sample'],
                testcase_type=tc['type']
            )
            db.session.add(testcase)
        
        # Quiz 5: Contains Duplicate (with failed submission)
        quiz5 = Quiz(
            title="Contains Duplicate",
            description="Check if array contains duplicates.",
            problem_statement="""Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Example 1:
Input: nums = [1,2,3,1]
Output: True

Example 2:
Input: nums = [1,2,3,4]
Output: False

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: True""",
            function_signature="def containsDuplicate(nums: List[int]) -> bool:",
            sample_input=json.dumps([[1, 2, 3, 1]]),
            sample_output=json.dumps(True),
            constraints="""1 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9""",
            problem_type='function',
            created_by=teacher.id,
            is_active=True
        )
        db.session.add(quiz5)
        db.session.flush()
        
        # Test cases for Contains Duplicate
        duplicate_testcases = [
            {'input': [[1, 2, 3, 1]], 'output': True, 'is_sample': True, 'type': 'normal'},
            {'input': [[1, 2, 3, 4]], 'output': False, 'is_sample': False, 'type': 'normal'},
            {'input': [[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]], 'output': True, 'is_sample': False, 'type': 'normal'},
            {'input': [[1]], 'output': False, 'is_sample': False, 'type': 'boundary'},
        ]
        
        for tc in duplicate_testcases:
            testcase = Testcase(
                quiz_id=quiz5.id,
                input_data=json.dumps(tc['input']),
                expected_output=json.dumps(tc['output']),
                is_sample=tc['is_sample'],
                testcase_type=tc['type']
            )
            db.session.add(testcase)
        
        # Submission for Contains Duplicate (Student2 failed - runtime error)
        submission4 = Submission(
            user_id=student2.id,
            quiz_id=quiz5.id,
            code="""from typing import List

def containsDuplicate(nums: List[int]) -> bool:
    # Runtime error - accessing index out of range
    for i in range(len(nums)):
        if nums[i] == nums[i+1]:
            return True
    return False""",
            language='python',
            status='fail',
            error_type='runtime_error',
            error_message='Runtime Error: list index out of range',
            passed_testcases=0,
            total_testcases=4,
            execution_time=0.01,
            submitted_at=datetime.now(timezone.utc) - timedelta(hours=3)
        )
        db.session.add(submission4)
        
        # Quiz 6: Best Time to Buy and Sell Stock (ready to submit)
        quiz6 = Quiz(
            title="Best Time to Buy and Sell Stock",
            description="Find maximum profit from buying and selling stock.",
            problem_statement="""You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.""",
            function_signature="def maxProfit(prices: List[int]) -> int:",
            sample_input=json.dumps([[7, 1, 5, 3, 6, 4]]),
            sample_output=json.dumps(5),
            constraints="""1 <= prices.length <= 10^5
0 <= prices[i] <= 10^4""",
            problem_type='function',
            created_by=teacher.id,
            is_active=True
        )
        db.session.add(quiz6)
        db.session.flush()
        
        # Test cases for Best Time to Buy and Sell Stock
        stock_testcases = [
            {'input': [[7, 1, 5, 3, 6, 4]], 'output': 5, 'is_sample': True, 'type': 'normal'},
            {'input': [[7, 6, 4, 3, 1]], 'output': 0, 'is_sample': False, 'type': 'normal'},
            {'input': [[1, 2]], 'output': 1, 'is_sample': False, 'type': 'boundary'},
            {'input': [[2, 4, 1]], 'output': 2, 'is_sample': False, 'type': 'normal'},
        ]
        
        for tc in stock_testcases:
            testcase = Testcase(
                quiz_id=quiz6.id,
                input_data=json.dumps(tc['input']),
                expected_output=json.dumps(tc['output']),
                is_sample=tc['is_sample'],
                testcase_type=tc['type']
            )
            db.session.add(testcase)
        
        # Commit all changes
        db.session.commit()
        
        print(f"Created {6} quizzes:")
        print("  1. Two Sum (2 submissions: 1 passed, 1 failed)")
        print("  2. Reverse String (1 submission: passed)")
        print("  3. Valid Parentheses (ready to submit)")
        print("  4. Maximum Subarray (ready to submit)")
        print("  5. Contains Duplicate (1 submission: failed)")
        print("  6. Best Time to Buy and Sell Stock (ready to submit)")
        print(f"\nCreated {4} submissions total")
        print("\nYou can now login as a student to see:")
        print("  - Quizzes with existing submissions (with status)")
        print("  - Quizzes ready to submit (no submissions yet)")

if __name__ == '__main__':
    seed_sample_data()

