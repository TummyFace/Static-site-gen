import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        """Test converting paragraphs with inline markdown"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        """Test code blocks don't parse inline markdown"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_level_1(self):
        """Test h1 heading"""
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_heading_with_inline_markdown(self):
        """Test heading with bold and italic"""
        md = "## This heading has **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This heading has <b>bold</b> and <i>italic</i></h2></div>",
        )

    def test_multiple_headings(self):
        """Test multiple headings with different levels"""
        md = """# Level 1

## Level 2

### Level 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Level 1</h1><h2>Level 2</h2><h3>Level 3</h3></div>",
        )

    def test_quote_single_line(self):
        """Test single line quote"""
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_quote_multiple_lines(self):
        """Test multiline quote"""
        md = """> This is a quote
> On multiple lines
> With more text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote On multiple lines With more text</blockquote></div>",
        )

    def test_quote_with_inline_markdown(self):
        """Test quote with bold and italic"""
        md = "> This quote has **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This quote has <b>bold</b> and <i>italic</i></blockquote></div>",
        )

    def test_unordered_list_simple(self):
        """Test simple unordered list"""
        md = """- Item 1
- Item 2
- Item 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        """Test unordered list with inline markdown"""
        md = """- **Bold** item
- _Italic_ item
- `code` item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>Bold</b> item</li><li><i>Italic</i> item</li><li><code>code</code> item</li></ul></div>",
        )

    def test_unordered_list_with_links(self):
        """Test unordered list with links"""
        md = """- [Link 1](https://example.com)
- [Link 2](https://boot.dev)"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li><a href="https://example.com">Link 1</a></li><li><a href="https://boot.dev">Link 2</a></li></ul></div>',
        )

    def test_ordered_list_simple(self):
        """Test simple ordered list"""
        md = """1. First
2. Second
3. Third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        """Test ordered list with inline markdown"""
        md = """1. **First** item
2. _Second_ item
3. `Third` item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>First</b> item</li><li><i>Second</i> item</li><li><code>Third</code> item</li></ol></div>",
        )

    def test_complex_document(self):
        """Test complex document with multiple block types"""
        md = """# Main Heading

This is a paragraph with **bold** text.

## Subheading

- List item 1
- List item 2

> A quote here

1. First ordered
2. Second ordered"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Main Heading</h1>"
            "<p>This is a paragraph with <b>bold</b> text.</p>"
            "<h2>Subheading</h2>"
            "<ul><li>List item 1</li><li>List item 2</li></ul>"
            "<blockquote>A quote here</blockquote>"
            "<ol><li>First ordered</li><li>Second ordered</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_code_block_with_language(self):
        """Test code block with language specifier"""
        md = """```python
def hello():
    print("world")
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><pre><code>def hello():\n    print("world")\n</code></pre></div>',
        )

    def test_code_block_empty(self):
        """Test empty code block"""
        md = "```\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>\n</code></pre></div>")

    def test_mixed_lists(self):
        """Test document with both ordered and unordered lists"""
        md = """- Unordered 1
- Unordered 2

1. Ordered 1
2. Ordered 2"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Unordered 1</li><li>Unordered 2</li></ul><ol><li>Ordered 1</li><li>Ordered 2</li></ol></div>",
        )

    def test_paragraph_with_links_and_images(self):
        """Test paragraph with links and images"""
        md = "Check [this](https://example.com) and ![alt text](image.jpg)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Check <a href="https://example.com">this</a> and <img src="image.jpg" alt="alt text" /></p></div>',
        )

    def test_heading_level_6(self):
        """Test h6 heading"""
        md = "###### This is level 6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h6>This is level 6</h6></div>")

    def test_single_paragraph(self):
        """Test single paragraph"""
        md = "Just a simple paragraph"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>Just a simple paragraph</p></div>")

    def test_all_formatting_in_paragraph(self):
        """Test paragraph with all inline formatting types"""
        md = "This has **bold**, _italic_, `code`, [link](url), and ![image](img.jpg)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn('<a href="url">link</a>', html)
        self.assertIn('<img src="img.jpg" alt="image" />', html)

    def test_code_block_with_backticks_inside(self):
        """Test code block with backticks in content"""
        md = "```\nCode with `backticks` inside\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("Code with `backticks` inside", html)

    def test_quote_without_space_after_gt(self):
        """Test quote without space after >"""
        md = """>Quote without space
>Another line"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote without space Another line</blockquote></div>",
        )

    def test_quote_mixed_spacing(self):
        """Test quote with mixed spacing after >"""
        md = """> Quote with space
>Quote without space"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote with space Quote without space</blockquote></div>",
        )

    def test_multiline_paragraph(self):
        """Test paragraph with multiple lines converted to single line"""
        md = """This is a paragraph
that spans multiple
lines in the markdown
but becomes one paragraph"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # All lines should be joined with spaces
        self.assertIn(
            "This is a paragraph that spans multiple lines in the markdown but becomes one paragraph",
            html,
        )

    def test_empty_markdown(self):
        """Test empty markdown string"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_only_whitespace(self):
        """Test markdown with only whitespace"""
        md = "\n\n   \n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_list_with_empty_items(self):
        """Test list items that are nearly empty"""
        md = """- 
- Item 2
- """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<li></li>", html)
        self.assertIn("<li>Item 2</li>", html)

    def test_heading_with_code(self):
        """Test heading with inline code"""
        md = "### Heading with `code` inside"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading with <code>code</code> inside</h3></div>",
        )

    def test_list_with_complex_items(self):
        """Test list with items containing multiple inline elements"""
        md = """- Item with **bold** and _italic_ and `code`
- Another [link](url) item
- Simple item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn('<a href="url">link</a>', html)

    def test_ordered_list_many_items(self):
        """Test ordered list with many items (double digit numbers)"""
        md = "\n".join([f"{i}. Item {i}" for i in range(1, 6)])
        node = markdown_to_html_node(md)
        html = node.to_html()
        for i in range(1, 6):
            self.assertIn(f"<li>Item {i}</li>", html)

    def test_paragraph_followed_by_quote(self):
        """Test paragraph followed by quote"""
        md = """This is a paragraph

> This is a quote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<p>This is a paragraph</p>", html)
        self.assertIn("<blockquote>This is a quote</blockquote>", html)

    def test_code_block_preserves_exact_formatting(self):
        """Test that code block preserves exact whitespace and formatting"""
        md = """```
def func():
    if True:
        return "indented"
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("def func():", html)
        self.assertIn("    if True:", html)
        self.assertIn('        return "indented"', html)

    def test_unicode_in_content(self):
        """Test unicode characters in content"""
        md = "Hello 世界 🌍"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("Hello 世界 🌍", html)

    def test_special_chars_in_content(self):
        """Test special HTML characters are preserved"""
        md = "This has <angle> brackets & special chars"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # The content should preserve these characters
        self.assertIn("This has <angle> brackets & special chars", html)


if __name__ == "__main__":
    unittest.main()
