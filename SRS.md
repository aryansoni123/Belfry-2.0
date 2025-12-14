# Software Requirements Specification (SRS)
## Belfry - Online Coding Assessment Platform

**Version:** 3.0  
**Date:** January 2025  
**Author:** Belfry Development Team

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for **Belfry**, an online coding assessment and practice platform designed for college students in India. The platform provides a LeetCode-style coding environment with server-side code execution, automatic test case generation, and role-based access control.

### 1.2 Scope
Belfry is a web-based application that enables:
- Teachers to create coding quizzes with automatic test case generation
- Students to practice coding problems and submit solutions
- Automated evaluation of code submissions with strict pass/fail criteria
- Secure code execution in isolated Docker containers

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS**: Software Requirements Specification
- **LeetCode-style**: Function-based coding problems where students implement specific function signatures
- **Test Case**: Input-output pair used to validate code correctness
- **Docker**: Containerization platform for secure code execution
- **SQLite**: Lightweight database used for data persistence
- **Flask**: Python web framework used for backend development

### 1.4 References
- Flask Documentation: https://flask.palletsprojects.com/
- Docker Documentation: https://docs.docker.com/
- SQLAlchemy Documentation: https://www.sqlalchemy.org/
- LeetCode Platform: https://leetcode.com/

### 1.5 Overview
This document is organized into sections covering:
- Overall Description (system perspective, features, constraints)
- Specific Requirements (functional, non-functional, interface requirements)
- System Architecture
- Database Design
- Security Requirements

---

## 2. Overall Description

### 2.1 Product Perspective
Belfry is a standalone web application built with:
- **Backend**: Python Flask framework
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **Code Execution**: Docker containers for isolation
- **Client-side Execution**: Pyodide for fast "Run" functionality

### 2.2 Product Functions
The system provides the following major functions:

1. **User Authentication & Authorization**
   - Login/logout functionality
   - Role-based access (Teacher/Student)
   - Session management

2. **Quiz Management (Teacher)**
   - Create coding quizzes
   - Edit existing quizzes
   - View quiz statistics
   - Automatic test case generation (500+ test cases)
   - Regenerate test cases

3. **Problem Solving (Student)**
   - View available quizzes
   - Solve coding problems
   - Run code against sample test cases (client-side)
   - Submit code for final evaluation (server-side)
   - View submission history

4. **Code Execution & Evaluation**
   - Syntax checking
   - Runtime execution in Docker containers
   - Strict output comparison
   - Resource limits (time, memory, CPU)
   - Early termination on first failure

5. **Test Case Generation**
   - Automatic generation of 500+ test cases
   - Boundary, normal, and random test cases
   - Support for function-based and stdin-based problems

### 2.3 User Classes and Characteristics

#### 2.3.1 Teachers (Administrators)
- **Role**: Create and manage coding quizzes
- **Characteristics**: 
  - Technical knowledge of programming concepts
  - Need to create problems quickly
  - Require automatic test case generation
  - Need to view student performance statistics

#### 2.3.2 Students
- **Role**: Practice coding and submit solutions
- **Characteristics**:
  - Learning programming
  - Need immediate feedback
  - Require clear problem statements
  - Need to understand why solutions fail

### 2.4 Operating Environment
- **Server**: Linux/Windows/Mac with Docker support
- **Client**: Modern web browsers (Chrome, Firefox, Safari, Edge)
- **Python**: Version 3.13
- **Docker**: Docker Desktop (Windows/Mac) or Docker Engine (Linux)

### 2.5 Design and Implementation Constraints
- **Database**: Must use SQLite (as specified)
- **Backend Framework**: Must use Flask
- **Authentication**: Must use Flask-Login
- **ORM**: Must use SQLAlchemy
- **Frontend Styling**: Tailwind CSS (no purple shades, Apple-like design)
- **Code Execution**: Must use Docker for server-side execution
- **No Client-side Execution for Submissions**: Only "Run" uses client-side; "Submit" must be server-side

### 2.6 Assumptions and Dependencies
- Docker Desktop/Engine is installed and running
- Python 3.13 is available
- Internet connection for CDN resources (Tailwind, Pyodide)
- Modern browser with JavaScript enabled

---

## 3. System Features

