def markdown_to_blocks(markdown):
    """
    Convert a markdown document into a list of block strings.
    
    Blocks are separated by double newlines (\\n\\n). Each block is stripped
    of leading and trailing whitespace, and empty blocks are removed.
    
    Args:
        markdown: Raw markdown string representing a full document
        
    Returns:
        List of block strings
    """
    # Split on double newlines
    blocks = markdown.split("\n\n")
    
    # Strip whitespace and filter out empty blocks
    filtered_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:  # Only include non-empty blocks
            filtered_blocks.append(stripped)
    
    return filtered_blocks
