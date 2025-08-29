#!/usr/bin/env python3
"""
Fix systematic colon corruption in LeetCode files.
All colons (:) have been replaced with equals signs (=) throughout the codebase.
"""

import re
from pathlib import Path


def fix_colon_corruption(content: str) -> tuple[str, bool]:
    """
    Fix systematic corruption where colons have been replaced with equals signs.
    
    Args:
        content: File content to fix
        
    Returns:
        Tuple of (fixed_content, was_modified)
    """
    original_content = content
    
    # 1. Fix class definitions: "class ClassName=" -> "class ClassName:"
    content = re.sub(r'^(\s*)class\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*', r'\1class \2:', content, flags=re.MULTILINE)
    
    # 2. Fix function definitions: "def func_name(args)=" -> "def func_name(args):"
    content = re.sub(r'^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*(->\s*[^=]+?)?\s*=\s*', r'\1def \2(\3):', content, flags=re.MULTILINE)
    
    # 3. Fix type annotations: "param=Type" -> "param: Type" (but not in assignments)
    # Look for parameter type annotations
    content = re.sub(r'(\w+)\s*=\s*([A-Z][A-Za-z0-9_\[\],\s]*)\s*(?=[\),])', r'\1: \2', content)
    
    # 4. Fix slice syntax: "s[start=end]" -> "s[start:end]"
    content = re.sub(r'(\[[\w\s]*?)=([^=\]]+?\])', r'\1:\2', content)
    
    # 5. Fix for loop syntax: "for x in list=" -> "for x in list:"
    content = re.sub(r'^(\s*)for\s+([^=]+?)\s+in\s+([^=]+?)=\s*$', r'\1for \2 in \3:', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)for\s+([^=]+?)\s+in\s+([^=]+?)=\s*#', r'\1for \2 in \3: #', content, flags=re.MULTILINE)
    
    # 6. Fix if/elif/else statements: "if condition=" -> "if condition:"
    content = re.sub(r'^(\s*)(if|elif)\s+([^=]+?)=\s*$', r'\1\2 \3:', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)(if|elif)\s+([^=]+?)=\s*#', r'\1\2 \3: #', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)else\s*=\s*$', r'\1else:', content, flags=re.MULTILINE)
    
    # 7. Fix while loops: "while condition=" -> "while condition:"
    content = re.sub(r'^(\s*)while\s+([^=]+?)=\s*$', r'\1while \2:', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)while\s+([^=]+?)=\s*#', r'\1while \2: #', content, flags=re.MULTILINE)
    
    # 8. Fix try/except/finally: "try=" -> "try:", "except Exception=" -> "except Exception:"
    content = re.sub(r'^(\s*)try\s*=\s*$', r'\1try:', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)except(\s+\w+)?\s*=\s*$', r'\1except\2:', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)finally\s*=\s*$', r'\1finally:', content, flags=re.MULTILINE)
    
    # 9. Fix dictionary syntax: "key= value" -> "key: value"
    # Be careful to only match within dictionary contexts
    content = re.sub(r'(\{[^}]*?)(\w+)\s*=\s*([^,}]+)([,}])', r'\1\2: \3\4', content)
    content = re.sub(r'(,\s*)(\w+)\s*=\s*([^,}]+)([,}])', r'\1\2: \3\4', content)
    
    # 10. Fix function return type annotations: ") -> Type=" -> ") -> Type:"
    content = re.sub(r'(\)\s*->\s*[^=]+?)=\s*"""', r'\1:\n        """', content)
    content = re.sub(r'(\)\s*->\s*[^=]+?)=\s*$', r'\1:', content, flags=re.MULTILINE)
    
    # 11. Fix lambda expressions: "lambda x=" -> "lambda x:"
    content = re.sub(r'lambda\s+([^=]+?)=\s*', r'lambda \1: ', content)
    
    # 12. Fix list/dict comprehensions: "[expr for x in list=condition]" -> "[expr for x in list if condition]"
    # This is tricky - need to identify comprehension contexts
    
    return content, content != original_content


def process_leetcode_files():
    """Process all LeetCode Python files to fix colon corruption."""
    leetcode_dir = Path("src/interview_workbook/leetcode")
    
    if not leetcode_dir.exists():
        print(f"❌ LeetCode directory not found: {leetcode_dir}")
        return
    
    # Find all Python files
    python_files = list(leetcode_dir.rglob("*.py"))
    print(f"🔧 Starting colon corruption fix for {len(python_files)} files...")
    
    files_modified = 0
    files_unchanged = 0
    
    for file_path in sorted(python_files):
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix colon corruption
            fixed_content, was_modified = fix_colon_corruption(content)
            
            if was_modified:
                # Write back the fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ Fixed colon corruption in: {file_path}")
                files_modified += 1
            else:
                print(f"⚪ No colon fixes needed: {file_path}")
                files_unchanged += 1
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print("\n📊 Colon Fix Summary:")
    print(f"   Total files processed: {len(python_files)}")
    print(f"   Files with colon fixes: {files_modified}")
    print(f"   Files unchanged: {files_unchanged}")


if __name__ == "__main__":
    process_leetcode_files()
