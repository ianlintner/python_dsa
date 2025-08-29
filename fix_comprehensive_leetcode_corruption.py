#!/usr/bin/env python3
"""
Comprehensive LeetCode corruption fixer - handles severe syntax corruption.
"""

import os
import re
from pathlib import Path
import logging
from typing import Dict, List, Tuple


def fix_severe_corruption(content: str) -> str:
    """Fix the most severe syntax corruption issues."""
    
    # Fix class definitions that got corrupted
    content = re.sub(r'class Solution\s*=\s*def ', 'class Solution:\n    def ', content)
    content = re.sub(r'class ([A-Za-z_][A-Za-z0-9_]*)\s*=\s*', r'class \1:', content)
    
    # Fix basic syntax issues
    content = re.sub(r'^\s*URL\s*=\s*', 'URL: ', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*Difficulty\s*=\s*', 'Difficulty: ', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*Category\s*=\s*', 'Category: ', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*Patterns\s*=\s*', 'Patterns:\n', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*Complexity\s*=\s*', 'Complexity:\n', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*Key Insights\s*=\s*', 'Key Insights:\n', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*Edge Cases\s*=\s*', 'Edge Cases:\n', content, flags=re.MULTILINE)
    
    # Fix function parameter annotations
    content = re.sub(r'(\w+)\s*=\s*List\[([^\]]+)\]', r'\1: List[\2]', content)
    content = re.sub(r'Args\s*=\s*', 'Args:\n            ', content)
    
    # Fix assignment vs annotation confusion  
    content = re.sub(r'if (.+?)\s*!=\s*0\s*=\s*#', r'if \1 != 0:  #', content)
    
    # Fix string literals in URLs
    content = re.sub(r'url="([^"]*)\s*=\s*([^"]*)"', r'url="\1/\2"', content)
    content = re.sub(r'"https\s*=\s*//', r'"https://', content)
    
    # Fix test case titles
    content = re.sub(r'"LeetCode (\d+)\s*=\s*([^"]*)"', r'"LeetCode \1: \2"', content)
    
    return content


def fix_function_definitions_comprehensive(content: str) -> str:
    """Fix function definitions that are missing implementations."""
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for function definition
        if re.match(r'\s*def\s+\w+.*:\s*$', line):
            fixed_lines.append(line)
            i += 1
            
            # Look ahead to see if there's a proper function body
            has_body = False
            lookahead = 0
            
            while i + lookahead < len(lines) and lookahead < 20:
                next_line = lines[i + lookahead]
                
                # If we find docstring, decorator, or proper indented content
                if (next_line.strip().startswith('"""') or
                    next_line.strip().startswith("'''") or
                    next_line.strip().startswith('@') or
                    next_line.strip().startswith('pass') or
                    (next_line.startswith('    ') and next_line.strip() and
                     not next_line.strip().startswith('def '))):
                    has_body = True
                    break
                
                # If we hit another function or class, no body
                if (re.match(r'\s*def\s+', next_line) or
                    re.match(r'\s*class\s+', next_line) or
                    (next_line.strip() and not next_line.startswith('    '))):
                    break
                    
                lookahead += 1
            
            # If no body found, add placeholder
            if not has_body:
                fixed_lines.append('        """TODO: Implement this method."""')
                fixed_lines.append('        pass')
                fixed_lines.append('')
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)


def fix_docstring_corruption(content: str) -> str:
    """Fix corrupted docstrings and mixed code."""
    
    # Remove lines that look like corrupted code mixed in docstrings
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Skip obviously corrupted lines but avoid removing valid docstring text
        if re.match(r'\s*Args\s*=\s*', line):
            continue
        if re.match(r'\s*solution\s*:\s*.*=\s*', line):
            continue
        
        # Skip lines that are clearly malformed syntax in docstrings
        if re.match(r'\s*\d+\.\s+[A-Z].*=.*-.*=.*-', line):
            continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def create_minimal_template(file_path: Path) -> str:
    """Create a minimal working template for severely corrupted files."""
    
    problem_name = file_path.stem.replace('_', ' ').title()
    class_name = 'Solution'
    
    return f'''"""
{problem_name}

TODO: Add problem description
"""

from typing import List, Optional
from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class {class_name}:
    def solve(self, *args) -> None:
        """TODO: Implement solution."""
        pass


def demo():
    """TODO: Implement demo function."""
    pass


# TODO: Add proper registration details if needed
'''


def process_file_comprehensive(file_path: Path) -> bool:
    """Process a file with comprehensive corruption fixes."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        if not original_content.strip():
            return False
        
        content = original_content
        
        # Try aggressive fixes first
        content = fix_severe_corruption(content)
        content = fix_docstring_corruption(content)
        content = fix_function_definitions_comprehensive(content)
        
        # If still severely corrupted, check syntax
        try:
            compile(content, str(file_path), 'exec')
        except SyntaxError as e:
            # If it's still broken, create minimal template
            logging.error(f"Syntax error in {file_path}: {e}")
            # Preserve original content unless catastrophic corruption
            if len(content.strip()) < 20:
                content = create_minimal_template(file_path)
        
        # Only write if content changed significantly
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Fixed: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        raise


def main():
    """Fix all severely corrupted LeetCode files."""
    
    base_dir = Path("src/interview_workbook/leetcode")
    
    if not base_dir.exists():
        print(f"Directory {base_dir} not found!")
        return
    
    # Get list of problem files (non-private files)
    problem_files = []
    for file_path in base_dir.rglob("*.py"):
        if not file_path.name.startswith('_') and file_path.name != 'top100_manifest.py':
            problem_files.append(file_path)
    
    print(f"Processing {len(problem_files)} problem files...")
    
    fixed_count = 0
    for file_path in problem_files:
        if process_file_comprehensive(file_path):
            fixed_count += 1
    
    print(f"\nProcessed {len(problem_files)} files, fixed {fixed_count} files.")
    
    # Now try to fix the utility files
    utility_files = [
        base_dir / "_audit.py",
        base_dir / "_discovery.py", 
        base_dir / "_nodes.py",
        base_dir / "_registry.py",
        base_dir / "_runner.py"
    ]
    
    print("\nFixing utility files...")
    utility_fixed = 0
    for file_path in utility_files:
        if file_path.exists() and process_file_comprehensive(file_path):
            utility_fixed += 1
    
    print(f"Fixed {utility_fixed} utility files.")


if __name__ == "__main__":
    main()
