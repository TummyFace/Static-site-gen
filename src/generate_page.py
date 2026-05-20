import os
from markdown_to_html import markdown_to_html_node
from block_type import extract_title


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template file
        dest_path: Path to write the generated HTML file
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown content
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    
    # Read template content
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    
    # Extract title from markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    output_content = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_string)
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write output file
    with open(dest_path, 'w') as file:
        file.write(output_content)
