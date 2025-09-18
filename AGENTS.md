# AGENTS Guide

This document captures **non-obvious, project-specific rules** and conventions for working with this codebase. It is distinct from general Python guidelines or standard tooling docs.

---

## Testing
- All tests use **pytest**.
- Activate shell python with source /Users/ianlintner/python_dsa/.venv/bin/activate
- Test discovery depends on `tests/conftest.py` ensuring the project root is on `sys.path`.
- Run a single test with:

  ```bash
  pytest tests/test_demos.py::test_run_all_demos_headless -v
  ```

- The primary test suite drives `discover_demos()` and `run_demo()` from `flask_app.app`.
- All discovered demos must implement a `demo()` function. Tests assert its existence and require it to run without exceptions.

---

## Demo System
- Demos are discovered dynamically using `discover_demos()` (returns categories of demos).
- Tests flatten categories into a list of metadata dicts:
  ```python
  {"id": module_path, "name": ..., ...}
  ```
- Each demo module must:
  - Be importable by its `"id"`.
  - Expose a callable `demo()`.

- `run_demo(module_id)` must return a `str` (empty string is valid).

---

## Randomness Seeding
- Test reliability depends on deterministic seeding:
  - `random.seed(0)`
  - `numpy.random.seed(0)` if NumPy is installed

Ensure demos respect these randomness seeds when introducing stochastic behaviors.

---

## Code Conventions
- Maintain determinism: results must be reproducible under fixed seeds.
- Demo output can be empty but must not raise.
- Any new demos should be designed to run **headless**—no GUI or interactive prompts.

---

## Hidden Rules
- Fix-up utilities (`fix_leetcode_syntax_corruption.py`, `fix_comprehensive_leetcode_corruption.py`) are not just scripts, they enforce **consistency of the LeetCode-style notebooks**. Do not modify them casually.
- All core algorithms live under `src/interview_workbook/`. Follow the existing categorization (`two_pointers/`, etc.).

---
