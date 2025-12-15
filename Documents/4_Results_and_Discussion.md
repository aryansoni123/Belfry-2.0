# Results and Discussion

## Summary of Results Obtained

The Belfry platform successfully implements a LeetCode-style online coding assessment system with secure code execution, automated test case generation, and role-based access control. The system demonstrates reliable evaluation of Python code submissions with accurate result comparison and comprehensive error handling. Testing results indicate high accuracy in identifying correct solutions, detecting syntax errors, runtime errors, and incorrect outputs.

Performance testing reveals that the system handles individual submissions efficiently, with average execution times under two seconds per test case. The Docker-based execution engine successfully isolates code execution, preventing security breaches and resource exhaustion attacks. Test case generation produces diverse test suites covering normal cases, boundary conditions, and random scenarios, ensuring thorough evaluation of student solutions.

User acceptance testing with sample teacher and student accounts demonstrates intuitive interfaces for quiz creation and problem solving. The separation between sample and hidden test cases provides appropriate feedback during development while maintaining evaluation integrity. Submission tracking enables progress monitoring and performance analysis for both students and teachers.

## Mapping of Results to Initial Objectives

The primary objective of creating a secure online coding assessment platform has been achieved through Docker containerization with strict resource limits. Each code submission executes in an isolated container with memory limits of 256MB, CPU quotas of 50%, and execution timeouts of 2 seconds per test case. Network access is disabled, and containers are destroyed immediately after execution, ensuring complete isolation.

The objective of implementing LeetCode-style function-based problems has been realized through the function signature model and driver code generation. Students implement specific function signatures rather than complete programs, and the system automatically integrates their code with test case execution logic. This approach provides better structure and clarity compared to stdin-based alternatives.

The objective of automated test case generation has been accomplished through constraint parsing and intelligent test case creation. The system extracts number ranges and data types from problem constraints, generating normal, boundary, and random test cases automatically. This reduces manual effort while ensuring comprehensive test coverage.

The objective of role-based access control has been implemented through user roles and route protection. Teachers have access to quiz creation, editing, and submission viewing, while students can browse quizzes, submit solutions, and view their own submission history. Access restrictions are enforced through decorators and role checks.

## Performance Analysis

Execution performance meets design requirements with average test case execution times under two seconds. The sequential test case evaluation stops at the first failure, minimizing execution time for incorrect solutions while ensuring thorough evaluation of correct solutions. Container creation and destruction overhead is acceptable, with minimal impact on overall response times.

Memory usage remains within acceptable limits, with each container constrained to 256MB. The system successfully prevents memory exhaustion attacks through container limits and proper cleanup. CPU usage is controlled through quotas, preventing resource starvation even under concurrent load.

Database performance is adequate for the expected user base, with SQLite handling queries efficiently. Indexes on foreign keys enable fast lookups for quiz-submission relationships. The database schema supports efficient queries for dashboards and statistics without requiring optimization.

Scalability testing indicates that the system can handle moderate concurrent loads, with multiple submissions executing simultaneously without interference. For larger deployments, the architecture supports horizontal scaling through load balancing and database migration to PostgreSQL or MySQL.

## Technical Challenges Faced

One significant challenge involved ensuring correct result comparison while handling various data types and edge cases. The initial implementation incorrectly flagged valid solutions as failures when stderr contained warning messages. This required prioritizing output correctness checking over error status, ensuring that correct JSON output is accepted regardless of warning messages.

Another challenge involved implementing proper container cleanup to prevent resource accumulation. Containers must be removed even when errors occur, requiring comprehensive error handling in finally blocks. The solution involved restructuring cleanup logic to ensure containers are always removed, even during exception handling.

Test case generation presented challenges in parsing constraints and generating appropriate test cases for different problem types. The solution involved developing pattern matching for constraint extraction and type-specific test case generation logic. The generator now successfully handles array, string, and number-based problems with appropriate test case diversity.

Handling in-place list modifications required special logic in driver code generation. Functions that modify input lists and return None needed special handling to detect and return the modified input. The solution involved checking return values and input types to identify in-place modifications.

## Solutions Implemented

