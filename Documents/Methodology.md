# Methodology: Algorithms Implemented in Belfry

This document details the core algorithms that power Belfry’s secure, LeetCode-style coding assessment platform. It focuses on how code is executed, how test cases are generated, and how submissions are evaluated and persisted, referencing the main implementation files (`judge.py`, `testcase_generator.py`, `student/routes.py`, `teacher/routes.py`, `models.py`).

## 1. Execution Engine Algorithms (`judge.py`)

### 1.1 Syntax Pre-check
- Input: user code string, declared language.
- Process: Python’s built-in `compile` is invoked in `OnlineJudge._check_syntax`.
- Outcome: returns `{valid: bool, error: msg}`. Failure short-circuits evaluation and attaches the syntax error to every test case.
- Rationale: fast rejection without container startup cost; prevents downstream container churn on malformed code.

### 1.2 Driver Code Generation
- Input: user code, function signature, single testcase.
- Steps in `_create_driver_code`:
  1) Extract function name from signature (defaulting to `solution`).
  2) Parse testcase JSON string safely using `repr` to embed it in generated code.
  3) Load JSON at runtime, dispatch call based on input shape:
     - List -> spread as positional args.
     - Dict -> pass as keyword args.
     - Scalar -> single argument.
  4) Detect in-place mutations: if return is `None` and first argument is list, treat the mutated list as output.
  5) Serialize result with `json.dumps` and print (container stdout forms the judged output).
- Outcome: per-test driver isolates user code from harness; no reliance on stdin.

### 1.3 Containerized Test Execution
- Input: generated driver code file mounted read-only into a Docker container.
- Resources: `mem_limit='256m'`, `cpu_quota=50000` (50% CPU), `network_disabled=True`, timeout ≈ `timeout+1` seconds.
- Steps in `_execute_testcase`:
  1) Write driver to temp dir.
  2) Launch container (`python solution.py`) in detached mode.
  3) Wait with timeout; on timeout -> stop/remove container and return `timeout`.
  4) Capture stdout/stderr separately.
  5) Remove container eagerly to avoid resource leakage.
- Outcome: ensures isolation (no network, bounded CPU/memory), deterministic per-test execution.

### 1.4 Output-First Adjudication
- Implemented after container completion:
  - Attempt `json.loads(stdout)`; if parse succeeds, compare to expected before considering stderr/exit code.
  - Strict deep comparison via `_compare_results`:
    - Type match required.
    - Lists: length equality + element-wise recursive compare (order-sensitive).
    - Dicts: key set equality + value-wise recursive compare.
    - Primitives: direct equality.
  - If JSON parse fails:
    - Non-zero exit or stderr -> `runtime_error`.
    - Else -> `invalid output format`.
- Rationale: prevents false negatives when correct output is produced alongside benign warnings.

### 1.5 Sequential Evaluation with Early Stop
- Implemented in `execute_submission`:
  - Iterate testcases in order.
  - Stop at first failure; mark remaining as “execution_stopped”.
  - Aggregate `passed_count`, `total_count`, `error_type`, `error_message`, `execution_time`.
- Trade-off: efficiency over full coverage per run; mirrors LeetCode-style strictness (all-or-nothing).

### 1.6 Batch Driver (Utility)
- `_create_batch_driver_code` supports multi-test execution in one run (not used in main flow) and follows the same argument dispatch logic, producing one JSON line per testcase.

## 2. Test Case Generation Algorithms (`testcase_generator.py`)

### 2.1 Legacy Stdin-Based Generator (`TestcaseGenerator.generate_testcases`)
- Detects problem type from statement keywords (array/string/number/generic).
- Extracts numeric ranges from constraints via regex patterns such as `a <= N <= b`.
- Generates three bands of cases (boundary, normal, random), totaling 500+ in array/generic paths:
  - Array: varied sizes, placeholder outputs (sum/max/min) as scaffolding.
  - String: single-char, short, and random medium strings with placeholder transforms.
  - Number: min/mid/max/random values with placeholder arithmetic.
- Purpose: backward compatibility for stdin problems; placeholders require manual curation.

