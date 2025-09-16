# Implementation Plan

[Overview]  
The goal is to simplify the user interface across both the Flask web app and the algorithm demo system by removing progress tracking and reducing visual clutter, making the dashboard more intuitive and user-friendly.

This implementation will focus on two main areas:  
1. **Flask Web App (`flask_app/`)** – Simplify templates, remove unnecessary progress indicators, and streamline navigation.  
2. **Algorithm Demo System (`src/main.py` and `src/interview_workbook/`)** – Remove progress tracking logic, simplify demo outputs, and ensure consistent UX principles across demos.  

The high-level approach is to identify and remove progress-related UI elements, refactor templates for clarity, and adjust backend demo functions to avoid verbose or overwhelming outputs. This ensures a clean, minimal, and user-friendly experience.

[Types]  
No new types are required.

We will remove any type definitions related to progress tracking (if present in `_types.py` or related files). All existing algorithm and demo types remain unchanged.

[Files]  
We will modify existing files to remove progress tracking and simplify UI.

- **New files**: None  
- **Modified files**:  
  - `flask_app/templates/base.html` → Remove progress bars, tracking widgets, and simplify layout.  
  - `flask_app/templates/index.html` → Simplify dashboard, remove progress indicators, highlight only key navigation.  
  - `flask_app/static/style.css` → Remove styles related to progress bars and tracking, simplify typography and spacing.  
  - `flask_app/app.py` → Remove backend logic that injects progress data into templates.  
  - `src/main.py` → Remove progress tracking in demo discovery and execution. Simplify demo listing and running.  
  - `src/interview_workbook/leetcode/_runner.py` → Remove `show_details` and progress-related flags from test/demo runner.  
- **Deleted files**: None  
- **Configuration updates**: None required.

[Functions]  
We will remove or simplify functions that handle progress tracking.

- **New functions**: None  
- **Modified functions**:  
  - `discover_demos()` in `src/main.py` → Remove progress-related metadata.  
  - `run_demo()` in `src/main.py` → Simplify output, remove progress tracking.  
  - `create_demo_output()` in `src/interview_workbook/leetcode/_runner.py` → Remove progress details, return only clean results.  
- **Removed functions**:  
  - Any helper functions in `_runner.py` that exist solely for progress tracking.

[Classes]  
We will simplify classes that currently handle progress tracking.

- **New classes**: None  
- **Modified classes**:  
  - `TestCase` in `src/interview_workbook/leetcode/_runner.py` → Remove `show_details` and progress-related attributes.  
- **Removed classes**: None

[Dependencies]  
No new dependencies are required.

We will ensure that no third-party progress tracking libraries (e.g., tqdm) are used. If present, they will be removed.

[Testing]  
We will update tests to reflect the removal of progress tracking.

- Modify `tests/test_flask_smoke.py` to ensure UI loads without progress indicators.  
- Modify `tests/test_demos.py` to validate simplified demo outputs.  
- Remove or adjust any tests that assert progress tracking behavior.  

[Implementation Order]  
We will proceed in the following order:

1. Update `flask_app/templates` and `flask_app/static/style.css` to remove progress UI.  
2. Update `flask_app/app.py` to remove backend progress injection.  
3. Update `src/main.py` to simplify demo discovery and execution.  
4. Update `src/interview_workbook/leetcode/_runner.py` to remove progress tracking logic.  
5. Update tests (`tests/test_flask_smoke.py`, `tests/test_demos.py`) to reflect simplified UI and outputs.  
6. Run full test suite to validate changes.
