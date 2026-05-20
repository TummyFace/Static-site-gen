import os
from generate_page import generate_page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages from all markdown files in a content directory.
    
    Args:
        dir_path_content: Path to the content directory containing markdown files
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated HTML files
        basepath: Base URL path for generated links and assets
    """
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                markdown_file = os.path.join(root, file)
                # Calculate relative path and convert to HTML filename
                rel_path = os.path.relpath(markdown_file, dir_path_content)
                html_file = rel_path.replace('.md', '.html').replace('.markdown', '.html')
                dest_path = os.path.join(dest_dir_path, html_file)
                
                # Generate the page
                generate_page(markdown_file, template_path, dest_path, basepath)
