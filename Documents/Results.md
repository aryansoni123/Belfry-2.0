# Results and Discussion

## Overview
This section reports observed outcomes of the Belfry platform against its objectives: secure execution, accurate grading, automated test generation, and supportive pedagogy. Results are derived from internal validation runs and design-time reasoning about the implemented algorithms in `judge.py`, `testcase_generator.py`, and the student/teacher pipelines.

## Alignment with Objectives
- **Secure execution:** Per-test Docker containers with disabled networking, 256 MB memory cap, ~50% CPU quota, and strict timeouts enforced during container wait. Containers are removed post-run, and temp directories are cleaned in `finally` blocks, reducing residual state and cross-submission leakage.
- **Accurate grading:** Output-first adjudication parses stdout as JSON and performs strict deep comparison before considering stderr/exit codes, preventing false negatives from benign warnings. Early-stop after first failure enforces all-pass grading while minimizing compute cost on failing submissions.
- **Automated test generation:** Function-based generator produces 500+ cases per quiz via constraint parsing, specialized generators (Two Sum, Valid Parentheses), and stochastic mutation padding. Legacy stdin generator maintains backward compatibility with boundary/normal/random strata.
- **Pedagogical feedback:** Dual pathways (Run for samples, Submit for all cases) mirror formative vs. summative assessment, providing rapid iteration without exposing hidden oracles.

## Quantitative Indicators (design-time targets)
- **Execution time:** Target < 2 seconds per test case under normal workloads with Python code inside containers; enforced via wait timeouts and container stop on exceed.
- **Isolation:** Network disabled; read-only bind of temp directory; per-container lifecycle eliminates persistence across runs.
- **Test suite volume:** ≥ 500 test cases generated for function-based problems, combining boundary, normal, random, and mutated variants to improve fault detection breadth.
- **Pass criteria:** 100% of executed test cases must pass; failures halt further execution, yielding deterministic earliest-failure reporting.

## Performance Characteristics
- **Determinism:** JSON I/O contract and strict type-aware comparison ensure repeatable judgments. Early-stop preserves a consistent failure point, aiding reproducibility.
- **Resource governance:** Memory and CPU quotas bound runaway submissions; timeouts guard against infinite loops. Container removal prevents resource accumulation.
- **Scalability considerations:** Current single-node design scales to moderate classroom loads. For higher concurrency, horizontal scaling, queued execution, and DB offload (to PostgreSQL/MySQL) would be needed.

## Accuracy and Reliability
- **Output correctness:** Deep comparison enforces type fidelity (lists vs. dicts vs. primitives) and order-sensitive list checks, reducing false positives from loosely matched outputs.
- **Oracle quality:** High for function-based cases with explicit expected outputs; lower for legacy stdin paths that use placeholder oracles, indicating the need for reference-solution–driven outputs to raise reliability.
- **Error reporting:** Syntax errors surfaced pre-execution; runtime/timeout surfaced with contextual messages; invalid-output-format captured when stdout is non-JSON yet exit is clean.

## Security Posture
- **Strengths:** Network isolation, bounded CPU/memory, ephemeral containers, read-only mounts, per-test teardown. These controls align with contemporary guidance on educational sandboxes.
- **Gaps:** No seccomp/AppArmor profiles or syscall whitelisting in current setup; Docker default sec profiles are assumed. File system scope is limited to the temp mount but not further jailed beyond container isolation.

## Test Generation Outcomes
- **Constraint-aware breadth:** Regex-based extraction of numeric bounds feeds specialized generators to respect size/value limits where provided.
- **Diversity via mutation:** `_mutate_input` perturbs exemplar structures (lists, scalars, strings) to introduce variability without hand-authoring each case.
- **Specialized coverage:** Two Sum generator guarantees solvable pairs across boundary/normal/large/duplicate-heavy/negative cases; Valid Parentheses generator alternates valid/invalid with a stack-based validator.
- **Limitations:** Placeholders persist in legacy stdin flows; absence of reference solutions can reduce oracle fidelity.

## User Experience and Feedback Loop
- **Run vs. Submit:** Sample-only runs offer quick feedback with low load; full submissions preserve assessment rigor by using hidden cases.
- **Submission records:** Stored status, error type, and counts enable teachers to review outcomes and students to track progress.

## Challenges Encountered
- Avoiding false negatives when stderr contained warnings; resolved by prioritizing output correctness before error status.
- Ensuring container cleanup on all paths to prevent resource leakage; addressed with defensive `finally` blocks and forced removal.
- Handling in-place mutations (functions returning `None` after modifying inputs); addressed in driver code to surface mutated inputs as outputs.

## Limitations
- Single-language (Python) support limits applicability across curricula.
- Legacy stdin generator relies on placeholder outputs; accuracy depends on manual oracle refinement or future reference solutions.
- Sequential early-stop prevents full visibility into all failing cases per submission; efficient but less informative for certain pedagogical needs.

## Recommendations and Future Work
- Integrate seccomp/AppArmor profiles for stronger syscall confinement.
- Add multi-language runners with language-specific drivers and syntax checks.
- Introduce reference-solution execution to auto-derive oracles, replacing placeholders in legacy flows.
- Provide optional “run all tests” (non-graded) mode for exploratory debugging when performance allows.
- Add per-test execution time/memory reporting to give students optimization feedback.

## Conclusion
The platform meets its core goals of secure, deterministic, and strict code evaluation with robust automated test generation and a feedback model aligned to instructional best practices. The principal areas for improvement are oracle fidelity in legacy paths, expansion to multiple languages, and deeper sandbox hardening for high-stakes deployments.

