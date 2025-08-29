#!/usr/bin/env python3
"""
Script to fix TestCase parameter issues in LeetCode files.

The TestCase class expects:
- input_args (positional)
- expected (positional)
- description (optional keyword)

But some files have syntax errors from previous fixes.
"""

import re
from pathlib import Path


def fix_testcase_in_file(file_path):
    """Fix TestCase parameters in a single file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Fix duplicate input_args= patterns
    content = re.sub(r"input_args=input_args=", "input_args=", content)

    # Fix missing commas in tuples by finding patterns like ([...], without closing paren
    # Fix patterns like: input_args=([1, 2, 3], 4,\n)
    def fix_tuple_pattern(match):
        full_match = match.group(0)
        # Extract the tuple content
        tuple_content = match.group(1)
        return f"input_args=({tuple_content})"

    # Pattern to match: input_args=([...], something,\n)
    content = re.sub(
        r"input_args=\(([^)]+),\s*\)", fix_tuple_pattern, content, flags=re.MULTILINE | re.DOTALL
    )

    # Fix standalone expected/description that became positional after keyword args
    # Pattern: TestCase(\n  input_args=...,\n), value, "description"
    def fix_positional_after_keyword(match):
        before = match.group(1)
        value = match.group(2).strip()
        desc = match.group(3).strip() if match.group(3) else '""'

        # Determine if value looks like expected result or description
        if desc.startswith('"') or desc.startswith("'"):
            # value is expected, desc is description
            return f"{before}\n        expected={value},\n        description={desc},\n    )"
        else:
            # value might be description if it looks like one
            if value.startswith('"') or value.startswith("'"):
                return f"{before}\n        description={value},\n    )"
            else:
                return f"{before}\n        expected={value},\n    )"

    # Fix TestCase(...\n), value, "description" patterns
    content = re.sub(
        r"(TestCase\([^)]+\)),\s*([^,\n]+),?\s*([^,\n]*)\)",
        fix_positional_after_keyword,
        content,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Fix extra commas in input_args tuples
    content = re.sub(r"input_args=\(([^)]+),,\)", r"input_args=(\1)", content)

    # Fix malformed TestCase declarations with missing closing parens
    # Look for patterns like: input_args=("something",,
    content = re.sub(r"input_args=\(([^,)]+),,", r"input_args=(\1)", content)

    # Fix missing quotes in string literals - look for obvious cases
    content = re.sub(r'input_args=\(([^)]*"[^"]*)\n', r'input_args=(\1"),\n', content)

    if content != original_content:
        print(f"Fixed TestCase parameters in: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    """Main function to fix all TestCase issues."""
    leetcode_dir = Path("src/interview_workbook/leetcode")
    files_fixed = 0

    for py_file in leetcode_dir.rglob("*.py"):
        if py_file.name.startswith("_"):
            continue  # Skip internal files

        if fix_testcase_in_file(py_file):
            files_fixed += 1

    print(f"Fixed TestCase parameters in {files_fixed} files")


if __name__ == "__main__":
    main()
