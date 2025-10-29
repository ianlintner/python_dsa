# AGENTS Guide

## Purpose

This document provides custom instructions and guidance for AI coding agents (including GitHub Copilot) working with this repository. It captures **non-obvious, project-specific rules** and conventions for building, testing, and validating changes in this codebase.

**Repository Overview:**
- **Name:** Python Interview Algorithms Workbook
- **Description:** Clean, idiomatic Python implementations for senior/staff-level interview prep with complexity notes, pitfalls, demos, and tests
- **Technologies:** Python 3.9+, Flask 3.0+, pytest 8.0+, Ruff (linter/formatter)
- **Purpose:** Educational resource for algorithm implementations and interview preparation

---

## Project Structure & Organization

The repository follows a `src/` layout:

```
python_dsa/
├── src/
│   ├── interview_workbook/        # Main package
│   │   ├── algorithms/            # Sorting, searching algorithms
│   │   ├── data_structures/       # DSU, Trie, LRU/LFU, Fenwick, Segment trees
│   │   ├── graphs/                # BFS, DFS, Dijkstra, MST, SCC
│   │   ├── dp/                    # Dynamic programming solutions
│   │   ├── strings/               # String algorithms (KMP, Z-algo, etc.)
│   │   ├── math_utils/            # Number theory utilities
│   │   ├── patterns/              # Common coding patterns
│   │   ├── systems/               # Systems design concepts
│   │   ├── concurrency/           # Concurrency patterns
│   │   └── nlp/                   # NLP utilities
│   └── main.py                    # CLI demo launcher
├── flask_app/                     # Web UI for demos
├── tests/                         # Pytest test suite
├── docs/                          # Documentation (MkDocs)
└── scripts/                       # Utility scripts
```

**Key Principles:**
- All imports use the package name: `from interview_workbook.algorithms.sorting.merge_sort import merge_sort`
- Tests import directly from `src/` via `tests/conftest.py` which adds src to `sys.path`
- Each algorithm module includes implementation, complexity analysis, pitfalls, and a `demo()` function

---

## Build, Test, and Development Commands

### Initial Setup
```bash
# Install package in editable mode with dev dependencies
python -m pip install -U pip
python -m pip install -e ".[dev]"

# Set up pre-commit hooks (optional but recommended)
pre-commit install
```

### Running Tests
```bash
# Run all tests with coverage
pytest -q

# Run specific test file
pytest tests/test_sorting.py -v

# Run single test
pytest tests/test_demos.py::test_run_all_demos_headless -v

# Run with verbose output
pytest -v
```

### Linting and Formatting
```bash
# Format code (Ruff formatter)
ruff format .

# Lint code (Ruff rules E,F,I,B,UP etc.)
ruff check .

# Auto-fix simple issues
ruff check --fix

# Run all pre-commit hooks
pre-commit run --all-files --show-diff-on-failure --color=always
```

### Running Demos
```bash
# List all available demos
python src/main.py --list

# Run specific demo
python src/main.py --demo sorting.merge_sort
python src/main.py --demo searching.binary_search
python src/main.py --demo dp.lcs
python src/main.py --demo graphs.scc
```

### Documentation
```bash
# Build documentation (requires Docker)
make docs

# Serve documentation locally
make serve-docs

# Clean built documentation
make clean-docs
```

---

## Code Style and Conventions

### General Guidelines
- **Python Version:** Target Python 3.9+ (as specified in pyproject.toml)
- **Line Length:** Maximum 100 characters
- **Formatting:** Use Ruff formatter (double quotes, 4-space indentation)
- **Import Order:** Ruff handles import sorting automatically
- **Type Hints:** Encouraged but not required for this educational repo
- **Docstrings:** Required for all public functions and classes

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private members: prefix with `_`

### Algorithm Implementation Standards
Every algorithm module should include:
1. **Implementation function(s)** with clear parameter names
2. **Docstring** explaining:
   - What the algorithm does
   - Time and space complexity
   - Parameters and return values
   - Example usage
3. **Common pitfalls** and edge cases as comments
4. **A `demo()` function** that demonstrates the algorithm with sample inputs

### Example Structure
```python
def algorithm_name(input_data, param=default):
    """
    Brief description of what the algorithm does.

    Time complexity: O(n log n)
    Space complexity: O(n)

    Args:
        input_data: Description
        param: Description (default: value)

    Returns:
        Description of return value

    Common pitfalls:
    - Edge case 1
    - Edge case 2
    """
    # Implementation here
    pass

def demo():
    """Demonstrate the algorithm with examples."""
    # Demo code here
    pass
```

---

## Architecture and Design Patterns

