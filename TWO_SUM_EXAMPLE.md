# Two Sum Problem - Complete Example for Belfry

## How to Create the Two Sum Quiz

### Step 1: Fill in the Create Quiz Form

**Problem Type:**
```
Function-based (LeetCode-style)
```

**Function Signature:**
```
def twoSum(nums: List[int], target: int) -> List[int]:
```

**Title:**
```
Two Sum
```

**Description:**
```
Find two numbers in an array that add up to a target value.
```

**Problem Statement:**
```
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

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
Output: [0,1]
```

**Constraints:**
```
2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9
Only one valid answer exists.
```

**Sample Input (JSON format):**
```
[[2,7,11,15], 9]
```

**Sample Output (JSON format):**
```
[0, 1]
```

---

## What Happens After Creation

1. **Sample Test Case**: Your sample input/output becomes the sample test case (visible to students)

2. **Auto-Generated Test Cases**: The system generates additional test cases:
   - `[[3, 2, 4], 6]` → `[1, 2]`
   - `[[3, 3], 6]` → `[0, 1]`
   - `[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19]` → `[8, 9]`

3. **All test cases are stored** with JSON input/output format

---

## Student Solution Format

Students should write code like this:

```python
from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    # Create a dictionary to store value -> index mapping
    num_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []  # Should not reach here per problem constraints
```

**Important Notes for Students:**
- They must implement the exact function signature provided
- They should NOT change the function name or parameters
- They should NOT add a main block or print statements
- The function should return the result (not print it)
- The system will call their function with test case inputs

---

## Execution Flow (LeetCode-Style)

1. **Student writes code** implementing the function

2. **Student clicks "Run"**:
   - Code is executed against sample test cases only
   - Results shown immediately
   - No submission saved

3. **Student clicks "Submit"**:
   - Code is executed against ALL test cases (including hidden ones)
   - Each test case runs in isolated Docker container
   - Results: PASS (all pass) or FAIL (any fail)
   - Submission saved to database

---

## Test Case Format

Each test case is stored as:

**Input Data (JSON):**
```json
[[2,7,11,15], 9]
```

**Expected Output (JSON):**
```json
[0, 1]
```

The system:
1. Parses the JSON input
2. Calls `twoSum([2,7,11,15], 9)`
3. Compares the returned value with `[0, 1]`
4. Returns PASS if they match exactly, FAIL otherwise

---

## Verification

After creating the quiz, you can:
1. View the quiz to see all generated test cases
2. Manually verify/correct test case expected outputs if needed
3. Test the quiz yourself by solving it as a student

---

## Key Points

✅ **Function-based**: Students implement functions, not stdin programs
✅ **JSON format**: Input/output stored as JSON strings
✅ **Strict comparison**: Results must match exactly
✅ **No partial marking**: All test cases must pass for PASS
✅ **Docker isolation**: Each execution runs in isolated container
✅ **Hidden test cases**: Students only see sample test cases

