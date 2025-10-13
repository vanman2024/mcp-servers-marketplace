#!/usr/bin/env python3
"""
CEG File Organization Scanner
Based on screenshot_organizer approach - uses keyword matching to suggest file destinations
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# CEG Business Operations root path
CEG_ROOT = Path("/mnt/g/My Drive/Collars-Employment-Group/CEG Business Operations")
RULES_FILE = CEG_ROOT / "file-organization-rules.yaml"

def load_rules(rules_path: Path) -> Dict:
    """Load categorization rules from YAML file"""
    with open(rules_path, 'r') as f:
        return yaml.safe_load(f)

def normalize_text(text: str) -> str:
    """Normalize text for matching (lowercase, strip)"""
    return text.lower().strip()

def match_keywords(filename: str, keywords: List[str]) -> bool:
    """Check if filename contains any of the keywords"""
    filename_norm = normalize_text(filename)
    for keyword in keywords:
        keyword_norm = normalize_text(keyword)
        if keyword_norm in filename_norm:
            return True
    return False

def categorize_file(filename: str, rules: Dict) -> Tuple[str, List[str]]:
    """
    Categorize a file based on keyword matching

    Returns:
        (category_name, matched_keywords)
    """
    matched_categories = []

    for category in rules.get('categories', []):
        cat_name = category['name']
        keywords = category.get('keywords', [])

        if match_keywords(filename, keywords):
            matched_keywords = [kw for kw in keywords if normalize_text(kw) in normalize_text(filename)]
            matched_categories.append((cat_name, matched_keywords))

    # Return first match (most specific should be first in rules)
    if matched_categories:
        return matched_categories[0]

    # Return default category
    return (rules.get('default', 'Inbox/Documents-to-Review'), [])

def scan_files(root_path: Path) -> List[Tuple[Path, str]]:
    """
    Scan for all document files recursively

    Returns:
        List of (file_path, relative_path_string)
    """
    files = []

    # File extensions to scan
    doc_exts = {'.gdoc', '.gsheet', '.gform', '.md', '.pdf', '.docx', '.xlsx', '.csv'}

    for filepath in root_path.rglob('*'):
        if filepath.is_file() and filepath.suffix.lower() in doc_exts:
            relative = filepath.relative_to(root_path)
            files.append((filepath, str(relative)))

    return files

def analyze_files(rules_path: Path, root_path: Path) -> Dict:
    """
    Analyze all files and suggest categorization

    Returns:
        {
            'suggestions': [(current_path, filename, suggested_category, keywords), ...],
            'by_category': {category: [files], ...},
            'uncategorized': [files]
        }
    """
    rules = load_rules(rules_path)
    files = scan_files(root_path)

    suggestions = []
    by_category = defaultdict(list)

    for filepath, relative_path in files:
        filename = filepath.name
        current_folder = str(filepath.parent.relative_to(root_path))

        suggested_category, matched_keywords = categorize_file(filename, rules)

        suggestions.append({
            'current_path': relative_path,
            'current_folder': current_folder,
            'filename': filename,
            'suggested_category': suggested_category,
            'matched_keywords': matched_keywords,
            'needs_move': current_folder != suggested_category
        })

        by_category[suggested_category].append(filename)

    return {
        'suggestions': suggestions,
        'by_category': dict(by_category),
        'total_files': len(files)
    }

def print_report(analysis: Dict, show_all: bool = False, show_moves_only: bool = True):
    """Print analysis report"""

    total = analysis['total_files']
    suggestions = analysis['suggestions']

    if show_moves_only:
        needs_move = [s for s in suggestions if s['needs_move']]
    else:
        needs_move = suggestions

    print(f"\n{'='*80}")
    print(f"CEG FILE ORGANIZATION ANALYSIS")
    print(f"{'='*80}\n")
    print(f"Total files scanned: {total}")
    print(f"Files needing relocation: {len([s for s in suggestions if s['needs_move']])}")
    print(f"\n{'='*80}\n")

    # Group by current folder
    by_current_folder = defaultdict(list)
    for suggestion in needs_move:
        by_current_folder[suggestion['current_folder']].append(suggestion)

    for folder in sorted(by_current_folder.keys()):
        files = by_current_folder[folder]
        print(f"\n📁 CURRENT LOCATION: {folder}/")
        print(f"   ({len(files)} files need to move)\n")

        for file_info in files[:20 if not show_all else None]:  # Limit to 20 per folder unless show_all
            print(f"   📄 {file_info['filename']}")
            print(f"      → MOVE TO: {file_info['suggested_category']}/")
            if file_info['matched_keywords']:
                print(f"      Keywords: {', '.join(file_info['matched_keywords'])}")
            print()

        if not show_all and len(files) > 20:
            print(f"   ... and {len(files) - 20} more files\n")

    # Summary by suggested category
    print(f"\n{'='*80}")
    print(f"SUMMARY BY DESTINATION FOLDER")
    print(f"{'='*80}\n")

    for category in sorted(analysis['by_category'].keys()):
        count = len(analysis['by_category'][category])
        print(f"  {category:.<60} {count:>4} files")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Scan CEG files and suggest organization')
    parser.add_argument('--show-all', action='store_true', help='Show all files (not just first 20 per folder)')
    parser.add_argument('--show-correct', action='store_true', help='Show files already in correct location')

    args = parser.parse_args()

    print("Loading rules...")
    print(f"Rules file: {RULES_FILE}")
    print(f"Scanning: {CEG_ROOT}")

    analysis = analyze_files(RULES_FILE, CEG_ROOT)

    print_report(
        analysis,
        show_all=args.show_all,
        show_moves_only=not args.show_correct
    )

if __name__ == '__main__':
    main()