### 3.1 Feature 1: User Authentication

#### 3.1.1 Description
Users can log in with username and password. The system supports two roles: Teacher and Student.

#### 3.1.2 Functional Requirements
- **FR-1.1**: System shall provide a login page
- **FR-1.2**: System shall validate username and password
- **FR-1.3**: System shall maintain user sessions
- **FR-1.4**: System shall redirect users to appropriate dashboards based on role
- **FR-1.5**: System shall provide logout functionality
- **FR-1.6**: System shall protect routes based on authentication status

#### 3.1.3 Input/Output
- **Input**: Username, Password
- **Output**: Redirect to dashboard or error message

### 3.2 Feature 2: Quiz Creation (Teacher)

#### 3.2.1 Description
Teachers can create coding quizzes with problem statements, function signatures, constraints, and sample inputs/outputs. The system automatically generates 500+ test cases.

#### 3.2.2 Functional Requirements
- **FR-2.1**: System shall provide a quiz creation form
- **FR-2.2**: System shall support function-based (LeetCode-style) problems
- **FR-2.3**: System shall support stdin-based (legacy) problems
- **FR-2.4**: System shall require function signature for function-based problems
- **FR-2.5**: System shall automatically generate 500+ test cases upon quiz creation
- **FR-2.6**: System shall mark one test case as "sample" (visible to students)
- **FR-2.7**: System shall store quiz metadata (title, description, problem statement, constraints)
- **FR-2.8**: System shall allow teachers to edit existing quizzes
- **FR-2.9**: System shall allow teachers to regenerate test cases

#### 3.2.3 Input/Output
- **Input**: 
  - Quiz title
  - Description
  - Problem type (function/stdin)
  - Function signature (for function-based)
  - Problem statement
  - Constraints
  - Sample input/output
- **Output**: Created quiz with 500+ test cases

### 3.3 Feature 3: Quiz Solving (Student)

#### 3.3.1 Description
Students can view available quizzes, read problem statements, write code, run code against sample test cases, and submit solutions for final evaluation.

#### 3.3.2 Functional Requirements
- **FR-3.1**: System shall display available quizzes on student dashboard
- **FR-3.2**: System shall show quiz status (not attempted, passed, failed)
- **FR-3.3**: System shall provide a code editor with syntax highlighting
- **FR-3.4**: System shall support tab/shift-tab for indentation
- **FR-3.5**: System shall allow students to run code against sample test cases (client-side)
- **FR-3.6**: System shall allow students to submit code for final evaluation (server-side)
- **FR-3.7**: System shall display test case results with input/expected/actual output
- **FR-3.8**: System shall stop execution on first test case failure
- **FR-3.9**: System shall show code format examples and tips

#### 3.3.3 Input/Output
- **Input**: Student code (Python function implementation)
- **Output**: Test case results, pass/fail status, error messages

### 3.4 Feature 4: Code Execution Engine

#### 3.4.1 Description
The system executes student code in isolated Docker containers with resource limits and strict evaluation.

#### 3.4.2 Functional Requirements
- **FR-4.1**: System shall check code syntax before execution
- **FR-4.2**: System shall execute code in Docker containers
- **FR-4.3**: System shall enforce execution timeout (2 seconds per test case)
- **FR-4.4**: System shall enforce memory limit (256MB per container)
- **FR-4.5**: System shall enforce CPU limit (50% quota)
- **FR-4.6**: System shall disable network access in containers
- **FR-4.7**: System shall destroy containers after execution
- **FR-4.8**: System shall compare outputs strictly (exact match required)
- **FR-4.9**: System shall stop execution on first failure
- **FR-4.10**: System shall handle syntax errors, runtime errors, and timeouts
- **FR-4.11**: System shall support function-based execution (inject user code into driver template)
- **FR-4.12**: System shall support in-place modification problems (e.g., reverse string)

#### 3.4.3 Input/Output
- **Input**: User code, function signature, test case input
- **Output**: Execution result (pass/fail), error type, execution time

### 3.5 Feature 5: Test Case Generation

#### 3.5.1 Description
The system automatically generates diverse test cases based on problem type, constraints, and sample input/output.

