# Test Case Generation - Automatic 500+ Test Cases

## Overview

Belfry automatically generates **at least 500 test cases** for every quiz when it is created. This happens automatically - no manual intervention required!

## How It Works

### Automatic Generation

When a teacher creates a new quiz:

1. **Quiz is created** with problem details
2. **Test case generator automatically runs** (no script needed!)
3. **500+ test cases are generated** based on:
   - Problem type (function-based or stdin-based)
   - Function signature (for function-based problems)
   - Sample input/output
   - Constraints
4. **Test cases are saved** to the database

### Test Case Distribution

Each quiz gets **at least 500 test cases** distributed as:

- **50 Boundary Cases**: Edge cases, minimum/maximum values, small inputs
- **350 Normal Cases**: Standard test cases with typical inputs
- **100 Random Cases**: Large inputs, varied data, stress tests
- **1 Sample Case**: The sample input/output provided by teacher (visible to students)

**Total: 501+ test cases per quiz**

## Test Case Types

### For Function-Based Problems (LeetCode-Style)

**Example: Two Sum**

The generator creates 500+ test cases with:
- Different array sizes (from minimum to maximum per constraints)
- Various target values
- Edge cases (duplicates, negative numbers, large arrays)
- Random combinations

**Distribution:**
- 50 boundary cases (small arrays, edge values)
- 300 normal cases (typical sizes)
- 100 large array cases (maximum sizes)
- 50 special edge cases (duplicates, negatives)

### For Stdin-Based Problems (Legacy)

**Example: Array Sum**

The generator creates 500+ test cases with:
- Different array sizes
- Various element values
- Edge cases (single element, large arrays)

**Distribution:**
- 50 boundary cases
- 350 normal cases
- 100 random cases

## Constraints Parsing

The generator intelligently parses constraints to generate appropriate test cases:

**Example Constraints:**
```
2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
```

The generator will:
- Create arrays with sizes from 2 to 10,000
- Use values from -10^9 to 10^9
- Generate boundary cases at min/max values

## Performance

- **Generation Time**: ~1-3 seconds for 500+ test cases
- **Database Storage**: Test cases are saved in batches (100 at a time) for efficiency
- **Memory Usage**: Optimized to handle large test case sets

## Verification

After creating a quiz, you can verify test case generation:

1. Go to Teacher Dashboard
2. Click "View" on the quiz
3. Check the test cases count (should show 500+)

## Manual Regeneration

If you need to regenerate test cases:

1. Edit the quiz
2. The system will regenerate test cases based on current problem details
3. Old test cases are replaced with new ones

## Technical Details

### Code Location

- **Generator**: `testcase_generator.py`
- **Auto-trigger**: `teacher/routes.py` (in `create_quiz()` function)

### Generation Functions

- `generate_function_testcases()`: For function-based problems
- `TestcaseGenerator.generate_testcases()`: For stdin-based problems
- `_generate_two_sum_testcases()`: Specialized for array problems
- `_generate_generic_function_testcases()`: Generic function problems

### Batch Processing

Test cases are saved in batches of 100 to:
- Prevent memory issues
- Improve database performance
- Allow progress tracking

## Example: Creating a Quiz

1. Teacher fills quiz form:
   - Title: "Two Sum"
   - Function Signature: `def twoSum(nums: List[int], target: int) -> List[int]:`
   - Sample Input: `[[2,7,11,15], 9]`
   - Sample Output: `[0, 1]`
   - Constraints: `2 <= nums.length <= 10^4`

2. Teacher clicks "Create Quiz"

3. System automatically:
   - Creates quiz record
   - Generates 500+ test cases
   - Saves all test cases to database
   - Shows success message: "Quiz created successfully with 501 test cases!"

4. Quiz is ready for students!

## Notes

- **Sample test case** (from teacher's input) is marked as `is_sample=True` (visible to students)
- **All other test cases** are marked as `is_sample=False` (hidden, used for evaluation)
- **Expected outputs** for generated test cases use placeholder logic - teachers should verify/correct if needed
- **Test case types** are categorized: `boundary`, `normal`, `random`

## Troubleshooting

**Q: Why do I only see a few test cases?**
A: Check if the quiz was created before the update. New quizzes will have 500+ test cases.

**Q: Can I manually add test cases?**
A: Yes, you can edit the quiz and add custom test cases in addition to the generated ones.

**Q: How long does generation take?**
A: Usually 1-3 seconds for 500+ test cases. Larger problems may take slightly longer.

**Q: Can I customize the number of test cases?**
A: Currently fixed at 500+ for consistency. This ensures thorough testing of student solutions.

