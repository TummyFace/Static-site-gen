from markdown_blocks import markdown_to_blocks
from block_type import block_to_block_type, BlockType
from split_nodes import text_to_textnodes
from htmlnode import ParentNode, LeafNode, text_node_to_html_node


def text_to_children(text):
    """
    Convert text with inline markdown to a list of HTMLNode children.
    
    Args:
        text: Text string that may contain inline markdown
        
    Returns:
        List of HTMLNode objects representing the inline markdown
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document to a single parent HTMLNode.
    
    Args:
        markdown: Raw markdown string representing a full document
        
    Returns:
        ParentNode representing the entire document
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        children.append(block_node)
    
    return ParentNode("div", children)


def block_to_html_node(block, block_type):
    """
    Convert a single markdown block to an HTMLNode based on its type.
    
    Args:
        block: A single markdown block string
        block_type: The BlockType of the block
        
    Returns:
        HTMLNode representing the block
    """
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    # Remove newlines within the paragraph and convert to single line
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    # Count the # characters to determine heading level
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break
    
    # Extract heading text (everything after the # chars and space)
    heading_text = block[heading_level + 1:]
    
    # Parse inline markdown in heading text
    children = text_to_children(heading_text)
    tag = f"h{heading_level}"
    return ParentNode(tag, children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    # Remove the opening and closing ``` lines
    lines = block.split("\n")
    
    # Remove first line (opening ```) and last line (closing ```)
    code_lines = lines[1:-1]
    code_text = "\n".join(code_lines)
    
    # Add trailing newline to preserve structure before closing ```
    # This handles the case where content ends with newline before closing ```
    if len(lines) > 2:  # More than just the opening and closing ```
        code_text += "\n"
    elif len(code_lines) == 0:
        # Empty code block - add a single newline
        code_text = "\n"
    
    # Code blocks should NOT parse inline markdown
    # Create a text node with the raw code and convert to HTML
    code_leaf = LeafNode("code", code_text)
    pre_node = ParentNode("pre", [code_leaf])
    return pre_node


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    # Each line starts with >, remove the > and optional space
    lines = block.split("\n")
    quote_lines = []
    
    for line in lines:
        # Remove the leading >
        if line.startswith(">"):
            line = line[1:]
        # Remove leading space if present
        if line.startswith(" "):
            line = line[1:]
        quote_lines.append(line)
    
    # Join lines and parse inline markdown
    quote_text = " ".join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        # Allow empty list items like "-" as well as "- item" and "-\titem".
        stripped = line.strip()

        if stripped == "-":
            item_text = ""
        elif stripped.startswith("- "):
            item_text = stripped[2:]
        elif stripped.startswith("-\t"):
            item_text = stripped[2:]
        elif stripped.startswith("-"):
            # Fallback for malformed/edge cases that still reached this function.
            item_text = stripped[1:].strip()
        else:
            # Shouldn't happen if block_type is correct, but handle gracefully.
            item_text = stripped
        
        children = text_to_children(item_text)
        list_item = ParentNode("li", children)
        list_items.append(list_item)
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        # Remove the "N. " prefix (find the period and space)
        period_index = line.index(".")
        # Skip the period and the space after it
        item_text = line[period_index + 2:] if period_index + 2 < len(line) else ""
        children = text_to_children(item_text)
        list_item = ParentNode("li", children)
        list_items.append(list_item)
    
    return ParentNode("ol", list_items)