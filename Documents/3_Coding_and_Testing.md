# Coding and Testing

## Overview of Coding Standards and Structure

The Belfry project adheres to Python PEP 8 coding standards with consistent naming conventions, proper indentation, and comprehensive docstrings. Code organization follows Flask best practices with modular blueprints, separation of concerns, and clear interface definitions. Each module maintains a single responsibility, enabling independent testing and modification.

Function and class definitions include comprehensive docstrings describing purpose, parameters, return values, and exceptions. Error handling follows Python exception hierarchy with appropriate error messages. Code comments explain complex logic and design decisions. Type hints are used where appropriate to improve code clarity and enable static analysis tools.

## Major Modules and Responsibilities

The app.py module serves as the application entry point, initializing Flask, database connections, and login management. It registers blueprints and defines the root route that redirects users to appropriate dashboards. The module ensures proper initialization order, with database setup preceding model imports to avoid circular dependencies.

The models.py module defines SQLAlchemy database models for User, Quiz, Testcase, and Submission entities. Each model includes appropriate field types, constraints, and relationships. The User model extends Flask-Login's UserMixin for authentication integration. Relationships use lazy loading for efficiency, with cascade deletion where appropriate to maintain referential integrity.

The judge.py module implements the OnlineJudge class, which handles secure code execution in Docker containers. The execute_submission method orchestrates the evaluation process, checking syntax, executing test cases sequentially, and aggregating results. The _execute_testcase method manages individual test case execution, including container creation, code execution, and result comparison. The _create_driver_code method generates wrapper code that integrates user code with test case execution logic.

The testcase_generator.py module provides automated test case generation capabilities. The generate_function_testcases function creates test cases for function-based problems by parsing function signatures, extracting data types, and generating appropriate inputs. The module includes constraint parsing to extract number ranges and data type information from problem statements.

The auth/routes.py module handles user authentication, including login, logout, and registration. The login route validates credentials and creates user sessions. The logout route clears session data. Registration is handled through the init_db.py script for initial setup, with potential for future user self-registration.

The teacher/routes.py module provides quiz management functionality. The create_quiz route handles quiz creation with test case generation. The edit_quiz route allows modification of existing quizzes. The view_quiz route displays quiz details and associated test cases. The regenerate_testcases route allows teachers to recreate test cases with updated constraints.

The student/routes.py module handles student interactions. The dashboard route displays available quizzes with submission status. The solve_quiz route presents the problem interface with code editor. The run_code route executes code against sample test cases for immediate feedback. The submit route evaluates code against all test cases and stores submission results.

## Testing Strategy

The testing strategy employs multiple levels of verification: unit testing for individual functions, integration testing for component interactions, and system testing for end-to-end workflows. Test cases cover normal operation, boundary conditions, error handling, and security scenarios. Manual testing validates user interface functionality and user experience.

Unit tests verify individual functions including test case generation, result comparison, and driver code creation. Integration tests verify interactions between modules, such as quiz creation triggering test case generation, and code submission invoking the execution engine. System tests verify complete workflows from quiz creation through student submission and evaluation.

## Test Case Table

| Test Case ID | Description | Input | Expected Output | Actual Output | Status |
|--------------|------------|-------|-----------------|---------------|--------|
| TC001 | User login with valid credentials | Username: teacher, Password: teacher123 | Redirect to teacher dashboard | Redirect to teacher dashboard | Pass |
| TC002 | User login with invalid credentials | Username: teacher, Password: wrongpass | Error message displayed | Error message displayed | Pass |
| TC003 | Create quiz with function signature | Title: Two Sum, Function: def twoSum(nums, target) | Quiz created with test cases | Quiz created with test cases | Pass |
| TC004 | Create quiz without required fields | Title: empty, Problem statement: empty | Validation error displayed | Validation error displayed | Pass |
| TC005 | Submit correct solution | Code implementing twoSum correctly | Status: pass, All test cases passed | Status: pass, All test cases passed | Pass |
| TC006 | Submit incorrect solution | Code with logic error | Status: fail, Test case failure reported | Status: fail, Test case failure reported | Pass |
| TC007 | Submit code with syntax error | Code with invalid Python syntax | Syntax error message displayed | Syntax error message displayed | Pass |
| TC008 | Submit code exceeding timeout | Code with infinite loop | Timeout error reported | Timeout error reported | Pass |
| TC009 | Run code against sample test cases | Code submitted via Run button | Results for sample cases only | Results for sample cases only | Pass |
| TC010 | View submission history | Access My Submissions page | List of previous submissions displayed | List of previous submissions displayed | Pass |
| TC011 | Teacher views quiz statistics | Access quiz view page | Submission counts and statistics displayed | Submission counts and statistics displayed | Pass |
| TC012 | Regenerate test cases | Click regenerate button | New test cases created, old ones deleted | New test cases created, old ones deleted | Pass |
| TC013 | Edit existing quiz | Modify quiz title and description | Changes saved to database | Changes saved to database | Pass |
| TC014 | Access protected route without login | Navigate to dashboard | Redirect to login page | Redirect to login page | Pass |
| TC015 | Student accesses teacher route | Student tries to access create_quiz | Access denied message | Access denied message | Pass |
| TC016 | Execute code with memory limit exceeded | Code allocating excessive memory | Memory limit error or container termination | Container terminated, error reported | Pass |
| TC017 | Execute code with network access attempt | Code using socket or urllib | Network error or blocked execution | Network access blocked | Pass |
| TC018 | Test case generation for array problem | Problem with array constraints | Array test cases generated | Array test cases generated | Pass |
| TC019 | Test case generation for string problem | Problem with string constraints | String test cases generated | String test cases generated | Pass |
| TC020 | Compare results with list output | Function returning list [1,2,3] | Exact match required | Exact match verified | Pass |

