"""
Safe script to restore quizzes WITHOUT dropping the database.
Only adds quizzes if they don't already exist.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Quiz, Testcase, Submission, User
from config import Config
from testcase_generator import TestcaseGenerator, generate_function_testcases
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta
import json

# Create app without importing routes
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def restore_quizzes_safe():
    """Restore quizzes without dropping database."""
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        # Create users if they don't exist
        if not User.query.filter_by(username='teacher').first():
            teacher = User(
                username='teacher',
                email='teacher@belfry.edu',
                password_hash=generate_password_hash('teacher123'),
                role='teacher'
            )
            db.session.add(teacher)
            print("Created teacher user")
        
        if not User.query.filter_by(username='student').first():
            student1 = User(
                username='student',
                email='student@belfry.edu',
                password_hash=generate_password_hash('student123'),
                role='student'
            )
            db.session.add(student1)
            print("Created student user")
        
        if not User.query.filter_by(username='student2').first():
            student2 = User(
                username='student2',
                email='student2@belfry.edu',
                password_hash=generate_password_hash('student123'),
                role='student'
            )
            db.session.add(student2)
            print("Created student2 user")
        
        db.session.commit()
        
        # Get teacher
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            print("ERROR: Could not find or create teacher user")
            return
        
        # Check existing quizzes
        existing_titles = {q.title for q in Quiz.query.all()}
        print(f"\nExisting quizzes: {len(existing_titles)}")
        for title in existing_titles:
            print(f"  - {title}")
        
        # Quiz 1: Two Sum
        if 'Two Sum' not in existing_titles:
            print("\nCreating: Two Sum")
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
            
            # Generate test cases
            testcases = generate_function_testcases(
                function_signature=quiz1.function_signature,
                sample_input=quiz1.sample_input,
                sample_output=quiz1.sample_output,
                constraints=quiz1.constraints
            )
            
            # Add test cases in batches
            batch_size = 100
            for i in range(0, len(testcases), batch_size):
                batch = testcases[i:i+batch_size]
                for tc in batch:
                    testcase = Testcase(
                        quiz_id=quiz1.id,
                        input_data=tc['input_data'],
                        expected_output=tc['expected_output'],
                        is_sample=tc['is_sample'],
                        testcase_type=tc['testcase_type']
                    )
                    db.session.add(testcase)
                db.session.flush()
            
            print(f"  Created with {len(testcases)} test cases")
        
        # Quiz 2: Reverse String
        if 'Reverse String' not in existing_titles:
            print("\nCreating: Reverse String")
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
            
            testcases = generate_function_testcases(
                function_signature=quiz2.function_signature,
                sample_input=quiz2.sample_input,
                sample_output=quiz2.sample_output,
                constraints=quiz2.constraints
            )
            
            batch_size = 100
            for i in range(0, len(testcases), batch_size):
                batch = testcases[i:i+batch_size]
                for tc in batch:
                    testcase = Testcase(
                        quiz_id=quiz2.id,
                        input_data=tc['input_data'],
                        expected_output=tc['expected_output'],
                        is_sample=tc['is_sample'],
                        testcase_type=tc['testcase_type']
                    )
                    db.session.add(testcase)
                db.session.flush()
            
            print(f"  Created with {len(testcases)} test cases")
        
        # Quiz 3: Valid Parentheses
        if 'Valid Parentheses' not in existing_titles:
            print("\nCreating: Valid Parentheses")
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
            
            testcases = generate_function_testcases(
                function_signature=quiz3.function_signature,
                sample_input=quiz3.sample_input,
                sample_output=quiz3.sample_output,
                constraints=quiz3.constraints
            )
            
            batch_size = 100
            for i in range(0, len(testcases), batch_size):
                batch = testcases[i:i+batch_size]
                for tc in batch:
                    testcase = Testcase(
                        quiz_id=quiz3.id,
                        input_data=tc['input_data'],
                        expected_output=tc['expected_output'],
                        is_sample=tc['is_sample'],
                        testcase_type=tc['testcase_type']
                    )
                    db.session.add(testcase)
                db.session.flush()
            
            print(f"  Created with {len(testcases)} test cases")
        
        # Quiz 4: Maximum Subarray
        if 'Maximum Subarray' not in existing_titles:
            print("\nCreating: Maximum Subarray")
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
            
            testcases = generate_function_testcases(
                function_signature=quiz4.function_signature,
                sample_input=quiz4.sample_input,
                sample_output=quiz4.sample_output,
                constraints=quiz4.constraints
            )
            
            batch_size = 100
            for i in range(0, len(testcases), batch_size):
                batch = testcases[i:i+batch_size]
                for tc in batch:
                    testcase = Testcase(
                        quiz_id=quiz4.id,
                        input_data=tc['input_data'],
                        expected_output=tc['expected_output'],
                        is_sample=tc['is_sample'],
                        testcase_type=tc['testcase_type']
                    )
                    db.session.add(testcase)
                db.session.flush()
            
            print(f"  Created with {len(testcases)} test cases")
        
        # Quiz 5: Contains Duplicate
        if 'Contains Duplicate' not in existing_titles:
            print("\nCreating: Contains Duplicate")
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
            
            testcases = generate_function_testcases(
                function_signature=quiz5.function_signature,
                sample_input=quiz5.sample_input,
                sample_output=quiz5.sample_output,
                constraints=quiz5.constraints
            )
            
            batch_size = 100
            for i in range(0, len(testcases), batch_size):
                batch = testcases[i:i+batch_size]
                for tc in batch:
                    testcase = Testcase(
                        quiz_id=quiz5.id,
                        input_data=tc['input_data'],
                        expected_output=tc['expected_output'],
                        is_sample=tc['is_sample'],
                        testcase_type=tc['testcase_type']
                    )
                    db.session.add(testcase)
                db.session.flush()
            
            print(f"  Created with {len(testcases)} test cases")
        
        # Quiz 6: Best Time to Buy and Sell Stock
        if 'Best Time to Buy and Sell Stock' not in existing_titles:
            print("\nCreating: Best Time to Buy and Sell Stock")
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
            
            testcases = generate_function_testcases(
                function_signature=quiz6.function_signature,
                sample_input=quiz6.sample_input,
                sample_output=quiz6.sample_output,
                constraints=quiz6.constraints
            )
            
            batch_size = 100
            for i in range(0, len(testcases), batch_size):
                batch = testcases[i:i+batch_size]
                for tc in batch:
                    testcase = Testcase(
                        quiz_id=quiz6.id,
                        input_data=tc['input_data'],
                        expected_output=tc['expected_output'],
                        is_sample=tc['is_sample'],
                        testcase_type=tc['testcase_type']
                    )
                    db.session.add(testcase)
                db.session.flush()
            
            print(f"  Created with {len(testcases)} test cases")
        
        db.session.commit()
        
        # Final summary
        all_quizzes = Quiz.query.all()
        print(f"\n=== Summary ===")
        print(f"Total quizzes: {len(all_quizzes)}")
        for quiz in all_quizzes:
            tc_count = Testcase.query.filter_by(quiz_id=quiz.id).count()
            print(f"  - {quiz.title}: {tc_count} test cases (Active: {quiz.is_active})")

if __name__ == '__main__':
    restore_quizzes_safe()