The output correctness priority solution modified the evaluation flow to check result correctness before examining error status. This ensures that correct solutions are not incorrectly rejected due to warning messages. The comparison logic was moved earlier in the execution pipeline, before error checking occurs.

The container cleanup solution implemented comprehensive finally blocks throughout the execution engine. Containers are stopped and removed in finally blocks, ensuring cleanup occurs even when exceptions are raised. Temporary directories are also cleaned up in finally blocks to prevent filesystem accumulation.

The test case generation solution developed constraint parsing using regular expressions to extract number ranges and data types. Type-specific generators create appropriate test cases based on detected problem types. The generator produces diverse test suites with normal, boundary, and random cases.

The in-place modification solution enhanced driver code to detect when functions modify input lists. When a function returns None and the first argument is a list, the driver code returns the modified list. This handles common patterns like list sorting and in-place array operations.

## Merits of the System

The system provides secure code execution through Docker containerization, ensuring that student code cannot access system resources or interfere with other submissions. Resource limits prevent denial-of-service attacks, and network isolation prevents external communication during execution.

The function-based problem model provides better structure than stdin-based approaches, enabling clearer problem statements and more accurate evaluation. The separation between sample and hidden test cases balances learning and evaluation, providing feedback during development while maintaining assessment integrity.

Automated test case generation reduces manual effort in quiz creation while ensuring comprehensive test coverage. The system generates diverse test cases covering normal operation, boundary conditions, and random scenarios, providing thorough evaluation of student solutions.

The role-based access control ensures appropriate separation between teacher and student functions, enabling effective quiz management and secure assessment. Submission tracking provides valuable analytics for both students and teachers, enabling progress monitoring and performance analysis.

## Demerits and Limitations

The system currently supports only Python, limiting its applicability for courses teaching other programming languages. Adding support for additional languages would require language-specific execution environments and test case generation logic. This limitation restricts the platform's versatility for comprehensive computer science curricula.

The test case generation relies on pattern matching and heuristics, which may not always produce optimal test cases. Some problems may require manual test case creation or refinement to ensure adequate coverage. The generator's effectiveness depends on well-structured problem statements and clear constraints.

The sequential test case evaluation stops at the first failure, which prevents students from seeing all test case results. While this ensures efficiency, it may limit learning opportunities by not revealing all failure points. Some students might benefit from seeing complete test case results even after failure.

The system uses SQLite for simplicity, which may limit scalability for large deployments. While adequate for moderate user bases, high-concurrency scenarios might require migration to more robust database systems. The current implementation does not include caching or optimization for high-load scenarios.

## Critical Evaluation of System Behavior

The system demonstrates reliable behavior under normal operating conditions, correctly evaluating submissions and handling errors appropriately. The strict evaluation model ensures high standards, requiring all test cases to pass for acceptance. This approach promotes thorough problem-solving but may be perceived as harsh for students making minor mistakes.

Security behavior is robust, with Docker isolation preventing code interference and resource attacks. However, the system is designed for educational use and may require additional hardening for high-stakes assessments. The current security model is adequate for classroom use but might need enhancement for production exam environments.

The user interface provides intuitive navigation and clear feedback, enabling effective use by both teachers and students. The separation of concerns in the codebase facilitates maintenance and future enhancements. The modular architecture supports independent testing and modification of components.

Performance behavior meets requirements for moderate user bases, with acceptable response times and resource usage. The system handles concurrent submissions effectively, with Docker isolation preventing interference. However, scalability to very large deployments would require architectural enhancements including load balancing and database optimization.

## System Limitations and Future Considerations

The current implementation focuses on algorithmic problem-solving and may not adequately evaluate code quality aspects like readability, documentation, or design patterns. Future enhancements could include code quality metrics and style checking to provide more comprehensive evaluation.

The test case generation, while functional, could benefit from machine learning approaches to generate more sophisticated test cases. Integration with reference solutions could enable automatic verification of generated test cases, improving accuracy and reducing manual effort.

The system does not currently support collaborative features like code sharing or peer review, which could enhance learning opportunities. Integration with version control systems could enable tracking of solution evolution and provide additional learning insights.

Real-time collaboration features could enable pair programming exercises or group problem-solving sessions. Integration with learning management systems could provide seamless integration with course materials and gradebooks, enhancing the educational value of the platform.

