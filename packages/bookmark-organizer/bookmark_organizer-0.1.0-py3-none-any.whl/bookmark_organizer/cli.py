"""Command-line interface for bookmark organization."""

import argparse
import json
from pathlib import Path
from typing import List, Dict
import os
from dotenv import load_dotenv
from .core import process_bookmarks
from .report import generate_report

def load_env():
    """Load environment variables from .env file if it exists."""
    # Try to load from current directory first
    if not load_dotenv():
        # If not found, try to load from the package directory
        package_dir = Path(__file__).parent.parent
        load_dotenv(package_dir / '.env')

def organize_bookmarks_cli():
    """CLI entry point for organizing bookmarks."""
    # Load environment variables
    load_env()
    
    parser = argparse.ArgumentParser(description="Organize Chrome bookmarks using AI")
    parser.add_argument(
        "--output-dir",
        default="organized_bookmarks",
        help="Directory to store organized bookmarks (default: organized_bookmarks)"
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace the original Chrome bookmarks file with the organized version"
    )
    parser.add_argument(
        "--html-file",
        help="Path to Chrome bookmarks HTML export file(s). Can be a comma-separated list for multiple files."
    )
    parser.add_argument(
        "--categories-file",
        help="Path to TSV file containing bookmark categories"
    )
    parser.add_argument(
        "--keep-utility",
        action="store_false",
        dest="filter_utility",
        help="Keep utility URLs like Google search results (default: filter out)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=5,
        help="Number of bookmarks to process in each batch (default: 5)"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Enable fast mode: larger chunks (25) and simplified categorization"
    )
    parser.add_argument(
        "--faster",
        action="store_true",
        help="Enable even faster mode: uses URL pattern matching to categorize without LLM when possible"
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge inputs from multiple sources, preserving both category sets"
    )
    # Add new API configuration arguments
    parser.add_argument(
        "--api-key",
        help="API key for the LLM service. Can also be set via API_KEY environment variable"
    )
    parser.add_argument(
        "--base-url",
        help="Base URL for the LLM service. Can also be set via BASE_URL environment variable"
    )
    parser.add_argument(
        "--model",
        help="Model name to use. Can also be set via MODEL environment variable"
    )
    
    args = parser.parse_args()
    
    # Get API configuration from args or environment variables
    api_key = args.api_key or os.getenv('API_KEY')
    base_url = args.base_url or os.getenv('BASE_URL')
    model = args.model or os.getenv('MODEL')
    
    if not api_key:
        print("Warning: No API key provided. Please set it via --api-key or API_KEY environment variable")
    if not base_url:
        print("Warning: No base URL provided. Please set it via --base-url or BASE_URL environment variable")
    if not model:
        print("Warning: No model specified. Please set it via --model or MODEL environment variable")
    
    # Handle multiple HTML files
    html_files = None
    if args.html_file:
        html_files = [path.strip() for path in args.html_file.split(',') if path.strip()]
        if not html_files:
            print("Error: No valid HTML files provided")
            return
    
    # If fast mode is enabled, override chunk size
    if args.fast and args.chunk_size == 5:  # Only override if user didn't specify a custom chunk size
        args.chunk_size = 50
    
    process_bookmarks(
        args.output_dir,
        replace_original=args.replace,
        html_paths=html_files,  # Pass list of files instead of single file
        categories_file=args.categories_file,
        filter_utility=args.filter_utility,
        chunk_size=args.chunk_size,
        fast_mode=args.fast,
        faster_mode=args.faster,
        merge_mode=args.merge,
        api_key=api_key,
        base_url=base_url,
        model=model
    )

def generate_report_cli():
    """CLI entry point for generating a report of organized bookmarks."""
    parser = argparse.ArgumentParser(description="Generate a report of organized bookmarks")
    parser.add_argument(
        "--bookmarks-dir",
        default="organized_bookmarks",
        help="Directory containing organized bookmarks (default: organized_bookmarks)"
    )
    parser.add_argument(
        "--output",
        default="bookmark_report.md",
        help="Output file for the report (default: bookmark_report.md)"
    )
    
    args = parser.parse_args()
    generate_report(args.bookmarks_dir, args.output)

if __name__ == "__main__":
    organize_bookmarks_cli() 