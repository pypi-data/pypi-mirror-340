"""Core functionality for bookmark organization and processing."""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse
import openai
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import re
from bookmark_organizer.report import generate_report

# LLM  configuration
API_KEY = os.getenv('API_KEY', '')
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8003/v1/')
MODEL = os.getenv('MODEL', 'openai/gpt-4o-mini')

@dataclass
class ProcessedBookmark:
    """Represents a processed bookmark with metadata."""
    url: str
    title: str
    category: str
    tags: List[str]
    description: str
    importance: int  # 1-5 scale
    parent_categories: List[str] = None  # Parent categories in hierarchy
    add_date: str = ""
    last_modified: str = ""
    icon: str = ""
    folder_path: str = ""

class CategoryHierarchy:
    """Manages hierarchical relationships between categories."""
    def __init__(self):
        self.parent_map: Dict[str, str] = {}  # child -> parent mapping
        self.children_map: Dict[str, Set[str]] = {}  # parent -> children mapping
        self.all_categories: Set[str] = set()
        self.base_urls: Dict[str, List[str]] = {}  # category -> base URL patterns

    def add_relationship(self, parent: str, child: str):
        """Add a parent-child relationship between categories."""
        self.parent_map[child] = parent
        if parent not in self.children_map:
            self.children_map[parent] = set()
        self.children_map[parent].add(child)
        self.all_categories.add(parent)
        self.all_categories.add(child)
        
    def add_base_url(self, category: str, base_url: str):
        """Add a base URL pattern for a category."""
        if category not in self.base_urls:
            self.base_urls[category] = []
        if base_url not in self.base_urls[category]:
            self.base_urls[category].append(base_url)

    def get_base_urls(self, category: str) -> List[str]:
        """Get base URL patterns for a category."""
        return self.base_urls.get(category, [])
        
    def get_all_base_urls(self) -> Dict[str, List[str]]:
        """Get all base URL patterns."""
        return self.base_urls

    def get_parents(self, category: str) -> List[str]:
        """Get all parent categories in hierarchy, from immediate parent to root."""
        parents = []
        current = category
        while current in self.parent_map:
            parent = self.parent_map[current]
            parents.append(parent)
            current = parent
        return parents

    def get_children(self, category: str) -> Set[str]:
        """Get immediate child categories."""
        return self.children_map.get(category, set())

    def get_all_descendants(self, category: str) -> Set[str]:
        """Get all descendant categories (children, grandchildren, etc.)."""
        descendants = set()
        to_process = [category]
        while to_process:
            current = to_process.pop()
            children = self.get_children(current)
            descendants.update(children)
            to_process.extend(children)
        return descendants

def build_category_hierarchy(categories_file: str) -> CategoryHierarchy:
    """Build category hierarchy by asking LLM about relationships between categories."""
    hierarchy = CategoryHierarchy()
    
    # Read categories from the specified file
    with open(categories_file, 'r', encoding='utf-8') as f:
        categories = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not categories:
        return hierarchy
    
    # Define well-known categories and their base URL patterns
    well_known_categories = {
        "Stack Overflow": ["stackoverflow.com"],
        "Stack Exchange": ["stackexchange.com", "serverfault.com", "superuser.com", "askubuntu.com"],
        "Github Repos": ["github.com", "raw.githubusercontent.com"],
        "Python packages": ["pypi.org", "python.org/pypi"],
        "R packages": ["cran.r-project.org", "bioconductor.org", "rdrr.io"],
        "Rust libraries": ["crates.io", "docs.rs"],
        "Wikipedia": ["wikipedia.org", "wikimedia.org"],
        "Documentation": ["readthedocs.io", "readthedocs.org", "docs."],
        "Social Media": ["twitter.com", "facebook.com", "linkedin.com", "instagram.com", "bsky.app"],
        "Research Papers": ["arxiv.org", "biorxiv.org", "medrxiv.org", "doi.org", "researchgate.net"],
        "Preprints": ["arxiv.org", "biorxiv.org", "medrxiv.org", "ssrn.com"],
        "Tech News": ["techcrunch.com", "wired.com", "arstechnica.com", "theverge.com", "hackernews.com", "news.ycombinator.com"],
    }
    
    # Add well-known base URLs to categories
    for category in categories:
        if category in well_known_categories:
            for url in well_known_categories[category]:
                hierarchy.add_base_url(category, url)
    
    # Setup the OpenAI client with LLM configuration
    client = openai.OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    
    print("\nAnalyzing category relationships...")
    categories_str = "\n".join(categories)
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a bookmark organization assistant. Your task is to analyze categories and determine their hierarchical relationships. Create a clean, organized hierarchy with broader parent categories and more specific subcategories. Respond only in JSON format."
                },
                {
                    "role": "user",
                    "content": f"""
    Please analyze these categories and determine their hierarchical relationships:

    {categories_str}

    For each category that should be a subcategory of another, specify the parent-child relationship.
    
    IMPORTANT GUIDELINES:
    - Create a clean hierarchy with fewer top-level categories and more subcategories
    - Every specialized category should ideally be a child of a broader category
    - Try to organize closely related categories under common parents
    - Prioritize depth over breadth in the hierarchy
    - Consider natural hierarchies like:
      * Specific paper types under "Research Papers"
      * Specific programming topics under "Programming Languages"
      * read the docs or mkdocs sites under "Documentation"
      * Learning materials under "Learning Resources"
    
    Return ONLY a JSON array of relationships, where each relationship is an object with "parent" and "child" fields.
    Example format:
    [
        {{"parent": "Research Papers", "child": "Biology papers"}},
        {{"parent": "Programming Languages", "child": "Web Development"}}
    ]
    """
                }
            ],
            max_tokens=800,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        
        try:
            # Remove any leading/trailing non-JSON content
            content = content.strip()
            if content.find('[') != -1:
                content = content[content.find('['):]
            if content.rfind(']') != -1:
                content = content[:content.rfind(']')+1]
                
            relationships = json.loads(content)
            
            # Add relationships to hierarchy
            for rel in relationships:
                if 'parent' in rel and 'child' in rel:
                    hierarchy.add_relationship(rel['parent'], rel['child'])
                    print(f"✓ Added relationship: {rel['parent']} -> {rel['child']}")
                    
                    # Propagate base URLs from child to parent if parent doesn't have URLs
                    child_urls = hierarchy.get_base_urls(rel['child'])
                    parent_urls = hierarchy.get_base_urls(rel['parent'])
                    
                    if child_urls and not parent_urls:
                        for url in child_urls:
                            hierarchy.add_base_url(rel['parent'], url)
                            print(f"  ✓ Propagated URL pattern: {url} to {rel['parent']}")
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Raw response: {content}")
            
    except Exception as e:
        print(f"Error building category hierarchy: {e}")
        
    # Add additional base URLs for categories using LLM if there are categories without base URLs
    categories_without_urls = [cat for cat in hierarchy.all_categories if not hierarchy.get_base_urls(cat)]
    
    if categories_without_urls:
        try:
            chunk_size = 10  # Process in smaller chunks for better responses
            for i in range(0, len(categories_without_urls), chunk_size):
                chunk = categories_without_urls[i:i+chunk_size]
                chunk_str = "\n".join(chunk)
                
                print(f"\nGenerating URL patterns for categories {i+1}-{min(i+chunk_size, len(categories_without_urls))}...")
                
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a bookmark organization assistant. Your task is to identify common website domain patterns for categories."
                        },
                        {
                            "role": "user",
                            "content": f"""
        For each of the following bookmark categories, provide up to 3 common website domain patterns (without http/https prefix):

        {chunk_str}

        For example:
        "Programming Languages": ["github.com", "dev.to", "stackoverflow.com"]
        "Health & Wellness": ["webmd.com", "mayoclinic.org", "healthline.com"]

        Return ONLY a JSON object where keys are category names and values are arrays of domain patterns.
        """
                        }
                    ],
                    max_tokens=800,
                    temperature=0.0,
                    response_format={"type": "json_object"}
                )
                
                content = response.choices[0].message.content.strip()
                
                try:
                    url_patterns = json.loads(content)
                    
                    for category, urls in url_patterns.items():
                        if category in hierarchy.all_categories:
                            for url in urls:
                                # Clean the URL (remove http/https if accidentally included)
                                clean_url = url.replace("http://", "").replace("https://", "")
                                hierarchy.add_base_url(category, clean_url)
                                print(f"✓ Added URL pattern for {category}: {clean_url}")
                
                except json.JSONDecodeError as e:
                    print(f"Failed to parse URL patterns from LLM: {e}")
                    
        except Exception as e:
            print(f"Error generating URL patterns: {e}")
    
    # Print summary of base URLs
    print("\nCategory base URL patterns:")
    for category in sorted(hierarchy.all_categories):
        urls = hierarchy.get_base_urls(category)
        if urls:
            print(f"  {category}: {', '.join(urls)}")
    
    return hierarchy

