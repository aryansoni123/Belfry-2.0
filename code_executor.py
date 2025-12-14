"""
Code execution module using Docker for secure code execution.
Similar to Skillrack and LeetCode execution model.
"""
import docker
import os
import tempfile
import shutil
from typing import Dict, Any, Optional
from config import Config

class CodeExecutor:
    """Execute code in Docker containers for security."""
    
    def __init__(self):
        """Initialize Docker client."""
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"Warning: Docker not available: {e}")
            self.client = None
    
    def execute_python(self, code: str, input_data: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Execute Python code in Docker container.
        
        Args:
            code: Python code to execute
            input_data: Input data for the program
            timeout: Execution timeout in seconds
            
        Returns:
            Dictionary with 'success', 'output', 'error', 'execution_time'
        """
        if not self.client:
            # Fallback to local execution if Docker not available
            return self._execute_local(code, input_data)
        
        # Create temporary directory for code
        temp_dir = tempfile.mkdtemp()
        code_file = os.path.join(temp_dir, 'solution.py')
        
        try:
            # Write code to file
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Prepare input
            input_file = os.path.join(temp_dir, 'input.txt')
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(input_data)
            
            # Execute in Docker container with input
            container = self.client.containers.run(
                Config.DOCKER_IMAGE,
                command='python solution.py',
                volumes={temp_dir: {'bind': '/app', 'mode': 'rw'}},
                working_dir='/app',
                mem_limit='128m',
                cpu_period=100000,
                cpu_quota=50000,  # 50% CPU
                network_disabled=True,
                remove=False,
                detach=False,
                stdin_open=True,
                stdout=True,
                stderr=True,
                timeout=timeout + 2
            )
            
            # Get container output
            container.reload()
            logs = container.logs(stdout=True, stderr=False)
            errors = container.logs(stdout=False, stderr=True)
            
            # Clean up container
            try:
                container.remove()
            except:
                pass
            
            # Parse output
            output = logs.decode('utf-8') if logs else ''
            error = errors.decode('utf-8') if errors else ''
            
            if error:
                return {
                    'success': False,
                    'output': output.strip(),
                    'error': f'Runtime Error: {error.strip()}',
                    'execution_time': 0
                }
            
            return {
                'success': True,
                'output': output.strip(),
                'error': None,
                'execution_time': 0
            }
            
        except docker.errors.ContainerError as e:
            error_msg = e.stderr.decode('utf-8') if hasattr(e, 'stderr') and e.stderr else str(e)
            try:
                if hasattr(e, 'container'):
                    e.container.remove()
            except:
                pass
            return {
                'success': False,
                'output': '',
                'error': f'Runtime Error: {error_msg}',
                'execution_time': 0
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Execution Error: {str(e)}',
                'execution_time': 0
            }
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def _execute_local(self, code: str, input_data: str) -> Dict[str, Any]:
        """
        Fallback local execution if Docker is not available.
        WARNING: This is less secure and should only be used in development.
        """
        import sys
        from io import StringIO
        import traceback
        
        # Capture stdout
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = captured_output = StringIO()
        sys.stderr = captured_error = StringIO()
        
        try:
            # Prepare input
            input_lines = input_data.strip().split('\n')
            input_index = [0]
            
            def mock_input(prompt=""):
                if input_index[0] < len(input_lines):
                    result = input_lines[input_index[0]]
                    input_index[0] += 1
                    return result
                return ""
            
            # Create execution namespace
            exec_namespace = {
                '__builtins__': {
                    'print': print,
                    'input': mock_input,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'sorted': sorted,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'abs': abs,
                    'round': round,
                    'enumerate': enumerate,
                    'zip': zip,
                    'map': map,
                    'filter': filter,
                    'any': any,
                    'all': all,
                    'bool': bool,
                    'chr': chr,
                    'ord': ord,
                    'bin': bin,
                    'hex': hex,
                    'oct': oct,
                    'pow': pow,
                    'divmod': divmod,
                }
            }
            
            # Check syntax first
            compile(code, '<string>', 'exec')
            
            # Execute code
            exec(code, exec_namespace)
            
            # Get output
            output = captured_output.getvalue()
            error = captured_error.getvalue()
            
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            if error:
                return {
                    'success': False,
                    'output': '',
                    'error': f'Runtime Error: {error.strip()}',
                    'execution_time': 0
                }
            
            return {
                'success': True,
                'output': output.strip(),
                'error': None,
                'execution_time': 0
            }
            
        except SyntaxError as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            return {
                'success': False,
                'output': '',
                'error': f'Syntax Error: Line {e.lineno}: {str(e)}',
                'execution_time': 0
            }
        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            return {
                'success': False,
                'output': '',
                'error': f'Runtime Error: {str(e)}',
                'execution_time': 0
            }