### Educational Focus
This repository is designed for **learning and interview preparation**, not production use. Code prioritizes:
- **Clarity** over performance optimizations
- **Correctness** with comprehensive edge case handling
- **Educational value** with detailed comments on complexity and pitfalls

### Demo System Architecture
- **Discovery:** `flask_app.app.discover_demos()` dynamically finds all demo functions
- **Execution:** `run_demo(module_id)` imports and executes the `demo()` function
- **Testing:** All demos are tested to ensure they run without exceptions
- **Headless Operation:** Demos must not require GUI or interactive prompts

### Pattern Categories
The codebase is organized by common interview patterns:
- **Two Pointers:** Problems solvable with two-pointer technique
- **Sliding Window:** Fixed or variable window problems
- **Binary Search on Answer:** When answer space is searchable
- **Backtracking:** Problems requiring exhaustive search with pruning
- **Meet in the Middle:** Problems with exponential search space reducible by splitting

---

## Testing Guidelines

### Test Framework and Configuration
- **Framework:** All tests use **pytest** (version 8.0+)
- **Configuration:** Test settings in `pyproject.toml` under `[tool.pytest.ini_options]`
- **Coverage:** Tests include coverage reporting via pytest-cov (enabled by default)
- **Test Discovery:** Tests in `tests/` directory, files matching `test_*.py` pattern
- **Module Path:** `tests/conftest.py` ensures the project root is on `sys.path`

### Running Tests
```bash
# Run all tests (includes coverage by default per pyproject.toml)
pytest -q

# Run specific test file
pytest tests/test_sorting.py -v

# Run single test
pytest tests/test_demos.py::test_run_all_demos_headless -v

# Run with detailed coverage report
pytest --cov=src --cov-report=term-missing

# Run without coverage (faster for quick checks)
pytest -q --no-cov
```

### Test Requirements
- The primary test suite drives `discover_demos()` and `run_demo()` from `flask_app.app`
- All discovered demos **must implement a `demo()` function**
- Tests assert the existence of `demo()` and require it to run without exceptions
- All tests must be **deterministic** and reproducible

### Writing Tests
When adding new algorithms or features:
1. Add tests to the appropriate `tests/test_*.py` file
2. Test edge cases: empty input, single element, sorted/reverse sorted, duplicates
3. Test with random data when applicable
4. Verify time/space complexity claims with larger inputs
5. Ensure tests run quickly (< 1 second each when possible)

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

## Randomness and Determinism

### Seeding Requirements
Test reliability depends on deterministic seeding:
- Use `random.seed(0)` for Python's random module
- Use `numpy.random.seed(0)` if NumPy is installed
- Always seed before generating random test data

### In Algorithm Implementations
- Ensure demos respect these randomness seeds when introducing stochastic behaviors
- For randomized algorithms (e.g., quicksort with random pivot), document the randomness
- Provide deterministic variants when possible for testing

### Test Reproducibility
- All test results must be reproducible under fixed seeds
- Results must be identical across multiple test runs
- Document any inherent non-determinism (e.g., hash table iteration order in Python 3.6+)

---

## Code Quality and Conventions

### Core Principles
- **Determinism:** Results must be reproducible under fixed seeds
- **No Exceptions:** Demo output can be empty but must not raise exceptions
- **Headless Operation:** All demos must run **headless**—no GUI or interactive prompts
- **Clean Code:** Maintain readability and follow idiomatic Python patterns

### File Organization
- All core algorithms live under `src/interview_workbook/`
- Follow the existing categorization: `two_pointers/`, `sorting/`, `graphs/`, etc.
- Keep related functionality together (e.g., all binary search variants in one module)

### Special Scripts
- **Fix-up utilities:** `fix_leetcode_syntax_corruption.py`, `fix_comprehensive_leetcode_corruption.py`
- These scripts enforce **consistency of the LeetCode-style notebooks**
- **Do not modify them casually**—they maintain notebook formatting standards
- Run these scripts after making changes to notebook files

---

## Security Considerations

### General Security Guidelines
- **No Hardcoded Secrets:** Never commit API keys, passwords, or tokens
- **Input Validation:** All public functions should validate inputs appropriately
- **Safe Imports:** Only import from trusted sources
- **Dependency Management:** Keep dependencies up to date via `pyproject.toml`

### Security Best Practices for This Repository
- This is an **educational repository** without external network access in core algorithms
- Flask app is for **local development only**—not intended for production deployment
- No user authentication or sensitive data handling
- All demos run in a sandboxed environment

### When Adding Dependencies
- Check dependency security advisories before adding new packages
- Prefer well-maintained packages with active communities
- Document why new dependencies are needed
- Keep the dependency list minimal

---

## Dependencies and Tools

