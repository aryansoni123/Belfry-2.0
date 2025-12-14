# Code Format Guide for Belfry

This guide explains how to write code when solving quizzes in Belfry.

## Function-Based Problems (LeetCode-Style)

Most problems in Belfry are **function-based**, meaning you implement a function that gets called by the system.

### ✅ Correct Format

**Example: Two Sum Problem**

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

### Key Points:

1. **Implement the exact function signature** provided in the problem
2. **Do NOT change** the function name or parameters
3. **Return the result** - don't print it
4. **No main block** - don't add `if __name__ == "__main__":`
5. **No input() calls** - the system calls your function
6. **No print() statements** - return the value instead

---

## Example Problems

### Example 1: Two Sum

**Function Signature:**
```python
def twoSum(nums: List[int], target: int) -> List[int]:
```

**Your Solution:**
```python
from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
```

**❌ WRONG:**
```python
# Don't do this!
def twoSum(nums: List[int], target: int) -> List[int]:
    result = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                result = [i, j]
                print(result)  # ❌ Don't print!
                return result
    return result

# ❌ Don't add main block!
if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    print(twoSum(nums, target))
```

---

### Example 2: Reverse String (In-Place)

**Function Signature:**
```python
def reverseString(s: List[str]) -> None:
```

**Your Solution:**
```python
from typing import List

def reverseString(s: List[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

**Note:** This function modifies the list in-place and returns `None`. The system checks the modified list.

**❌ WRONG:**
```python
def reverseString(s: List[str]) -> None:
    s = s[::-1]  # ❌ This creates a new list, doesn't modify in-place!
    return s  # ❌ Should return None!
```

---

### Example 3: Valid Parentheses

**Function Signature:**
```python
def isValid(s: str) -> bool:
```

**Your Solution:**
```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return len(stack) == 0
```

**❌ WRONG:**
```python
def isValid(s: str) -> bool:
    # ❌ Don't read input!
    s = input("Enter string: ")
    
    # Your logic here...
    result = True
    
    # ❌ Don't print!
    print(result)
    return result
```

---

### Example 4: Maximum Subarray

**Function Signature:**
```python
def maxSubArray(nums: List[int]) -> int:
```

**Your Solution:**
```python
from typing import List

def maxSubArray(nums: List[int]) -> int:
    max_sum = current_sum = nums[0]
    
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

---

## Stdin-Based Problems (Legacy)

Some older problems may use stdin format. For these:

**✅ Correct Format:**
```python
# Read input
n = int(input())
arr = list(map(int, input().split()))

# Process
result = sum(arr)

# Print output
print(result)
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Adding Main Block
```python
# ❌ WRONG
def solution():
    # code here
    pass

if __name__ == "__main__":
    solution()
```

### ❌ Mistake 2: Using input() in Function-Based Problems
```python
# ❌ WRONG
def twoSum(nums: List[int], target: int) -> List[int]:
    nums = list(map(int, input().split()))  # ❌ Don't read input!
    target = int(input())  # ❌ Don't read input!
    # ...
```

### ❌ Mistake 3: Printing Instead of Returning
```python
# ❌ WRONG
def twoSum(nums: List[int], target: int) -> List[int]:
    result = [0, 1]
    print(result)  # ❌ Don't print!
    return result  # ✅ This is correct
```

### ❌ Mistake 4: Changing Function Signature
```python
# ❌ WRONG - Changed parameter name
def twoSum(numbers: List[int], t: int) -> List[int]:  # ❌ Wrong parameter names!

# ✅ CORRECT - Exact signature
def twoSum(nums: List[int], target: int) -> List[int]:  # ✅ Correct!
```

### ❌ Mistake 5: Not Importing Required Types
```python
# ❌ WRONG - Missing import
def twoSum(nums, target):  # ❌ Missing type hints!

# ✅ CORRECT
from typing import List
def twoSum(nums: List[int], target: int) -> List[int]:  # ✅ Has type hints!
```

---

## Quick Checklist

Before submitting your code, make sure:

- [ ] You implemented the exact function signature provided
- [ ] You return the result (not print it)
- [ ] No `if __name__ == "__main__":` block
- [ ] No `input()` calls for function-based problems
- [ ] No `print()` statements (except for debugging, remove before submit)
- [ ] You imported required types (`from typing import List, Dict, etc.`)
- [ ] Your code handles edge cases
- [ ] You tested with the sample test cases using "Run" button

---

## Testing Your Code

1. **Use "Run" button** to test against sample test cases
2. **Check the output** - make sure it matches expected results
3. **Fix any errors** shown in the results panel
4. **Click "Submit"** only when all sample test cases pass

---

## Example: Complete Solution

**Problem:** Two Sum

**Function Signature:**
```python
def twoSum(nums: List[int], target: int) -> List[int]:
```

**Complete Solution:**
```python
from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    """
    Find two numbers in nums that add up to target.
    Return their indices.
    """
    # Create hash map: value -> index
    num_map = {}
    
    # Iterate through array
    for i, num in enumerate(nums):
        # Calculate complement
        complement = target - num
        
        # Check if complement exists in map
        if complement in num_map:
            # Found the pair!
            return [num_map[complement], i]
        
        # Store current number and its index
        num_map[num] = i
    
    # No solution found (shouldn't happen per problem constraints)
    return []
```

**That's it!** Just the function implementation. No main block, no input/output handling.

---

## Need Help?

- Check the problem statement for the exact function signature
- Look at the sample test cases to understand input/output format
- Use the "Run" button to test your code before submitting
- Read error messages carefully - they tell you what's wrong

