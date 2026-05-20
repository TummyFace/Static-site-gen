def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    import os
    from .generate_page import render_markdown_to_html

    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                markdown_file = os.path.join(root, file)
                html_file = os.path.relpath(markdown_file, dir_path_content).replace('.md', '.html').replace('.markdown', '.html')
                output_html = render_markdown_to_html(template_path, markdown_file)
                dest_path = os.path.join(dest_dir_path, html_file)
                with open(dest_path, 'w') as f:
                    f.write(output_html)
    import os
    from .generate_page import render_markdown_to_html

    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                markdown_file = os.path.join(root, file)
                html_file = os.path.relpath(markdown_file, dir_path_content).replace('.md', '.html').replace('.markdown', '.html')
                output_html = render_markdown_to_html(template_path, markdown_file)
                dest_path = os.path.join(dest_dir_path, html_file)
                with open(dest_path, 'w') as f:
                    f.write(output_html)

if __name__ == '__main__':
    generate_pages_recursive('/home/tummyface/workspace/static-site-gen/content', '/home/tummyface/workspace/static-site-gen/template.html', '/home/tummyface/workspace/static-site-gen/public')