import os
import sys

# Ensure 'src' directory is on sys.path so tests can import packages like
# 'algorithms', 'data_structures', etc. without installation.
THIS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(THIS_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
