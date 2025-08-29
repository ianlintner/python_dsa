#!/usr/bin/env python3
"""
Simple script to fix core Python syntax corruption in LeetCode files.
Focuses on restoring basic Python syntax patterns.
"""

import os
import re
from pathlib import Path


def fix_basic_python_syntax(content: str) -> str:
    """Fix basic Python syntax corruption."""

    # Fix class definitions: "class Solution=" -> "class Solution:"
    content = re.sub(
        r"^(\s*)class\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*",
        r"\1class \2:",
        content,
        flags=re.MULTILINE,
    )

    # Fix function definitions: "def function_name(...params...)=" -> "def function_name(...params...):"
    content = re.sub(
        r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*=\s*",
        lambda m: m.group(0).replace("=", ":"),
        content,
        flags=re.MULTILINE,
    )

    # Fix method definitions with return types: "def method(self, args) -> ReturnType="
    content = re.sub(
        r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*->\s*[^=]+\s*=\s*$",
        lambda m: m.group(0).rstrip("= \t\n") + ":",
        content,
        flags=re.MULTILINE,
    )

    # Fix if statements: "if condition=" -> "if condition:"
    content = re.sub(r"^(\s*)if\s+([^=]+)\s*=\s*$", r"\1if \2:", content, flags=re.MULTILINE)

    # Fix else statements: "else=" -> "else:"
    content = re.sub(r"^(\s*)else\s*=\s*$", r"\1else:", content, flags=re.MULTILINE)

    # Fix elif statements: "elif condition=" -> "elif condition:"
    content = re.sub(r"^(\s*)elif\s+([^=]+)\s*=\s*$", r"\1elif \2:", content, flags=re.MULTILINE)

    # Fix for loops: "for item in iterable=" -> "for item in iterable:"
    content = re.sub(
        r"^(\s*)for\s+([^=]+)\s+in\s+([^=]+)\s*=\s*$",
        r"\1for \2 in \3:",
        content,
        flags=re.MULTILINE,
    )

    # Fix while loops: "while condition=" -> "while condition:"
    content = re.sub(r"^(\s*)while\s+([^=]+)\s*=\s*$", r"\1while \2:", content, flags=re.MULTILINE)

    # Fix try/except blocks: "try=" -> "try:", "except=" -> "except:"
    content = re.sub(r"^(\s*)(try|except|finally)\s*=\s*$", r"\1\2:", content, flags=re.MULTILINE)

    # Fix with statements: "with something=" -> "with something:"
    content = re.sub(r"^(\s*)with\s+([^=]+)\s*=\s*$", r"\1with \2:", content, flags=re.MULTILINE)

    return content


def fix_file_syntax(filepath: str) -> bool:
    """Fix syntax in a single file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original_content = f.read()

        fixed_content = fix_basic_python_syntax(original_content)

        if original_content != fixed_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            print(f"✅ Fixed basic syntax in: {filepath}")
            return True
        else:
            print(f"⚪ No syntax changes needed: {filepath}")
            return False

    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False


def main():
    """Main execution function."""
    print("🔧 Fixing core Python syntax corruption...")

    # Find all LeetCode Python files
    leetcode_dir = Path("src/interview_workbook/leetcode")
    python_files = []

    for root, dirs, files in os.walk(leetcode_dir):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    print(f"Found {len(python_files)} LeetCode Python files to process")

    fixed_count = 0
    total_count = len(python_files)

    # Process each file
    for filepath in sorted(python_files):
        if fix_file_syntax(filepath):
            fixed_count += 1

    print("\n📊 Summary:")
    print(f"   Total files processed: {total_count}")
    print(f"   Files with syntax fixes: {fixed_count}")
    print(f"   Files unchanged: {total_count - fixed_count}")


if __name__ == "__main__":
    main()
