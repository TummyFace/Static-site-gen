from enum import Enum


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block: A single block of markdown text (leading/trailing whitespace stripped)
        
    Returns:
        BlockType enum value representing the block type
    """
    lines = block.split("\n")
    
    # Check for heading (1-6 # chars followed by space)
    if lines[0].startswith("#"):
        heading_level = 0
        for char in lines[0]:
            if char == "#":
                heading_level += 1
            else:
                break
        # Must be 1-6 # chars and followed by a space
        if 1 <= heading_level <= 6 and len(lines[0]) > heading_level and lines[0][heading_level] == " ":
            return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (all lines start with >)
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    # Check for unordered list
    # Allows "- item", "-\titem", and bare "-" for empty list items
    is_unordered_list = True
    for line in lines:
        stripped = line.strip()
        if not (stripped == "-" or stripped.startswith("- ") or stripped.startswith("-\t")):
            is_unordered_list = False
            break

    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with number. space, incrementing by 1)
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_number = i + 1
        expected_start = f"{expected_number}. "
        if not line.startswith(expected_start):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def extract_title(markdown):
    """
    Extract the h1 header from a markdown file.
    
    Args:
        markdown: The markdown content as a string
        
    Returns:
        The text of the h1 header (without the # and surrounding whitespace)
        
    Raises:
        Exception: If no h1 header is found
    """
    lines = markdown.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            # Remove the # and any leading/trailing whitespace
            return line.strip()[1:].strip()
    raise Exception("No h1 header found")
