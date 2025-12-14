# Sample Data Summary

This document describes the sample quizzes and submissions that have been seeded into Belfry.

## How to Use

Run the seed script to populate the database:

```bash
python seed_sample_data.py
```

**Note:** This script will recreate the database, so any existing data will be lost. It also creates default users if they don't exist.

## Created Quizzes

### 1. Two Sum ✅ (Has Submissions)
- **Status**: 2 submissions (1 passed, 1 failed)
- **Student1**: ✅ Passed (5/5 test cases)
- **Student2**: ❌ Failed (4/5 test cases - wrong answer)

**Function Signature:**
```python
def twoSum(nums: List[int], target: int) -> List[int]:
```

**Sample Test Case:**
- Input: `[[2, 7, 11, 15], 9]`
- Output: `[0, 1]`

---

### 2. Reverse String ✅ (Has Submission)
- **Status**: 1 submission (passed)
- **Student1**: ✅ Passed (4/4 test cases)

**Function Signature:**
```python
def reverseString(s: List[str]) -> None:
```

**Sample Test Case:**
- Input: `[["h", "e", "l", "l", "o"]]`
- Output: `["o", "l", "l", "e", "h"]`

---

### 3. Valid Parentheses 📝 (Ready to Submit)
- **Status**: No submissions yet
- **Ready for students to attempt**

**Function Signature:**
```python
def isValid(s: str) -> bool:
```

**Sample Test Case:**
- Input: `["()"]`
- Output: `true`

---

### 4. Maximum Subarray 📝 (Ready to Submit)
- **Status**: No submissions yet
- **Ready for students to attempt**

**Function Signature:**
```python
def maxSubArray(nums: List[int]) -> int:
```

**Sample Test Case:**
- Input: `[[-2, 1, -3, 4, -1, 2, 1, -5, 4]]`
- Output: `6`

---

### 5. Contains Duplicate ❌ (Has Failed Submission)
- **Status**: 1 submission (failed)
- **Student2**: ❌ Failed (runtime error - index out of range)

**Function Signature:**
```python
def containsDuplicate(nums: List[int]) -> bool:
```

**Sample Test Case:**
- Input: `[[1, 2, 3, 1]]`
- Output: `true`

---

### 6. Best Time to Buy and Sell Stock 📝 (Ready to Submit)
- **Status**: No submissions yet
- **Ready for students to attempt**

**Function Signature:**
```python
def maxProfit(prices: List[int]) -> int:
```

**Sample Test Case:**
- Input: `[[7, 1, 5, 3, 6, 4]]`
- Output: `5`

---

## Submission Statistics

- **Total Quizzes**: 6
- **Quizzes with Submissions**: 3
- **Quizzes Ready to Submit**: 3
- **Total Submissions**: 4
  - ✅ Passed: 2
  - ❌ Failed: 2

## Test Cases

Each quiz has:
- **1 sample test case** (visible to students)
- **3-4 hidden test cases** (used for evaluation)

Test case types:
- **Normal**: Standard test cases
- **Boundary**: Edge cases (single element, min/max values)
- **Random**: Larger or varied inputs

## Student Dashboard View

When students log in, they will see:

1. **Two Sum** - Status: "Passed" (for student1) or "Failed" (for student2)
2. **Reverse String** - Status: "Passed" (for student1)
3. **Valid Parentheses** - Status: "Not Attempted"
4. **Maximum Subarray** - Status: "Not Attempted"
5. **Contains Duplicate** - Status: "Failed" (for student2)
6. **Best Time to Buy and Sell Stock** - Status: "Not Attempted"

## Default Accounts

The seed script creates these accounts if they don't exist:

- **Teacher**: username=`teacher`, password=`teacher123`
- **Student1**: username=`student`, password=`student123`
- **Student2**: username=`student2`, password=`student123`

## Notes

- All quizzes are **function-based** (LeetCode-style)
- Test cases use **JSON format** for input/output
- Submissions include execution time and error details
- Failed submissions show error type (runtime_error, wrong_answer, etc.)

## Resetting Sample Data

To reset and regenerate sample data:

```bash
python seed_sample_data.py
```

This will:
1. Drop all existing tables
2. Recreate database with latest schema
3. Create default users
4. Create all sample quizzes and submissions

