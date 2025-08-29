# AGENTS Debug Rules

This document outlines **hidden debugging gotchas** and practices specific to this project. These are designed to help contributors diagnose and fix issues efficiently in the deterministic, test-driven demo system.

---

## Deterministic Behavior
- **Always confirm seeding** before debugging randomness issues.
  - `random.seed(0)` must be called.
  - If NumPy is installed, `numpy.random.seed(0)` as well.
- Tests may fail nondeterministically if seeds are missing—check initialization first.

---

## Demo Debugging
- All demos must run **headless** (no GUI or user input).
- Debug demos by importing the module and running `demo()` directly.
- If a demo silently fails, wrap `run_demo(module_id)` in verbose logging to capture edge cases.

---

## Common Pitfalls
- **Import Errors**:
  - Ensure `tests/conftest.py` has placed project root in `sys.path`.
  - If an import fails during debugging, confirm the relative placement under `src/interview_workbook/`.

- **Silent Failures**:
  - `demo()` must always return a string. An empty string is valid, `None` is not.
  - If `None` appears, fix the `demo()` return path.

- **Utility Scripts**:
  - Do not attempt to “fix” corrupted LeetCode notebook dumps manually. Use:
    - `fix_leetcode_syntax_corruption.py`
    - `fix_comprehensive_leetcode_corruption.py`
  - Debugging should confirm these utilities preserve execution parity.

---

## Test Debugging
- Run single test cases with:

  ```bash
  pytest tests/test_demos.py::test_run_all_demos_headless -v
  ```

- Sort order for demo execution is deterministic. Failures can therefore be bisected reliably.

---

## Strategy
- Debug issues **per demo module**, since all are independent Python scripts.
- Failures are usually due to:
  1. Missing deterministic seed.
  2. Demo not returning `str`.
  3. Misplaced file under incorrect category.
  4. Hidden import of non-stdlib dependency.

Keep checks simple: this system prioritizes reproducibility over flexibility.
