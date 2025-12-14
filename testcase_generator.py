"""
Testcase generator for automatic test case creation (LeetCode-style function-based).
Generates normal, boundary, and random test cases based on problem constraints.
"""
import random
import re
import json
from typing import List, Dict, Any, Tuple

class TestcaseGenerator:
    """Generates test cases for coding problems similar to Skillrack and LeetCode."""
    
    @staticmethod
    def generate_testcases(problem_statement: str, sample_input: str = None, 
                          sample_output: str = None, constraints: str = None) -> List[Dict[str, Any]]:
        """
        Generate test cases based on problem statement and constraints.
        Legacy method for stdin-based problems.
        
        Args:
            problem_statement: The problem description
            sample_input: Sample input if provided
            sample_output: Sample output if provided
            constraints: Problem constraints
            
        Returns:
            List of testcase dictionaries with input_data, expected_output, and testcase_type
        """
        testcases = []
        
        # Add sample testcase if provided
        if sample_input and sample_output:
            testcases.append({
                'input_data': sample_input.strip(),
                'expected_output': sample_output.strip(),
                'is_sample': True,
                'testcase_type': 'normal'
            })
        
        # Parse constraints to extract number ranges
        number_ranges = TestcaseGenerator._extract_number_ranges(constraints or '')
        
        # Detect problem type
        problem_type = TestcaseGenerator._detect_problem_type(problem_statement)
        
        # Generate test cases based on problem type
        if problem_type == 'array':
            testcases.extend(TestcaseGenerator._generate_array_testcases(number_ranges, sample_input, sample_output))
        elif problem_type == 'string':
            testcases.extend(TestcaseGenerator._generate_string_testcases(number_ranges, sample_input, sample_output))
        elif problem_type == 'number':
            testcases.extend(TestcaseGenerator._generate_number_testcases(number_ranges, sample_input, sample_output))
        else:
            # Generic test cases
            testcases.extend(TestcaseGenerator._generate_generic_testcases(number_ranges, sample_input, sample_output))
        
        return testcases
    
    @staticmethod
    def _extract_number_ranges(constraints: str) -> Dict[str, Tuple[int, int]]:
        """Extract number ranges from constraints text."""
        ranges = {}
        
        # Pattern: "1 <= N <= 100" or "N ranges from 1 to 100"
        patterns = [
            r'(\d+)\s*<=\s*(\w+)\s*<=\s*(\d+)',
            r'(\w+)\s+from\s+(\d+)\s+to\s+(\d+)',
            r'(\w+)\s+range[s]?\s+(\d+)\s+to\s+(\d+)',
            r'(\d+)\s*-\s*(\d+)',  # Simple range like "1-100"
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, constraints, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 3:
                    var_name = match.group(2)
                    min_val = int(match.group(1))
                    max_val = int(match.group(3))
                else:
                    var_name = 'N'
                    min_val = int(match.group(1))
                    max_val = int(match.group(2))
                ranges[var_name] = (min_val, max_val)
        
        # Default ranges if none found
        if not ranges:
            ranges['N'] = (1, 100)
            ranges['n'] = (1, 100)
        
        return ranges
    
    @staticmethod
    def _detect_problem_type(problem_statement: str) -> str:
        """Detect the type of problem from statement."""
        statement_lower = problem_statement.lower()
        
        if any(word in statement_lower for word in ['array', 'list', 'elements', 'index', 'arr']):
            return 'array'
        elif any(word in statement_lower for word in ['string', 'character', 'substring', 'palindrome', 'str']):
            return 'string'
        elif any(word in statement_lower for word in ['number', 'integer', 'digit', 'sum', 'product', 'num']):
            return 'number'
        else:
            return 'generic'
    
    @staticmethod
    def _generate_array_testcases(ranges: Dict[str, Tuple[int, int]], 
                                  sample_input: str = None, sample_output: str = None) -> List[Dict[str, Any]]:
        """Generate 500+ test cases for array problems."""
        testcases = []
        n_range = ranges.get('N', ranges.get('n', (1, 100)))
        
        # Generate 500+ test cases
        # Boundary cases (50)
        for i in range(50):
            size = n_range[0] + (i % 5)
            arr = [random.randint(1, 100) for _ in range(size)]
            testcases.append({
                'input_data': f'{size}\n' + ' '.join(map(str, arr)),
                'expected_output': str(sum(arr)),  # Placeholder
                'is_sample': False,
                'testcase_type': 'boundary'
            })
        
        # Normal cases (350)
        for i in range(350):
            size = random.randint(n_range[0], min(n_range[1], 100))
            arr = [random.randint(1, 1000) for _ in range(size)]
            testcases.append({
                'input_data': f'{size}\n' + ' '.join(map(str, arr)),
                'expected_output': str(max(arr)),  # Placeholder
                'is_sample': False,
                'testcase_type': 'normal'
            })
        
        # Random cases (100)
        for i in range(100):
            size = random.randint(n_range[0], n_range[1])
            arr = [random.randint(1, 10000) for _ in range(size)]
            testcases.append({
                'input_data': f'{size}\n' + ' '.join(map(str, arr)),
                'expected_output': str(min(arr)),  # Placeholder
                'is_sample': False,
                'testcase_type': 'random'
            })
        
        return testcases
    
    @staticmethod
    def _generate_string_testcases(ranges: Dict[str, Tuple[int, int]], 
                                   sample_input: str = None, sample_output: str = None) -> List[Dict[str, Any]]:
        """Generate test cases for string problems."""
        testcases = []
        
        # Boundary: Single character
        testcases.append({
            'input_data': 'a',
            'expected_output': 'a',
            'is_sample': False,
            'testcase_type': 'boundary'
        })
        
        # Normal: Short string
        testcases.append({
            'input_data': 'hello',
            'expected_output': 'olleh',  # Placeholder
            'is_sample': False,
            'testcase_type': 'normal'
        })
        
        # Random: Medium length
        medium_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
        testcases.append({
            'input_data': medium_str,
            'expected_output': medium_str.upper(),  # Placeholder
            'is_sample': False,
            'testcase_type': 'random'
        })
        
        return testcases
    
    @staticmethod
    def _generate_number_testcases(ranges: Dict[str, Tuple[int, int]], 
                                   sample_input: str = None, sample_output: str = None) -> List[Dict[str, Any]]:
        """Generate test cases for number problems."""
        testcases = []
        n_range = ranges.get('N', ranges.get('n', (1, 100)))
        
        # Boundary: Minimum value
        testcases.append({
            'input_data': str(n_range[0]),
            'expected_output': str(n_range[0]),
            'is_sample': False,
            'testcase_type': 'boundary'
        })
        
        # Boundary: Maximum value
        testcases.append({
            'input_data': str(n_range[1]),
            'expected_output': str(n_range[1]),
            'is_sample': False,
            'testcase_type': 'boundary'
        })
        
        # Normal: Middle value
        mid_val = n_range[0] + (n_range[1] - n_range[0]) // 2
        testcases.append({
            'input_data': str(mid_val),
            'expected_output': str(mid_val * 2),  # Placeholder
            'is_sample': False,
            'testcase_type': 'normal'
        })
        
        # Random: Random value in range
        rand_val = random.randint(n_range[0], n_range[1])
        testcases.append({
            'input_data': str(rand_val),
            'expected_output': str(rand_val ** 2),  # Placeholder
            'is_sample': False,
            'testcase_type': 'random'
        })
        
        return testcases
    
    @staticmethod
    def _generate_generic_testcases(ranges: Dict[str, Tuple[int, int]], 
                                    sample_input: str = None, sample_output: str = None) -> List[Dict[str, Any]]:
        """Generate 500+ generic test cases when problem type cannot be determined."""
        testcases = []
        n_range = ranges.get('N', ranges.get('n', (1, 100)))
        
        # Generate 500+ test cases
        # Boundary cases (50)
        for i in range(50):
            val = n_range[0] + (i % 5)
            testcases.append({
                'input_data': str(val),
                'expected_output': str(val),
                'is_sample': False,
                'testcase_type': 'boundary'
            })
        
        # Normal cases (350)
        for i in range(350):
            val = random.randint(n_range[0], min(n_range[1], 1000))
            testcases.append({
                'input_data': str(val),
                'expected_output': str(val),
                'is_sample': False,
                'testcase_type': 'normal'
            })
        
        # Random cases (100)
        for i in range(100):
            val = random.randint(n_range[0], n_range[1])
            testcases.append({
                'input_data': str(val),
                'expected_output': str(val),
                'is_sample': False,
                'testcase_type': 'random'
            })
        
        return testcases


def generate_function_testcases(function_signature: str,
                                sample_input: str = None,
                                sample_output: str = None,
                                constraints: str = None) -> List[Dict[str, Any]]:
    """
    Generate test cases for function-based problems (LeetCode-style).
    
    Args:
        function_signature: Function signature (e.g., "def twoSum(nums: List[int], target: int) -> List[int]:")
        sample_input: Sample input as JSON string (e.g., '[[2,7,11,15], 9]')
        sample_output: Sample output as JSON string (e.g., '[0, 1]')
        constraints: Problem constraints
        
    Returns:
        List of testcase dictionaries with JSON input_data and expected_output
    """
    testcases = []
    
    # Add sample testcase if provided
    if sample_input and sample_output:
        # Validate JSON format
        try:
            json.loads(sample_input)
            json.loads(sample_output)
            testcases.append({
                'input_data': sample_input.strip(),
                'expected_output': sample_output.strip(),
                'is_sample': True,
                'testcase_type': 'normal'
            })
        except json.JSONDecodeError:
            # If not JSON, treat as legacy format
            pass
    
    # Parse function signature to understand parameters
    # Extract parameter types and generate test cases accordingly
    params = _parse_function_signature(function_signature)
    
    # Check parameter types to determine problem type
    param_types = list(params.values())
    has_string_param = any('str' in str(t).lower() for t in param_types)
    has_list_param = any('list' in str(t).lower() for t in param_types)
    
    # Generate additional test cases based on function parameters
    # Always generate 500+ test cases
    if 'nums' in params or 'arr' in params or 'array' in params:
        # Array-based problem (like Two Sum)
        additional = _generate_two_sum_testcases(sample_input, sample_output, constraints)
        testcases.extend(additional)
    elif has_string_param and ('isValid' in function_signature or 'valid' in function_signature.lower() or 'parentheses' in function_signature.lower()):
        # String-based problem like Valid Parentheses
        additional = _generate_valid_parentheses_testcases(sample_input, sample_output, constraints)
        testcases.extend(additional)
    elif has_string_param:
        # Generic string-based problem
        additional = _generate_string_function_testcases(params, sample_input, sample_output, constraints)
        testcases.extend(additional)
    else:
        # Generic function test cases
        additional = _generate_generic_function_testcases(params, sample_input, sample_output)
        testcases.extend(additional)
    
    # Ensure we have at least 500 test cases
    while len(testcases) < 500:
        # Duplicate and mutate some existing test cases
        base_tc = random.choice(testcases)
        mutated_input = _mutate_input(json.loads(base_tc['input_data']), mutation_level=0.3)
        testcases.append({
            'input_data': json.dumps(mutated_input),
            'expected_output': base_tc['expected_output'],
            'is_sample': False,
            'testcase_type': 'random'
        })
    
    return testcases


def _parse_function_signature(signature: str) -> Dict[str, str]:
    """Parse function signature to extract parameter names and types."""
    params = {}
    try:
        # Extract parameters from signature
        # e.g., "def twoSum(nums: List[int], target: int) -> List[int]:"
        if '(' in signature and ')' in signature:
            param_part = signature.split('(')[1].split(')')[0]
            for param in param_part.split(','):
                param = param.strip()
                if ':' in param:
                    name, type_hint = param.split(':', 1)
                    params[name.strip()] = type_hint.strip()
    except:
        pass
    return params


def _generate_two_sum_testcases(sample_input: str = None, 
                                sample_output: str = None,
                                constraints: str = None) -> List[Dict[str, Any]]:
    """Generate 500+ test cases for Two Sum problem."""
    testcases = []
    
    # Parse constraints to get array size limits
    min_size = 2
    max_size = 1000
    min_val = -10**9
    max_val = 10**9
    
    if constraints:
        import re
        size_match = re.search(r'(\d+)\s*<=\s*nums\.length\s*<=\s*(\d+)', constraints)
        if size_match:
            min_size = int(size_match.group(1))
            max_size = int(size_match.group(2))
        
        val_match = re.search(r'(-?\d+)\s*<=\s*nums\[i\]\s*<=\s*(-?\d+)', constraints)
        if val_match:
            min_val = int(val_match.group(1))
            max_val = int(val_match.group(2))
    
    # Generate 500+ test cases
    # 1. Boundary cases (50)
    for i in range(50):
        # Small arrays (ensure size >= 2 for two sum)
        size = max(min_size, min_size + (i % 5))
        if size < 2:
            size = 2
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        # Ensure there's a valid pair
        idx1, idx2 = random.sample(range(size), 2)
        target = arr[idx1] + arr[idx2]
        expected = sorted([idx1, idx2])
        testcases.append({
            'input_data': json.dumps([arr, target]),
            'expected_output': json.dumps(expected),
            'is_sample': False,
            'testcase_type': 'boundary'
        })
    
    # 2. Normal cases (300)
    for i in range(300):
        size = random.randint(max(min_size, 2), min(max_size, 100))
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        # Ensure there's a valid pair
        idx1, idx2 = random.sample(range(size), 2)
        target = arr[idx1] + arr[idx2]
        expected = sorted([idx1, idx2])
        testcases.append({
            'input_data': json.dumps([arr, target]),
            'expected_output': json.dumps(expected),
            'is_sample': False,
            'testcase_type': 'normal'
        })
    
    # 3. Large arrays (100)
    for i in range(100):
        size = random.randint(max(min_size, max_size // 2, 2), max_size)
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        # Ensure there's a valid pair
        idx1, idx2 = random.sample(range(size), 2)
        target = arr[idx1] + arr[idx2]
        expected = sorted([idx1, idx2])
        testcases.append({
            'input_data': json.dumps([arr, target]),
            'expected_output': json.dumps(expected),
            'is_sample': False,
            'testcase_type': 'random'
        })
    
    # 4. Edge cases (50)
    # Duplicate values
    for i in range(25):
        size = random.randint(max(min_size, 2), 50)
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        # Add duplicates
        val = random.choice(arr)
        arr.append(val)
        target = val * 2
        # Find indices
        indices = [i for i, x in enumerate(arr) if x == val]
        if len(indices) >= 2:
            expected = sorted(indices[:2])
            testcases.append({
                'input_data': json.dumps([arr, target]),
                'expected_output': json.dumps(expected),
                'is_sample': False,
                'testcase_type': 'boundary'
            })
    
    # Negative numbers
    for i in range(25):
        size = random.randint(max(min_size, 2), 50)
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        idx1, idx2 = random.sample(range(size), 2)
        target = arr[idx1] + arr[idx2]
        expected = sorted([idx1, idx2])
        testcases.append({
            'input_data': json.dumps([arr, target]),
            'expected_output': json.dumps(expected),
            'is_sample': False,
            'testcase_type': 'boundary'
        })
    
    return testcases


def _generate_valid_parentheses_testcases(sample_input: str = None,
                                          sample_output: str = None,
                                          constraints: str = None) -> List[Dict[str, Any]]:
    """Generate 500+ test cases for Valid Parentheses problem."""
    testcases = []
    
    # Parse constraints
    min_len = 1
    max_len = 10000
    if constraints:
        len_match = re.search(r'(\d+)\s*<=\s*s\.length\s*<=\s*(\d+)', constraints)
        if len_match:
            min_len = int(len_match.group(1))
            max_len = int(len_match.group(2))
    
    brackets = ['(', ')', '[', ']', '{', '}']
    
    def is_valid(s):
        """Helper to check if parentheses string is valid."""
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        for char in s:
            if char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
            else:
                stack.append(char)
        return len(stack) == 0
    
    def generate_valid_string(length):
        """Generate a valid parentheses string."""
        if length % 2 != 0:
            length -= 1
        result = []
        stack = []
        pairs = [('(', ')'), ('[', ']'), ('{', '}')]
        for _ in range(length // 2):
            if random.random() < 0.5 and stack:
                # Close a bracket
                result.append(stack.pop())
            else:
                # Open a bracket
                pair = random.choice(pairs)
                result.append(pair[0])
                stack.append(pair[1])
        # Close remaining brackets
        while stack:
            result.append(stack.pop())
        return ''.join(result)
    
    def generate_invalid_string(length):
        """Generate an invalid parentheses string."""
        if length < 2:
            return random.choice(brackets)
        # Mix valid and invalid patterns
        if random.random() < 0.5:
            # Unmatched opening
            s = generate_valid_string(length - 2)
            return s + random.choice(['(', '[', '{'])
        else:
            # Unmatched closing
            s = generate_valid_string(length - 2)
            return random.choice([')', ']', '}']) + s
    
    # Boundary cases (50)
    for i in range(50):
        length = min_len + (i % 10)
        if i % 2 == 0:
            s = generate_valid_string(length)
            expected = True
        else:
            s = generate_invalid_string(length)
            expected = False
        testcases.append({
            'input_data': json.dumps([s]),
            'expected_output': json.dumps(expected),
            'is_sample': False,
            'testcase_type': 'boundary'
        })
    
    # Normal cases (350)
    for i in range(350):
        length = random.randint(min_len, min(max_len, 100))
        if i % 2 == 0:
            s = generate_valid_string(length)
            expected = True
        else:
            s = generate_invalid_string(length)
            expected = False
        testcases.append({
            'input_data': json.dumps([s]),
            'expected_output': json.dumps(expected),
            'is_sample': False,
            'testcase_type': 'normal'
        })
    
    # Large cases (100)
    for i in range(100):
        length = random.randint(max(min_len, max_len // 2), max_len)
        if i % 2 == 0:
            s = generate_valid_string(length)
            expected = True
        else:
            s = generate_invalid_string(length)
            expected = False
        testcases.append({
            'input_data': json.dumps([s]),
            'expected_output': json.dumps(expected),
            'is_sample': False,
            'testcase_type': 'random'
        })
    
    return testcases


def _generate_string_function_testcases(params: Dict[str, str],
                                        sample_input: str = None,
                                        sample_output: str = None,
                                        constraints: str = None) -> List[Dict[str, Any]]:
    """Generate 500+ test cases for generic string-based problems."""
    testcases = []
    
    # Parse constraints
    min_len = 1
    max_len = 1000
    if constraints:
        len_match = re.search(r'(\d+)\s*<=\s*\w+\.length\s*<=\s*(\d+)', constraints)
        if len_match:
            min_len = int(len_match.group(1))
            max_len = int(len_match.group(2))
    
    # Parse sample input
    sample_str = None
    if sample_input:
        try:
            sample_data = json.loads(sample_input)
            if isinstance(sample_data, list) and len(sample_data) > 0:
                sample_str = sample_data[0] if isinstance(sample_data[0], str) else str(sample_data[0])
            elif isinstance(sample_data, str):
                sample_str = sample_data
        except:
            pass
    
    # Generate 500+ test cases
    # Boundary cases (50)
    for i in range(50):
        length = min_len + (i % 10)
        if sample_str:
            # Use sample as template
            s = ''.join(random.choices(sample_str if sample_str else 'abcdefghijklmnopqrstuvwxyz', k=length))
        else:
            s = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
        testcases.append({
            'input_data': json.dumps([s]),
            'expected_output': sample_output or json.dumps(s),
            'is_sample': False,
            'testcase_type': 'boundary'
        })
    
    # Normal cases (350)
    for i in range(350):
        length = random.randint(min_len, min(max_len, 100))
        if sample_str:
            s = ''.join(random.choices(sample_str if sample_str else 'abcdefghijklmnopqrstuvwxyz', k=length))
        else:
            s = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
        testcases.append({
            'input_data': json.dumps([s]),
            'expected_output': sample_output or json.dumps(s),
            'is_sample': False,
            'testcase_type': 'normal'
        })
    
    # Random cases (100)
    for i in range(100):
        length = random.randint(max(min_len, max_len // 2), max_len)
        if sample_str:
            s = ''.join(random.choices(sample_str if sample_str else 'abcdefghijklmnopqrstuvwxyz', k=length))
        else:
            s = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
        testcases.append({
            'input_data': json.dumps([s]),
            'expected_output': sample_output or json.dumps(s),
            'is_sample': False,
            'testcase_type': 'random'
        })
    
    return testcases


def _generate_generic_function_testcases(params: Dict[str, str],
                                         sample_input: str = None,
                                         sample_output: str = None) -> List[Dict[str, Any]]:
    """Generate 500+ generic test cases for function-based problems."""
    testcases = []
    
    # Try to parse sample input to understand format
    sample_input_data = None
    if sample_input:
        try:
            sample_input_data = json.loads(sample_input)
        except:
            pass
    
    # Generate 500+ test cases based on parameter types
    # Boundary cases (50)
    for i in range(50):
        if sample_input_data is not None:
            # Use sample as template
            test_input = _mutate_input(sample_input_data, mutation_level=0.1)
            testcases.append({
                'input_data': json.dumps(test_input),
                'expected_output': sample_output or json.dumps(test_input),  # Placeholder
                'is_sample': False,
                'testcase_type': 'boundary'
            })
        else:
            # Generic fallback
            testcases.append({
                'input_data': json.dumps([i]),
                'expected_output': json.dumps([i]),
                'is_sample': False,
                'testcase_type': 'boundary'
            })
    
    # Normal cases (350)
    for i in range(350):
        if sample_input_data is not None:
            test_input = _mutate_input(sample_input_data, mutation_level=0.5)
            testcases.append({
                'input_data': json.dumps(test_input),
                'expected_output': sample_output or json.dumps(test_input),  # Placeholder
                'is_sample': False,
                'testcase_type': 'normal'
            })
        else:
            testcases.append({
                'input_data': json.dumps([random.randint(1, 1000)]),
                'expected_output': json.dumps([random.randint(1, 1000)]),
                'is_sample': False,
                'testcase_type': 'normal'
            })
    
    # Random cases (100)
    for i in range(100):
        if sample_input_data is not None:
            test_input = _mutate_input(sample_input_data, mutation_level=1.0)
            testcases.append({
                'input_data': json.dumps(test_input),
                'expected_output': sample_output or json.dumps(test_input),  # Placeholder
                'is_sample': False,
                'testcase_type': 'random'
            })
        else:
            testcases.append({
                'input_data': json.dumps([random.randint(1, 10000)]),
                'expected_output': json.dumps([random.randint(1, 10000)]),
                'is_sample': False,
                'testcase_type': 'random'
            })
    
    return testcases


def _mutate_input(sample_input: Any, mutation_level: float = 0.5) -> Any:
    """Mutate sample input to create new test cases."""
    import copy
    mutated = copy.deepcopy(sample_input)
    
    if isinstance(mutated, list):
        if len(mutated) > 0:
            if isinstance(mutated[0], (int, float)):
                # List of numbers
                for i in range(len(mutated)):
                    if random.random() < mutation_level:
                        mutated[i] = random.randint(-1000, 1000)
            elif isinstance(mutated[0], list):
                # Nested list
                for sublist in mutated:
                    _mutate_input(sublist, mutation_level)
        # Randomly change size
        if random.random() < mutation_level * 0.3:
            new_size = max(1, len(mutated) + random.randint(-2, 5))
            if new_size > len(mutated):
                mutated.extend([random.randint(1, 100) for _ in range(new_size - len(mutated))])
            elif new_size < len(mutated):
                mutated = mutated[:new_size]
    elif isinstance(mutated, (int, float)):
        mutated = random.randint(int(mutated * 0.5), int(mutated * 1.5)) if mutated > 0 else random.randint(-1000, 1000)
    elif isinstance(mutated, str):
        # For strings, generate similar length
        mutated = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=len(mutated)))
    
    return mutated