def load_categories(categories_file: str) -> Tuple[List[str], CategoryHierarchy]:
    """Load categories and their hierarchy from the specified TSV file."""
    if not Path(categories_file).exists():
        print(f"Error: Categories file not found: {categories_file}")
        return [], CategoryHierarchy()
    
    with open(categories_file, 'r', encoding='utf-8') as f:
        categories = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    hierarchy = build_category_hierarchy(categories_file)
    return categories, hierarchy

def validate_bookmarks_html(html_path: str) -> bool:
    """Validate that the file exists and has the correct Chrome bookmarks format."""
    path = Path(html_path)
    if not path.exists():
        print(f"Error: File not found: {html_path}")
        return False
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for typical Chrome bookmarks export markers
        if not all(marker in content for marker in [
            "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
            "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">",
            "<TITLE>Bookmarks</TITLE>"
        ]):
            print("Error: File doesn't appear to be a valid Chrome bookmarks export")
            print("Make sure you exported your bookmarks from Chrome using:")
            print("Chrome Menu > Bookmarks > Bookmark Manager > ⋮ > Export bookmarks")
            return False
            
        return True
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

def normalize_url(url: str) -> str:
    """Normalize URLs to identify duplicates with different formats."""
    # Parse the URL
    parsed = urlparse(url)
    
    # Normalize domain (treat www and https the same)
    netloc = parsed.netloc.lower()
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    
    # Special handling for specific domains
    if netloc == 'github.com':
        # Remove ?tab=readme-ov-file and similar parameters
        path = re.sub(r'\?tab=.*$', '', parsed.path)
    elif netloc == 'biorxiv.org':
        # Remove version and .full suffix from biorxiv URLs
        path = re.sub(r'v\d+\.full$', '', parsed.path)
    else:
        path = parsed.path
    
    # Remove /index.php from paths
    path = re.sub(r'/index\.php$', '', path)
    
    # Remove trailing slashes
    path = path.rstrip('/')
    
    # Reconstruct the normalized URL
    return f"{parsed.scheme}://{netloc}{path}"

def is_utility_url(url: str) -> bool:
    """Check if URL is a utility/search page that should be filtered."""
    parsed = urlparse(url.lower())
    domain = parsed.netloc
    path = parsed.path
    
    # List of patterns for utility URLs
    utility_patterns = [
        # Search engines
        r'google\.com/search',
        r'bing\.com/search',
        r'search\.yahoo\.com',
        # Common utility pages
        r'google\.com/mail',  # Gmail
        r'google\.com/calendar',  # Google Calendar
        r'drive\.google\.com',  # Google Drive
        r'docs\.google\.com',  # Google Docs
        r'translate\.google\.com',  # Google Translate
        r'maps\.google\.com',  # Google Maps
        # Add more patterns as needed
    ]
    
    # Check if URL matches any utility pattern
    full_url = f"{domain}{path}"
    return any(re.search(pattern, full_url) for pattern in utility_patterns)

