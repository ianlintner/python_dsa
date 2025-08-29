#!/usr/bin/env python3
"""
Fix remaining syntax issues in LeetCode files after colon corruption fixes.

This script addresses:
1. Missing function parameters with type annotations
2. Missing assignment operators (= signs)
3. Malformed function signatures and variable assignments
"""

import re
from pathlib import Path


def fix_function_signatures(content):
    """Fix malformed function signatures and type annotations."""
    
    # Pattern 1: Fix functions missing parameter names before return type annotation
    # def function_name(-> ReturnType: -> def function_name() -> ReturnType:
    content = re.sub(
        r'def\s+(\w+)\(\s*->\s*([^:]+):\s*$',
        r'def \1() -> \2:',
        content,
        flags=re.MULTILINE
    )
    
    # Pattern 2: Fix functions with parameters but missing commas/proper syntax
    # def function_name(param-> ReturnType: -> def function_name(param) -> ReturnType:
    content = re.sub(
        r'def\s+(\w+)\(([^)]*?)\s*->\s*([^:]+):\s*$',
        lambda m: f"def {m.group(1)}({m.group(2).rstrip(', ')}) -> {m.group(3)}:",
        content,
        flags=re.MULTILINE
    )
    
    return content


def fix_assignment_operators(content):
    """Fix missing assignment operators in variable assignments."""
    
    # Pattern 1: Fix variable assignments with parenthesis instead of equals
    # variable):value -> variable = value
    content = re.sub(
        r'^(\s*)([a-zA-Z_]\w*)\)\s*[:=]\s*(.+)$',
        r'\1\2 = \3',
        content,
        flags=re.MULTILINE
    )
    
    # Pattern 2: Fix variable assignments with colon instead of equals  
    # variable):value -> variable = value
    content = re.sub(
        r'^(\s*)([a-zA-Z_]\w*)\):\s*(.+)$', 
        r'\1\2 = \3',
        content,
        flags=re.MULTILINE
    )
    
    return content


def fix_specific_patterns(content):
    """Fix specific patterns found in the codebase."""
    
    # Fix audit_data parameter missing in functions
    if 'def generate_category_section(' in content:
        content = re.sub(
            r'def generate_category_section\(\s*->\s*str:',
            'def generate_category_section(category, audit_data) -> str:',
            content
        )
    
    if 'def generate_neetcode_docs(' in content:
        content = re.sub(
            r'def generate_neetcode_docs\(\s*->\s*str:',
            'def generate_neetcode_docs(audit_data) -> str:',
            content
        )
    
    # Fix common variable assignment patterns
    patterns_to_fix = [
        (r'^(\s*)registered\):\s*get_registered_slugs\(\)$', r'\1registered = get_registered_slugs()'),
        (r'^(\s*)cat_name\):\s*category\.value$', r'\1cat_name = category.value'),
        (r'^(\s*)total\):\s*audit_data\["total_manifest"\]$', r'\1total = audit_data["total_manifest"]'),
        (r'^(\s*)audit_data\):\s*run_audit\(\)$', r'\1audit_data = run_audit()'),
        (r'^(\s*)docs_path\):\s*Path\(', r'\1docs_path = Path('),
    ]
    
    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content


def fix_encoding_issues(content):
    """Fix encoding-related syntax issues."""
    
    # Fix encoding parameter syntax
    content = re.sub(
        r'encoding:\s*"utf-8"',
        'encoding="utf-8"',
        content
    )
    
    return content


def fix_class_and_structure_issues(content):
    """Fix class definitions and structure issues."""
    
    # Fix class method definitions that got corrupted
    # class MyClass:def method(self -> class MyClass:\n    def method(self
    content = re.sub(
        r'(class\s+\w+):\s*def\s+(\w+)\(([^)]*)\s*->\s*([^:]+):',
        r'\1:\n    def \2(\3) -> \4:',
        content,
        flags=re.MULTILINE
    )
    
    return content


def process_file(file_path):
    """Process a single Python file to fix syntax issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        if not original_content.strip():
            return False
        
        content = original_content
        
        # Apply all fix functions
        content = fix_function_signatures(content)
        content = fix_assignment_operators(content)
        content = fix_specific_patterns(content)
        content = fix_encoding_issues(content)
        content = fix_class_and_structure_issues(content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to fix syntax issues in all LeetCode files."""
    
    # Directory containing LeetCode problems
    leetcode_dir = Path("src/interview_workbook/leetcode")
    
    if not leetcode_dir.exists():
        print(f"Directory {leetcode_dir} does not exist!")
        return
    
    # Find all Python files
    python_files = list(leetcode_dir.rglob("*.py"))
    
    print(f"Found {len(python_files)} Python files to process...")
    
    fixed_count = 0
    for file_path in python_files:
        if process_file(file_path):
            fixed_count += 1
            print(f"Fixed: {file_path}")
    
    print(f"\nCompleted! Fixed {fixed_count} out of {len(python_files)} files.")
    
    if fixed_count > 0:
        print("\nSuggesting to run ruff format check to verify fixes...")


if __name__ == "__main__":
    main()
