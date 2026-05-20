import logging
import os
import sys
from textnode import TextNode, TextType
from copy_static import copy_directory_recursive
from generate_pages_recursive import generate_pages_recursive

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Copy static files to docs directory
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
    
    logger.info("Starting copy of static files to docs directory...")
    copy_directory_recursive(static_dir, docs_dir)
    logger.info("Static files copied successfully!")
    
    # Generate all pages recursively from content directory
    base_dir = os.path.dirname(__file__)
    content_dir = os.path.join(base_dir, "..", "content")
    template_path = os.path.join(base_dir, "..", "template.html")
    
    logger.info("Generating pages from markdown files...")
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)
    logger.info("All pages generated successfully!")


if __name__ == "__main__":
    main()