def parse_bookmarks_html(html_path: str, filter_utility: bool = True) -> List[Dict]:
    """Parse Chrome bookmarks from exported HTML file."""
    if not validate_bookmarks_html(html_path):
        return []
        
    print(f"\nParsing HTML file: {html_path}")
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
    
    # Find all A tags with href attributes
    all_bookmarks = soup.find_all('a', href=True)
    print(f"\nFound {len(all_bookmarks)} bookmarks with href attributes")
    
    # Process each bookmark
    bookmarks = []
    skipped = 0
    utility_skipped = 0
    local_skipped = 0
    seen_urls = set()  # Track unique normalized URLs
    
    for a in all_bookmarks:
        url = a['href']
        # Skip javascript: bookmarks and empty URLs
        if url.startswith('javascript:') or not url:
            skipped += 1
            continue
        
        # Skip local file URLs
        if url.startswith('file://') or url.startswith('/') or url.startswith('\\') or url.startswith('C:\\') or url.startswith('D:\\'):
            local_skipped += 1
            continue
        
        # Skip utility URLs if filtering is enabled
        if filter_utility and is_utility_url(url):
            utility_skipped += 1
            continue
        
        # Normalize URL for deduplication
        normalized_url = normalize_url(url)
        if normalized_url in seen_urls:
            skipped += 1
            continue
        
        seen_urls.add(normalized_url)
        
        # Find the closest parent DT and its parent DL
        dt = a.find_parent('dt')
        if not dt:
            continue
            
        # Find all parent H3 elements by walking up the tree
        current = dt
        folders = []
        while current:
            parent_dl = current.find_parent('dl')
            if not parent_dl:
                break
            parent_dt = parent_dl.find_parent('dt')
            if parent_dt:
                h3 = parent_dt.find('h3')
                if h3:
                    folders.append(h3.text.strip())
            current = parent_dt
        
        folder_path = "/".join(reversed(folders)) if folders else ""
        
        bookmark = {
            'url': url,  # Keep original URL in the bookmark
            'normalized_url': normalized_url,  # Store normalized version for reference
            'title': a.text.strip() or url,  # Use URL if title is empty
            'folder_path': folder_path,
            'add_date': a.get('ADD_DATE', str(int(time.time()))),
            'icon': a.get('ICON', ''),
            'last_modified': a.get('LAST_MODIFIED', ''),
            'id': a.get('id', str(hash(normalized_url) % 100000))
        }
        bookmarks.append(bookmark)
    
    print(f"\nProcessed {len(bookmarks)} valid bookmarks")
    print(f"Skipped {skipped} duplicates")
    print(f"Skipped {utility_skipped} utility/search URLs")
    print(f"Skipped {local_skipped} local file URLs")
    
    # Print some folder statistics
    folder_counts = {}
    for b in bookmarks:
        if b['folder_path']:
            folder_counts[b['folder_path']] = folder_counts.get(b['folder_path'], 0) + 1
    
    print("\nBookmarks by folder:")
    for folder, count in sorted(folder_counts.items()):
        print(f"  {folder}: {count} bookmarks")
    
    if bookmarks:
        print("\nSample bookmark:")
        print(json.dumps(bookmarks[0], indent=2))
    
    return bookmarks

def apply_quick_sort_rules(url: str, title: str, hierarchy: CategoryHierarchy = None) -> Optional[Dict]:
    """Apply quick sorting rules to categorize bookmarks without using LLM."""
    parsed = urlparse(url.lower())
    domain = parsed.netloc
    path = parsed.path

    # Social Media rules
    if any(domain.endswith(site) for site in ['twitter.com', 'facebook.com', 'bsky.app']):
        return {
            'category': 'Social Media',
            'tags': ['social media', domain.split('.')[0]],
            'description': f"A {domain.split('.')[0].title()} post or profile",
            'importance': 2  # Default importance for social media
        }

    # R Packages rules
    if any(domain.endswith(site) for site in ['cran.r-project.org', 'bioconductor.org', 'rdrr.io']):
        return {
            'category': 'R packages',
            'tags': ['R', 'package', 'programming'],
            'description': f"An R package documentation or repository on {domain}",
            'importance': 4  # Higher importance for programming resources
        }

    # Python Packages rules
    if domain == 'pypi.org':
        return {
            'category': 'Python packages',
            'tags': ['Python', 'package', 'programming'],
            'description': f"A Python package on PyPI: {title}",
            'importance': 4
        }

    # Documentation rules
    if domain.endswith('readthedocs.io') or domain.endswith('readthedocs.org'):
        return {
            'category': 'Documentation',
            'tags': ['docs', 'programming', 'reference'],
            'description': f"Documentation on ReadTheDocs: {title}",
            'importance': 4
        }
        
    # Check base URLs from the hierarchy if provided
    if hierarchy:
        full_domain = domain + path.rstrip('/')
        best_match = None
        best_match_category = None
        
        for category, base_urls in hierarchy.get_all_base_urls().items():
            for base_url in base_urls:
                # Check if the domain starts with or contains the base URL
                if domain == base_url or domain.endswith('.' + base_url) or full_domain.startswith(base_url):
                    parent_categories = hierarchy.get_parents(category)
                    
                    # If this category has parents and is not too deep in the hierarchy,
                    # prefer the parent category (max 2 levels up)
                    if parent_categories and len(parent_categories) <= 2:
                        highest_parent = parent_categories[-1]
                        best_match = base_url
                        best_match_category = highest_parent
                    else:
                        best_match = base_url
                        best_match_category = category
        
        if best_match_category:
            tags = []
            
            # Generate tags based on URL and category
            domain_parts = domain.split('.')
            if len(domain_parts) > 1:
                tags.append(domain_parts[0])  # Add domain name as a tag
            
            tags.append(best_match_category.lower())  # Add lowercase category as a tag
            
            # Add additional tags based on path segments
            path_parts = [p for p in path.split('/') if p and not p.startswith('?')]
            if path_parts:
                tags.append(path_parts[0])  # Add first path segment as a tag
            
            # Ensure we have at least 2 unique tags
            tags = list(set(tags))
            if len(tags) < 2:
                tags.append('bookmark')
            
            # Lookup parent categories for the selected category
            parent_categories = hierarchy.get_parents(best_match_category)
            
            return {
                'category': best_match_category,
                'tags': tags[:3],  # Limit to 3 tags
                'description': f"A {best_match_category} resource from {domain}",
                'importance': 3,  # Default importance for pattern-matched URLs
                'parent_categories': parent_categories
            }

    return None

def map_to_existing_category(new_category: str, existing_categories: List[str]) -> str:
    """Map a potentially new category to an existing one if it's similar."""
    # If the category already exists, return it
    if new_category in existing_categories:
        return new_category
        
    # Check for case insensitive match
    for category in existing_categories:
        if category.lower() == new_category.lower():
            return category
            
    # Check for partial matches (new category contains existing one or vice versa)
    for category in existing_categories:
        if category.lower() in new_category.lower() or new_category.lower() in category.lower():
            return category
            
    # If no match found, return the original category
    return new_category