### 2.2 Function-Based Generator (`generate_function_testcases`)
- Inputs: function signature, sample input/output (JSON), constraints.
- Pipeline:
  1) Validate and add provided sample (marked `is_sample=True`).
  2) Parse parameters from signature to infer types/semantics.
  3) Route to specialized generators:
     - `_generate_two_sum_testcases`: ensures a guaranteed pair per case; covers boundary, normal, large, duplicate-heavy, and negative-number scenarios; sizes bound by constraints where present.
     - `_generate_valid_parentheses_testcases`: uses a stack-based validator and paired/random generators to emit valid/invalid strings across length bands; constraints bound length.
     - `_generate_string_function_testcases`: length-bounded random strings (boundary/normal/random) using sample as alphabet seed when available.
     - `_generate_generic_function_testcases`: mutates sample inputs (if present) with controlled randomness; otherwise falls back to scalar lists.
  4) Diversity padding: while `len(testcases) < 500`, mutate random existing inputs via `_mutate_input` (element perturbation, size jitter, string resampling) and reuse expected output placeholder.
- Output: JSON-formatted `input_data` and `expected_output`, with testcase_type tags (`boundary`, `normal`, `random`) and sample flag.

### 2.3 Input Mutation (`_mutate_input`)
- Deep-copies the sample input, then:
  - For numeric lists: probabilistic element replacement and occasional length changes.
  - For nested lists: recursive mutation.
  - For scalars: randomized scaling.
  - For strings: regenerate with same length using alphabetic randomness.
- Purpose: rapidly expands coverage space while preserving structural similarity.

### 2.4 Valid Parentheses Generation Details
- Uses local `is_valid` stack checker and two generators:
  - `generate_valid_string`: mixes opening/closing with a stack to guarantee balance; closes residual stack at end.
  - `generate_invalid_string`: injects unmatched opening/closing brackets around a shorter valid core.
- Produces balanced sets across boundary/normal/random buckets, toggling validity to ensure both pass/fail coverage.

## 3. Submission and Evaluation Pipelines

### 3.1 Student “Run” Path (`student/routes.py`)
- Scope: sample testcases only (`is_sample=True`).
- Steps:
  1) Fetch quiz and sample testcases.
  2) Build judge payload (input/expected JSON strings).
  3) Call `execute_submission` with 2s/256m limits.
  4) Return per-test results without persisting to DB.
- Goal: fast formative feedback without affecting submission history.

### 3.2 Student “Submit” Path
- Scope: all testcases (sample + hidden).
- Steps:
  1) Fetch quiz and all associated testcases.
  2) Execute via judge with same resource limits.
  3) Persist `Submission` with status, error info, pass counts, timing.
- Goal: summative evaluation with strict all-pass requirement.

### 3.3 Teacher Creation and Regeneration (`teacher/routes.py`)
- On create:
  - Validate inputs; require function signature for function-based problems.
  - Generate testcases via function-based or legacy generator.
  - Batch-insert testcases (size 100) to reduce transaction overhead.
- On regenerate:
  - Delete existing testcases, flush, regenerate using stored quiz metadata, batch-insert new cases.
- Goal: reproducible, high-volume testcase provisioning with ownership checks.

## 4. Data Integrity and Comparison Logic

- Models (`models.py`):
  - `Quiz` to `Testcase` uses cascade delete to keep testcases aligned with quiz lifecycle.
  - `Submission` records retain execution metadata (status, error_type, counts, timing) for auditability.
- Comparison:
  - Strict type matching avoids silent coercion.
  - Recursive list/dict equality enforces determinism and order sensitivity.
- Early-stop semantics:
  - Prevent unnecessary container runs after first failure, conserving compute and surfacing the earliest failing input.

## 5. Security and Resource Control

- Container isolation: no network, read-only mount of temp directory, ephemeral containers destroyed after each test.
- Resource quotas: memory capped; CPU quota halves core availability; timeouts enforced at the container wait layer and by explicit exception handling.
- Cleanup discipline: containers removed on all paths; temp directories removed in `finally` to prevent leakage.

## 6. Determinism and Reproducibility

- JSON I/O contract ensures stable serialization; driver code prints a single JSON line per test.
- Expected outputs are JSON strings stored with each testcase, enabling exact matching.
- Mutations are stochastic but bounded; generator always pads to 500+ cases, ensuring volume consistency.
- Early-stop preserves consistent failure ordering, aiding reproducible debugging.

## 7. Extensibility Notes

- Language support: syntax checker and driver are Python-specific; extending to other languages would require language-specific syntax validation, runner images, and invocation templates.
- Testcase quality: legacy generators use placeholders; accuracy improves when teachers provide sample I/O and constraints. Reference solutions could be added to auto-derive expected outputs for generated cases.
- Execution policy: batch driver utilities could enable amortized container costs for trusted scenarios but would need additional isolation guarantees.

