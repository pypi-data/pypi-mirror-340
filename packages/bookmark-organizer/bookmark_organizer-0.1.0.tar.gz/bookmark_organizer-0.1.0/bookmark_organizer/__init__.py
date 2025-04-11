"""
Bookmark Organizer - AI-powered Chrome bookmark organization tool
"""

from .core import (
    process_bookmarks,
    ProcessedBookmark,
    CategoryHierarchy,
    build_category_hierarchy,
    load_categories,
    validate_bookmarks_html,
    parse_bookmarks_html,
    apply_quick_sort_rules,
    process_bookmarks_chunk,
    combine_bookmarks,
    merge_hierarchies,
    generate_chrome_formats,
    get_chrome_bookmarks_file,
    load_chrome_bookmarks,
    extract_bookmarks,
    sanitize_filename,
    save_processed_bookmark,
    extract_categories_from_bookmarks
)

from .cli import (
    organize_bookmarks_cli,
    generate_report_cli
)

from .report import generate_report

__version__ = "0.1.0"
__all__ = [
    'process_bookmarks',
    'ProcessedBookmark',
    'CategoryHierarchy',
    'build_category_hierarchy',
    'load_categories',
    'validate_bookmarks_html',
    'parse_bookmarks_html',
    'apply_quick_sort_rules',
    'process_bookmarks_chunk',
    'combine_bookmarks',
    'merge_hierarchies',
    'generate_chrome_formats',
    'get_chrome_bookmarks_file',
    'load_chrome_bookmarks',
    'extract_bookmarks',
    'sanitize_filename',
    'save_processed_bookmark',
    'extract_categories_from_bookmarks',
    'organize_bookmarks_cli',
    'generate_report_cli',
    'generate_report'
] 