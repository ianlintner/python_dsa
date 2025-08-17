# Implementation Plan

[Overview]
Ensure the repository maintains ≥90% test coverage and that all algorithm demos and Flask visualizations run without errors in CI by adding coverage enforcement, augmenting tests, and fixing any demo-breaking defects.

This implementation will:
- Enforce a 90% coverage threshold across all code under src/.
- Expand the test suite to cover uncovered modules and to smoke-test Flask endpoints and headless demo() functions.
- Fix a discovered defect in floyd_warshall that would break the negative-cycle demo, ensuring demos are stable.
- Update CI to measure coverage and fail if the threshold is not met, with artifacts to aid local debugging.

[Types]  
Minimal type-system changes: introduce an explicit negative-infinity constant and remove a runtime-unsafe sentinel.

Type and constant specifications:
- File: src/interview_workbook/graphs/floyd_warshall.py
  - Add constant: NEG_INF: float = float("-inf")
  - Replace any usage of undefined -INF sentinel with NEG_INF.
  - Remove or inline dead helpers related to -INF placeholder (_propagate_neg_inf), or keep only if explicitly used.
  - Keep existing typing (list[list[float]], list[list[int | None]]) and guard reconstruct_path against None safely (already present).

[Files]
Add pytest-cov configuration, expand tests, and adjust a few existing files to enforce coverage and stabilize demos.

New files to be created:
- tests/test_demos.py
  - Purpose: iterate all modules under src that expose a callable demo() and assert they run without exceptions. Use deterministic seeds where applicable (via random.seed) and cap any excessive output by not asserting on content. Provide a skip/allowlist mechanism if any demo proves flaky on CI.
- tests/test_flask_smoke.py
  - Purpose: Flask smoke tests using app.test_client():
    - GET routes: "/", "/big_o", "/viz_sorting", "/viz_graph", "/viz_path", "/viz_arrays", "/viz_mst", "/viz_topo", "/viz_nn"
    - POST API routes with minimal payloads to validate JSON responses: "/api/viz/sorting", "/api/viz/graph", "/api/viz/path", "/api/viz/arrays", "/api/viz/mst", "/api/viz/topo", "/api/viz/nn"
    - "/demo" flow: render page for a discovered module and run it via POST to ensure output/errors handling is robust.
- tests/test_graphs_floyd_warshall.py
  - Purpose: unit tests for floyd_warshall covering:
    - No negative cycles, correct APSP distances and path reconstruction.
    - Negative cycle case: verify distances influenced by the cycle become float("-inf") and next_hop paths are undefined (None).
- tests/test_dp_lcs.py
  - Purpose: coverage for src/dp/lcs.py (lcs_length and lcs_reconstruct basic assertions).
- tests/test_math_utils_extra.py
  - Purpose: additional coverage for number theory helpers not currently exercised (e.g., smallest_prime_factors, factorize_with_spf, prefix_sums_2d/sum_region, mod_inverse variants).

Existing files to be modified:
- pyproject.toml
  - [project.optional-dependencies].dev: add "pytest-cov>=4.1.0".
  - [tool.pytest.ini_options].addopts: change to include coverage and threshold:
    - "-q --cov=src --cov-report=term-missing:skip-covered --cov-report=xml --cov-fail-under=90"
- .github/workflows/ci.yml
  - Ensure tests run with coverage (picked up from addopts).
  - Add step to upload coverage.xml as an artifact named "coverage-xml".
- Makefile (optional quality-of-life)
  - Add target coverage to run pytest with coverage (redundant if addopts exists but helpful):
    - coverage: $(PYTHON) -m pytest
- src/interview_workbook/graphs/floyd_warshall.py
  - Replace -INF with an explicit NEG_INF constant; remove the name-defined type-ignores and any dead placeholder logic tied to the previous sentinel.
  - Keep demo() intact; it should no longer error on negative cycles.

