# Belfry - LeetCode-Style Online Coding Assessment Platform

A secure, server-side online judge for coding practice and assessments, built with Flask and Docker. Execution behavior is functionally identical to LeetCode, while maintaining Belfry's custom UI/UX.

## 🎯 Key Features

- **LeetCode-Style Execution**: Function-based problems with server-side execution
- **Docker Sandboxing**: Each submission runs in an isolated container
- **Strict Evaluation**: PASS only if ALL test cases pass (no partial marking)
- **Hidden Test Cases**: Sample test cases visible, hidden test cases for evaluation
- **Role-Based Access**: Teacher (Admin) and Student roles
- **Auto Test Case Generation**: Automatic generation of normal, boundary, and random test cases

## 🏗️ Architecture

### Execution Engine (`judge.py`)

The core execution engine implements a true LeetCode-style online judge:

- **Function-Based Problems**: Students implement functions, not stdin programs
- **Docker Isolation**: Each test case runs in a separate, isolated container
- **Resource Limits**: 
  - Execution timeout: 2 seconds per test case
  - Memory limit: 256MB per container
  - CPU limit: 50% CPU quota
- **Security**: 
  - No network access
  - No filesystem access outside container
  - Containers destroyed after execution

### Problem Model

**Function-Based (LeetCode-Style):**
```python
def twoSum(nums: List[int], target: int) -> List[int]:
    # Student implements this function
    pass
```

**Test Case Format:**
- Input: JSON string of function arguments (e.g., `[[2,7,11,15], 9]`)
- Expected Output: JSON string of return value (e.g., `[0, 1]`)

### Execution Flow

1. **Student writes code** implementing the function
2. **Run**: Executes against sample test cases only (quick feedback)
3. **Submit**: Executes against ALL test cases (including hidden), saves submission

## 🚀 Installation & Setup

### Prerequisites

- Python 3.13+
- Docker Desktop (for code execution)
- pip

### Step 1: Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Initialize Database

```bash
# Create database and seed default accounts
python init_db.py --seed
```

This creates:
- **Teacher account**: username=`teacher`, password=`teacher123`
- **Student account**: username=`student`, password=`student123`

### Step 3: Start Docker

Ensure Docker Desktop is running. The execution engine requires Docker to run student code in isolated containers.

### Step 4: Run the Application

```bash
# Set Flask environment
export FLASK_APP=app.py
export FLASK_ENV=development

# Run Flask
flask run
```

Or:

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📝 Creating a Quiz (Teacher)

### Function-Based Problem (Recommended)

1. Login as teacher
2. Go to "Create Quiz"
3. Select "Function-based (LeetCode-style)"
4. Enter function signature: `def twoSum(nums: List[int], target: int) -> List[int]:`
5. Enter problem statement, constraints, sample input/output
6. Click "Create Quiz"

**Sample Input Format (JSON):**
```
[[2,7,11,15], 9]
```

**Sample Output Format (JSON):**
```
[0, 1]
```

See `TWO_SUM_EXAMPLE.md` for a complete example.

### Legacy Stdin-Based Problem

1. Select "Stdin-based (Legacy)"
2. Enter problem statement
3. Enter sample input/output as plain text
4. System generates test cases automatically

## 💻 Solving a Quiz (Student)

1. Login as student
2. View available quizzes on dashboard
3. Click "Solve" on a quiz
4. Implement the function (or stdin program for legacy)
5. Click "Run" to test against sample test cases
6. Click "Submit" to evaluate against all test cases

**For Function-Based Problems:**
- Implement the exact function signature provided
- Do NOT change function name or parameters
- Do NOT add main block or print statements
- Return the result (don't print it)

**See `CODE_FORMAT_GUIDE.md` for detailed examples and common mistakes to avoid.**

## 🔧 Configuration

Edit `config.py` to customize:

```python
DOCKER_IMAGE = 'python:3.13-slim'  # Docker image for execution
DOCKER_TIMEOUT = 2  # Timeout per test case (seconds)
DOCKER_MEMORY_LIMIT = '256m'  # Memory limit per container
```

## 📁 Project Structure

```
belfry/
├── app.py                 # Main Flask application
├── config.py              # Configuration
├── models.py              # Database models
├── judge.py               # LeetCode-style execution engine
├── code_executor.py       # Legacy executor (deprecated)
├── testcase_generator.py  # Auto test case generation
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image for execution
│
├── auth/                  # Authentication blueprint
│   ├── __init__.py
│   └── routes.py
│
├── teacher/               # Teacher blueprint
│   ├── __init__.py
│   └── routes.py
│
├── student/               # Student blueprint
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
└── instance/              # SQLite database (created automatically)
    └── belfry.db
```

## 🧪 Execution Details

### How Code Execution Works

1. **Syntax Check**: Code is compiled to check for syntax errors
2. **Docker Container**: Each test case runs in a fresh container
3. **Driver Code**: User code is injected into a driver template that:
   - Imports necessary modules
   - Parses test case input (JSON)
   - Calls user's function
   - Serializes result to JSON
   - Prints result
4. **Comparison**: Returned value compared with expected output (strict equality)
5. **Result**: PASS if all test cases pass, FAIL otherwise

### Error Types

- **Syntax Error**: Invalid Python syntax
- **Runtime Error**: Exception during execution
- **Timeout**: Execution exceeds time limit
- **Wrong Answer**: Output doesn't match expected

### Security Notes

- **Docker Isolation**: Each execution is isolated
- **Resource Limits**: Memory and CPU limits prevent resource exhaustion
- **No Network**: Containers have no internet access
- **Auto Cleanup**: Containers are destroyed after execution

**Important**: This system is designed for educational use. For production exam environments, additional security hardening may be required.

## 🎨 UI/UX

- **Color Scheme**: Red, yellow, orange only (no purple)
- **Tailwind CSS**: Modern, clean, academic UI
- **Responsive**: Works on desktop and tablet
- **LeetCode-Like Execution**: Separate Run and Submit buttons
- **Real-Time Feedback**: Immediate results after Run/Submit

## 📊 Database Schema

- **Users**: Authentication and role management
- **Quizzes**: Problem definitions (function-based or stdin-based)
- **Testcases**: Test case data (JSON input/output for function-based)
- **Submissions**: Student submissions with results

## 🔄 Migration from Legacy System

If you have existing stdin-based quizzes, they will continue to work. New quizzes should use function-based format for LeetCode-style execution.

## 🐛 Troubleshooting

### Docker Not Available

If you see "Docker is not available" errors:
1. Ensure Docker Desktop is running
2. Check Docker daemon: `docker ps`
3. Verify Docker Python SDK: `pip install docker==7.0.0`

### Execution Timeout

If submissions timeout:
- Check Docker resource limits
- Increase `DOCKER_TIMEOUT` in `config.py` (not recommended for production)
- Verify Docker containers are being created/destroyed properly

### Test Case Generation

Auto-generated test cases use placeholder expected outputs. For accurate evaluation:
1. Create quiz with sample input/output
2. Manually verify/correct generated test cases in quiz view
3. Or provide a reference solution (future enhancement)

## 📚 Example: Two Sum Problem

See `TWO_SUM_EXAMPLE.md` for a complete walkthrough of creating and solving the Two Sum problem.

## 🚧 Future Enhancements

- Support for C++, Java, JavaScript
- Reference solution for accurate test case generation
- Memory usage tracking
- Execution time per test case
- Batch submission processing
- Code similarity detection

## 📄 License

This project is for educational use.

## 👥 Credits

Built as a LeetCode-style online judge for college coding assessments.