def process_bookmarks_chunk(bookmarks: List[Dict], hierarchy: CategoryHierarchy, fast_mode: bool = False, faster_mode: bool = False) -> List[Optional[ProcessedBookmark]]:
    """Process a chunk of bookmarks using quick sort rules first, then LLM for remaining ones."""
    if not bookmarks:
        return []

    processed_bookmarks = []
    remaining_bookmarks = []

    # First pass: Apply quick sort rules
    for bookmark in bookmarks:
        quick_sort_result = apply_quick_sort_rules(bookmark['url'], bookmark['title'], hierarchy)
        if quick_sort_result:
            # Get parent categories for the quick-sorted category
            parent_categories = hierarchy.get_parents(quick_sort_result['category'])
            
            processed_bookmarks.append(ProcessedBookmark(
                url=bookmark['url'],
                title=bookmark['title'],
                category=quick_sort_result['category'],
                tags=quick_sort_result['tags'],
                description=quick_sort_result['description'],
                importance=quick_sort_result['importance'],
                parent_categories=parent_categories,
                add_date=bookmark.get('add_date', ''),
                last_modified=bookmark.get('last_modified', ''),
                icon=bookmark.get('icon', ''),
                folder_path=bookmark.get('folder_path', '')
            ))
        else:
            remaining_bookmarks.append(bookmark)

    # If all bookmarks were handled by quick sort rules, return results
    if not remaining_bookmarks:
        return processed_bookmarks
        
    # Second pass (faster_mode): Try URL pattern matching against all base URLs
    if faster_mode:
        pattern_matched_bookmarks = []
        still_remaining_bookmarks = []
        
        for bookmark in remaining_bookmarks:
            # Try to match against base URL patterns
            url = bookmark['url']
            title = bookmark['title']
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            path = parsed.path
            
            matched = False
            for category, base_urls in hierarchy.get_all_base_urls().items():
                full_domain = domain + path.rstrip('/')
                
                for base_url in base_urls:
                    if (domain == base_url or 
                        domain.endswith('.' + base_url) or 
                        domain.startswith(base_url) or
                        full_domain.find(base_url) != -1):
                        
                        matched = True
                        parent_categories = hierarchy.get_parents(category)
                        
                        # If this category has parents, prefer using the highest appropriate parent
                        # but not going too high in the hierarchy (max 2 levels up)
                        if parent_categories and len(parent_categories) <= 2:
                            highest_parent = parent_categories[-1]  # Get the highest parent
                            category = highest_parent
                            parent_categories = parent_categories[:-1]  # Remove the used parent
                            
                        # Generate tags based on URL parts
                        tags = []
                        domain_parts = domain.split('.')
                        if len(domain_parts) > 1:
                            tags.append(domain_parts[0])
                        
                        tags.append(category.lower())
                        
                        path_parts = [p for p in path.split('/') if p and not p.startswith('?')]
                        if path_parts:
                            tags.append(path_parts[0])
                            
                        # Ensure unique tags
                        tags = list(set(tags))[:3]
                        if len(tags) < 2:
                            tags.append('bookmark')
                        
                        pattern_matched_bookmarks.append(ProcessedBookmark(
                            url=bookmark['url'],
                            title=bookmark['title'],
                            category=category,
                            tags=tags,
                            description=f"A {category} resource from {domain}",
                            importance=3,  # Default importance for pattern-matched URLs
                            parent_categories=parent_categories,
                            add_date=bookmark.get('add_date', ''),
                            last_modified=bookmark.get('last_modified', ''),
                            icon=bookmark.get('icon', ''),
                            folder_path=bookmark.get('folder_path', '')
                        ))
                        break
                
                if matched:
                    break
                    
            if not matched:
                still_remaining_bookmarks.append(bookmark)
        
        # Update the processed bookmarks list and the remaining bookmarks list
        processed_bookmarks.extend(pattern_matched_bookmarks)
        remaining_bookmarks = still_remaining_bookmarks
        
        # If all remaining bookmarks were handled by pattern matching, return results
        if not remaining_bookmarks:
            return processed_bookmarks

    # Get categories from hierarchy for remaining bookmarks
    categories = sorted(list(hierarchy.all_categories))
    categories_str = "\n".join(categories) if categories else "No predefined categories"

    # Format remaining bookmarks for the prompt
    bookmarks_str = "\n".join([
        f"URL {i+1}: {b['url']}\n"
        f"Title {i+1}: {b['title']}\n"
        for i, b in enumerate(remaining_bookmarks)
    ])

    # Setup the OpenAI client with llm configuration
    client = openai.OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    
    try:
        if fast_mode:
            # Fast mode: only get categories
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a bookmark categorization assistant. Your task is to quickly analyze URLs and titles to assign them to the most appropriate categories. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": f"""
Categorize these {len(remaining_bookmarks)} bookmarks using ONLY the available categories:

{bookmarks_str}

Available Categories:
{categories_str}

IMPORTANT GUIDELINES:
- ONLY use categories from the provided list
- DO NOT create new categories
- Prioritize using broader parent categories over niche categories when possible
- Choose the most appropriate category that fits each bookmark
- Consider the URL domain and title carefully

Return ONLY a JSON array of categories, exactly one for each bookmark with a total of {len(remaining_bookmarks)} entries. Example:
["category1", "category2", "category3", ...]

Ensure the array contains EXACTLY {len(remaining_bookmarks)} items.
"""
                    }
                ],
                max_tokens=800,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
        else:
            # Normal mode: full metadata
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a bookmark organization assistant. Your task is to analyze URLs and their titles to provide meaningful categorization and metadata. Be concise but informative. Create new categories when existing ones don't fit well. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": f"""
Please analyze these {len(remaining_bookmarks)} bookmarks and provide structured categorization for each:

{bookmarks_str}

Available Categories:
{categories_str}

IMPORTANT GUIDELINES:
- Strongly prefer using existing categories from the provided list above
- Only create a new category if absolutely necessary and no existing category fits
- Prioritize broader parent categories over creating new specialized categories
- Choose the most appropriate category that fits each bookmark's content
- Consider the URL domain and title carefully when categorizing

For each bookmark, provide the following information in a JSON array with EXACTLY {len(remaining_bookmarks)} items:
1. category: STRONGLY prefer choosing from existing categories - only create new ones if absolutely necessary
2. tags: 2-4 relevant tags for each bookmark
3. description: A brief (max 2 sentences) description of what each bookmark contains
4. importance: Rate from 1-5 how important/useful each bookmark seems (1=least, 5=most)

Return ONLY valid JSON without any additional text, in this exact format:
[
  {{"category": "chosen_category", "tags": ["tag1", "tag2"], "description": "brief description", "importance": number}},
  {{"category": "chosen_category", "tags": ["tag1", "tag2"], "description": "brief description", "importance": number}},
  ...
]

