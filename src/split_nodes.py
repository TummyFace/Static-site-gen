import re
from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        if text.count(delimiter) % 2 != 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {text}")
        parts = text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:  # Skip empty text parts
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    """
    Split TextNodes on markdown image syntax ![alt](url).
    
    Processes only TEXT type nodes. Images are converted to IMAGE type nodes
    with the URL stored as the url parameter. Preserves non-TEXT nodes as-is.
    
    Args:
        old_nodes: List of TextNode objects
        
    Returns:
        List of TextNode objects with images split out as IMAGE type nodes
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(node)
            continue
        
        # Split on the image pattern
        pattern = r"!\[[^\]]*\]\([^)]*\)"
        parts = re.split(pattern, text)
        
        for i in range(len(parts)):
            if parts[i]:  # Add text part if not empty
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            if i < len(images):  # Add image if exists
                alt_text, url = images[i]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes on markdown link syntax [anchor](url).
    
    Processes only TEXT type nodes. Links are converted to LINK type nodes
    with the URL stored as the url parameter. Preserves non-TEXT nodes as-is.
    
    Args:
        old_nodes: List of TextNode objects
        
    Returns:
        List of TextNode objects with links split out as LINK type nodes
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        
        if not links:
            new_nodes.append(node)
            continue
        
        # Split on the link pattern (but not on images which start with !)
        pattern = r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)"
        parts = re.split(pattern, text)
        
        # re.split with capturing groups includes captured groups in result
        # parts will be: [text_before, group1, group2, text_between, group1, group2, text_after]
        # We need to extract links (group1, group2 pairs) and interleave with text
        
        i = 0
        while i < len(parts):
            # This is text before a link (or remaining text)
            if parts[i]:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            
            # Check if there's a link next (group1 and group2)
            if i + 2 < len(parts):
                anchor_text = parts[i + 1]
                url = parts[i + 2]
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                i += 3
            else:
                break
    
    return new_nodes


def text_to_textnodes(text):
    """
    Convert raw markdown text into a list of TextNode objects.
    
    Processes all markdown syntax: bold (**), italic (*  or _), code (`),
    images (![alt](url)), and links ([anchor](url)).
    
    Args:
        text: Raw markdown text string
        
    Returns:
        List of TextNode objects with appropriate types
    """
    # Start with a single TEXT node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split on delimiters in order: bold, italic, code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Split on images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes