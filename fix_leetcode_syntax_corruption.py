#!/usr/bin/env python3
"""
Comprehensive LeetCode syntax corruption fixer.

This script fixes the widespread syntax errors in the LeetCode files caused by
corruption during file processing.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


def fix_function_definitions(content: str) -> str:
    """Fix corrupted function definitions."""
    
    # Fix solve method signatures
    patterns = [
        (r'def solve\(\) -> None:', 'def solve(self, nums: List[int]) -> None:'),
        (r'def solve\(\) -> bool:', 'def solve(self, s: str) -> bool:'),
        (r'def solve\(\) -> int:', 'def solve(self, nums: List[int]) -> int:'),
        (r'def solve\(\) -> List\[int\]:', 'def solve(self, nums: List[int]) -> List[int]:'),
        (r'def solve\(\) -> List\[List\[int\]\]:', 'def solve(self, nums: List[int]) -> List[List[int]]:'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Fix other method signatures
    content = re.sub(r'def ([a-zA-Z_][a-zA-Z0-9_]*)\(\) -> ([^:]+):', 
                     r'def \1(self, *args) -> \2:', content)
    
    return content


def fix_operators(content: str) -> str:
    """Fix corrupted operators."""
    
    # Fix assignment operators
    content = re.sub(r'(\w+)\s*:\s*([^=\n]+)$', r'\1 = \2', content, flags=re.MULTILINE)
    content = re.sub(r'(\w+)\s*\+:\s*(\d+)', r'\1 += \2', content)
    content = re.sub(r'(\w+)\s*-:\s*(\d+)', r'\1 -= \2', content)
    
    # Fix comparison operators
    content = re.sub(r'if\s+(.+?)\s*!:\s*(.+?):', r'if \1 != \2:', content)
    content = re.sub(r'if\s+(.+?)\s*!:\s*$', r'if \1 != 0:', content, flags=re.MULTILINE)
    
    return content


def fix_control_flow(content: str) -> str:
    """Fix corrupted control flow statements."""
    
    # Fix while loops
    content = re.sub(r'while\s+(.+?)\s*:\s*$', r'while \1:', content, flags=re.MULTILINE)
    
    # Fix for loops  
    content = re.sub(r'for\s+(\w+)\s+in\s+(.+?)\s*:\s*$', r'for \1 in \2:', content, flags=re.MULTILINE)
    
    return content


def fix_docstrings(content: str) -> str:
    """Fix corrupted docstrings and separate them from code."""
    
    # Fix broken docstrings that got mixed with code
    lines = content.split('\n')
    fixed_lines = []
    in_docstring = False
    
    for line in lines:
        # Skip lines that look like corrupted code mixed in docstrings
        if 'Args:' in line and any(char in line for char in [':', '=', '!', '+']):
            # This is likely corrupted code, skip it
            continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def add_missing_function_bodies(content: str) -> str:
    """Add placeholder implementations for functions missing bodies."""
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a function definition
        if re.match(r'\s*def\s+\w+.*:', line):
            fixed_lines.append(line)
            i += 1
            
            # Check if next line is properly indented function body
            if i < len(lines):
                next_line = lines[i]
                if next_line.strip() and not next_line.startswith('    ') and not next_line.strip().startswith('"""'):
                    # Missing function body, add placeholder
                    fixed_lines.append('        """TODO: Implement this method."""')
                    fixed_lines.append('        pass')
            else:
                # End of file, add placeholder
                fixed_lines.append('        """TODO: Implement this method."""')
                fixed_lines.append('        pass')
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)


def fix_documentation_formatting(content: str) -> str:
    """Fix documentation that uses = instead of : for structure."""
    
    # Fix patterns like "Patterns=- Something" to "Patterns:\n- Something"
    content = re.sub(r'^(\w+)=- ', r'\1:\n- ', content, flags=re.MULTILINE)
    
    # Fix other documentation patterns
    content = re.sub(r'^(\w+)=(.+)$', r'\1: \2', content, flags=re.MULTILINE)
    
    return content


def fix_test_cases(content: str) -> str:
    """Fix corrupted test case definitions."""
    
    # Fix TestCase syntax issues
    content = re.sub(r'TestCase\(input_args=\(([^)]+)\),\s*expected=([^,]+),?.*?\)', 
                     r'TestCase(input_data=\1, expected=\2)', content)
    
    return content


def fix_demo_functions(content: str) -> str:
    """Fix corrupted demo functions."""
    
    # Find and fix demo function definitions
    content = re.sub(r'def demo\(\):\s*"""[^"]*"""[^"]*solution\s*:', 
                     'def demo():\n    """Run demo with test cases."""', content)
    
    return content


def process_file(file_path: Path) -> bool:
    """Process a single Python file to fix syntax errors."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        if not original_content.strip():
            return False
        
        # Apply all fixes
        content = original_content
        content = fix_function_definitions(content)
        content = fix_operators(content)
        content = fix_control_flow(content)
        content = fix_docstrings(content)
        content = add_missing_function_bodies(content)
        content = fix_documentation_formatting(content)
        content = fix_test_cases(content)
        content = fix_demo_functions(content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Fix all LeetCode Python files."""
    
    base_dir = Path("src/interview_workbook/leetcode")
    
    if not base_dir.exists():
        print(f"Directory {base_dir} not found!")
        return
    
    fixed_count = 0
    total_count = 0
    
    # Process all Python files in leetcode directory
    for file_path in base_dir.rglob("*.py"):
        if file_path.name.startswith('_'):
            # Skip private/utility files for now
            continue
            
        total_count += 1
        if process_file(file_path):
            fixed_count += 1
    
    print(f"\nProcessed {total_count} files, fixed {fixed_count} files.")


if __name__ == "__main__":
    main()
