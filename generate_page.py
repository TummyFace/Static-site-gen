#!/usr/bin/env python3
import os
from pathlib import Path

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.scandir(dir_path_content):
        if entry.is_file() and entry.name.endswith('.md'):
            with open(entry.path, 'r') as f:
                markdown_content = f.read()

            # Read the template file
            with open(template_path, 'r') as t:
                template_content = t.read()

            # Generate the HTML content
            html_content = template_content.replace('<!-- CONTENT -->', markdown_content)

            # Create the destination directory if it doesn't exist
            dest_dir = Path(dest_dir_path) / entry.name[:-3]
            dest_dir.mkdir(parents=True, exist_ok=True)

            # Write the generated HTML to the public directory
            with open(dest_dir / 'index.html', 'w') as out:
                out.write(html_content)

def main():
    dir_path_content = '/home/tummyface/workspace/static-site-gen/content'
    template_path = '/home/tummyface/workspace/static-site-gen/template.html'
    dest_dir_path = '/home/tummyface/workspace/static-site-gen/public'

    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)

if __name__ == '__main__':
    main()