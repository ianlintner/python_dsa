# AGENTS Code Rules

This document captures **hidden rules and coding-specific conventions** for contributors. These rules enforce consistency and reliability across demos, algorithms, and LeetCode-style modules.

---

## Core Coding Rules
- **Deterministic Behavior**
  - Always seed randomness with `random.seed(0)`
  - If using NumPy, use `numpy.random.seed(0)`
  - No unseeded calls to stochastic functions—tests rely on determinism.

- **Demo Functions**
  - Each demo module must provide a top-level `demo()` callable.
  - `demo()` must run headless (no GUI, no user prompt).
  - Output should always be a `str` (may be empty).

- **Categorization**
  - Placement under `src/interview_workbook/` is mandatory.
  - Use existing category folders (e.g., `two_pointers/`) to organize new problems.
  - New subcategories must follow the same pattern.

---

## Algorithm Files
- All solutions are standalone Python scripts.
- File and function names follow **snake_case**.
- Imports must remain **relative-free** inside categories to ensure portability (`import` from stdlib or third-party only).
- All imports must be placed at the very top of the file, immediately after any module docstring.

---

## Utility Scripts
- Do **not** casually modify:
  - `fix_leetcode_syntax_corruption.py`
  - `fix_comprehensive_leetcode_corruption.py`
- These enforce notebook-to-python consistency; changing them risks widespread corruption.

---

## Testing Constraints
- All demos and algorithms must execute under pytest with no interactive input.
- Algorithms should fail fast when misused, but avoid raising exceptions in test demo runs.

---

## Style
- Follow `ruff` linter rules (pre-commit ensures enforcement).
- Explicit is better than implicit—avoid clever one-liners.
- Consistent docstrings: short summary sentence, then details if needed.

---
