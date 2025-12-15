# Project Design and Methodology

## System Overview and Design Philosophy

Belfry is a LeetCode-style online coding assessment platform designed for educational use in college computer science courses. The system enables teachers to create coding problems and students to submit solutions that are automatically evaluated against comprehensive test cases. The design philosophy emphasizes security through isolation, accuracy through strict evaluation, and usability through intuitive interfaces.

The system architecture follows a three-tier model: presentation layer (web interface), application layer (Flask routes and business logic), and data layer (SQLite database). Security is paramount, with each code submission executing in an isolated Docker container with strict resource limits. The evaluation model requires all test cases to pass for a submission to be marked as correct, ensuring high standards of solution quality.

## System Architecture

The system employs a modular architecture organized around Flask blueprints. The main application (app.py) initializes the Flask instance, database connection, and login manager. Three primary blueprints handle different functionalities: authentication (auth), teacher operations (teacher), and student operations (student). Each module maintains separation of concerns with clear interfaces and minimal coupling.

The execution engine operates independently, receiving code submissions and test cases, executing them in Docker containers, and returning evaluation results. This separation allows the execution engine to be tested and modified without affecting the web interface. The test case generator operates as a utility module, creating test cases during quiz creation and supporting regeneration when needed.

## Entity Relationship Diagram (ERD)

The database schema consists of four primary entities with well-defined relationships. The User entity represents both teachers and students, distinguished by a role attribute. Each User can create multiple Quiz entities (one-to-many relationship through created_by foreign key). Each Quiz contains multiple Testcase entities (one-to-many relationship with cascade deletion). Each User can submit multiple Submission entities for different quizzes (many-to-many relationship through User and Quiz).

The User entity includes authentication fields (username, email, password_hash) and role information. The Quiz entity stores problem metadata including title, description, problem statement, function signature, constraints, and problem type. The Testcase entity stores input data and expected output as JSON strings, along with flags indicating whether it is a sample test case and its type (normal, boundary, random). The Submission entity tracks code, language, status, error information, and test case results.

## Data Flow Diagram (DFD)

The system's data flow follows distinct paths for different operations. For quiz creation, data flows from the teacher interface through the create_quiz route to the Quiz model, which triggers test case generation. Generated test cases flow into the Testcase model and are associated with the quiz. For code submission, student code flows from the solve interface through the submit route to the judge engine, which executes the code and returns results that flow into the Submission model.

The execution flow involves code and test cases flowing into Docker containers, with execution results flowing back to the judge engine for comparison. Results then flow into the Submission model and back to the student interface. The data flow maintains clear separation between user input, processing, and output, with validation occurring at each stage to ensure data integrity.

## State Transition Diagram

The submission evaluation process follows a state machine with three primary states: pending, pass, and fail. Submissions begin in the pending state when initially created. During execution, the system evaluates test cases sequentially, stopping at the first failure. If all test cases pass, the submission transitions to the pass state. If any test case fails, the submission transitions to the fail state with appropriate error information.

The quiz lifecycle follows a simpler state machine: active and inactive. Quizzes are created in the active state and can be deactivated by teachers. Only active quizzes appear in student dashboards. The user authentication state machine includes logged-out and logged-in states, with role-based transitions determining access to teacher or student interfaces.

## Flowchart of Development Steps

The development process followed a structured methodology. Phase one involved requirements analysis and system design, including ERD creation, DFD development, and architecture planning. Phase two focused on database implementation, creating SQLAlchemy models and establishing relationships. Phase three developed the execution engine, implementing Docker integration and test case evaluation logic.

Phase four built the web interface, creating Flask routes, templates, and user authentication. Phase five implemented test case generation, developing constraint parsing and automated test case creation. Phase six integrated all components, testing end-to-end functionality. Phase seven involved security hardening, implementing resource limits and container isolation. Phase eight focused on user experience improvements, refining interfaces and adding feedback mechanisms.

## Data Collection Methods

The system collects data through multiple channels. User registration collects username, email, and role information. Quiz creation collects problem metadata, function signatures, constraints, and sample inputs/outputs. Code submission collects student code, selected language, and submission timestamp. Execution results collect test case outcomes, error messages, execution time, and memory usage.

The system stores all submissions for analysis, enabling teachers to review student progress and identify common errors. Submission history allows students to track their improvement over time. The database maintains referential integrity through foreign key constraints, ensuring data consistency and enabling efficient queries for dashboards and statistics.

## Tools, Technologies, and Platforms