#### 3.5.2 Functional Requirements
- **FR-5.1**: System shall generate at least 500 test cases per quiz
- **FR-5.2**: System shall generate boundary test cases (edge values, minimum/maximum)
- **FR-5.3**: System shall generate normal test cases (typical inputs)
- **FR-5.4**: System shall generate random test cases (large inputs, varied data)
- **FR-5.5**: System shall parse constraints to determine valid input ranges
- **FR-5.6**: System shall support function-based problem generation
- **FR-5.7**: System shall support stdin-based problem generation
- **FR-5.8**: System shall use sample input/output as the sample test case
- **FR-5.9**: System shall mark sample test cases as visible to students

#### 3.5.3 Input/Output
- **Input**: Problem type, function signature, constraints, sample I/O
- **Output**: 500+ test cases with input_data and expected_output

### 3.6 Feature 6: Submission Management

#### 3.6.1 Description
The system stores and tracks student submissions with results, execution times, and error messages.

#### 3.6.2 Functional Requirements
- **FR-6.1**: System shall store all code submissions
- **FR-6.2**: System shall record submission status (pass/fail/pending)
- **FR-6.3**: System shall record passed/total test case counts
- **FR-6.4**: System shall record execution time
- **FR-6.5**: System shall record error messages and types
- **FR-6.6**: System shall allow students to view submission history
- **FR-6.7**: System shall display previous submission code when retrying

#### 3.6.3 Input/Output
- **Input**: Code, quiz_id, user_id
- **Output**: Submission record with results

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **NFR-1**: Code execution should complete within 2 seconds per test case
- **NFR-2**: "Run" functionality (client-side) should provide instant feedback (< 1 second)
- **NFR-3**: Page load time should be under 2 seconds
- **NFR-4**: System should handle at least 50 concurrent users

### 4.2 Security Requirements
- **NFR-5**: Code execution must be isolated in Docker containers
- **NFR-6**: Containers must have no network access
- **NFR-7**: Containers must have restricted filesystem access
- **NFR-8**: Passwords must be hashed (using Werkzeug)
- **NFR-9**: Sessions must be secure (Flask-Login)
- **NFR-10**: Routes must be protected by authentication

