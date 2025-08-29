#!/usr/bin/env python3
"""
Final comprehensive fix for all remaining LeetCode TestCase syntax errors.

This script addresses the remaining syntax errors preventing ruff format from parsing files:
1. Misplaced expected= and description= inside input_args tuples
2. Positional arguments following keyword arguments
3. Missing commas in single-element tuples
4. Mismatched parentheses and brackets
5. Invalid = usage in dictionary contexts
"""

import re
from pathlib import Path


def fix_malformed_testcase_calls(content: str) -> str:
    """Fix all malformed TestCase calls with comprehensive pattern matching."""

    # Pattern 1: Fix input_args with embedded expected=/description=
    # Example: TestCase(input_args=(12, expected=[10, description=8, 0, 5, 3], [2, 4, 1, 1, 3)), 3, "Example 1")
    pattern1 = re.compile(
        r'TestCase\(\s*input_args=\(([^)]*expected=\s*[^,)]+[^)]*)\),\s*([^,]+),\s*([^)]+)\)',
        re.MULTILINE | re.DOTALL
    )

    def fix_pattern1(match):
        args_with_embedded = match.group(1)
        second_part = match.group(2).strip()
        third_part = match.group(3).strip()

        # Extract the actual input_args before the embedded expected=
        # This is a complex pattern, let's try to extract the valid input args
        # Look for the pattern up to "expected="
        pre_expected = re.split(r',\s*expected=', args_with_embedded)[0]

        # Clean up the input args - remove any remaining malformed parts
        clean_input_args = re.sub(r'\s*description=\s*[^,)]*', '', pre_expected)
        clean_input_args = re.sub(r'\s*expected=\s*[^,)]*', '', clean_input_args)
        clean_input_args = clean_input_args.strip().rstrip(',')

        return f'TestCase(input_args=({clean_input_args},), expected={second_part}, description={third_part})'

    content = pattern1.sub(fix_pattern1, content)

    # Pattern 2: Fix simple positional arguments following keyword arguments
    # Example: TestCase(input_args=(1), ["()"], "Example: n=1")
    pattern2 = re.compile(
        r'TestCase\(\s*input_args=\(([^)]+)\),\s*([^,\[\{][^,)]*),\s*("[^"]*")\)',
        re.MULTILINE
    )

    def fix_pattern2(match):
        input_args = match.group(1).strip()
        expected_val = match.group(2).strip()
        description = match.group(3).strip()

        # Ensure input_args is a proper tuple
        if not input_args.endswith(',') and ',' not in input_args:
            input_args = input_args + ','

        return f'TestCase(input_args=({input_args}), expected={expected_val}, description={description})'

    content = pattern2.sub(fix_pattern2, content)

    # Pattern 3: Fix TestCase calls with list/dict expected values as positional args
    # Example: TestCase(input_args=(1), ["()"], "Example: n=1")
    pattern3 = re.compile(
        r'TestCase\(\s*input_args=\(([^)]+)\),\s*(\[[^\]]*\]|\{[^}]*\}),\s*("[^"]*")\)',
        re.MULTILINE | re.DOTALL
    )

    def fix_pattern3(match):
        input_args = match.group(1).strip()
        expected_val = match.group(2).strip()
        description = match.group(3).strip()

        # Ensure input_args is a proper tuple
        if not input_args.endswith(',') and ',' not in input_args:
            input_args = input_args + ','

        return f'TestCase(input_args=({input_args}), expected={expected_val}, description={description})'

    content = pattern3.sub(fix_pattern3, content)

    # Pattern 4: Fix mismatched parentheses - convert ] to ) in TestCase input_args
    pattern4 = re.compile(
        r'TestCase\(\s*input_args=\(([^)\]]*)\]([^)]*)\)',
        re.MULTILINE | re.DOTALL
    )

    def fix_pattern4(match):
        args_before = match.group(1)
        args_after = match.group(2) if match.group(2) else ""
        return f'TestCase(input_args=({args_before}){args_after})'

    content = pattern4.sub(fix_pattern4, content)

    # Pattern 5: Fix dictionary syntax - change = to : in dictionary contexts
    # Look for patterns like {"key" = "value"} and change to {"key": "value"}
    pattern5 = re.compile(r'(\{[^}]*)"([^"]+)"\s*=\s*("?[^,}]+"?)([^}]*\})')

    def fix_pattern5(match):
        before = match.group(1)
        key = match.group(2)
        value = match.group(3)
        after = match.group(4)
        return f'{before}"{key}": {value}{after}'

    content = pattern5.sub(fix_pattern5, content)

    # Pattern 6: Fix tuple syntax issues - ensure proper tuple format
    # Fix cases like input_args=([1, 2, 3]) to input_args=([1, 2, 3],)
    pattern6 = re.compile(r'input_args=\((\[[^\]]+\])\)')

    def fix_pattern6(match):
        list_content = match.group(1)
        return f'input_args=({list_content},)'

    content = pattern6.sub(fix_pattern6, content)

    return content


def process_file(file_path: Path) -> bool:
    """Process a single Python file to fix TestCase syntax errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        fixed_content = fix_malformed_testcase_calls(content)

        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ Fixed syntax errors in: {file_path}")
            return True
        else:
            print(f"⚪ No changes needed: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    """Process all LeetCode Python files to fix remaining syntax errors."""
    leetcode_dir = Path("src/interview_workbook/leetcode")

    if not leetcode_dir.exists():
        print(f"❌ LeetCode directory not found: {leetcode_dir}")
        return

    # Find all Python files in the leetcode directory (excluding __init__.py and private modules)
    python_files = []
    for file_path in leetcode_dir.rglob("*.py"):
        if file_path.name not in ["__init__.py"] and not file_path.name.startswith("_"):
            python_files.append(file_path)

    print(f"Found {len(python_files)} LeetCode Python files to process")

    fixed_count = 0
    for file_path in sorted(python_files):
        if process_file(file_path):
            fixed_count += 1

    print("\n📊 Summary:")
    print(f"   Total files processed: {len(python_files)}")
    print(f"   Files modified: {fixed_count}")
    print(f"   Files unchanged: {len(python_files) - fixed_count}")


if __name__ == "__main__":
    main()