The system is built using Python 3.13 as the primary programming language. Flask 3.0 serves as the web framework, providing routing, templating, and session management. SQLAlchemy 2.0 handles database operations through object-relational mapping. Flask-Login manages user authentication and session handling. Docker provides containerization for secure code execution.

The frontend uses HTML5 with Jinja2 templating and Tailwind CSS for styling. JavaScript handles client-side interactions including code editor functionality and asynchronous submission requests. The Docker Python SDK enables programmatic container management. The system runs on any platform supporting Python and Docker, with SQLite as the database backend for simplicity and portability.

## Modular Architecture Description

The authentication module (auth blueprint) handles user registration, login, logout, and session management. It validates credentials, manages password hashing, and enforces authentication requirements through decorators. The teacher module (teacher blueprint) provides quiz creation, editing, test case management, submission viewing, and statistics display. It enforces teacher role requirements and manages quiz lifecycle.

The student module (student blueprint) handles quiz browsing, problem viewing, code submission, and submission history. It restricts access to appropriate content and provides code execution interfaces. The judge module (judge.py) operates independently, handling code execution, test case evaluation, and result comparison. The test case generator module (testcase_generator.py) creates test cases based on problem constraints and sample data.

## Use Case Diagram

Primary actors include Teachers and Students. Teacher use cases include creating quizzes, editing quizzes, viewing submissions, managing test cases, and regenerating test cases. Student use cases include browsing quizzes, viewing problem statements, submitting code, running code against sample test cases, and viewing submission history. The system actor handles code execution and test case evaluation automatically.

Secondary actors include the Docker system, which executes code, and the database system, which stores persistent data. The authentication system manages user sessions. Use cases maintain clear boundaries with well-defined inputs and outputs, enabling independent testing and modification of individual components.

## Class Diagram

The User class extends UserMixin from Flask-Login and includes attributes for authentication and role management. It maintains relationships with Quiz (as creator) and Submission (as submitter). The Quiz class represents coding problems with attributes for metadata, function signatures, and problem type. It maintains relationships with Testcase and Submission entities.

The Testcase class stores input/output data and test case metadata. It belongs to a Quiz through a foreign key relationship. The Submission class tracks student code submissions with execution results, error information, and test case statistics. It belongs to both a User and a Quiz. The OnlineJudge class encapsulates execution logic, managing Docker containers and evaluating test cases. The TestcaseGenerator class provides static methods for automated test case creation.

## Sequence Diagram

The quiz creation sequence begins when a teacher submits quiz data through the web interface. The create_quiz route validates input and creates a Quiz object. The system then calls the test case generator with problem constraints and sample data. Generated test cases are associated with the quiz and stored in the database. The system redirects to the quiz view page.

The code submission sequence begins when a student submits code. The submit route retrieves the quiz and all test cases. The code and test cases are passed to the OnlineJudge.execute_submission method. For each test case, the judge creates a Docker container, executes the code, and compares results. Results are aggregated and stored in a Submission object. The system returns evaluation results to the student interface.

## Activity Diagram

The code execution activity begins with syntax checking. If syntax errors exist, execution stops and results are returned. Otherwise, the system iterates through test cases sequentially. For each test case, a Docker container is created with resource limits. Driver code is generated that wraps the user's code and executes the test case. The container executes the code and returns output. Output is parsed and compared with expected results. If results match, the next test case is evaluated. If results differ, execution stops and failure is reported. After all test cases pass or the first failure occurs, results are aggregated and returned.

## Component Diagram

The system consists of five primary components: Web Interface, Application Server, Execution Engine, Database, and Docker Runtime. The Web Interface component handles user interactions through HTML templates and JavaScript. The Application Server component (Flask) manages routing, authentication, and business logic. The Execution Engine component handles code evaluation and test case comparison.

The Database component stores persistent data including users, quizzes, test cases, and submissions. The Docker Runtime component provides isolated execution environments. Components communicate through well-defined interfaces: HTTP requests between Web Interface and Application Server, method calls between Application Server and Execution Engine, database queries between Application Server and Database, and container management between Execution Engine and Docker Runtime.

## Deployment Diagram

The system deploys on a single server hosting the Flask application, SQLite database, and Docker daemon. The web server (Flask development server or production WSGI server) handles HTTP requests and serves templates. The database file resides on the server filesystem. Docker containers are created dynamically during code execution and destroyed immediately after completion.

For production deployment, the system can be containerized using Docker Compose, separating the web application, database, and execution environment. Load balancing can distribute requests across multiple application instances. The database can be migrated to PostgreSQL or MySQL for better concurrency and scalability. Container orchestration platforms like Kubernetes can manage Docker execution containers at scale.

