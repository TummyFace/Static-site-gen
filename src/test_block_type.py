import unittest
from block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    # Heading Tests
    def test_block_to_block_type_heading_level_1(self):
        """Test heading level 1"""
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_level_2(self):
        """Test heading level 2"""
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_level_3(self):
        """Test heading level 3"""
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_level_4(self):
        """Test heading level 4"""
        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_level_5(self):
        """Test heading level 5"""
        block = "##### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_level_6(self):
        """Test heading level 6"""
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_invalid_heading_level_7(self):
        """Test 7 hashes is not a heading"""
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_heading_no_space(self):
        """Test heading without space after # is not a heading"""
        block = "#This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_only_hashes(self):
        """Test heading with only hashes and space"""
        block = "## "
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_hash_in_paragraph(self):
        """Test hash not at start of line"""
        block = "This is text with # in the middle"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Code Block Tests
    def test_block_to_block_type_code_block_simple(self):
        """Test simple code block"""
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_with_language(self):
        """Test code block with language specifier"""
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_multiline(self):
        """Test multiline code block"""
        block = "```\ndef hello():\n    print('world')\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_block_with_backticks_inside(self):
        """Test code block containing single backticks"""
        block = "```\nsome `code` here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_invalid_code_block_only_start(self):
        """Test code block with only opening backticks"""
        block = "```\nprint('hello')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_code_block_only_end(self):
        """Test code block with only closing backticks"""
        block = "print('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_code_block_backticks_in_middle(self):
        """Test backticks in middle of paragraph"""
        block = "This has ``` backticks in it"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block_empty(self):
        """Test empty code block"""
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # Quote Block Tests
    def test_block_to_block_type_quote_single_line(self):
        """Test single line quote"""
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_multiple_lines(self):
        """Test multiline quote"""
        block = "> This is a quote\n> On multiple lines\n> With more text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_without_space_after_gt(self):
        """Test quote without space after >"""
        block = ">This is a quote without space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_with_mixed_spacing(self):
        """Test quote with mixed spacing"""
        block = "> Quote with space\n>Quote without space\n> Another with space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_invalid_quote_missing_one_gt(self):
        """Test quote missing > on one line"""
        block = "> This is a quote\nThis line is missing the >\n> Back to quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_with_special_chars(self):
        """Test quote with special characters"""
        block = "> Quote with **bold** and _italic_"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_only_gt(self):
        """Test quote with only >"""
        block = ">"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    # Unordered List Tests
    def test_block_to_block_type_unordered_list_single_item(self):
        """Test single item unordered list"""
        block = "- Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_multiple_items(self):
        """Test multiple item unordered list"""
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_with_formatting(self):
        """Test unordered list with markdown formatting"""
        block = "- **Bold** item\n- _Italic_ item\n- `code` item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_empty_items(self):
        """Test unordered list with items that have minimal content"""
        block = "- \n- Item\n- "
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_invalid_unordered_list_no_space(self):
        """Test invalid unordered list missing space after -"""
        block = "-Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_unordered_list_mixed(self):
        """Test mixed list markers"""
        block = "- Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_long_items(self):
        """Test unordered list with long items"""
        block = "- This is a very long item with lots of text\n- Another long item with **bold** and more content"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    # Ordered List Tests
    def test_block_to_block_type_ordered_list_single_item(self):
        """Test single item ordered list"""
        block = "1. Item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_multiple_items(self):
        """Test multiple item ordered list"""
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_many_items(self):
        """Test ordered list with many items"""
        block = "1. First\n2. Second\n3. Third\n4. Fourth\n5. Fifth\n6. Sixth\n7. Seventh\n8. Eighth\n9. Ninth\n10. Tenth"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_with_formatting(self):
        """Test ordered list with markdown formatting"""
        block = "1. **Bold** item\n2. _Italic_ item\n3. `code` item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_list_starts_at_2(self):
        """Test invalid ordered list starting at 2"""
        block = "2. Item 1\n3. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list_wrong_sequence(self):
        """Test invalid ordered list with wrong sequence"""
        block = "1. Item 1\n3. Item 3\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list_no_space(self):
        """Test invalid ordered list missing space after period"""
        block = "1.Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list_missing_period(self):
        """Test invalid ordered list missing period"""
        block = "1 Item 1\n2 Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_empty_items(self):
        """Test ordered list with empty items"""
        block = "1. \n2. Item\n3. "
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_list_resets(self):
        """Test invalid ordered list that resets numbering"""
        block = "1. Item 1\n2. Item 2\n1. Item 1 again"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Paragraph Tests
    def test_block_to_block_type_paragraph_simple(self):
        """Test simple paragraph"""
        block = "This is just a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_formatting(self):
        """Test paragraph with markdown formatting"""
        block = "This is a paragraph with **bold** and _italic_ and `code`"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiline(self):
        """Test multiline paragraph"""
        block = "This is line 1\nThis is line 2\nThis is line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_special_chars(self):
        """Test paragraph with special characters"""
        block = "This has !@#$%^&*() in it"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_links_and_images(self):
        """Test paragraph with links and images"""
        block = "Check [this](url) and ![alt](img.jpg)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_starting_with_number(self):
        """Test paragraph starting with number but not ordered list format"""
        block = "100 is a lot of items, not 1. like an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_list_like_content(self):
        """Test paragraph that looks like list but isn't"""
        block = "- This is not a list because this line\ndoesn't start with -"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # Edge Cases
    def test_block_to_block_type_empty_like_line(self):
        """Test block that's essentially empty"""
        block = " "
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_single_character(self):
        """Test single character block"""
        block = "a"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unicode_text(self):
        """Test block with unicode characters"""
        block = "Hello 世界 🌍"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unicode_list(self):
        """Test unicode in list"""
        block = "- Item 世界\n- Item 🌍"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_complex_heading_content(self):
        """Test heading with complex content"""
        block = "## This heading has **bold** and _italic_ and `code`"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code_with_unusual_language(self):
        """Test code block with unusual language identifier"""
        block = "```lisp\n(defn hello [] \"world\")\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_ordered_list_double_digit_items(self):
        """Test ordered list progressing through double digits"""
        items = "\n".join([f"{i}. Item {i}" for i in range(1, 12)])
        block = items
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_quote_with_empty_lines(self):
        """Test quote where empty line has just >"""
        block = "> First line\n>\n> Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_mixed_symbols_not_list(self):
        """Test text with mixed list-like symbols"""
        block = "- bullet here\n1. not continuing the pattern"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
