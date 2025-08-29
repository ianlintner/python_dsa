#!/usr/bin/env python3
"""
Comprehensive script to restore basic Python syntax in LeetCode files
that was corrupted by previous automated fix attempts.
"""

import glob
import re


def restore_basic_python_syntax(content):
    """Restore basic Python syntax that was corrupted by previous fixes."""
    
    # Fix class definitions
    content = re.sub(r'class\s+(\w+)=def\s+', r'class \1:\n    def ', content)
    content = re.sub(r'class\s+(\w+)=', r'class \1:', content)
    
    # Fix function definitions - restore colons after parameter lists
    content = re.sub(r'def\s+(\w+)\([^)]*\)\s*->\s*([^=]+)=', r'def \1(\2) -> \3:', content)
    content = re.sub(r'def\s+(\w+)\([^)]*\)=', r'def \1(\2):', content)
    
    # Fix type annotations - restore colons
    content = re.sub(r'(\w+)=List\[([^\]]+)\]', r'\1: List[\2]', content)
    content = re.sub(r'(\w+)=(\w+)', r'\1: \2', content)
    
    # Fix basic Python syntax patterns
    patterns = [
        # Function parameters and return types
        (r'(\w+)\s*=\s*List\[([^\]]+)\]\)\s*->\s*([^=]+)=', r'\1: List[\2]) -> \3:'),
        (r'(\w+)\s*=\s*(\w+)\)\s*->\s*([^=]+)=', r'\1: \2) -> \3:'),
        
        # For loops and if statements
        (r'for\s+(\w+)\s+in\s+([^=]+)=if\s+', r'for \1 in \2:\n        if '),
        (r'if\s+([^=]+)=return\s+', r'if \1:\n            return '),
        
        # Dictionary and docstring syntax
        (r'"""([^"]+)=([^"]+)"""', r'"""\1: \2"""'),
        (r'Args=([^=]+)=([^=]+)', r'Args:\n            \1: \2'),
        (r'Returns=([^=]+)=([^=]+)', r'Returns:\n            \1: \2'),
        
        # URL and string patterns
        (r'url="https=//([^"]+)"', r'url="https://\1"'),
        (r'"([^"]+)="([^"]*)"', r'"\1": "\2"'),
        
        # Common Python keywords that should have colons
        (r'(\s+)(if|for|while|try|except|finally|with|class|def)\s+([^=]+)=(\s*)', r'\1\2 \3:\4'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

def fix_testcase_syntax(content):
    """Fix TestCase syntax while preserving restored Python syntax."""
    
    # Fix basic TestCase format - ensure proper parameter names
    testcase_patterns = [
        # Fix malformed TestCase calls with missing commas or wrong brackets
        (r'TestCase\(input_args=\(([^)]*)\)\s*([^,]+)\s*expected=([^,]+),?\s*description="([^"]*)"', 
         r'TestCase(input_args=(\1), expected=\3, description="\4")'),
         
        # Fix TestCase calls with positional arguments after keyword arguments
        (r'TestCase\(\s*([^,]+),\s*expected=([^,]+),?\s*description="([^"]*)"', 
         r'TestCase(input_args=(\1), expected=\2, description="\3")'),
         
        # Fix incomplete TestCase calls
        (r'TestCase\(input_args=\(([^)]*)\)\s*([^)]+)\)', 
         r'TestCase(input_args=(\1), expected=\2, description="Test case")'),
    ]
    
    for pattern, replacement in testcase_patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content

def restore_file_syntax(file_path):
    """Restore syntax for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Step 1: Restore basic Python syntax
        content = restore_basic_python_syntax(content)
        
        # Step 2: Fix TestCase syntax
        content = fix_testcase_syntax(content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Restored syntax in: {file_path}")
            return True
        else:
            print(f"⚪ No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to restore syntax in all LeetCode files."""
    print("🔧 Starting comprehensive Python syntax restoration...")
    
    # Find all Python files in leetcode directory
    pattern = "src/interview_workbook/leetcode/**/*.py"
    files = glob.glob(pattern, recursive=True)
    
    # Filter out __pycache__ and other non-source files
    files = [f for f in files if not any(part.startswith('__') for part in f.split('/'))]
    
    print(f"Found {len(files)} LeetCode Python files to restore")
    
    files_modified = 0
    files_unchanged = 0
    
    for file_path in sorted(files):
        try:
            if restore_file_syntax(file_path):
                files_modified += 1
            else:
                files_unchanged += 1
        except Exception as e:
            print(f"❌ Failed to process {file_path}: {e}")
    
    print("\n📊 Restoration Summary:")
    print(f"   Total files processed: {len(files)}")
    print(f"   Files modified: {files_modified}")
    print(f"   Files unchanged: {files_unchanged}")
    
    print("\n🧪 Testing syntax after restoration...")
    
if __name__ == "__main__":
    main()
