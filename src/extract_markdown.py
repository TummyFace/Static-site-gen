import re


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    
    Args:
        text: Raw markdown text containing images in the format ![alt](url)
        
    Returns:
        List of tuples containing (alt_text, url) for each image found
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text.
    
    Args:
        text: Raw markdown text containing links in the format [anchor](url)
        
    Returns:
        List of tuples containing (anchor_text, url) for each link found
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
