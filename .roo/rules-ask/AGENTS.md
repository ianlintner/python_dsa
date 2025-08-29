# AGENTS Ask Rules

This document highlights **documentation and context caveats** for contributors when asking or answering technical questions in this project.

---

## Demo Expectations
- Every demo module under `src/interview_workbook/` must expose a top-level `demo()` callable.
- `demo()` must:
  - Run **headless** (no GUI, no user input).
  - Always return a `str` (may be empty).

When in doubt about demo correctness, emphasize return value and determinism.

---

## Randomness Clarification
- Contributors may ask "Why are demo outputs inconsistent?"
  - Standard resolution: All randomness **must** be seeded with `random.seed(0)` (and `numpy.random.seed(0)` if NumPy is available).
  - Unseeded random calls are disallowed.

---

## Testing Note
- Tests rely on:
  - `discover_demos()` → returns dictionary of categories of demos.
  - `run_demo(module_id)` → executes `demo()` and returns captured output.
- Questions about failures can often be explained by one of:
  1. Missing `demo()`.
  2. Return type not `str`.
  3. Demo placed outside required path (`src/interview_workbook/`).

---

## Utilities
- Notebook corruption is handled by:
  - `fix_leetcode_syntax_corruption.py`
  - `fix_comprehensive_leetcode_corruption.py`
- If asked: *“Why not hand-edit corrupted dumps?”*
  - Answer: Determinism and test parity require these utilities—manual edits risk divergence.

---

## General Guidance
- Avoid ambiguous answers: prefer explicit test references.
- Use pytest invocation examples for clarifying test expectations:

  ```bash
  pytest tests/test_demos.py::test_run_all_demos_headless -v
  ```

- Steer contributors toward headless, deterministic, reproducible solutions.

---
