#!/usr/bin/env python3
"""
Utility script to fix common Sphinx documentation warnings.
"""

import os
import re
import sys
from pathlib import Path

def fix_duplicate_labels(file_path):
    """
    Fix duplicate labels in a markdown file by adding unique suffixes.
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all section headers
    header_pattern = re.compile(r'^(#+)\s+(.*?)$', re.MULTILINE)
    headers = header_pattern.findall(content)
    
    # Track seen headers to detect duplicates
    seen_headers = {}
    replacements = []
    
    for level, title in headers:
        # Normalize the title to create a label
        normalized_title = title.lower().replace(' ', '-')
        
        # Check if this is a duplicate
        if normalized_title in seen_headers:
            seen_headers[normalized_title] += 1
            # Create a new unique title with a suffix
            new_title = f"{title}-{seen_headers[normalized_title]}"
            replacements.append((f"{level} {title}", f"{level} {new_title}"))
        else:
            seen_headers[normalized_title] = 1
    
    # Apply replacements
    for old, new in replacements:
        content = content.replace(old, new, 1)  # Replace only the first occurrence
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    return len(replacements)

def fix_doc_not_in_toctree(root_dir, doc_path):
    """
    Add a document to an appropriate toctree.
    """
    # Determine which toctree to add it to based on the document's name or path
    doc_name = os.path.basename(doc_path)
    
    # Map of doc names to appropriate index files and toctree captions
    doc_map = {
        'README.md': ('index.md', 'Getting Started'),
        'dependencies.md': ('index.md', 'Reference'),
        'testing.md': ('index.md', 'Development')
    }
    
    if doc_name not in doc_map:
        print(f"Don't know which toctree to add {doc_name} to.")
        return False
    
    index_file, caption = doc_map[doc_name]
    index_path = os.path.join(root_dir, index_file)
    
    if not os.path.exists(index_path):
        print(f"Index file {index_path} not found.")
        return False
    
    # Read the index file
    with open(index_path, 'r') as f:
        content = f.read()
    
    # Find the appropriate toctree
    toctree_pattern = re.compile(r'```{\s*toctree\s*}.*?:caption:\s*' + caption + r'.*?```', re.DOTALL)
    toctree_match = toctree_pattern.search(content)
    
    if not toctree_match:
        print(f"Couldn't find toctree with caption '{caption}' in {index_path}")
        return False
    
    # Get the relative path of the doc file from the index file
    doc_rel_path = os.path.relpath(doc_path, os.path.dirname(index_path))
    doc_rel_path = os.path.splitext(doc_rel_path)[0]  # Remove the extension
    
    # Check if the document is already in the toctree
    if doc_rel_path in toctree_match.group(0):
        print(f"{doc_name} is already in the {caption} toctree.")
        return False
    
    # Add the document to the toctree
    toctree_content = toctree_match.group(0)
    new_toctree_content = toctree_content.replace('```', f'{doc_rel_path}\n```', 1)
    new_content = content.replace(toctree_content, new_toctree_content)
    
    # Write the updated content back to the file
    with open(index_path, 'w') as f:
        f.write(new_content)
    
    print(f"Added {doc_name} to the {caption} toctree in {index_path}")
    return True

def main():
    """Main entry point for the script."""
    docs_dir = Path("docs")
    
    if not docs_dir.exists():
        print(f"Directory {docs_dir} not found.")
        return 1
    
    print("Fixing documentation warnings...")
    
    # Fix duplicate labels
    md_files = list(docs_dir.glob('**/*.md'))
    total_fixed_labels = 0
    
    for md_file in md_files:
        fixed = fix_duplicate_labels(md_file)
        if fixed:
            print(f"Fixed {fixed} duplicate labels in {md_file}")
            total_fixed_labels += fixed
    
    # Fix documents not in toctree
    not_in_toctree = [
        docs_dir / "README.md",
        docs_dir / "dependencies.md",
        docs_dir / "testing.md"
    ]
    
    total_fixed_toctrees = 0
    for doc in not_in_toctree:
        if doc.exists():
            if fix_doc_not_in_toctree(docs_dir, doc):
                total_fixed_toctrees += 1
    
    print(f"Fixed {total_fixed_labels} duplicate labels and {total_fixed_toctrees} toctree issues.")
    
    # Rebuild the docs
    os.chdir(docs_dir)
    print("Rebuilding documentation...")
    os.system("bash build_docs.sh")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
