# Literature Review

## Introduction to Literature Review

The development of online coding assessment platforms has emerged as a critical component in modern computer science education and technical recruitment. This literature review examines existing research and implementations of online judge systems, automated code evaluation platforms, and secure code execution environments. The analysis focuses on identifying best practices, technical approaches, and architectural patterns that inform the design and implementation of Belfry, a LeetCode-style online coding assessment platform.

The review encompasses studies from academic publications, industry implementations, and open-source projects that address key challenges in automated code evaluation: security, scalability, accuracy, and user experience. By synthesizing findings from multiple sources, this review establishes a foundation for understanding the current state of the art and identifying opportunities for innovation in educational coding assessment systems.

## Comparative Analysis of Existing Systems

| YEAR | AUTHOR | PURPOSE | TECHNIQUES | ACCURACY |
|------|--------|---------|------------|----------|
| 2018 | LeetCode Platform | Online coding practice and assessment | Function-based evaluation, test case matching, runtime analysis | High accuracy for deterministic problems |
| 2019 | HackerRank | Technical recruitment and skill assessment | Docker containerization, multiple language support, plagiarism detection | High accuracy with comprehensive test coverage |
| 2020 | CodeChef | Competitive programming platform | Server-side execution, resource limits, real-time evaluation | High accuracy for algorithmic problems |
| 2021 | AtCoder | Japanese competitive programming platform | Strict I/O format validation, automated test case generation | Very high accuracy with strict validation |
| 2022 | Codeforces | Competitive programming and contests | Fast evaluation, multiple test cases, partial scoring | High accuracy with efficient execution |
| 2023 | Skillrack | Indian coding practice platform | Stdin-based evaluation, auto test case generation | Moderate accuracy, focuses on I/O matching |
| 2024 | Online Judge Research | Academic study on secure code execution | Sandboxing techniques, resource isolation, security analysis | High security with controlled accuracy |

## Source of Study: LeetCode Platform

**Publication Details:** LeetCode is a commercial online platform launched in 2015, widely used for coding interview preparation and technical skill assessment. The platform serves millions of users globally and has become a standard reference for function-based coding problems.

**Topics Studied:**

The LeetCode platform demonstrates a function-based problem model where students implement specific function signatures rather than complete programs. The system uses server-side execution with strict test case matching, where solutions must pass all test cases to be considered correct. The platform emphasizes clean code structure, proper algorithm implementation, and efficient solutions.

**Lessons Learnt from the Study:**

Function-based problems provide better structure and clarity compared to stdin-based approaches. The separation between sample test cases and hidden test cases creates a balanced learning experience. The strict evaluation model ensures that only fully correct solutions are accepted, promoting thorough problem-solving skills. The platform's success demonstrates the importance of immediate feedback and clear problem statements.

**Proposed Modules that would Apply the Study:**

The Belfry system incorporates LeetCode's function-based problem model through the Quiz model and function signature validation. The execution engine implements similar strict evaluation criteria where all test cases must pass. The test case generation module creates both sample and hidden test cases following LeetCode's pattern. The submission evaluation system uses the same pass-or-fail approach without partial marking.

## Source of Study: Docker-Based Code Execution Research

**Publication Details:** Multiple academic papers and industry implementations have explored Docker containerization for secure code execution. Key references include research on sandboxing techniques, container security, and resource isolation in educational computing environments.

**Topics Studied:**

Docker containerization provides process isolation, resource limits, and network restrictions for executing untrusted code. Research demonstrates that containers offer better security than traditional process isolation while maintaining reasonable performance overhead. Studies examine memory limits, CPU quotas, timeout mechanisms, and filesystem restrictions as essential security controls.

**Lessons Learnt from the Study:**

Container-based execution provides strong isolation between different submissions, preventing code interference and security breaches. Resource limits prevent denial-of-service attacks through resource exhaustion. Network isolation prevents external communication during code execution. The ephemeral nature of containers ensures clean execution environments for each test case.

**Proposed Modules that would Apply the Study:**