The array MUST contain exactly {len(remaining_bookmarks)} items, one for each bookmark.
"""
                    }
                ],
                max_tokens=800,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
        
        content = response.choices[0].message.content.strip()
        
        try:
            # Remove any leading/trailing non-JSON content
            content = content.strip()
            if content.find('[') != -1:
                content = content[content.find('['):]
            if content.rfind(']') != -1:
                content = content[:content.rfind(']')+1]
                
            data_list = json.loads(content)
            
            if not isinstance(data_list, list):
                print(f"Error: Expected list format in response, got {type(data_list)}")
                return processed_bookmarks + [None] * len(remaining_bookmarks)
                
            # Handle case where LLM returns wrong number of results
            if len(data_list) != len(remaining_bookmarks):
                print(f"Warning: Expected {len(remaining_bookmarks)} results, got {len(data_list)}. Adjusting...")
                
                # If we got more results than needed, trim the excess
                if len(data_list) > len(remaining_bookmarks):
                    data_list = data_list[:len(remaining_bookmarks)]
                # If we got fewer results than needed, add None entries for the missing ones
                else:
                    data_list = data_list + [None] * (len(remaining_bookmarks) - len(data_list))
            
            # Process LLM results
            for bookmark, data in zip(remaining_bookmarks, data_list):
                if data is None:
                    print(f"Missing data for bookmark: {bookmark['title'][:30]}...")
                    processed_bookmarks.append(None)
                    continue
                    
                if fast_mode:
                    # In fast mode, data is just the category string
                    try:
                        category = data if isinstance(data, str) else str(data)
                        
                        # Map to existing category if possible
                        original_category = category
                        category = map_to_existing_category(category, categories)
                        
                        if original_category != category:
                            print(f"  Mapped category '{original_category}' to existing category '{category}'")
                        
                        parent_categories = hierarchy.get_parents(category)
                        
                        processed_bookmarks.append(ProcessedBookmark(
                            url=bookmark['url'],
                            title=bookmark['title'],
                            category=category,
                            tags=['auto-categorized'],
                            description=f"Bookmark from {urlparse(bookmark['url']).netloc}",
                            importance=3,  # Default importance in fast mode
                            parent_categories=parent_categories,
                            add_date=bookmark.get('add_date', ''),
                            last_modified=bookmark.get('last_modified', ''),
                            icon=bookmark.get('icon', ''),
                            folder_path=bookmark.get('folder_path', '')
                        ))
                    except Exception as e:
                        print(f"Error processing fast mode data for {bookmark['title'][:30]}: {e}")
                        processed_bookmarks.append(None)
                else:
                    # Normal mode processing
                    try:
                        required_fields = ['category', 'tags', 'description', 'importance']
                        if not all(field in data for field in required_fields):
                            print(f"Missing required fields in LLM response for {bookmark['title'][:30]}...")
                            processed_bookmarks.append(None)
                            continue
                            
                        # Map new category to existing one if possible
                        original_category = data['category']
                        data['category'] = map_to_existing_category(data['category'], categories)
                        
                        if original_category != data['category']:
                            print(f"  Mapped category '{original_category}' to existing category '{data['category']}'")
                        
                        # Validate importance is between 1-5
                        if not isinstance(data['importance'], (int, float)) or not (1 <= data['importance'] <= 5):
                            data['importance'] = max(1, min(5, int(float(str(data['importance']))) if str(data['importance']).replace('.', '', 1).isdigit() else 3))
                            
                        # Ensure tags is a list
                        if not isinstance(data['tags'], list):
                            if isinstance(data['tags'], str):
                                data['tags'] = [data['tags']]
                            else:
                                data['tags'] = ['auto-categorized']
                        
                        # Limit tags to 2-4
                        if len(data['tags']) < 2:
                            data['tags'] = data['tags'] + ['general']
                        if len(data['tags']) > 4:
                            data['tags'] = data['tags'][:4]
                        
                        # Get parent categories
                        parent_categories = hierarchy.get_parents(data['category'])
                            
                        processed_bookmarks.append(ProcessedBookmark(
                            url=bookmark['url'],
                            title=bookmark['title'],
                            category=data['category'],
                            tags=data['tags'],
                            description=data['description'],
                            importance=data['importance'],
                            parent_categories=parent_categories,
                            add_date=bookmark.get('add_date', ''),
                            last_modified=bookmark.get('last_modified', ''),
                            icon=bookmark.get('icon', ''),
                            folder_path=bookmark.get('folder_path', '')
                        ))
                    except Exception as e:
                        print(f"Error processing normal mode data for {bookmark['title'][:30]}: {e}")
                        processed_bookmarks.append(None)
            
            return processed_bookmarks
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Raw response: {content}")
            return processed_bookmarks + [None] * len(remaining_bookmarks)
            
    except Exception as e:
        print(f"\nError processing chunk: {str(e)}")
        return processed_bookmarks + [None] * len(remaining_bookmarks)

def combine_bookmarks(bookmarks_lists: List[List[Dict]]) -> List[Dict]:
    """Combine multiple lists of bookmarks and deduplicate based on normalized URLs and titles."""
    seen_urls = set()
    seen_titles = set()
    combined_bookmarks = []
    skipped_count = 0
    
    for bookmarks in bookmarks_lists:
        for bookmark in bookmarks:
            try:
                # Ensure we have a normalized URL
                if 'normalized_url' not in bookmark:
                    if 'url' not in bookmark:
                        print(f"Warning: Bookmark missing URL, skipping: {bookmark.get('title', 'Untitled')}")
                        skipped_count += 1
                        continue
                    # Try to normalize the URL if not already done
                    bookmark['normalized_url'] = normalize_url(bookmark['url'])
                
                # Ensure we have a title
                if 'title' not in bookmark:
                    print(f"Warning: Bookmark missing title, using URL: {bookmark['url']}")
                    bookmark['title'] = bookmark['url']
                
                normalized_url = bookmark['normalized_url']
                normalized_title = bookmark['title'].lower().strip()
                
                # Skip if we've seen either the URL or title before
                if normalized_url in seen_urls or normalized_title in seen_titles:
                    skipped_count += 1
                    continue
                    
                seen_urls.add(normalized_url)
                seen_titles.add(normalized_title)
                combined_bookmarks.append(bookmark)
            except Exception as e:
                print(f"Warning: Error processing bookmark, skipping: {str(e)}")
                skipped_count += 1
                continue
    
    if skipped_count > 0:
        print(f"\nSkipped {skipped_count} bookmarks during deduplication")
    
    return combined_bookmarks

def merge_hierarchies(hierarchy1: CategoryHierarchy, hierarchy2: CategoryHierarchy) -> CategoryHierarchy:
    """Merge two category hierarchies into one."""
    merged = CategoryHierarchy()
    
    # Copy all categories and relationships from the first hierarchy
    for child, parent in hierarchy1.parent_map.items():
        merged.add_relationship(parent, child)
    
    # Copy all base URLs from the first hierarchy
    for category, urls in hierarchy1.base_urls.items():
        for url in urls:
            merged.add_base_url(category, url)
    
    # Copy all categories and relationships from the second hierarchy
    for child, parent in hierarchy2.parent_map.items():
        merged.add_relationship(parent, child)
    
    # Copy all base URLs from the second hierarchy
    for category, urls in hierarchy2.base_urls.items():
        for url in urls:
            merged.add_base_url(category, url)
    
    return merged

def process_bookmarks(output_dir: str = "organized_bookmarks", replace_original: bool = False, 
                     html_paths: List[str] = None, categories_file: str = None, 
                     filter_utility: bool = True, chunk_size: int = 5,
                     fast_mode: bool = False, faster_mode: bool = False,
                     merge_mode: bool = False, api_key: str = None,
                     base_url: str = None, model: str = None) -> None:
    """Main function to process all Chrome bookmarks."""
    try:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Create subdirectories for different types of outputs
        (output_path / "intermediate").mkdir(exist_ok=True)
        (output_path / "backups").mkdir(exist_ok=True)
        (output_path / "reports").mkdir(exist_ok=True)
        
        # Load category hierarchy
        if not categories_file:
            categories_file = str(Path(__file__).parent / "data" / "group_ideas.tsv")
            print(f"No categories file specified, using default: {categories_file}")
        
        try:
            base_categories, base_hierarchy = load_categories(categories_file)
        except FileNotFoundError:
            print(f"Error: Categories file not found: {categories_file}")
            print("Please provide a valid categories file using --categories-file")
            return
        except Exception as e:
            print(f"Error loading categories file: {str(e)}")
            return
        
        if faster_mode:
            print("\nFaster mode enabled: Using URL pattern matching for categorization")
            print(f"URL patterns available for {len(base_hierarchy.get_all_base_urls())} categories")
            
        if merge_mode:
            print("\nMerge mode enabled: Processing inputs separately and combining results")
            if not html_paths or len(html_paths) < 2:
                print("Warning: Merge mode requires at least two HTML files. Falling back to standard processing.")
                merge_mode = False
        
        # Set API configuration
        if api_key:
            os.environ['API_KEY'] = api_key
        if base_url:
            os.environ['BASE_URL'] = base_url
        if model:
            os.environ['MODEL'] = model
        
        # Load bookmarks from all sources 
        all_bookmarks_lists = []
        
        # Load from HTML files if provided
        if html_paths:
            for html_path in html_paths:
                try:
                    print(f"\nLoading bookmarks from HTML file: {html_path}")
                    bookmarks = parse_bookmarks_html(html_path, filter_utility=filter_utility)
                    if bookmarks:
                        all_bookmarks_lists.append(bookmarks)
                        print(f"Found {len(bookmarks)} bookmarks in {html_path}")
                except Exception as e:
                    print(f"Error loading HTML file {html_path}: {str(e)}")
                    continue
        else:
            # Load from Chrome (existing code)
            try:
                bookmarks_file = get_chrome_bookmarks_file()
                backup_path = output_path / "backups" / f"bookmarks_backup_{int(time.time())}.json"
                
                print(f"Creating backup at: {backup_path}")
                with open(bookmarks_file, 'r', encoding='utf-8') as src, \
                     open(backup_path, 'w', encoding='utf-8') as dst:
                    data = json.load(src)
                    json.dump(data, dst, indent=2)
                
                # Load and process bookmarks
                bookmarks_data = load_chrome_bookmarks()
                
                # Extract bookmarks from all root folders
                bookmarks = []
                for root_name, root_data in bookmarks_data['roots'].items():
                    print(f"Processing root: {root_name}")
                    bookmarks.extend(extract_bookmarks(root_data))
                all_bookmarks_lists.append(bookmarks)
            except Exception as e:
                print(f"Error loading Chrome bookmarks: {str(e)}")
                return
        
        if not all_bookmarks_lists:
            print("No bookmarks found to process")
            return
        
        # Combine and deduplicate bookmarks
        print("\nCombining and deduplicating bookmarks...")
        try:
            bookmarks = combine_bookmarks(all_bookmarks_lists)
            print(f"Combined total: {len(bookmarks)} unique bookmarks")
            
            # Save intermediate combined bookmarks
            intermediate_path = output_path / "intermediate" / "combined_bookmarks.json"
            with open(intermediate_path, 'w', encoding='utf-8') as f:
                json.dump(bookmarks, f, indent=2)
            print(f"Saved combined bookmarks to: {intermediate_path}")
        except Exception as e:
            print(f"Error combining bookmarks: {str(e)}")
            return
        
        # Process the bookmarks
        try:
            processed_bookmarks, categories = process_bookmarks_list(
                bookmarks, 
                base_hierarchy,
                output_path, 
                chunk_size, 
                fast_mode, 
                faster_mode
            )
            
            if not processed_bookmarks:
                print("No bookmarks were successfully processed")
                return
                
            # Generate Chrome-compatible formats
            generate_chrome_formats(categories, base_hierarchy, output_path)
            
            # Generate report
            report_path = output_path / "reports" / "bookmark_report.md"
            generate_report(str(output_path), str(report_path))
            
            print("\nProcessing complete!")
            print(f"Total bookmarks processed: {len(processed_bookmarks)}")
            print(f"Categories created: {len(categories)}")
            print(f"Output directory: {output_path}")
            print(f"Report generated: {report_path}")
            
        except Exception as e:
            print(f"Error processing bookmarks: {str(e)}")
            return
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return

def process_bookmarks_list(bookmarks: List[Dict], hierarchy: CategoryHierarchy, 
                          output_path: Path, chunk_size: int, fast_mode: bool, 
                          faster_mode: bool, save_individual: bool = True) -> Tuple[List[ProcessedBookmark], Dict]:
    """Process a list of bookmarks and optionally save them individually."""
    # First pass: Apply quick sort rules to all bookmarks
    processed_bookmarks = []
    remaining_bookmarks = []
    quick_sort_counts = {}  # Track counts for each quick sort category
    pattern_match_counts = {}  # Track counts for pattern matched categories
    
    print("\nApplying quick sort rules...")
    for bookmark in bookmarks:
        quick_sort_result = apply_quick_sort_rules(bookmark['url'], bookmark['title'], hierarchy)
        if quick_sort_result:
            # Get parent categories for the quick-sorted category
            parent_categories = hierarchy.get_parents(quick_sort_result['category'])
            
            processed = ProcessedBookmark(
                url=bookmark['url'],
                title=bookmark['title'],
                category=quick_sort_result['category'],
                tags=quick_sort_result['tags'],
                description=quick_sort_result['description'],
                importance=quick_sort_result['importance'],
                parent_categories=parent_categories,
                add_date=bookmark.get('add_date', ''),
                last_modified=bookmark.get('last_modified', ''),
                icon=bookmark.get('icon', ''),
                folder_path=bookmark.get('folder_path', '')
            )
            
            # Save the bookmark if requested
            if save_individual:
                save_processed_bookmark(processed, output_path)
            
            # Add to processed list and update counts
            processed_bookmarks.append(processed)
            quick_sort_counts[quick_sort_result['category']] = quick_sort_counts.get(quick_sort_result['category'], 0) + 1
        else:
            remaining_bookmarks.append(bookmark)
    
    # Print quick sort statistics
    if quick_sort_counts:
        print("\nQuick sort results:")
        for category, count in sorted(quick_sort_counts.items()):
            print(f"✓ {category}: {count} bookmarks")
        print(f"\nTotal quick sorted: {len(processed_bookmarks)}")
        print(f"Remaining for LLM: {len(remaining_bookmarks)}")
    
    # Process remaining bookmarks in chunks using LLM
    if remaining_bookmarks:
        print(f"\nProcessing remaining {len(remaining_bookmarks)} bookmarks in chunks of {chunk_size}...")
        print(f"Mode: {'Fast (categories only)' if fast_mode else 'Normal (full metadata)'}")
        if faster_mode:
            print("URL pattern matching enabled for faster processing")
        
        # Process bookmarks in chunks
        for i in tqdm(range(0, len(remaining_bookmarks), chunk_size),
                    total=len(remaining_bookmarks)/chunk_size,
                    desc=f"Processing with LLM"):
            chunk = remaining_bookmarks[i:i + chunk_size]
            print(f"\nProcessing chunk {i//chunk_size + 1}/{(len(remaining_bookmarks) + chunk_size - 1)//chunk_size}")
            
            # Print titles being processed
            for b in chunk:
                print(f"- {b['title'][:60]}...")
            
            processed_chunk = process_bookmarks_chunk(chunk, hierarchy, fast_mode=fast_mode, faster_mode=faster_mode)
            
            # Process results
            for bookmark, processed in zip(chunk, processed_chunk):
                if processed:
                    print(f"✓ {bookmark['title'][:30]}: {processed.category}")
                    if processed.parent_categories:
                        print(f"  Parent Categories: {' > '.join(reversed(processed.parent_categories))}")
                    if not fast_mode:  # Only show importance in normal mode
                        print(f"  Importance: {'★' * processed.importance}{'☆' * (5 - processed.importance)}")
                    
                    processed_bookmarks.append(processed)
                    
                    # Track statistics for pattern-matched bookmarks
                    if faster_mode and bookmark not in remaining_bookmarks:
                        pattern_match_counts[processed.category] = pattern_match_counts.get(processed.category, 0) + 1
                    
                    # Save the bookmark if requested
                    if save_individual:
                        save_processed_bookmark(processed, output_path)
                else:
                    print(f"✗ Failed to process: {bookmark['title'][:30]}")
    
    # Print pattern match statistics
    if pattern_match_counts:
        print("\nURL pattern match results:")
        for category, count in sorted(pattern_match_counts.items()):
            print(f"✓ {category}: {count} bookmarks")
    
    # Group all processed bookmarks by category
    categories = group_bookmarks_by_category(processed_bookmarks)
    
    return processed_bookmarks, categories

def group_bookmarks_by_category(processed_bookmarks: List[ProcessedBookmark]) -> Dict:
    """Group processed bookmarks by category."""
    categories = {}
    for bookmark in processed_bookmarks:
        if bookmark.category not in categories:
            categories[bookmark.category] = []
        
        categories[bookmark.category].append({
            'url': bookmark.url,
            'title': bookmark.title,
            'category': bookmark.category,
            'parent_categories': bookmark.parent_categories,
            'tags': bookmark.tags,
            'description': bookmark.description,
            'importance': bookmark.importance,
            'original_folder': bookmark.folder_path,
            'date_added': bookmark.add_date,
            'id': str(hash(bookmark.url) % 100000)
        })
    
    return categories

def generate_chrome_formats(categories: Dict, hierarchy: CategoryHierarchy, output_path: Path) -> None:
    """Generate Chrome-compatible formats for the bookmarks."""
    # Create chrome directory for Chrome-specific outputs
    chrome_dir = output_path / "chrome"
    chrome_dir.mkdir(exist_ok=True)
    
    chrome_json_path = chrome_dir / 'bookmarks.json'
    chrome_html_path = chrome_dir / 'bookmarks.html'
    
    # Generate JSON format
    chrome_format = generate_chrome_json(categories, hierarchy)
    with open(chrome_json_path, 'w', encoding='utf-8') as f:
        json.dump(chrome_format, f, indent=2)
    
    # Generate HTML format
    generate_chrome_html(categories, hierarchy, chrome_html_path)
    
    print(f"Chrome JSON format saved to: {chrome_json_path}")
    print(f"Chrome HTML format saved to: {chrome_html_path}")

def generate_chrome_json(categories: Dict[str, List[Dict]], hierarchy: CategoryHierarchy) -> Dict:
    """Generate Chrome-compatible JSON format."""
    chrome_format = {
        'version': 1,
        'roots': {
            'bookmark_bar': {
                'children': [],
                'date_added': str(int(time.time() * 1000000)),
                'date_modified': str(int(time.time() * 1000000)),
                'id': '1',
                'name': 'Bookmarks Bar',
                'type': 'folder'
            },
            'other': {
                'children': [],
                'date_added': str(int(time.time() * 1000000)),
                'date_modified': str(int(time.time() * 1000000)),
                'id': '2',
                'name': 'Other Bookmarks',
                'type': 'folder'
            },
            'synced': {
                'children': [],
                'date_added': str(int(time.time() * 1000000)),
                'date_modified': str(int(time.time() * 1000000)),
                'id': '3',
                'name': 'Mobile Bookmarks',
                'type': 'folder'
            }
        }
    }
    
    def create_folder_structure(category: str, bookmarks: List[Dict]) -> Dict:
        folder = {
            'children': [],
            'date_added': str(int(time.time() * 1000000)),
            'date_modified': str(int(time.time() * 1000000)),
            'id': str(hash(category) % 100000),
            'name': category,
            'type': 'folder'
        }
        
        # Add all bookmarks for this category
        for bookmark in sorted(bookmarks, key=lambda x: (-x['importance'], x['title'])):
            bookmark_entry = {
                'date_added': bookmark['date_added'],
                'id': bookmark['id'],
                'name': bookmark['title'],
                'type': 'url',
                'url': bookmark['url'],
                'meta_info': {
                    'tags': bookmark['tags'],
                    'description': bookmark['description'],
                    'importance': bookmark['importance']
                }
            }
            folder['children'].append(bookmark_entry)
        
        return folder
    
    # Create folders for root categories (those without parents)
    root_categories = {cat for cat in categories if not hierarchy.get_parents(cat)}
    for category in sorted(root_categories):
        folder = create_folder_structure(category, categories[category])
        
        # Add subfolders for child categories
        child_categories = hierarchy.get_children(category)
        for child in sorted(child_categories):
            if child in categories:
                child_folder = create_folder_structure(child, categories[child])
                folder['children'].append(child_folder)
        
        chrome_format['roots']['bookmark_bar']['children'].append(folder)
    
    return chrome_format

def generate_chrome_html(categories: Dict[str, List[Dict]], hierarchy: CategoryHierarchy, output_path: str) -> None:
    """Generate Chrome-compatible HTML bookmarks file."""
    html_template = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    {content}
</DL><p>"""

    def format_bookmark(bookmark: Dict) -> str:
        date_added = bookmark.get('date_added', str(int(time.time())))
        return f"""<DT><A HREF="{bookmark['url']}" ADD_DATE="{date_added}">{bookmark['title']}</A>"""

    def format_folder(name: str, content: str) -> str:
        date_added = str(int(time.time()))
        return f"""<DT><H3 ADD_DATE="{date_added}">{name}</H3>
    <DL><p>
        {content}
    </DL><p>"""

    # Generate content for root categories
    root_categories = {cat for cat in categories if not hierarchy.get_parents(cat)}
    content_parts = []
    
    for category in sorted(root_categories):
        # Format bookmarks in this category
        bookmark_parts = [format_bookmark(b) for b in sorted(categories[category], key=lambda x: (-x['importance'], x['title']))]
        
        # Add subfolders for child categories
        child_categories = hierarchy.get_children(category)
        for child in sorted(child_categories):
            if child in categories:
                child_bookmarks = [format_bookmark(b) for b in sorted(categories[child], key=lambda x: (-x['importance'], x['title']))]
                bookmark_parts.append(format_folder(child, "\n        ".join(child_bookmarks)))
        
        # Create folder for this category
        content_parts.append(format_folder(category, "\n        ".join(bookmark_parts)))
    
    # Generate final HTML
    html_content = html_template.format(content="\n    ".join(content_parts))
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def get_chrome_bookmarks_file() -> Path:
    """Get the path to Chrome's bookmarks file based on the OS."""
    home = Path.home()
    
    if os.name == 'nt':  # Windows
        path = home / "AppData/Local/Google/Chrome/User Data/Default/Bookmarks"
    elif os.name == 'posix':  # Linux/Unix
        path = home / ".config/google-chrome/Default/Bookmarks"
        # Add alternative paths for Linux
        if not path.exists():
            path = home / ".var/app/com.google.Chrome/config/google-chrome/Default/Bookmarks"  # Flatpak
        if not path.exists():
            path = home / "snap/chromium/common/chromium/Default/Bookmarks"  # Snap
    else:  # macOS
        path = home / "Library/Application Support/Google/Chrome/Default/Bookmarks"
    
    print(f"Looking for bookmarks file at: {path}")
    print(f"File exists: {path.exists()}")
    return path

