#!/usr/bin/env python3
"""
Comprehensive TestCase syntax fixer for LeetCode files.

This script fixes various syntax errors introduced by previous automated fixes:
1. Double commas in tuples: input_args=("value",,)
2. Duplicate parameter names: input_args=input_args=
3. Positional arguments following keyword arguments
4. Malformed tuples and missing parentheses
5. Missing closing quotes in string literals
"""

import os
import re
from pathlib import Path


def fix_double_commas(content: str) -> str:
    """Fix double commas in tuple literals."""
    # Fix patterns like ("value",,) -> ("value",)
    content = re.sub(r'(["\'])\s*,\s*,\s*\)', r"\1,)", content)

    # Fix patterns like (value,,) -> (value,)
    content = re.sub(r"([^\s,]+)\s*,\s*,\s*\)", r"\1,)", content)

    # Fix patterns like ,, inside tuples
    content = re.sub(r",\s*,(?=\s*[,)])", r",", content)

    return content


def fix_duplicate_input_args(content: str) -> str:
    """Fix duplicate input_args parameter names."""
    # Fix input_args=input_args= patterns
    content = re.sub(r"input_args\s*=\s*input_args\s*=", "input_args=", content)

    return content


def fix_expected_parameter(content: str) -> str:
    """Fix expected= parameter positioning."""
    # Fix expected=expected= patterns
    content = re.sub(r"expected\s*=\s*expected\s*=", "expected=", content)

    return content


def fix_testcase_structure(content: str) -> str:
    """Fix TestCase structure to use proper keyword arguments."""

    # Pattern 1: Fix malformed TestCase with keyword args followed by positional
    # TestCase(input_args=(...), positional_expected, "description")
    pattern1 = re.compile(
        r'TestCase\s*\(\s*input_args\s*=\s*\([^)]*\)\s*,?\s*\)\s*,\s*([^,\n]+)\s*,\s*(["\'][^"\']*["\'])\s*\)',
        re.MULTILINE | re.DOTALL,
    )

    def replace1(match):
        expected = match.group(1).strip()
        description = match.group(2).strip()
        # Extract the input_args content from the original match
        input_part = match.group(0).split("input_args=")[1].split("),")[0] + ")"
        return f"TestCase(input_args={input_part}, expected={expected}, description={description})"

    content = pattern1.sub(replace1, content)

    # Pattern 2: Fix TestCase with broken tuple structure
    # TestCase(\n        input_args=("value",,\n    ), expected, description)
    pattern2 = re.compile(
        r'TestCase\s*\(\s*input_args\s*=\s*\([^)]*,\s*,\s*\)\s*,\s*([^,\n]+)\s*,\s*(["\'][^"\']*["\'])',
        re.MULTILINE | re.DOTALL,
    )

    def replace2(match):
        expected = match.group(1).strip()
        description = match.group(2).strip()
        # Extract and fix the input_args tuple
        full_match = match.group(0)
        tuple_match = re.search(r"input_args\s*=\s*\(([^)]*)\)", full_match, re.DOTALL)
        if tuple_match:
            tuple_content = tuple_match.group(1).strip()
            # Remove double commas and fix tuple
            tuple_content = re.sub(r",\s*,", ",", tuple_content)
            tuple_content = re.sub(
                r",\s*$", "", tuple_content
            )  # Remove trailing comma before closing
            if not tuple_content.endswith(",") and "," not in tuple_content:
                tuple_content += ","  # Add comma for single-item tuple
            return f"TestCase(input_args=({tuple_content}), expected={expected}, description={description})"

    content = pattern2.sub(replace2, content)

    return content


def fix_missing_quotes(content: str) -> str:
    """Fix missing closing quotes in string literals."""
    # This is a basic fix - more complex cases may need manual intervention
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Check for unbalanced quotes (simple heuristic)
        single_quotes = line.count("'")
        double_quotes = line.count('"')

        # If odd number of quotes, might be missing closing quote
        if single_quotes % 2 == 1 and "missing closing quote" in line:
            # Try to add closing quote at end of string context
            line = re.sub(r"([^']*'[^']*)'?\s*$", r"\1'", line)
        elif double_quotes % 2 == 1 and "missing closing quote" in line:
            line = re.sub(r'([^"]*"[^"]*)"?\s*$', r'\1"', line)

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_colon_errors(content: str) -> str:
    """Fix 'Expected :, found =' errors in dictionary-like structures."""
    # Fix patterns where = is used instead of : in dict-like contexts
    # This is context-sensitive, so be careful

    # Fix test case parameter patterns like expected=[1: 2] where : should be ,
    content = re.sub(r"expected\s*=\s*\[([^\]]*?):\s*([^\]]*?)\]", r"expected=[\1, \2]", content)

    return content


def fix_leetcode_file(file_path: Path) -> bool:
    """Fix a single LeetCode Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        content = original_content

        # Apply all fixes in sequence
        content = fix_double_commas(content)
        content = fix_duplicate_input_args(content)
        content = fix_expected_parameter(content)
        content = fix_testcase_structure(content)
        content = fix_missing_quotes(content)
        content = fix_colon_errors(content)

        # Additional specific pattern fixes

        # Fix input_args=(value,, -> input_args=(value,)
        content = re.sub(r"input_args\s*=\s*\(([^,)]+),\s*,\s*\)", r"input_args=(\1,)", content)

        # Fix ) expected= -> , expected=
        content = re.sub(r"\)\s*,\s*expected\s*=", r", expected=", content)

        # Fix patterns like ), True, -> , expected=True,
        content = re.sub(
            r'input_args\s*=\s*\([^)]*\)\s*,?\s*\)\s*,\s*([^,\n]+)\s*,\s*(["\'][^"\']*["\'])',
            lambda m: f"input_args={m.group(0).split('input_args=')[1].split('),')[0]}), expected={m.group(1).strip()}, description={m.group(2).strip()}",
            content,
        )

        # Write back only if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all LeetCode files."""
    leetcode_dir = Path("src/interview_workbook/leetcode")

    if not leetcode_dir.exists():
        print(f"Directory {leetcode_dir} does not exist!")
        return

    # Find all Python files in leetcode subdirectories
    python_files = []
    for root, dirs, files in os.walk(leetcode_dir):
        # Skip private/internal directories
        if any(part.startswith("_") for part in Path(root).parts):
            continue

        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                python_files.append(Path(root) / file)

    print(f"Found {len(python_files)} Python files to process...")

    fixed_count = 0
    for file_path in sorted(python_files):
        if fix_leetcode_file(file_path):
            fixed_count += 1

    print(f"\nProcessing complete! Fixed {fixed_count} files out of {len(python_files)} total.")


if __name__ == "__main__":
    main()
