# Proxy module to expose interview_workbook sorting under src.algorithms.sorting.*
# This enables tests importing src.algorithms.sorting.* to resolve correctly.
from interview_workbook.algorithms.sorting.bubble_sort import *  # noqa: F401,F403
