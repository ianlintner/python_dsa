#!/usr/bin/env python3
"""
Comprehensive script to fix remaining TestCase and function definition corruption patterns.
Addresses the systematic corruption issues shown in ruff format errors.
"""

import os
import re


def fix_testcase_parameter_corruption(content):
    """Fix TestCase calls with malformed parameter structures."""
    # Pattern 1: Fix TestCase calls where expected: and description: appear as positional args
    # Example: TestCase(input_args=("test"), expected: True, description: "test")
    # Should be: TestCase(input_args=("test",), expected=True, description="test")

    # Fix the basic expected: and description: syntax
    content = re.sub(
        r'(TestCase\([^)]*?)expected:\s*([^,)]+?),\s*description:\s*([^)]+?)\)',
        r'\1expected=\2, description=\3)',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # Fix missing closing quotes in test strings
    content = re.sub(
        r'TestCase\(input_args=\("([^"]*?)\),\s*expected([^,)]+?),\s*description([^)]+?)\)',
        r'TestCase(input_args=("\1",), expected\2, description\3)',
        content
    )

    # Fix incomplete TestCase calls that end abruptly
    content = re.sub(
        r'TestCase\(input_args=\(\s*\n\s*\]',
        r'TestCase(input_args=("",), expected=True, description="Placeholder")\n]',
        content,
        flags=re.MULTILINE
    )

    return content

def fix_function_definition_corruption(content):
    """Fix corrupted function definitions like 'def demo(-> str):'"""

    # Pattern: def demo(-> str): should be def demo() -> str:
    content = re.sub(
        r'def\s+(\w+)\(\s*->\s*([^)]+?)\)\s*:',
        r'def \1() -> \2:',
        content
    )

    # Pattern: def demo(-> str):"""docstring"""
    content = re.sub(
        r'def\s+(\w+)\(\s*->\s*([^)]+?)\)\s*:\s*"""',
        r'def \1() -> \2:\n    """',
        content
    )

    return content

def fix_register_problem_corruption(content):
    """Fix register_problem() calls with mixed positional/keyword arguments."""

    # Fix the colon syntax in register_problem calls
    # Pattern: slug: "value" should be slug="value"
    content = re.sub(
        r'(\s+)(\w+):\s*([^,\n]+?),',
        r'\1\2=\3,',
        content
    )

    return content

def fix_function_call_corruption(content):
    """Fix various function call corruptions."""

    # Fix time_complexity: "value" patterns in function calls
    content = re.sub(
        r'(\w+):\s*"([^"]+)"',
        r'\1="\2"',
        content
    )

    # Fix approach_notes: """ patterns
    content = re.sub(
        r'approach_notes:\s*"""',
        r'approach_notes="""',
        content
    )

    return content

def fix_url_corruption(content):
    """Fix URL corruption where https:// becomes https=//"""

    content = re.sub(r'https=//', r'https://', content)
    content = re.sub(r'http=//', r'http://', content)

    return content

def fix_dictionary_syntax_corruption(content):
    """Fix dictionary syntax where = appears instead of :"""

    # In string literals that look like dictionaries or key-value pairs
    # Be careful to only fix actual dictionary syntax, not assignment

    # Fix Key insights=value patterns in docstrings
    content = re.sub(
        r'(Key insights)=(\d+\.)',
        r'\1:\n\2',
        content
    )

    return content

def apply_all_fixes(content):
    """Apply all fix patterns to the content."""

    content = fix_testcase_parameter_corruption(content)
    content = fix_function_definition_corruption(content)
    content = fix_register_problem_corruption(content)
    content = fix_function_call_corruption(content)
    content = fix_url_corruption(content)
    content = fix_dictionary_syntax_corruption(content)

    return content

def process_file(file_path):
    """Process a single Python file to fix syntax errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        fixed_content = apply_all_fixes(original_content)

        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all LeetCode Python files."""

    leetcode_dir = "src/interview_workbook/leetcode"

    if not os.path.exists(leetcode_dir):
        print(f"Directory {leetcode_dir} not found!")
        return

    # Find all Python files in the LeetCode directory
    python_files = []
    for root, dirs, files in os.walk(leetcode_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    print(f"Found {len(python_files)} Python files to process...")

    fixed_count = 0

    for file_path in python_files:
        if process_file(file_path):
            fixed_count += 1
            print(f"Fixed: {file_path}")

    print("\nProcessing complete!")
    print(f"Fixed {fixed_count} out of {len(python_files)} files")

    if fixed_count > 0:
        print("\nNow run: python -m ruff format src/interview_workbook/leetcode/ --check")
        print("to verify the fixes")

if __name__ == "__main__":
    main()
