#!/usr/bin/env python3
"""
Comprehensive script to fix all remaining TestCase syntax errors in LeetCode files.
Handles multiple error patterns identified from ruff output.
"""

import glob
import re


def fix_testcase_positional_args(content: str) -> str:
    """Fix positional arguments following keyword arguments in TestCase calls."""
    # Pattern to match TestCase calls with mixed positional/keyword args
    pattern = r"TestCase\(\s*input_args=([^,)]+),\s*([^,)]+),\s*([^)]+)\)"

    def replace_mixed_args(match):
        input_args = match.group(1).strip()
        expected = match.group(2).strip()
        description = match.group(3).strip()

        # If expected doesn't start with a keyword, add expected=
        if not expected.startswith(("expected=", "name=")):
            expected = f"expected={expected}"

        # If description doesn't start with a keyword, add description=
        if not description.startswith(("description=", "name=")):
            description = f"description={description}"

        return f"TestCase(input_args={input_args}, {expected}, {description})"

    content = re.sub(pattern, replace_mixed_args, content, flags=re.MULTILINE | re.DOTALL)
    return content


def fix_malformed_testcase_calls(content: str) -> str:
    """Fix various malformed TestCase call patterns."""

    # Fix double commas
    content = re.sub(r",,+", ",", content)

    # Fix trailing commas before closing parenthesis in tuples
    content = re.sub(r",\s*\)", ")", content)

    # Fix duplicate parameter names like input_args=input_args=
    content = re.sub(r"(\w+)=\1=", r"\1=", content)

    # Fix malformed tuple declarations
    content = re.sub(r"input_args=\([^)]*,,", lambda m: m.group(0).replace(",,", ","), content)

    return content


def fix_bracket_mismatches(content: str) -> str:
    """Fix mismatched brackets and parentheses."""
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # Fix common bracket mismatches in TestCase calls
        if "TestCase(" in line and "])" in line:
            # Replace ]) with ))
            line = line.replace("])", "))")
        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_unterminated_strings(content: str) -> str:
    """Fix unterminated string literals."""
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        # Look for lines with odd number of quotes that might be unterminated
        if line.count('"') % 2 == 1 and not line.strip().endswith('"""'):
            # Try to close unterminated strings
            if "description=" in line:
                line = line + '"'
        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_dictionary_syntax(content: str) -> str:
    """Fix dictionary syntax errors like missing colons."""
    # Fix patterns like 'key' = value to 'key': value in dictionary contexts
    pattern = r"'([^']+)'\s*=\s*([^,}]+)"

    def replace_dict_equals(match):
        key = match.group(1)
        value = match.group(2).strip()
        return f"'{key}': {value}"

    # Only replace in contexts that look like dictionaries
    lines = content.split("\n")
    fixed_lines = []
    in_dict_context = False

    for line in lines:
        if "{" in line and "=" in line and ":" not in line:
            in_dict_context = True
        elif "}" in line:
            in_dict_context = False

        if in_dict_context:
            line = re.sub(pattern, replace_dict_equals, line)

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def fix_file(file_path: str) -> bool:
    """Fix all syntax errors in a single file. Returns True if changes were made."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        content = original_content

        # Apply all fixes
        content = fix_testcase_positional_args(content)
        content = fix_malformed_testcase_calls(content)
        content = fix_bracket_mismatches(content)
        content = fix_unterminated_strings(content)
        content = fix_dictionary_syntax(content)

        # Only write if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all LeetCode Python files."""

    # Find all Python files in the leetcode directory
    pattern = "src/interview_workbook/leetcode/**/*.py"
    python_files = glob.glob(pattern, recursive=True)

    # Filter out __init__.py and utility files
    python_files = [
        f
        for f in python_files
        if not f.endswith("__init__.py")
        and not any(part.startswith("_") for part in f.split("/") if part.endswith(".py"))
    ]

    print(f"Found {len(python_files)} Python files to process...")

    fixed_count = 0
    for file_path in python_files:
        if fix_file(file_path):
            print(f"Fixed: {file_path}")
            fixed_count += 1
        else:
            print(f"No changes needed: {file_path}")

    print(f"\nProcessing complete! Fixed {fixed_count} files out of {len(python_files)} total.")


if __name__ == "__main__":
    main()
