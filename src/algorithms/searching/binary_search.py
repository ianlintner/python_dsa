# Proxy module to expose interview_workbook searching under src.algorithms.searching.*
# This enables tests importing src.algorithms.searching.* to resolve correctly.
from interview_workbook.algorithms.searching.binary_search import *  # noqa: F401,F403