def load_chrome_bookmarks() -> Dict:
    """Load and parse Chrome's bookmarks file."""
    bookmarks_file = get_chrome_bookmarks_file()
    if not bookmarks_file.exists():
        raise FileNotFoundError(f"Chrome bookmarks file not found at: {bookmarks_file}")
    
    with open(bookmarks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Loaded bookmarks file. Root keys: {list(data.keys())}")
        print(f"Available roots: {list(data['roots'].keys())}")
        return data

def extract_bookmarks(node: Dict, bookmarks: List[Dict] = None, folder_path: str = "") -> List[Dict]:
    """Recursively extract bookmarks from Chrome's bookmarks JSON structure."""
    if bookmarks is None:
        bookmarks = []
    
    # Handle folder names for path tracking
    current_path = folder_path
    if node.get('type') == 'folder':
        current_path = f"{folder_path}/{node['name']}" if folder_path else node['name']
    
    if node.get('type') == 'url':
        bookmarks.append({
            'url': node['url'],
            'title': node['name'],
            'folder_path': current_path,
            'date_added': node.get('date_added', ''),
            'id': node.get('id', '')
        })
    
    # Process children if they exist
    if 'children' in node:
        for child in node['children']:
            extract_bookmarks(child, bookmarks, current_path)
    
    return bookmarks 

def sanitize_filename(title: str, url_hash: int) -> str:
    """Create a safe filename from a bookmark title."""
    # Replace problematic characters with underscores
    safe_title = re.sub(r'[^\w\s-]', '_', title)
    # Replace multiple spaces/underscores with a single underscore
    safe_title = re.sub(r'[-\s_]+', '_', safe_title)
    # Trim to reasonable length and add hash
    return f"{safe_title[:50]}_{url_hash % 10000:04d}.json".strip('_')

def save_processed_bookmark(bookmark: ProcessedBookmark, output_dir: Path) -> None:
    """Save a processed bookmark to the appropriate category directory."""
    # Create a safe filename
    filename = sanitize_filename(bookmark.title, hash(bookmark.url))
    
    # Create category directory and save the main file
    category_dir = output_dir / "categories" / bookmark.category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    bookmark_data = {
        'url': bookmark.url,
        'title': bookmark.title,
        'category': bookmark.category,
        'parent_categories': bookmark.parent_categories,
        'tags': bookmark.tags,
        'description': bookmark.description,
        'importance': bookmark.importance,
        'add_date': bookmark.add_date,
        'last_modified': bookmark.last_modified,
        'icon': bookmark.icon,
        'folder_path': bookmark.folder_path
    }
    
    # Save the main file
    source_file = category_dir / filename
    with open(source_file, 'w', encoding='utf-8') as f:
        json.dump(bookmark_data, f, indent=2, ensure_ascii=False)
    
    # Create symlinks or copies in parent category directories
    if bookmark.parent_categories:
        for parent in bookmark.parent_categories:
            parent_dir = output_dir / "categories" / parent
            parent_dir.mkdir(parents=True, exist_ok=True)
            
            target_file = parent_dir / filename
            if not target_file.exists():
                try:
                    # Try creating a symlink first
                    target_file.symlink_to(source_file.resolve())
                except (OSError, NotImplementedError):
                    # If symlink fails, create a copy
                    with open(target_file, 'w', encoding='utf-8') as f:
                        json.dump(bookmark_data, f, indent=2, ensure_ascii=False)

def extract_categories_from_bookmarks(bookmarks: List[Dict]) -> Set[str]:
    """Extract potential categories from bookmark folder paths."""
    categories = set()
    
    # Extract from folder paths
    for bookmark in bookmarks:
        if 'folder_path' in bookmark and bookmark['folder_path']:
            # Add each folder in the path as a potential category
            folders = bookmark['folder_path'].split('/')
            for folder in folders:
                if folder and len(folder) > 2:  # Skip empty or very short folder names
                    categories.add(folder)
    
    # Add some default categories that are always useful
    default_categories = [
        "Programming Languages", 
        "Research Papers", 
        "Documentation", 
        "Tutorials", 
        "Social Media",
        "News",
        "Technology",
        "Reference"
    ]
    
    for category in default_categories:
        categories.add(category)
    
    print(f"Extracted {len(categories)} potential categories from bookmarks")
    return categories 