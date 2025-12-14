"""
LeetCode-style Online Judge Engine for Belfry.
Server-side execution engine with Docker-based sandboxing.

This module implements a true LeetCode-style execution system:
- Function-based problems (not stdin-only)
- Docker container isolation
- Runtime and memory limits
- Strict correctness checking
- Deterministic results
- No partial marking
"""
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
    docker = None

import os
import tempfile
import shutil
import json
import time
import traceback
from typing import Dict, Any, List, Optional, Tuple
from config import Config

class OnlineJudge:
    """
    LeetCode-style online judge for secure code execution.
    
    Each submission runs in an isolated Docker container with:
    - Execution timeout (1-2 seconds)
    - Memory limit (256MB)
    - CPU limit
    - No network access
    - No filesystem access outside container
    """
    
    def __init__(self):
        """Initialize Docker client for code execution."""
        if not DOCKER_AVAILABLE:
            print("ERROR: Docker Python library not installed.")
            print("Please install it with: pip install docker==7.0.0")
            self.client = None
            self.docker_available = False
            return
            
        try:
            import platform
            
            # On Windows, use named pipe directly
            if platform.system() == 'Windows':
                # Windows Docker Desktop uses named pipe
                base_url = 'npipe:////./pipe/docker_engine'
                self.client = docker.DockerClient(base_url=base_url, timeout=10)
            else:
                # Linux/Mac - use default connection
                self.client = docker.from_env()
            
            # Test connection
            self.client.ping()
            self.docker_available = True
            print("Docker connection successful!")
            
        except docker.errors.APIError as e:
            print(f"ERROR: Docker API error: {e}")
            print("WARNING: Code execution requires Docker. Please ensure Docker Desktop is running.")
            self.client = None
            self.docker_available = False
        except Exception as e:
            error_msg = str(e)
            if 'http+docker' in error_msg:
                print("ERROR: Docker connection issue detected.")
                print("This might be due to environment variables or Docker Desktop configuration.")
                print("SOLUTION: Try restarting Docker Desktop, then restart the Flask app.")
            else:
                print(f"ERROR: Docker not available: {e}")
            print("WARNING: Code execution requires Docker. Please ensure Docker Desktop is running.")
            self.client = None
            self.docker_available = False
    
    def execute_submission(self, 
                          user_code: str,
                          function_signature: str,
                          testcases: List[Dict[str, Any]],
                          language: str = 'python',
                          timeout: float = 2.0,
                          memory_limit: str = '256m') -> Dict[str, Any]:
        """
        Execute a submission against multiple test cases (LeetCode-style).
        
        Args:
            user_code: User's solution code (function implementation)
            function_signature: Function signature (e.g., "def twoSum(nums: List[int], target: int) -> List[int]:")
            testcases: List of test cases, each with 'input_data' (JSON) and 'expected_output' (JSON)
            language: Programming language (currently only 'python')
            timeout: Execution timeout per test case in seconds
            memory_limit: Memory limit for container (e.g., '256m')
            
        Returns:
            Dictionary with:
            - status: 'pass' or 'fail'
            - passed_count: Number of test cases passed
            - total_count: Total number of test cases
            - error_type: 'runtime_error', 'timeout', 'wrong_answer', 'syntax_error', or None
            - error_message: Error message if failed
            - execution_time: Total execution time
            - testcase_results: List of results for each test case
        """
        if not self.docker_available:
            return {
                'status': 'fail',
                'passed_count': 0,
                'total_count': len(testcases),
                'error_type': 'system_error',
                'error_message': 'Docker is not available. Code execution requires Docker.',
                'execution_time': 0,
                'testcase_results': []
            }
        
        results = {
            'status': 'fail',
            'passed_count': 0,
            'total_count': len(testcases),
            'error_type': None,
            'error_message': None,
            'execution_time': 0,
            'testcase_results': []
        }
        
        # Check syntax first (quick check)
        syntax_check = self._check_syntax(user_code, language)
        if not syntax_check['valid']:
            results['error_type'] = 'syntax_error'
            results['error_message'] = syntax_check['error']
            results['testcase_results'] = [
                {
                    'passed': False, 
                    'error': syntax_check['error'], 
                    'error_type': 'syntax_error',
                    'input': tc.get('input_data', ''),
                    'expected': tc.get('expected_output', ''),
                    'actual': None
                }
                for tc in testcases
            ]
            return results
        
        # Execute test cases - STOP ON FIRST FAILURE
        start_time = time.time()
        all_passed = True
        
        for idx, testcase in enumerate(testcases):
            testcase_result = self._execute_testcase(
                user_code=user_code,
                function_signature=function_signature,
                testcase=testcase,
                language=language,
                timeout=timeout,
                memory_limit=memory_limit,
                testcase_index=idx
            )
            
            results['testcase_results'].append(testcase_result)
            
            if testcase_result['passed']:
                results['passed_count'] += 1
            else:
                # FIRST FAILURE - stop immediately, mark as FAIL
                all_passed = False
                if not results['error_type']:
                    results['error_type'] = testcase_result.get('error_type', 'wrong_answer')
                    results['error_message'] = testcase_result.get('error', 'Test case failed')
                
                # Fill remaining test cases as not executed
                remaining_count = len(testcases) - idx - 1
                for _ in range(remaining_count):
                    results['testcase_results'].append({
                        'passed': False,
                        'error': 'Execution stopped - previous test case failed',
                        'error_type': 'execution_stopped',
                        'input': '',
                        'expected': '',
                        'actual': None
                    })
                break  # STOP - don't run remaining test cases
        
        results['execution_time'] = time.time() - start_time
        results['status'] = 'pass' if all_passed else 'fail'
        
        return results
    
    def _check_syntax(self, code: str, language: str) -> Dict[str, Any]:
        """Check code syntax before execution."""
        if language != 'python':
            return {'valid': False, 'error': f'Language {language} not supported'}
        
        try:
            compile(code, '<string>', 'exec')
            return {'valid': True, 'error': None}
        except SyntaxError as e:
            return {
                'valid': False,
                'error': f'Syntax Error: Line {e.lineno}: {str(e)}'
            }
    
    def _execute_testcase(self,
                          user_code: str,
                          function_signature: str,
                          testcase: Dict[str, Any],
                          language: str,
                          timeout: float,
                          memory_limit: str,
                          testcase_index: int) -> Dict[str, Any]:
        """
        Execute a single test case in Docker container.
        
        Returns:
            Dictionary with 'passed', 'error', 'error_type', 'execution_time'
        """
        if language != 'python':
            return {
                'passed': False,
                'error': f'Language {language} not supported',
                'error_type': 'unsupported_language'
            }
        
        # Create driver code
        driver_code = self._create_driver_code(user_code, function_signature, testcase)
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        code_file = os.path.join(temp_dir, 'solution.py')
        
        try:
            # Write driver code to file
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(driver_code)
            
            # Execute in Docker container
            container = None
            try:
                # Run container in detached mode for better control
                container = self.client.containers.run(
                    Config.DOCKER_IMAGE,
                    command=['python', 'solution.py'],
                    volumes={temp_dir: {'bind': '/app', 'mode': 'ro'}},
                    working_dir='/app',
                    mem_limit=memory_limit,
                    cpu_period=100000,
                    cpu_quota=50000,  # 50% CPU
                    network_disabled=True,
                    remove=False,
                    detach=True
                )
                
                # Wait for container to finish with timeout
                try:
                    exit_code = container.wait(timeout=int(timeout) + 1)
                except Exception as wait_error:
                    # Timeout occurred
                    container.stop(timeout=1)
                    container.remove(force=True)
                    return {
                        'passed': False,
                        'error': 'Time Limit Exceeded',
                        'error_type': 'timeout',
                        'output': ''
                    }
                
                # Get logs (stdout and stderr separately)
                logs = container.logs(stdout=True, stderr=False)
                errors = container.logs(stdout=False, stderr=True)
                
                output = logs.decode('utf-8').strip() if logs else ''
                error = errors.decode('utf-8').strip() if errors else ''
                
                # Clean up container
                container.remove(force=True)
                container = None
                
                # PRIORITY: Check output correctness FIRST, not error status
                # This fixes the bug where correct output is marked as runtime error
                # Only treat as error if output is invalid or doesn't match expected
                
                # Parse JSON output
                try:
                    result = json.loads(output)
                    expected = json.loads(testcase['expected_output'])
                    
                    # Compare results (strict equality)
                    if self._compare_results(result, expected):
                        # Output matches! This is a PASS, regardless of stderr or exit_code
                        # (stderr might contain warnings, but if output is correct, it's fine)
                        return {
                            'passed': True,
                            'error': None,
                            'error_type': None,
                            'output': output,
                            'input': testcase.get('input_data', ''),
                            'expected': json.dumps(expected),
                            'actual': json.dumps(result)
                        }
                    else:
                        return {
                            'passed': False,
                            'error': 'Wrong Answer',
                            'error_type': 'wrong_answer',
                            'output': output,
                            'input': testcase.get('input_data', ''),
                            'expected': json.dumps(expected),
                            'actual': json.dumps(result)
                        }
                except json.JSONDecodeError:
                    # Output is not valid JSON - check if there was a real runtime error
                    if exit_code != 0 or error:
                        # Real runtime error occurred
                        return {
                            'passed': False,
                            'error': f'Runtime Error: {error}' if error else 'Runtime Error',
                            'error_type': 'runtime_error',
                            'output': output,
                            'input': testcase.get('input_data', ''),
                            'expected': testcase.get('expected_output', ''),
                            'actual': output
                        }
                    else:
                        # Output format is invalid but no runtime error
                        return {
                            'passed': False,
                            'error': f'Invalid output format: {output}',
                            'error_type': 'runtime_error',
                            'output': output,
                            'input': testcase.get('input_data', ''),
                            'expected': testcase.get('expected_output', ''),
                            'actual': output
                        }
                
            except docker.errors.ContainerError as e:
                error_msg = e.stderr.decode('utf-8') if hasattr(e, 'stderr') and e.stderr else str(e)
                if container:
                    try:
                        container.remove(force=True)
                    except:
                        pass
                return {
                    'passed': False,
                    'error': f'Runtime Error: {error_msg}',
                    'error_type': 'runtime_error',
                    'output': '',
                    'input': testcase.get('input_data', ''),
                    'expected': testcase.get('expected_output', ''),
                    'actual': ''
                }
            except Exception as e:
                # Clean up container on any error
                if container:
                    try:
                        container.stop(timeout=1)
                        container.remove(force=True)
                    except:
                        pass
                
                # Check if it's a timeout
                if 'timeout' in str(e).lower() or 'timed out' in str(e).lower() or isinstance(e, TimeoutError):
                    return {
                        'passed': False,
                        'error': 'Time Limit Exceeded',
                        'error_type': 'timeout',
                        'output': '',
                        'input': testcase.get('input_data', ''),
                        'expected': testcase.get('expected_output', ''),
                        'actual': ''
                    }
                else:
                    error_msg = str(e)
                    return {
                        'passed': False,
                        'error': f'Execution Error: {error_msg}',
                        'error_type': 'runtime_error',
                        'output': '',
                        'input': testcase.get('input_data', ''),
                        'expected': testcase.get('expected_output', ''),
                        'actual': ''
                    }
                        
        finally:
            # Cleanup temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def _create_driver_code(self, user_code: str, function_signature: str, testcase: Dict[str, Any]) -> str:
        """
        Create driver code that wraps user code and executes test case.
        
        Driver template structure:
        1. Import necessary modules
        2. User's code (function implementation)
        3. Parse test case input (JSON)
        4. Call user's function
        5. Serialize result to JSON
        6. Print result
        """
        # Parse function signature to extract function name
        func_name = self._extract_function_name(function_signature)
        
        # Parse input data (JSON string)
        input_data_str = testcase['input_data']
        
        # Create driver template
        # Use repr() to safely escape the JSON string
        input_data_repr = repr(input_data_str)
        
        driver = f"""# Driver code for LeetCode-style execution
import json
from typing import List, Dict, Tuple, Optional

# User's solution code
{user_code}

# Test case execution
try:
    # Parse input arguments from JSON string
    input_data = json.loads({input_data_repr})
    
    # Call user's function
    # Handle both single argument and multiple arguments
    if isinstance(input_data, list) and len(input_data) > 0:
        # Multiple arguments passed as list
        result = {func_name}(*input_data)
        # For in-place modification, check if first argument was modified
        if result is None and isinstance(input_data[0], list):
            result = input_data[0]
    elif isinstance(input_data, dict):
        # Named arguments passed as dict
        result = {func_name}(**input_data)
    else:
        # Single argument
        result = {func_name}(input_data)
        # For in-place modification, check if input was modified
        if result is None and isinstance(input_data, list):
            result = input_data
    
    # Serialize and print result
    print(json.dumps(result))
    
except Exception as e:
    import traceback
    traceback.print_exc()
    raise
"""
        return driver
    
    def _create_batch_driver_code(self, user_code: str, function_signature: str, testcases: List[Dict[str, Any]]) -> str:
        """Create driver code that executes multiple test cases in one run."""
        func_name = self._extract_function_name(function_signature)
        
        testcase_code = "testcases = [\n"
        for tc in testcases:
            input_repr = repr(tc['input_data'])
            expected_repr = repr(tc['expected_output'])
            testcase_code += f"    ({input_repr}, {expected_repr}),\n"
        testcase_code += "]\n"
        
        driver = f"""# Batch driver code
import json
from typing import List, Dict, Tuple, Optional

# User's solution code
{user_code}

# Execute all test cases
{testcase_code}
results = []
for input_data_str, expected_str in testcases:
    try:
        input_data = json.loads(input_data_str)
        if isinstance(input_data, list) and len(input_data) > 0:
            result = {func_name}(*input_data)
            if result is None and isinstance(input_data[0], list):
                result = input_data[0]
        elif isinstance(input_data, dict):
            result = {func_name}(**input_data)
        else:
            result = {func_name}(input_data)
            if result is None and isinstance(input_data, list):
                result = input_data
        results.append(json.dumps(result))
    except Exception as e:
        results.append(json.dumps({{"error": str(e)}}))

# Print one result per line
for r in results:
    print(r)
"""
        return driver
    
    def _extract_function_name(self, function_signature: str) -> str:
        """Extract function name from signature."""
        # e.g., "def twoSum(nums: List[int], target: int) -> List[int]:" -> "twoSum"
        if 'def ' in function_signature:
            func_part = function_signature.split('def ')[1].split('(')[0].strip()
            return func_part
        return 'solution'
    
    def _compare_results(self, actual: Any, expected: Any) -> bool:
        """
        Compare actual and expected results with strict equality.
        Handles lists, dicts, primitives, etc.
        """
        # Direct comparison for primitives
        if type(actual) != type(expected):
            return False
        
        # List comparison (order matters)
        if isinstance(actual, list):
            if len(actual) != len(expected):
                return False
            return all(self._compare_results(a, e) for a, e in zip(actual, expected))
        
        # Dict comparison
        if isinstance(actual, dict):
            if set(actual.keys()) != set(expected.keys()):
                return False
            return all(self._compare_results(actual[k], expected[k]) for k in actual.keys())
        
        # Primitive comparison
        return actual == expected

