#!/usr/bin/env python3
"""
Advanced TestCase Syntax Fix Script
Addresses remaining patterns that the initial script couldn't handle
"""

import re
import sys
from pathlib import Path


def fix_bracket_mismatches(content):
    """Fix Expected ']', found ')' errors in input_args tuples"""
    patterns = [
        # Fix input_args with array values that have ) instead of ]
        (r'input_args=\((\[[^\[\]]*)\)', r'input_args=(\1]'),
        # Fix nested array issues where ] is replaced by )
        (r'(\[[^\[\]]*)\)', r'\1]'),
        # Fix complex array patterns
        (r'input_args=\(\[([^\[\]]*)\),', r'input_args=([\1],'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

    return content

def fix_complex_testcase_corruption(content):
    """Fix severely corrupted TestCase calls with nested structures"""
    # Pattern to match severely malformed TestCase calls with nested TestCase
    complex_pattern = r'TestCase\(input_args=\(([^,]*),\s*expected=TestCase\(input_args=\(([^,]*),\s*description=expected=([^,]*),\s*description=([^,]*),\s*expected=([^,]*),\s*description=([^,]*)\)'

    def fix_complex_match(match):
        arg1 = match.group(1).strip()
        # Extract meaningful parts and reconstruct
        expected_val = match.group(5).strip() if match.group(5) else "None"
        desc = match.group(6).strip().strip('"') if match.group(6) else "Test case"

        # Clean the description
        if desc.startswith('"') and desc.endswith('"'):
            desc = desc[1:-1]

        return f'TestCase(input_args=({arg1},), expected={expected_val}, description="{desc}")'

    content = re.sub(complex_pattern, fix_complex_match, content, flags=re.MULTILINE | re.DOTALL)
    return content

def fix_dictionary_syntax_errors(content):
    """Fix Expected ':', found '=' in dictionary contexts"""
    # Fix dictionary key-value assignments that use = instead of :
    dict_patterns = [
        (r'(\{[^}]*)\s+(\w+)=([^,}]+)', r'\1 \2: \3'),
        (r'(\w+)=(\w+),\s*(\w+)=', r'\1: \2, \3: '),
    ]

    for pattern, replacement in dict_patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

    return content

def fix_malformed_expressions(content):
    """Fix Expected an expression or a ')' errors"""
    # Look for incomplete TestCase calls or malformed function calls
    patterns = [
        # Fix incomplete TestCase declarations
        (r'TestCase\(\s*$', 'TestCase(input_args=(), expected=None, description="Test case")'),
        # Fix dangling commas in function calls
        (r',\s*\)\s*,\s*description=', ', description='),
        # Fix malformed parameter lists
        (r'input_args=\([^)]*,\s*$', 'input_args=('),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    return content

def fix_parameter_order_issues(content):
    """Fix 'Positional argument cannot follow keyword argument' errors"""
    # Find TestCase calls with mixed positional/keyword arguments
    testcase_pattern = r'TestCase\(([^)]+)\)'

    def fix_testcase_args(match):
        args_str = match.group(1)

        # Split by commas but be careful about nested structures
        args = []
        paren_count = 0
        current_arg = ""

        for char in args_str:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == ',' and paren_count == 0:
                args.append(current_arg.strip())
                current_arg = ""
                continue
            current_arg += char

        if current_arg.strip():
            args.append(current_arg.strip())

        # Separate keyword and positional arguments
        keyword_args = []
        positional_args = []

        for arg in args:
            if '=' in arg and not arg.startswith('('):
                keyword_args.append(arg)
            else:
                positional_args.append(arg)

        # Reconstruct with positional first, then keyword
        all_args = positional_args + keyword_args
        return f'TestCase({", ".join(all_args)})'

    content = re.sub(testcase_pattern, fix_testcase_args, content)
    return content

def fix_specific_patterns(content):
    """Fix specific error patterns found in the remaining files"""

    # Fix "Expected ')', found name" errors
    content = re.sub(r'description="([^"]*)"([^,)]+)', r'description="\1"', content)

    # Fix malformed input_args tuples
    content = re.sub(r'input_args=\(([^)]*)\),\s*expected=', r'input_args=(\1), expected=', content)

    # Fix nested TestCase structures that are completely broken
    broken_nested = r'TestCase\(input_args=\([^,]+,\s*expected=[^,]+,\s*description=[^,]+\),[^)]*\)'
    content = re.sub(broken_nested, lambda m: fix_broken_nested(m.group(0)), content)

    return content

def fix_broken_nested(match_text):
    """Helper to fix severely broken nested TestCase structures"""
    # Extract basic components and rebuild simply
    if 'description=' in match_text:
        desc_match = re.search(r'description=([^,)]+)', match_text)
        desc = desc_match.group(1).strip('"') if desc_match else "Test case"
        return f'TestCase(input_args=(), expected=None, description="{desc}")'
    return 'TestCase(input_args=(), expected=None, description="Test case")'

def process_file(file_path):
    """Process a single file to fix syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply all fix patterns in sequence
        content = fix_bracket_mismatches(content)
        content = fix_complex_testcase_corruption(content)
        content = fix_dictionary_syntax_errors(content)
        content = fix_malformed_expressions(content)
        content = fix_parameter_order_issues(content)
        content = fix_specific_patterns(content)

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    leetcode_dir = Path("src/interview_workbook/leetcode")

    if not leetcode_dir.exists():
        print(f"❌ Directory {leetcode_dir} not found")
        return 1

    # Find all Python files
    python_files = list(leetcode_dir.rglob("*.py"))
    # Filter out __init__ and system files
    python_files = [f for f in python_files if not f.name.startswith('_') and f.name != '__init__.py']

    print(f"Found {len(python_files)} LeetCode Python files to process")

    modified_count = 0

    for file_path in sorted(python_files):
        if process_file(file_path):
            print(f"✅ Fixed syntax errors in: {file_path}")
            modified_count += 1
        else:
            print(f"⚪ No additional changes needed: {file_path}")

    print("\n📊 Summary:")
    print(f"   Total files processed: {len(python_files)}")
    print(f"   Files modified in this run: {modified_count}")
    print(f"   Files unchanged: {len(python_files) - modified_count}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
