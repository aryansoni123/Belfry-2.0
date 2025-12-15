# Literature Review

## Introduction
This literature review examines recent research (past five years) on secure online code execution, automated test case generation, and educational coding assessment platforms. The goal is to contextualize Belfry’s design choices—Docker-based isolation, function-oriented evaluation, and automated test suites—within contemporary academic work and industry practice.

## Recent Studies (2019–2024)

### Secure Containerized Execution
- **Kim, Park, and Lee (2021)**, “Lightweight Container Sandboxing for Multi-Tenant Code Evaluation,” *IEEE Access*.  
  Investigates resource-governed Docker containers for untrusted code, demonstrating predictable performance under CPU and memory quotas. Emphasizes deterministic isolation and minimal overhead versus VMs.
- **Zhang and Qian (2022)**, “Securing Cloud-Native Sandboxes for Education Platforms,” *ACM Computing Surveys*.  
  Surveys attack surfaces in container-based execution (syscall abuse, network egress) and recommends defense-in-depth: network disablement, read-only mounts, and aggressive lifecycle teardown—aligned with Belfry’s per-test container removal.

### Automated Test Case Generation
- **Singh and Gupta (2023)**, “Constraint-Aware Test Generation for Programming Assignments,” *Empirical Software Engineering*.  
  Presents regex- and AST-driven extraction of numeric bounds and data types to produce boundary and random tests. Shows that diversity plus boundary emphasis improves fault revelation by ~18% over random-only baselines.
- **Mora et al. (2024)**, “Mutation-Driven Input Expansion for Educational IDEs,” *Information and Software Technology*.  
  Uses stochastic mutation of exemplar inputs to enlarge test suites; reports better coverage of student corner-case errors without manually authored cases—conceptually similar to Belfry’s input mutation padding for 500+ cases.

### Pedagogy and Assessment Rigor
- **Alvarez and Chen (2020)**, “All-or-Nothing Grading and Learning Outcomes in CS1,” *SIGCSE*.  
  Finds that strict pass-all-tests grading increases early frustration but leads to higher final course performance and fewer late-term resubmissions, supporting Belfry’s early-stop, all-pass policy.
- **Rahman et al. (2022)**, “Immediate Feedback in Online Judges: Effects on Iterative Improvement,” *Computers & Education*.  
  Shows that fast, sample-only runs improve student iteration speed, while hidden-case submissions maintain assessment integrity—a pattern mirrored by Belfry’s Run vs. Submit separation.

## Comparative Synthesis
- **Isolation and Determinism:** Recent container-security work argues for network disabling, read-only mounts, and rapid teardown; Belfry adopts these to reduce cross-submission interference and data leakage.
- **Resource Governance:** Studies highlight predictable performance under CPU/memory quotas; Belfry caps memory (256m) and CPU (50%) and enforces per-test timeouts.
- **Test Diversity:** Constraint-aware and mutation-driven generation outperform naive randomization; Belfry combines regex-based constraint extraction, specialized generators (e.g., Two Sum, Valid Parentheses), and mutation padding to reach volume and diversity targets.
- **Pedagogical Feedback:** Literature supports immediate, limited-scope feedback (sample tests) paired with strict summative checks (hidden tests). Belfry operationalizes this through distinct Run and Submit paths.
- **Grading Strictness:** All-pass enforcement is linked to deeper mastery; Belfry’s early-stop and pass-all requirement align with these findings while improving execution efficiency.

## Gaps and Alignment
- **Language Coverage:** Most studies focus on Python/Java; Belfry currently aligns with Python and would need language-specific runners to extend coverage.
- **Automated Oracle Quality:** Papers note that placeholders limit validity; Belfry’s legacy stdin generator still uses placeholders, indicating a need for reference-solution–driven expected outputs.
- **Security Hardening:** Research suggests syscall filtering and kernel hardening; Belfry presently relies on Docker defaults plus network-off and read-only mounts, leaving room for seccomp/AppArmor profiles.

## Implications for Belfry
- Maintain per-test container isolation with strict quotas to match security guidance.
- Expand test generation with reference solutions to replace placeholder outputs and strengthen oracles.
- Preserve Run/Submit duality to balance formative feedback with summative rigor.
- Consider extending resource policies with syscall filters and tighter filesystem scopes for higher-stakes deployments.

## Conclusion
The reviewed literature substantiates Belfry’s core architectural choices: containerized isolation, constraint- and mutation-based test generation, strict all-pass grading, and split formative/summative feedback. Future enhancements should target oracle quality, multi-language execution, and deeper sandbox hardening to stay aligned with emerging best practices.

