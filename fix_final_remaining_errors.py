#!/usr/bin/env python3
"""
Fix final remaining syntax errors in LeetCode files.
Targets the specific patterns identified in the latest ruff output.
"""

import os
import re
import glob

def fix_class_solution_corruption(content):
    """Fix corrupted class Solution definitions"""
    # Pattern: class Solution: List[int], target: int) -> List[int]:
    # Should be: class Solution:\n    def method_name(self, ...):
    content = re.sub(
        r'class\s+Solution:\s*([^)]+\))\s*->\s*([^:]+):',
        r'class Solution:\n    def solve(self, \1 -> \2:',
        content
    )
    
    # Pattern: class Solution: str) -> bool:
    content = re.sub(
        r'class\s+Solution:\s*([^)]+\))\s*->\s*([^:]+):',
        r'class Solution:\n    def solve(self, \1 -> \2:',
        content
    )
    
    # More generic class corruption fix
    content = re.sub(
        r'class\s+Solution:\s*([^{:\n]+):',
        r'class Solution:\n    def solve(self, \1:',
        content
    )
    
    return content

def fix_function_parameter_corruption(content):
    """Fix function parameter syntax issues"""
    # Fix functions with missing self parameter that start with types
    content = re.sub(
        r'def\s+(\w+)\(\s*([A-Z][^,)]+),\s*',
        r'def \1(self, \2, ',
        content
    )
    
    # Fix parameter annotation corruption
    content = re.sub(
        r'(\w+):\s*([A-Z][^,)]+),\s*(\w+):\s*([A-Z][^,)]+)\)',
        r'\1: \2, \3: \4)',
        content
    )
    
    return content

def fix_testcase_syntax_corruption(content):
    """Fix TestCase parameter syntax"""
    # Fix input_args: pattern
    content = re.sub(
        r'TestCase\(input_args:\s*',
        r'TestCase(input_args=',
        content
    )
    
    # Fix other TestCase parameter issues
    content = re.sub(
        r'TestCase\(([^)]+):\s*',
        r'TestCase(\1=',
        content
    )
    
    return content

def fix_register_problem_corruption(content):
    """Fix register_problem call syntax"""
    # Fix id: pattern
    content = re.sub(
        r'register_problem\(\s*id:\s*(\d+),',
        r'register_problem(id=\1,',
        content
    )
    
    # Fix slug: pattern
    content = re.sub(
        r'slug:\s*"([^"]+)"',
        r'slug="\1"',
        content
    )
    
    # Fix title: pattern
    content = re.sub(
        r'title:\s*"([^"]+)"',
        r'title="\1"',
        content
    )
    
    return content

def fix_demo_function_corruption(content):
    """Fix demo function syntax issues"""
    # Fix problem_title: pattern
    content = re.sub(
        r'problem_title:\s*"([^"]+)"',
        r'problem_title="\1"',
        content
    )
    
    # Fix multiline string in create_demo_output
    content = re.sub(
        r'approach_notes="([^"]+)"\):',
        r'approach_notes="\1")',
        content
    )
    
    return content

def fix_docstring_corruption(content):
    """Fix docstring syntax issues"""
    # Fix docstrings that got corrupted
    content = re.sub(
        r'def\s+(\w+)\(\):\s*"""([^"]+)"""([^"]+)"""',
        r'def \1():\n    """\2"""\3',
        content
    )
    
    # Fix function definitions with missing colon after docstring
    content = re.sub(
        r'(def\s+\w+\([^)]*\))\s*->\s*([^:]+):\s*"""([^"]+)"""([^"\n]*)',
        r'\1 -> \2:\n    """\3"""\4',
        content
    )
    
    return content

def fix_assignment_corruption(content):
    """Fix assignment and comparison operators"""
    # Fix Results = pattern
    content = re.sub(
        r'(\s+)results\s*=\s*run_test_cases\([^)]+\)\s*',
        r'\1results = run_test_cases(',
        content
    )
    
    # Complete the function call properly
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        if 'results = run_test_cases(' in line and not line.rstrip().endswith(')'):
            # Find the matching closing parenthesis across lines
            paren_count = line.count('(') - line.count(')')
            complete_line = line
            i += 1
            while i < len(lines) and paren_count > 0:
                complete_line += ' ' + lines[i].strip()
                paren_count += lines[i].count('(') - lines[i].count(')')
                i += 1
            
            # Fix the complete function call
            if 'solution.' in complete_line and not complete_line.endswith(')'):
                complete_line += ')'
            
            fixed_lines.append(complete_line)
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