Files to be moved/deleted:
- None required. If _propagate_neg_inf is dead code after changes, either remove it or leave with a comment; choice documented in Functions section.

[Functions]
Introduce no new library functions; fix a defect and add tests that exercise public functions and demos.

New functions:
- None in library code.
- Test helpers inside tests/ as needed (e.g., a discover_demos() helper mirroring flask_app.app.discover_demos but operating purely on src to collect module demo() targets).

Modified functions:
- src/interview_workbook/graphs/floyd_warshall.py:floyd_warshall(dist)
  - Behavior change: when negative cycles are detected, set dist[i][j] = NEG_INF (float("-inf")) instead of an undefined -INF sentinel. Remove type: ignore[name-defined]. Ensure next_hop[i][j] = None in that case, consistent with "path undefined due to negative cycle" semantics.
- Optional cleanup: remove _propagate_neg_inf or update its docstring to note it is no longer used.

Removed functions:
- src/interview_workbook/graphs/floyd_warshall.py:_propagate_neg_inf (only if unused after refactor). Replacement strategy: direct usage of NEG_INF.

[Classes]
No new classes; no class modifications required.

[Dependencies]
Add pytest-cov for coverage enforcement.

Details:
- Add dev dependency: pytest-cov>=4.1.0
- No runtime dependencies added; Flask already present.
- No coverage exclusions: apply to all src/*.

[Testing]
Add comprehensive tests for coverage and demo/visualization stability.

Test additions and strategies:
- Demos headless:
  - Iterate all src modules with a callable demo() (excluding __init__.py).
  - Import module and call demo(); assert no exception. Seed random if needed (random.seed(0)).
  - Provide a small skip set if any demo is inherently long-running or env-sensitive (e.g., concurrency demos). If discovered flaky, parametrize to smaller bounds in future PR; for now, capture and mark xfail on instability.
- Flask smoke tests:
  - Use test_client to GET dashboard and visualization pages; assert 200 and that the HTML contains known titles.
  - For each /api/viz/* endpoint, POST minimal valid payload and assert JSON contains expected keys ("frames", "grid", etc.) or valid "output" in /api/demo.
  - Exercise /demo: GET to render meta then POST to run single representative demo (e.g., interview_workbook.algorithms.sorting.quick_sort).
- Floyd–Warshall:
  - Construct graphs with and without negative cycles:
    - Without: verify specific shortest paths and reconstruct_path correctness.
    - With: verify NEG_INF propagation and has_negative_cycle returns True. path reconstruction should return [] when undefined.
- DP and number theory small cases:
  - lcs_length/lcs_reconstruct simple strings.
  - smallest_prime_factors + factorize_with_spf basic assertions.
  - prefix_sums_2d + sum_region on a tiny matrix.
  - mod_inverse_fermat/extgcd with small primes/composites where defined.

Determinism and runtime:
- Set seeds for visualizations and demos where possible.
- Keep array sizes/grid sizes small in API payloads to keep CI runtime low.

[Implementation Order]
Apply fixes and configuration before adding new tests, then enforce coverage in CI.

1. Update pyproject.toml dev extras to include pytest-cov and update pytest addopts with coverage threshold and reports.
2. Fix floyd_warshall: introduce NEG_INF constant and replace undefined -INF sentinel; remove type ignore; remove dead helper if applicable.
3. Add tests:
   - tests/test_graphs_floyd_warshall.py (APSP + negative cycle).
   - tests/test_dp_lcs.py and tests/test_math_utils_extra.py (targeted coverage).
   - tests/test_demos.py (headless demo() run).
   - tests/test_flask_smoke.py (GET UI pages and /api endpoints).
4. Update .github/workflows/ci.yml to upload coverage.xml as an artifact (tests already run with coverage via addopts).
5. Optional: add Makefile coverage target (quality-of-life).
6. Run pre-commit and pytest locally; confirm ≥90% coverage.
7. Push; ensure CI passes with enforced coverage and green demo tests.