### 4.3 Usability Requirements
- **NFR-11**: UI must be clean and Apple-like in design
- **NFR-12**: UI must use specified color palette (#AAAFCB, #918E46, #5AA07B, #5F4B35)
- **NFR-13**: Code editor must support syntax highlighting
- **NFR-14**: Code editor must support tab/shift-tab indentation
- **NFR-15**: Error messages must be clear and helpful
- **NFR-16**: Code format examples must be provided

### 4.4 Reliability Requirements
- **NFR-17**: System must handle Docker unavailability gracefully
- **NFR-18**: System must validate all inputs
- **NFR-19**: System must handle database errors gracefully
- **NFR-20**: System must prevent SQL injection (using ORM)

### 4.5 Portability Requirements
- **NFR-21**: System must run on Windows, Linux, and Mac
- **NFR-22**: System must work with modern browsers
- **NFR-23**: System must use SQLite for easy deployment

---

## 5. System Architecture

### 5.1 Architecture Overview
Belfry follows a modular Flask application structure with blueprints for different functionalities.

### 5.2 Component Structure
```
belfry/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models (User, Quiz, Testcase, Submission)
├── judge.py               # Code execution engine
├── testcase_generator.py  # Automatic test case generation
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
│
├── auth/                  # Authentication blueprint
│   ├── __init__.py
│   └── routes.py
│
├── teacher/               # Teacher functionality blueprint
│   ├── __init__.py
│   └── routes.py
│
├── student/               # Student functionality blueprint
│   ├── __init__.py
│   └── routes.py
│
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── teacher_dashboard.html
│   ├── create_quiz.html
│   ├── student_dashboard.html
│   └── solve_quiz.html
│
└── instance/              # SQLite database
    └── belfry.db
```

### 5.3 Database Schema

#### 5.3.1 Users Table
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password_hash` (String)
- `role` (String: 'teacher' or 'student')
- `created_at` (DateTime)

#### 5.3.2 Quizzes Table
- `id` (Integer, Primary Key)
- `title` (String)
- `description` (Text)
- `problem_statement` (Text)
- `function_signature` (Text, nullable)
- `sample_input` (Text, nullable)
- `sample_output` (Text, nullable)
- `constraints` (Text, nullable)
- `problem_type` (String: 'function' or 'stdin')
- `created_by` (Integer, Foreign Key → Users.id)
- `created_at` (DateTime)
- `is_active` (Boolean)

#### 5.3.3 Testcases Table
- `id` (Integer, Primary Key)
- `quiz_id` (Integer, Foreign Key → Quizzes.id)
- `input_data` (Text, JSON string)
- `expected_output` (Text, JSON string)
- `is_sample` (Boolean)
- `testcase_type` (String: 'normal', 'boundary', 'random')

#### 5.3.4 Submissions Table
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key → Users.id)
- `quiz_id` (Integer, Foreign Key → Quizzes.id)
- `code` (Text)
- `language` (String)
- `status` (String: 'pass', 'fail', 'pending')
- `error_message` (Text, nullable)
- `error_type` (String, nullable)
- `passed_testcases` (Integer)
- `total_testcases` (Integer)
- `execution_time` (Float, nullable)
- `submitted_at` (DateTime)

### 5.4 Execution Flow

#### 5.4.1 Run Code Flow (Client-side)
1. Student clicks "Run"
2. Code is executed in browser using Pyodide
3. Sample test cases are executed
4. Results are displayed immediately

#### 5.4.2 Submit Code Flow (Server-side)
1. Student clicks "Submit"
2. Code is sent to server
3. Syntax check is performed
4. For each test case (until first failure):
   - Docker container is created
   - Driver code is generated
   - Code is executed with resource limits
   - Output is compared strictly
   - Container is destroyed
5. Results are stored in database
6. Response is sent to client

---

## 6. Interface Requirements

### 6.1 User Interfaces
- **Login Page**: Username/password form
- **Teacher Dashboard**: List of quizzes with statistics
- **Create Quiz Page**: Form for quiz creation
- **Student Dashboard**: List of available quizzes with status
- **Solve Quiz Page**: Problem statement, code editor, results panel

### 6.2 Hardware Interfaces
- Standard web server hardware
- Docker-capable system

### 6.3 Software Interfaces
- **Python 3.13**: Runtime environment
- **Docker**: Containerization platform
- **SQLite**: Database system
- **Web Browser**: Client interface

### 6.4 Communication Interfaces
- **HTTP/HTTPS**: Web protocol
- **REST API**: For code execution endpoints

---

## 7. System Constraints

### 7.1 Technical Constraints
- Must use Flask framework
- Must use SQLite database
- Must use Docker for code execution
- Must support Python 3.13 only (initially)
- Must use Tailwind CSS for styling

### 7.2 Business Constraints
- Designed for college students in India
- Free/open-source platform
- Educational use case

### 7.3 Regulatory Constraints
- Must comply with data privacy requirements
- Must not store sensitive student information unnecessarily

---

## 8. Quality Attributes

### 8.1 Maintainability
- Modular code structure with blueprints
- Clear separation of concerns
- Comprehensive comments
- Documentation

### 8.2 Scalability
- Docker-based execution allows horizontal scaling
- SQLite can be migrated to PostgreSQL/MySQL for production
- Stateless execution design

### 8.3 Testability
- Unit tests can be written for test case generation
- Integration tests for execution engine
- Manual testing with sample quizzes

---

## 9. Appendices

### 9.1 Glossary
- **Driver Code**: Template code that wraps user code and executes test cases
- **Function-Based Problem**: LeetCode-style problem where students implement a function
- **Stdin-Based Problem**: Legacy problem where students read from stdin
- **Test Case**: Input-output pair for validation
- **Sample Test Case**: Test case visible to students before submission

### 9.2 Sample Data
Default accounts:
- Teacher: `teacher` / `teacher123`
- Student: `student` / `student123`
- Student2: `student2` / `student123`

### 9.3 Change Log
- **v3.0**: LeetCode-style execution, client-side "Run", 500+ test cases, Apple-like UI
- **v2.0**: Stdin-based problems, basic execution
- **v1.0**: Initial release

---

## 10. Approval

This SRS document has been reviewed and approved by:
- **Development Team**: [Date]
- **Project Manager**: [Date]
- **Stakeholders**: [Date]

---

**End of SRS Document**