The judge.py module implements Docker-based execution with configurable resource limits including memory constraints, CPU quotas, and execution timeouts. Each test case runs in a separate container instance, ensuring complete isolation. The system disables network access and restricts filesystem access to the container's temporary directory. Container cleanup ensures no persistent state between executions.

## Source of Study: Automated Test Case Generation

**Publication Details:** Research on automated test case generation spans multiple domains including software testing, competitive programming platforms, and educational assessment systems. Key techniques include constraint-based generation, random test case creation, and boundary value analysis.

**Topics Studied:**

Automated test case generation reduces manual effort in creating comprehensive test suites. Constraint parsing from problem statements enables intelligent test case creation. Boundary value testing ensures edge cases are covered. Random test case generation provides diverse input scenarios. The combination of normal, boundary, and random test cases creates robust evaluation sets.

**Lessons Learnt from the Study:**

Effective test case generation requires understanding problem constraints and data types. Boundary cases are critical for catching common implementation errors. Random test cases help identify non-deterministic bugs and edge cases not anticipated by problem creators. Sample test cases serve educational purposes while hidden test cases ensure evaluation integrity.

**Proposed Modules that would Apply the Study:**

The testcase_generator.py module implements constraint parsing to extract number ranges and data type information from problem statements. The generator creates three types of test cases: normal cases based on sample inputs, boundary cases using constraint limits, and random cases for comprehensive coverage. The system generates both sample and hidden test cases automatically during quiz creation.

## Source of Study: Role-Based Access Control in Educational Systems

**Publication Details:** Academic research on role-based access control in educational platforms examines teacher-student interactions, assessment management, and submission tracking. Studies focus on maintaining assessment integrity while providing appropriate access levels.

**Topics Studied:**

Role-based access control separates administrative functions from student interactions. Teachers require capabilities for creating quizzes, managing test cases, and viewing submissions. Students need access to problem statements, code submission interfaces, and their own submission history. The separation ensures assessment security and prevents unauthorized access to solutions.

**Lessons Learnt from the Study:**

Clear role separation improves system security and usability. Teachers benefit from comprehensive quiz management interfaces with statistics and analytics. Students require focused interfaces for problem-solving without access to hidden test cases or other students' solutions. Submission tracking enables progress monitoring and performance analysis.

**Proposed Modules that would Apply the Study:**

The authentication system implements role-based access control with teacher and student roles. The teacher blueprint provides quiz creation, editing, test case management, and submission viewing capabilities. The student blueprint focuses on quiz browsing, code submission, and personal submission history. The User model stores role information and enforces access restrictions through route decorators.

## Source of Study: Flask Web Application Architecture

**Publication Details:** Flask is a lightweight Python web framework documented extensively in official documentation and community resources. Best practices for Flask application structure emphasize modular design, blueprint organization, and separation of concerns.

**Topics Studied:**

Flask's blueprint system enables modular application organization with separate modules for different functionalities. The Model-View-Controller pattern separates data models, business logic, and presentation layers. SQLAlchemy integration provides object-relational mapping for database interactions. Template inheritance creates consistent user interfaces across application pages.

**Lessons Learnt from the Study:**

Modular architecture improves code maintainability and scalability. Blueprint organization allows independent development of different application components. Database models should encapsulate data relationships and business logic. Template inheritance reduces code duplication and ensures consistent UI design. Separation of concerns simplifies testing and debugging.

**Proposed Modules that would Apply the Study:**

The application structure follows Flask best practices with separate blueprints for authentication, teacher functions, and student functions. The models.py file defines database schemas using SQLAlchemy with proper relationships between User, Quiz, Testcase, and Submission models. Template inheritance through base.html ensures consistent navigation and styling. The modular structure enables independent testing and future extensions.

## Conclusion

This literature review establishes that successful online coding assessment platforms combine secure execution environments, intelligent test case generation, and user-friendly interfaces. The Belfry system synthesizes these elements by implementing Docker-based security, automated test case generation, and role-based access control within a Flask web application framework. The reviewed systems demonstrate that function-based problems provide better structure than stdin-based approaches, and that containerization offers superior security compared to traditional process isolation. These findings directly inform the design decisions and implementation strategies employed in the Belfry platform.

