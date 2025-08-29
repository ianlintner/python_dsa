#!/usr/bin/env python3
"""
Final script to fix remaining colon corruption issues in LeetCode files.
Addresses specific patterns like "Expected ':', found '='" errors.
"""

import os
import re


def fix_function_annotations(content):
    """Fix function annotation syntax issues."""

    # Pattern: def func_name= value should be def func_name: type
    content = re.sub(r"def\s+(\w+)\s*=\s*([^:]+):", r"def \1() -> \2:", content)

    # Pattern: def func() -> type= value should be def func() -> type:
    content = re.sub(r"(def\s+\w+\([^)]*\)\s*->\s*[^=]+)=([^:]+):", r"\1:", content)

    return content


def fix_dict_and_annotation_syntax(content):
    """Fix dictionary syntax and type annotations."""

    # Fix type annotations like "var= Type[Something]" should be "var: Type[Something]"
    content = re.sub(r"(\s+)(\w+)=\s*(Type\[[^\]]+\])", r"\1\2: \3", content)

    # Fix type annotations like "var= Dict[str, any]" should be "var: Dict[str, any]"
    content = re.sub(r"(\s+)(\w+)=\s*(Dict\[[^\]]+\])", r"\1\2: \3", content)

    # Fix type annotations like "var= List[Something]" should be "var: List[Something]"
    content = re.sub(r"(\s+)(\w+)=\s*(List\[[^\]]+\])", r"\1\2: \3", content)

    # Fix type annotations like "var= Optional[Something]" should be "var: Optional[Something]"
    content = re.sub(r"(\s+)(\w+)=\s*(Optional\[[^\]]+\])", r"\1\2: \3", content)

    return content


def fix_function_parameter_syntax(content):
    """Fix function parameter syntax issues."""

    # Pattern: func(param= type) should be func(param: type)
    content = re.sub(r"(\w+\s*\([^)]*?)(\w+)=([^,)]+)", r"\1\2: \3", content)

    return content


def fix_class_and_method_syntax(content):
    """Fix class and method definition syntax."""

    # Pattern: class ClassName= should be class ClassName:
    content = re.sub(r"class\s+(\w+)=([^:]*):", r"class \1:", content)

    return content


def fix_variable_annotation_syntax(content):
    """Fix variable annotation syntax issues."""

    # Pattern: variable= type (at start of line) should be variable: type
    content = re.sub(
        r"^(\s*)(\w+)=\s*([A-Z][a-zA-Z_\[\],\s]*?)\s*$", r"\1\2: \3", content, flags=re.MULTILINE
    )

    return content


def fix_dict_literal_syntax(content):
    """Fix dictionary literal syntax where = is used instead of :"""

    # Pattern: {"key"= "value"} should be {"key": "value"}
    content = re.sub(r'(["\'][\w\s]+["\'])\s*=\s*(["\'][^"\']*["\'])', r"\1: \2", content)

    # Pattern: {key= value} should be {key: value} in dict context
    content = re.sub(r"(\{[^}]*?)(\w+)=([^,}]+)", r"\1\2: \3", content)

    return content


def fix_indentation_issues(content):
    """Fix basic indentation issues."""

    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        # If line has content but starts with unexpected character, try to fix basic indentation
        if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
            # If this looks like it should be indented (common patterns)
            if line.strip().startswith(
                (
                    "return ",
                    "if ",
                    "for ",
                    "while ",
                    "else:",
                    "elif ",
                    "try:",
                    "except ",
                    "finally:",
                    "with ",
                )
            ):
                line = "    " + line.strip()
            elif line.strip().startswith(("def ", "class ")):
                # These should typically not be indented unless they're nested
                pass
            else:
                # For other cases, if the previous line ended with :, this might need indentation
                if fixed_lines and fixed_lines[-1].strip().endswith(":"):
                    line = "    " + line.strip()

        fixed_lines.append(line)

    return "\n".join(fixed_lines)


def apply_all_fixes(content):
    """Apply all fix patterns to the content."""

    content = fix_function_annotations(content)
    content = fix_dict_and_annotation_syntax(content)
    content = fix_function_parameter_syntax(content)
    content = fix_class_and_method_syntax(content)
    content = fix_variable_annotation_syntax(content)
    content = fix_dict_literal_syntax(content)
    content = fix_indentation_issues(content)

    return content


def process_file(file_path):
    """Process a single Python file to fix syntax errors."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        fixed_content = apply_all_fixes(original_content)

        if fixed_content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
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
            if file.endswith(".py"):
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
