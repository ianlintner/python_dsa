#!/usr/bin/env python3
"""
Script to fix TestCase parameter issues in LeetCode files.

The TestCase class expects:
- input_args (positional)
- expected (positional)
- description (optional keyword)

But some files are using incorrect parameter names like:
- name= instead of description=
- input_data= instead of input_args=
- input= instead of input_args=
"""

import re
from pathlib import Path


def fix_testcase_in_file(file_path):
    """Fix TestCase parameters in a single file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Pattern to match TestCase constructor calls
    testcase_pattern = r"TestCase\s*\(\s*([^)]+)\s*\)"

    def fix_testcase_match(match):
        args_str = match.group(1)

        # Split arguments carefully (handling nested parentheses and quotes)
        args = []
        current_arg = ""
        paren_depth = 0
        bracket_depth = 0
        in_quotes = False
        quote_char = None

        for char in args_str:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
                current_arg += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_arg += char
            elif not in_quotes:
                if char == "(":
                    paren_depth += 1
                    current_arg += char
                elif char == ")":
                    paren_depth -= 1
                    current_arg += char
                elif char == "[":
                    bracket_depth += 1
                    current_arg += char
                elif char == "]":
                    bracket_depth -= 1
                    current_arg += char
                elif char == "," and paren_depth == 0 and bracket_depth == 0:
                    args.append(current_arg.strip())
                    current_arg = ""
                else:
                    current_arg += char
            else:
                current_arg += char

        if current_arg.strip():
            args.append(current_arg.strip())

        # Now fix the arguments
        fixed_args = []
        input_args_found = False
        expected_found = False

        for arg in args:
            arg = arg.strip()
            if arg.startswith("name="):
                # Change name= to description=
                fixed_args.append("description=" + arg[5:])
            elif arg.startswith("input_data="):
                # Change input_data= to input_args=
                fixed_args.append("input_args=" + arg[11:])
                input_args_found = True
            elif arg.startswith("input="):
                # Change input= to input_args=
                fixed_args.append("input_args=" + arg[6:])
                input_args_found = True
            elif arg.startswith("expected="):
                fixed_args.append(arg)
                expected_found = True
            elif arg.startswith("description="):
                fixed_args.append(arg)
            else:
                # Positional argument - figure out what it should be
                if not input_args_found:
                    fixed_args.append("input_args=" + arg)
                    input_args_found = True
                elif not expected_found:
                    fixed_args.append("expected=" + arg)
                    expected_found = True
                else:
                    fixed_args.append(arg)

        return f"TestCase(\n        {',\n        '.join(fixed_args)},\n    )"

    # Apply the fixes
    content = re.sub(testcase_pattern, fix_testcase_match, content, flags=re.MULTILINE | re.DOTALL)

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
