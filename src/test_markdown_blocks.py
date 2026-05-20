import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        """Test the basic example from requirements"""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        """Test with a single block (no double newlines)"""
        md = "This is just a single block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just a single block"])

    def test_markdown_to_blocks_multiple_blocks(self):
        """Test with multiple blocks"""
        md = "Block 1\n\nBlock 2\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        """Test that leading and trailing whitespace is removed"""
        md = "   Block 1   \n\n   Block 2   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_empty_string(self):
        """Test with empty string"""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        """Test with only whitespace"""
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_excess_newlines(self):
        """Test with excessive newlines (more than double)"""
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        # Multiple newlines should create empty blocks that get filtered
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_tabs_and_spaces(self):
        """Test with mixed tabs and spaces"""
        md = "  \t  Block 1  \t  \n\n  \t  Block 2  \t  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_with_heading(self):
        """Test with markdown heading"""
        md = "# This is a heading\n\nThis is a paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# This is a heading", "This is a paragraph"])

    def test_markdown_to_blocks_with_code_block(self):
        """Test with code block containing multiple lines"""
        md = """
```python
def hello():
    print("world")
```

This is regular text
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "```python\ndef hello():\n    print(\"world\")\n```",
                "This is regular text",
            ],
        )

    def test_markdown_to_blocks_with_list(self):
        """Test with list blocks"""
        md = """
- Item 1
- Item 2
- Item 3

Next paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- Item 1\n- Item 2\n- Item 3",
                "Next paragraph",
            ],
        )

    def test_markdown_to_blocks_with_ordered_list(self):
        """Test with ordered list"""
        md = "1. First\n2. Second\n3. Third\n\nParagraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["1. First\n2. Second\n3. Third", "Paragraph"])

    def test_markdown_to_blocks_with_blockquote(self):
        """Test with blockquote"""
        md = "> This is a quote\n\nThis is not"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["> This is a quote", "This is not"])

    def test_markdown_to_blocks_preserves_internal_newlines(self):
        """Test that single newlines within blocks are preserved"""
        md = """Line 1
Line 2
Line 3

Block 2"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line 1\nLine 2\nLine 3", "Block 2"],
        )

    def test_markdown_to_blocks_only_double_newlines(self):
        """Test that only double newlines separate blocks"""
        md = "Block 1\nNot a block separator\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Block 1\nNot a block separator", "Block 2"],
        )

    def test_markdown_to_blocks_complex_document(self):
        """Test with complex markdown document"""
        md = """# Main Heading

This is an introductory paragraph with **bold** and _italic_ text.

## Subheading

Here's a list:
- Item one
- Item two
- Item three

And here's some code:
```
code here
```

Final paragraph with a [link](https://example.com)."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Main Heading",
                "This is an introductory paragraph with **bold** and _italic_ text.",
                "## Subheading",
                "Here's a list:\n- Item one\n- Item two\n- Item three",
                "And here's some code:\n```\ncode here\n```",
                "Final paragraph with a [link](https://example.com).",
            ],
        )

    def test_markdown_to_blocks_newline_at_start(self):
        """Test with leading newline"""
        md = "\n\nBlock 1\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_newline_at_end(self):
        """Test with trailing newlines"""
        md = "Block 1\n\nBlock 2\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_newline_at_both_ends(self):
        """Test with leading and trailing newlines"""
        md = "\n\nBlock 1\n\nBlock 2\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_single_line_multiple_spaces(self):
        """Test single line with multiple spaces within"""
        md = "This   has   multiple   spaces"
        blocks = markdown_to_blocks(md)
        # Internal spaces should be preserved
        self.assertEqual(blocks, ["This   has   multiple   spaces"])

    def test_markdown_to_blocks_mixed_formatting(self):
        """Test block with mixed formatting"""
        md = "**bold** _italic_ `code` [link](url) ![image](img.png)\n\nNext block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["**bold** _italic_ `code` [link](url) ![image](img.png)", "Next block"],
        )

    def test_markdown_to_blocks_empty_blocks_between_content(self):
        """Test with empty blocks between content blocks"""
        md = "Block 1\n\n\n\n\n\nBlock 2\n\n\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

    def test_markdown_to_blocks_paragraph_with_line_breaks(self):
        """Test paragraph that spans multiple lines but is one block"""
        md = """This paragraph spans
multiple lines
but is still one block

This is a different block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This paragraph spans\nmultiple lines\nbut is still one block",
                "This is a different block",
            ],
        )

    def test_markdown_to_blocks_unicode_characters(self):
        """Test with unicode characters"""
        md = "Hello 世界\n\nΓειά σας κόσμε"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Hello 世界", "Γειά σας κόσμε"])

    def test_markdown_to_blocks_special_characters(self):
        """Test with special characters"""
        md = "!@#$%^&*()\n\n<>?:\"{}|"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["!@#$%^&*()", "<>?:\"{}|"])

    def test_markdown_to_blocks_very_long_block(self):
        """Test with very long block"""
        long_line = "This is a very long line of text " * 50
        md = f"{long_line}\n\nShort block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [long_line.strip(), "Short block"])

    def test_markdown_to_blocks_multiline_list(self):
        """Test list that might have internal formatting"""
        md = """- Item **1**
- Item _2_
- Item `3`

Next block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- Item **1**\n- Item _2_\n- Item `3`", "Next block"],
        )


if __name__ == "__main__":
    unittest.main()