def fix_indentation_and_structure(content):
    """Fix indentation and basic structure issues"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Fix unindent issues after class definitions
        if i > 0 and lines[i-1].strip().startswith('class ') and lines[i-1].strip().endswith(':'):
            if stripped and not line.startswith('    '):
                fixed_lines.append('    ' + stripped)
            else:
                fixed_lines.append(line)
        # Fix method definitions that should be indented in class
        elif stripped.startswith('def ') and i > 0:
            # Check if we're inside a class
            in_class = False
            for j in range(i-1, -1, -1):
                if lines[j].strip().startswith('class '):
                    in_class = True
                    break
                elif lines[j].strip().startswith('def ') and not lines[j].startswith('    '):
                    break
            
            if in_class and not line.startswith('    '):
                fixed_lines.append('    ' + stripped)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_specific_corruption_patterns(content):
    """Fix very specific corruption patterns seen in the output"""
    # Fix "Only single target (not tuple) can be annotated" errors
    content = re.sub(
        r'class\s+Solution:\s*([^,]+),\s*([^)]+\))\s*->\s*([^:]+):',
        r'class Solution:\n    def solve(self, \1: \2) -> \3:',
        content
    )
    
    # Fix "Expected newline, found ')'" errors in function signatures
    content = re.sub(
        r'def\s+(\w+)\([^)]+\)([^:]*\))\s*->\s*([^:]+):',
        r'def \1(\2 -> \3:',
        content
    )
    
    # Fix malformed function definitions
    content = re.sub(
        r'def\s+(\w+)\(\s*->\s*([^)]+)\):',
        r'def \1() -> \2:',
        content
    )
    
    return content

def fix_eof_and_completeness(content):
    """Fix EOF and file completeness issues"""
    # Ensure files end properly
    if not content.strip().endswith('\n'):
        content += '\n'
    
    # Fix unclosed parentheses in register_problem
    if 'register_problem(' in content and content.count('register_problem(') > content.count('register_problem('):
        content = content.replace('register_problem(', 'register_problem(') + ')'
    
    return content

def process_file(filepath):
    """Process a single file with all fixes"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all fixes in sequence
        content = fix_class_solution_corruption(content)
        content = fix_function_parameter_corruption(content)
        content = fix_testcase_syntax_corruption(content)
        content = fix_register_problem_corruption(content)
        content = fix_demo_function_corruption(content)
        content = fix_docstring_corruption(content)
        content = fix_assignment_corruption(content)
        content = fix_indentation_and_structure(content)
        content = fix_specific_corruption_patterns(content)
        content = fix_eof_and_completeness(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all LeetCode Python files"""
    
    # Find all Python files in leetcode directories  
    leetcode_dirs = [
        'src/interview_workbook/leetcode/arrays_hashing/*.py',
        'src/interview_workbook/leetcode/two_pointers/*.py', 
        'src/interview_workbook/leetcode/sliding_window/*.py',
        'src/interview_workbook/leetcode/stack/*.py',
        'src/interview_workbook/leetcode/binary_search/*.py',
        'src/interview_workbook/leetcode/linked_list/*.py',
        'src/interview_workbook/leetcode/trees/*.py',
        'src/interview_workbook/leetcode/heap/*.py',
        'src/interview_workbook/leetcode/backtracking/*.py',
        'src/interview_workbook/leetcode/tries/*.py',
        'src/interview_workbook/leetcode/graphs/*.py',
        'src/interview_workbook/leetcode/dp_1d/*.py',
        'src/interview_workbook/leetcode/dp_2d/*.py',
        'src/interview_workbook/leetcode/bit_manip/*.py',
        'src/interview_workbook/leetcode/math_geometry/*.py',
        'src/interview_workbook/leetcode/greedy/*.py',
        'src/interview_workbook/leetcode/intervals/*.py',
        'src/interview_workbook/leetcode/_*.py'
    ]
    
    all_files = []
    for pattern in leetcode_dirs:
        all_files.extend(glob.glob(pattern))
    
    # Exclude __init__.py files but include _*.py files
    python_files = [f for f in all_files if not f.endswith('__init__.py')]
    
    print(f"Processing {len(python_files)} LeetCode Python files...")
    
    fixed_count = 0
    for filepath in python_files:
        if process_file(filepath):
            fixed_count += 1
            print(f"Fixed: {filepath}")
    
    print(f"\nCompleted processing. Fixed {fixed_count} out of {len(python_files)} files.")
    print("Run 'python -m ruff format src/interview_workbook/leetcode/ --check' to verify fixes")

if __name__ == "__main__":
    main()
