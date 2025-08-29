# AGENTS Architecture Rules

This document captures **non-obvious architectural constraints** and conventions that govern this project. It complements design and architectural reasoning beyond standard Python practices.

---

## Project Structure
- **All core algorithms** must live under `src/interview_workbook/`.
- Algorithms are placed into **categorized subdirectories** (e.g., `two_pointers/`, `sliding_window/`, etc.).
- New categories must follow the established folder pattern and naming conventions (lowercase snake_case).
- No cross-package relative imports are allowed; only use **stdlib** or **third-party libraries**.
- Utilities for LeetCode fix-ups (`fix_leetcode_syntax_corruption.py`, `fix_comprehensive_leetcode_corruption.py`) enforce **portability and reproducibility** — do not bypass or modify them casually.

---

## Demo & Execution Model
- Every algorithm file must expose a **top-level `demo()`** function.
- `demo()` runs **headlessly**:
  - No GUI, no user prompts, no external inputs.
  - Must always return a `str` (may be empty).
- Demos are dynamically discovered via `discover_demos()` → `run_demo()`.

---

## Determinism
- Randomized algorithms must be deterministic for testing:
  - Always seed with `random.seed(0)`.
  - If NumPy is used, also set `numpy.random.seed(0)`.
- Test reliability depends on reproducibility under these seeds.

---

## Testing System
- **Pytest** is the exclusive framework.
- Central meta-test runs **all demos**:
  - `pytest tests/test_demos.py::test_run_all_demos_headless -v`
- Discovery depends on `tests/conftest.py`, which injects project root into `sys.path`.

---

## Hidden Constraints
- **Fix-up utilities** (`fix_leetcode_syntax_corruption.py`, `fix_comprehensive_leetcode_corruption.py`) enforce **consistency** of the LeetCode-to-Python pipeline. Altering their output contract risks breaking discovery and test reliability.
- Any new **architectural layers** (e.g., categories, new discovery utilities) must align with:
  - Headless execution mandate
  - Determinism requirement
  - Portability across environments

---

## Style & Governance
- Enforced via **pre-commit hooks** and `ruff`:
  - Explicit > implicit, avoid clever one-liners.
  - Maintain consistent snake_case naming.
  - Docstrings: concise summary followed by optional detail.
- Architecture-level changes require validating that:
  - Discovery (`discover_demos`) still includes all demos.
  - `run_demo()` still properly executes them.
  - Seeding and determinism rules are preserved.