### Core Dependencies
- **Python:** 3.9 or higher
- **Flask:** 3.0.0+ (for web UI)
- **pytest:** 8.0.0+ (testing framework)
- **pytest-cov:** 4.1.0+ (coverage reporting)
- **Ruff:** 0.5.6+ (linter and formatter)
- **pre-commit:** 3.6.0+ (git hooks)

### Optional Dependencies
- **NumPy:** For numerical algorithms (not a hard requirement)
- **MkDocs:** For documentation generation (Docker-based)

### Development Workflow
1. Install with: `python -m pip install -e ".[dev]"`
2. Set up pre-commit hooks: `pre-commit install`
3. Before committing:
   - Run `ruff format .` to format code
   - Run `ruff check --fix` to fix linting issues
   - Run `pytest -q` to ensure tests pass
4. Pre-commit hooks will run automatically on `git commit`

### CI/CD Pipeline
GitHub Actions CI workflow:
1. Installs dependencies with `pip install -e ".[dev]"`
2. Runs pre-commit hooks (format + lint + misc checks)
3. Runs tests via `pytest -q`
4. Reports coverage

---

## Working with Demos

### Demo Function Requirements
Each demo module must:
- Be importable by its module ID (e.g., `sorting.merge_sort`)
- Expose a callable `demo()` function with no parameters
- Return a string (empty string is valid)
- Run without raising exceptions
- Complete execution in reasonable time (< 5 seconds)

### Demo Discovery Process
- `discover_demos()` returns categories of demos as a nested dictionary
- Tests flatten categories into a list of metadata dicts: `{"id": module_path, "name": ..., ...}`
- `run_demo(module_id)` dynamically imports and executes the demo function

### Adding New Demos
1. Create algorithm implementation with `demo()` function
2. Place in appropriate category under `src/interview_workbook/`
3. Ensure `demo()` function exists and runs without errors
4. Test with: `python src/main.py --demo category.module_name`
5. Verify it appears in: `python src/main.py --list`

---

## PR and Change Guidelines

### Before Submitting Changes
1. **Run tests:** `pytest -q` must pass
2. **Format code:** `ruff format .`
3. **Fix linting:** `ruff check --fix`
4. **Check coverage:** Maintain or improve test coverage
5. **Update docs:** If adding new features, update relevant documentation

### PR Acceptance Criteria
- All tests pass
- Code is properly formatted (Ruff)
- No new linting errors
- Test coverage maintained or improved
- Documentation updated if needed
- Demo functions work correctly
- Changes are minimal and focused

### Review Checklist
- [ ] Implementation is correct and handles edge cases
- [ ] Time/space complexity is documented
- [ ] Tests cover new functionality
- [ ] Code follows existing style conventions
- [ ] Demo function exists and works
- [ ] No breaking changes to existing APIs

---

## Common Pitfalls and Tips

### For AI Coding Agents
1. **Always run tests** after making changes: `pytest -q`
2. **Format before committing:** `ruff format .` and `ruff check --fix`
3. **Check demo functions:** Ensure they run with `python src/main.py --demo module.name`
4. **Maintain determinism:** Use proper seeding for random operations
5. **Don't break existing code:** This is an educational repo—preserve working implementations
6. **Keep it simple:** Prioritize clarity over clever optimizations

### Common Issues
- **Import errors:** Ensure you're running from the repo root
- **Test failures:** Check that random seeds are set correctly
- **Demo not found:** Verify the module path matches the file structure
- **Linting errors:** Run `ruff check --fix` to auto-fix most issues

### Quick Reference Commands
```bash
# Full development cycle
python -m pip install -e ".[dev]"    # Install with dev deps
pytest -q                             # Run tests
ruff format .                         # Format code
ruff check --fix                      # Fix linting
python src/main.py --demo module.name # Test demo

# Quick fixes
ruff check --fix                      # Auto-fix linting issues
pytest tests/test_file.py -v         # Debug specific test
python src/main.py --list            # List all demos
```

---

## Summary for AI Agents

**What to do when making changes:**
1. Install dependencies: `python -m pip install -e ".[dev]"`
2. Make minimal, focused changes
3. Run tests: `pytest -q`
4. Format: `ruff format .`
5. Lint: `ruff check --fix`
6. Test demos: `python src/main.py --demo module.name`
7. Verify everything works before submitting

**Key principles:**
- Maintain determinism (seed random operations)
- Keep demos headless (no GUI)
- Follow existing code structure and patterns
- Document time/space complexity
- Test edge cases thoroughly
- Don't break existing functionality

**When in doubt:**
- Check existing implementations for examples
- Run the full test suite
- Verify demos still work
- Keep changes minimal and surgical
