# Belfry - LeetCode-Style Online Coding Assessment Platform

A secure, server-side online judge for coding practice and assessments, built with Flask and Docker. Execution behavior is functionally identical to LeetCode, while maintaining Belfry's custom UI/UX.

## 🎯 Key Features

- **LeetCode-Style Execution**: Function-based problems with server-side execution
- **Docker Sandboxing**: Each submission runs in an isolated container
- **Strict Evaluation**: PASS only if ALL test cases pass (no partial marking)
- **Hidden Test Cases**: Sample test cases visible, hidden test cases for evaluation
- **Role-Based Access**: Teacher (Admin) and Student roles
- **Auto Test Case Generation**: Automatic generation of normal, boundary, and random test cases
- **One-Command Orchestration**: Professional setup via Docker Compose

## 🏗️ Architecture

### Dual-Container System

The platform is architected using two distinct Docker environments for maximum security and ease of deployment:

1.  **Web Application (The Brain)**: Runs the Flask server, manages the database, and handles the UI. It orchestrates the execution by talking to the Docker daemon.
2.  **Execution Sandbox (The Muscle)**: A minimal `python:3.13-slim` image used exclusively for running untrusted student code. This image is pre-built to ensure instant startup times for test cases.

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

## 🚀 Recruiter-Ready Setup (Recommended)

The easiest way to see Belfry in action is using **Docker Compose**. This sets up the web server, initializes the database with sample data, and builds the execution sandbox automatically.

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/aryansoni123/Belfry-2.0.git
cd Belfry-2.0

# Start everything
docker-compose up --build
```

The application will be available at `http://localhost:5000`.

**Default Accounts:**
- **Teacher**: username=`teacher`, password=`teacher123`
- **Student**: username=`student`, password=`student123`

---

## 🛠️ Manual Installation (Development)

### Prerequisites

- Python 3.13+
- Docker Desktop (Required for code execution)
- pip

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database

```bash
python init_db.py --seed
```

### Step 3: Run the Application

```bash
python app.py
```

---

## 📝 Creating a Quiz (Teacher)

1. Login as teacher -> "Create Quiz"
2. Select **"Function-based (LeetCode-style)"**
3. Enter function signature: `def twoSum(nums: List[int], target: int) -> List[int]:`
4. Enter problem details and sample input/output in JSON format.

**Sample Input Format (JSON):** `[[2,7,11,15], 9]`
**Sample Output Format (JSON):** `[0, 1]`

## 💻 Solving a Quiz (Student)

1. Login as student -> Select a quiz.
2. Implement the exact function signature provided.
3. Use **"Run"** for quick feedback on sample cases.
4. Use **"Submit"** for final evaluation against hidden cases.

---

## 📁 Project Structure

```
belfry/
├── app.py                 # Main Flask application
├── docker-compose.yml     # Orchestration for App + Sandbox
├── Dockerfile             # Web Application image
├── Dockerfile.sandbox     # Isolated execution image
├── judge.py               # LeetCode-style execution engine
├── config.py              # Configuration & Resource Limits
├── models.py              # Database models
├── templates/             # UI Templates (Tailwind CSS)
└── instance/              # SQLite database
```

## 🧪 Execution Details

### How Code Execution Works

1.  **Syntax Check**: Code is compiled to check for syntax errors before spawning a container.
2.  **Container Spawning**: `judge.py` uses the Docker SDK to start a container from the `belfry-sandbox` image.
3.  **Driver Injection**: A driver script is injected that imports the user's code, parses JSON inputs, calls the function, and captures the result.
4.  **Strict Comparison**: Results are compared using deep equality.

### Security Notes

- **Network Disabled**: Containers have no internet access.
- **Read-Only Volume**: The code is mounted as read-only.
- **Resource Constraints**: Strict memory and CPU quotas prevent "fork bombs" or resource exhaustion.

## 🎨 UI/UX

- **Modern Aesthetic**: Built with Tailwind CSS.
- **Interactive Feedback**: Real-time status updates during code execution.
- **Clean Design**: Optimized for academic and assessment environments.

## 📄 License

This project is for educational use and technical demonstration.

## 👥 Credits

Built as a LeetCode-style online judge for coding practice and assessments.
