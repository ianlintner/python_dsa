#!/usr/bin/env python3
"""
Comprehensive fix for remaining LeetCode syntax errors.
This script targets the most severely corrupted files with systematic repairs.
"""

import os
import re

def fix_class_method_signatures(content: str) -> str:
    """Fix class method signatures that are missing 'self' parameter."""
    # Fix method definitions missing self parameter
    patterns = [
        (r'(\s+)def (\w+)\(\) -> ([^:]+):', r'\1def \2(self) -> \3:'),
        (r'(\s+)def (\w+)\(([^)]*)\) -> ([^:]+):', lambda m: f'{m.group(1)}def {m.group(2)}(self, {m.group(3)}) -> {m.group(4)}:' if 'self' not in m.group(3) else m.group(0)),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content

def fix_corrupted_docstrings(content: str) -> str:
    """Fix corrupted docstrings that became Python code."""
    lines = content.split('\n')
    result_lines = []
    in_corrupted_docstring = False

    for i, line in enumerate(lines):
        # Detect lines that look like corrupted docstrings (unindented text after function def)
        if (re.match(r'\s+def \w+.*:', line) and
            i + 1 < len(lines) and
            re.match(r'\s+"""', lines[i + 1])):

            # This looks like a proper docstring start
            result_lines.append(line)
            continue

        # Look for lines that are clearly not Python code but text
        if (re.match(r'\s*[A-Z][^=:]*[.!?]\s*$', line) or
            re.match(r'\s*•\s+', line) or
            re.match(r'\s*-\s+[A-Z]', line)):
            # Skip these text lines that shouldn't be in Python code
            continue

        # Fix lines that look like corrupted docstring content
        if re.match(r'\s*(Key Insights|Common Pitfalls|Follow-up Questions|Algorithm Steps)=', line):
            continue  # Skip these corrupted headers

        result_lines.append(line)

    return '\n'.join(result_lines)

def fix_missing_imports(content: str) -> str:
    """Add missing imports that are commonly needed."""
    lines = content.split('\n')

    # Check if we need Optional import
    if 'Optional[' in content and 'from typing import' in content:
        for i, line in enumerate(lines):
            if line.startswith('from typing import') and 'Optional' not in line:
                # Add Optional to the import
                if ', ' in line:
                    lines[i] = line.rstrip() + ', Optional'
                else:
                    parts = line.split(' import ')
                    lines[i] = f"{parts[0]} import {parts[1]}, Optional"
                break

    return '\n'.join(lines)

def fix_malformed_function_calls(content: str) -> str:
    """Fix malformed function calls and TestCase definitions."""
    # Fix TestCase calls with wrong parameter syntax
    patterns = [
        # Fix TestCase with description= inside input_args
        (r'TestCase\(input_args=\([^)]*description="[^"]*"[^)]*\),\s*expected=([^,]+),\s*description="([^"]*)"\)',
         r'TestCase(input_args=(\1,), expected=\2, description="\3")'),

        # Fix malformed list/tuple syntax in TestCase
        (r'TestCase\(input_args=\(([^)]*),\s*expected:\s*([^)]+)\)',
         r'TestCase(input_args=(\1,), expected=\2, description="Test case")'),

        # Fix register_problem calls split across lines incorrectly
        (r'register_problem\(\s*id=(\d+),\s*slug="([^"]*)",', r'register_problem(\n    id=\1,\n    slug="\2",'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

    return content

def fix_indentation_errors(content: str) -> str:
    """Fix basic indentation errors."""
    lines = content.split('\n')
    result_lines = []

    for i, line in enumerate(lines):
        # Fix lines that should be indented after class/function definitions
        if (i > 0 and
            re.match(r'\s*(class \w+:|def \w+.*:)\s*$', lines[i-1]) and
            line.strip() and
            not line.startswith('    ') and
            not line.strip().startswith('"""')):
            # Add proper indentation
            result_lines.append('    ' + line.strip())
        else:
            result_lines.append(line)

    return '\n'.join(result_lines)

def process_file(filepath: str) -> bool:
    """Process a single file and apply all fixes."""
    try:
        with open(filepath, 'r') as f:
            original_content = f.read()

        if not original_content.strip():
            return False

        content = original_content

        # Apply all fixes
        content = fix_class_method_signatures(content)
        content = fix_corrupted_docstrings(content)
        content = fix_missing_imports(content)
        content = fix_malformed_function_calls(content)
        content = fix_indentation_errors(content)

        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"✓ Fixed: {filepath}")
            return True
        else:
            return False

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all LeetCode files."""
    base_dir = "src/interview_workbook/leetcode"

    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} not found!")
        return

    total_files = 0
    fixed_files = 0

    # Process all Python files in the LeetCode directory
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py') and not file.startswith('_'):
                filepath = os.path.join(root, file)
                total_files += 1

                if process_file(filepath):
                    fixed_files += 1

    print(f"\n=== Summary ===")
    print(f"Total files processed: {total_files}")
    print(f"Files fixed: {fixed_files}")
    print(f"Files unchanged: {total_files - fixed_files}")

if __name__ == "__main__":
    main()
