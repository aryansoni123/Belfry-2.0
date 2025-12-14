# How to Create a Quiz in Belfry

## Current System Behavior

The system automatically generates test cases based on:
1. **Problem Statement** - Detects problem type (array, string, number, generic)
2. **Constraints** - Extracts number ranges (e.g., "1 <= N <= 100")
3. **Sample Input/Output** - Used as the sample test case (visible to students)

**Important Note**: Auto-generated test cases will have placeholder expected outputs. For best results, provide accurate sample input/output, and the system will use that as the sample test case.

---

## Example: Two Sum Problem

### Step-by-Step Guide

#### 1. **Quiz Title**
```
Two Sum
```

#### 2. **Description** (Optional but recommended)
```
Find two numbers in an array that add up to a target value.
```

#### 3. **Problem Statement** (Required)
```
Given an array of integers and a target value, find two distinct indices such that the values at those indices sum to the target.

Input Format:
- First line contains an integer N (size of array)
- Second line contains N space-separated integers (the array)
- Third line contains an integer T (target value)

Output Format:
- Print two space-separated integers representing the indices (0-indexed)
- If no solution exists, print "No solution"

Example:
If array is [2, 7, 11, 15] and target is 9, the answer is indices 0 and 1 because nums[0] + nums[1] = 2 + 7 = 9.
```

#### 4. **Constraints** (Important for test case generation)
```
2 <= N <= 1000
-10^9 <= arr[i] <= 10^9
-10^9 <= T <= 10^9
```

#### 5. **Sample Input** (Critical - This becomes the sample test case)
```
4
2 7 11 15
9
```

#### 6. **Sample Output** (Critical - Must match exactly)
```
0 1
```

---

## What Happens When You Create the Quiz

1. **Sample Test Case**: The sample input/output you provide becomes the sample test case (visible to students)

2. **Auto-Generated Test Cases**: The system will generate additional test cases:
   - Boundary cases (small arrays, edge values)
   - Normal cases (medium arrays)
   - Random cases (larger arrays)
   
   **Note**: Auto-generated test cases will have placeholder expected outputs. You may need to:
   - Manually edit them after creation, OR
   - Provide a reference solution (future enhancement)

---

## Complete Two Sum Example

Here's the complete form data:

**Title**: `Two Sum`

**Description**: `Find two numbers in an array that add up to a target value.`

**Problem Statement**:
```
Given an array of integers and a target value, find two distinct indices such that the values at those indices sum to the target.

Input Format:
- First line: integer N (array size)
- Second line: N space-separated integers
- Third line: integer T (target value)

Output Format:
- Two space-separated integers (indices, 0-indexed)
- Print "No solution" if no pair exists

Example:
Array: [2, 7, 11, 15], Target: 9
Output: 0 1
Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

**Constraints**:
```
2 <= N <= 1000
-10^9 <= arr[i] <= 10^9
-10^9 <= T <= 10^9
```

**Sample Input**:
```
4
2 7 11 15
9
```

**Sample Output**:
```
0 1
```

---

## Expected Student Solution Format

Students should write code that reads input in this format:

```python
n = int(input())
arr = list(map(int, input().split()))
target = int(input())

# Solution logic here
# Find two indices i, j such that arr[i] + arr[j] == target

# Output
print(i, j)  # or "No solution"
```

---

## Tips for Creating Quizzes

1. **Always provide Sample Input/Output**: This is the most important field - it becomes the sample test case students can test against

2. **Be specific with Constraints**: The system uses constraints to generate appropriate test case ranges

3. **Use clear Problem Statement**: Include input/output format clearly so students know what to expect

4. **Test your sample**: Make sure your sample input/output is correct - students will use it to test their code

5. **Review generated test cases**: After creation, view the quiz and check the auto-generated test cases. You may need to manually correct expected outputs for complex problems.

---

## After Creating the Quiz

1. Go to "View Quiz" to see all generated test cases
2. Check if auto-generated test cases have correct expected outputs
3. If needed, you can manually edit test cases or regenerate them
4. The sample test case (from your Sample Input/Output) will be visible to students
5. Hidden test cases are used for final evaluation

---

## Current Limitations

- Auto-generated test cases use placeholder expected outputs
- For complex problems, you may need to manually verify/correct test cases
- The system works best when you provide accurate sample input/output

