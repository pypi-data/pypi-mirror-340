"""Report generation functionality for bookmark organization."""

import json
from pathlib import Path
from typing import Dict, List

def generate_report(bookmarks_dir: str, output_file: str) -> None:
    """Generate a markdown report of organized bookmarks."""
    bookmarks_path = Path(bookmarks_dir)
    if not bookmarks_path.exists():
        print(f"Error: Bookmarks directory not found: {bookmarks_path}")
        return
    
    # Collect all bookmarks
    bookmarks_by_category: Dict[str, List[Dict]] = {}
    processed_files = set()  # Track processed files to avoid duplicates
    
    # Look for bookmarks in the categories directory
    categories_dir = bookmarks_path / "categories"
    if not categories_dir.exists():
        print(f"Error: Categories directory not found: {categories_dir}")
        return
    
    for category_dir in categories_dir.iterdir():
        if not category_dir.is_dir():
            continue
            
        category = category_dir.name
        bookmarks_by_category[category] = []
        
        for bookmark_file in category_dir.glob("*.json"):
            # Skip if we've already processed this file (via symlink)
            if bookmark_file.resolve() in processed_files:
                continue
                
            try:
                with open(bookmark_file, 'r', encoding='utf-8') as f:
                    bookmark = json.load(f)
                    bookmarks_by_category[category].append(bookmark)
                    processed_files.add(bookmark_file.resolve())
            except Exception as e:
                print(f"Warning: Failed to read bookmark file {bookmark_file}: {e}")
    
    # Remove empty categories
    bookmarks_by_category = {k: v for k, v in bookmarks_by_category.items() if v}
    
    if not bookmarks_by_category:
        print("No bookmarks found to generate report.")
        return
    
    # Sort bookmarks by importance within each category
    for category in bookmarks_by_category:
        bookmarks_by_category[category].sort(key=lambda x: (-x['importance'], x['title']))
    
    # Generate markdown report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Organized Bookmarks Report\n\n")
        
        # Table of Contents
        f.write("## Table of Contents\n")
        for category in sorted(bookmarks_by_category.keys()):
            f.write(f"- [{category}](#{category.lower().replace(' ', '-')})\n")
        f.write("\n")
        
        # Categories
        for category in sorted(bookmarks_by_category.keys()):
            f.write(f"## {category}\n\n")
            bookmarks = bookmarks_by_category[category]
            
            for bookmark in bookmarks:
                f.write(f"### [{bookmark['title']}]({bookmark['url']})\n")
                f.write(f"- **Description**: {bookmark['description']}\n")
                f.write(f"- **Tags**: {', '.join(bookmark['tags'])}\n")
                f.write(f"- **Importance**: {'⭐' * bookmark['importance']}\n")
                if bookmark.get('parent_categories'):
                    f.write(f"- **Parent Categories**: {' > '.join(reversed(bookmark['parent_categories']))}\n")
                f.write("\n")
    
    total_bookmarks = sum(len(bookmarks) for bookmarks in bookmarks_by_category.values())
    print(f"\nReport generated: {output_file}")
    print(f"Total bookmarks: {total_bookmarks}")
    print(f"Categories: {len(bookmarks_by_category)}")
    print("\nCategories and bookmark counts:")
    for category in sorted(bookmarks_by_category.keys()):
        print(f"  - {category}: {len(bookmarks_by_category[category])} bookmarks") 