## Bugs and Issues Identified

During development, several bugs were identified and resolved. An initial issue involved incorrect result comparison where valid output was incorrectly flagged as runtime errors. The fix involved prioritizing output correctness checking over error status, ensuring that correct JSON output is accepted even if stderr contains warnings.

Another issue involved test case execution continuing after the first failure, which violated the requirement that all test cases must pass. The fix implemented early termination, stopping execution immediately upon the first test case failure and marking the submission as failed.

Container cleanup issues were identified where containers were not always properly removed after execution, leading to resource accumulation. The fix implemented comprehensive cleanup in finally blocks, ensuring containers are removed even when errors occur.

A bug in driver code generation caused incorrect handling of in-place list modifications, where functions modifying input lists returned None. The fix added logic to detect in-place modifications and return the modified input when the function returns None.

## Fixes Applied

The output correctness priority fix modified the _execute_testcase method to check output correctness before checking error status. This ensures that correct solutions are not incorrectly marked as failures due to warning messages in stderr. The comparison logic was moved earlier in the execution flow, before error checking.

The early termination fix modified the execute_submission method to break immediately upon encountering a failed test case. Remaining test cases are marked as not executed, and the submission status is set to fail. This ensures consistent behavior with the requirement that all test cases must pass.

The container cleanup fix added comprehensive error handling in finally blocks throughout the execution engine. Containers are stopped and removed even when exceptions occur, preventing resource leaks. Temporary directories are also cleaned up in finally blocks to ensure filesystem hygiene.

The in-place modification fix enhanced the driver code generation to detect when functions modify input lists in place. When a function returns None and the first argument is a list, the driver code returns the modified list instead of None. This handles common patterns like list sorting and in-place array modifications.

## Re-testing Results

After applying fixes, all test cases were re-executed to verify resolution. The output correctness fix was verified by testing solutions that produce correct output but generate warning messages. All such cases now correctly pass evaluation.

The early termination fix was verified by submitting code that fails on the second test case. Execution correctly stops after the first failure, and the submission is marked as failed with appropriate error information. Remaining test cases are marked as not executed.

The container cleanup fix was verified through extended testing sessions with multiple submissions. No container accumulation was observed, and system resources remained stable. The in-place modification fix was verified by testing functions that modify input lists, ensuring correct evaluation of such solutions.

## Important Code Snippets

The driver code generation snippet demonstrates how user code is integrated with test case execution. The code imports necessary modules, includes the user's solution, parses JSON input, calls the user's function with appropriate argument handling, and serializes the result to JSON for output. This approach enables function-based evaluation similar to LeetCode.

The result comparison snippet implements strict equality checking for complex data types. The _compare_results method recursively compares lists and dictionaries, ensuring that order matters for lists and that dictionary keys match exactly. This strict comparison ensures accurate evaluation of solutions.

The Docker container execution snippet demonstrates resource limit configuration. Containers are created with memory limits, CPU quotas, and network restrictions. The timeout mechanism ensures containers are terminated if execution exceeds the time limit. This configuration provides security while maintaining reasonable performance.

The test case generation snippet shows constraint parsing from problem statements. Regular expressions extract number ranges and data type information, which are then used to generate appropriate test cases. The generator creates normal, boundary, and random test cases to provide comprehensive coverage.

## Verification and Validation

Code verification involved static analysis using Python linters to identify potential issues and ensure code quality. Dynamic testing verified functionality through execution of test cases covering normal operation and error conditions. Code reviews ensured adherence to coding standards and identified potential improvements.

Validation confirmed that the system meets specified requirements: secure code execution, accurate evaluation, role-based access control, and intuitive user interfaces. Performance testing verified that the system handles multiple concurrent submissions without degradation. Security testing confirmed that code execution is properly isolated and resource limits are enforced.

The testing process demonstrated that the system reliably evaluates code submissions, correctly identifies syntax errors and runtime errors, and accurately compares results. The system successfully handles edge cases including timeout scenarios, memory limits, and various data types. User interface testing confirmed that all features are accessible and functional for both teachers and students.

