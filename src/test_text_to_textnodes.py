import unittest
from split_nodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_basic_example(self):
        """Test the example from the requirements"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        """Test with plain text, no markdown"""
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_bold_only(self):
        """Test with only bold text"""
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_italic_only(self):
        """Test with only italic text"""
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_code_only(self):
        """Test with only code text"""
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_image_only(self):
        """Test with only an image"""
        text = "![alt text](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_link_only(self):
        """Test with only a link"""
        text = "[link text](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("link text", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_bold(self):
        """Test with multiple bold sections"""
        text = "**bold1** and **bold2** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_bold_and_italic(self):
        """Test with both bold and italic"""
        text = "This is **bold** and _italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_bold_and_code(self):
        """Test with both bold and code"""
        text = "This is **bold** and `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_all_formatting(self):
        """Test with all formatting types"""
        text = "**bold** _italic_ `code` ![image](url) [link](url)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_empty_string(self):
        """Test with empty string"""
        text = ""
        nodes = text_to_textnodes(text)
        # Empty string produces an empty list (split_nodes_delimiter filters empty parts)
        expected = []
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_images(self):
        """Test with multiple images"""
        text = "First ![img1](url1) then ![img2](url2)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" then ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_links(self):
        """Test with multiple links"""
        text = "First [link1](url1) then [link2](url2)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" then ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_complex_urls(self):
        """Test with complex URLs in links and images"""
        text = "![alt](https://example.com/img.jpg?size=large) [text](https://example.com/page?id=1&sort=date)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("alt", TextType.IMAGE, "https://example.com/img.jpg?size=large"),
            TextNode(" ", TextType.TEXT),
            TextNode("text", TextType.LINK, "https://example.com/page?id=1&sort=date"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_code_with_special_chars(self):
        """Test code block with special characters"""
        text = "Use `const x = 42` in your code"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("const x = 42", TextType.CODE),
            TextNode(" in your code", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_consecutive_bold_italic(self):
        """Test consecutive bold and italic"""
        text = "**bold**_italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_link_with_anchor(self):
        """Test link with anchor fragment"""
        text = "Go to [section](https://example.com#intro)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Go to ", TextType.TEXT),
            TextNode("section", TextType.LINK, "https://example.com#intro"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_relative_link(self):
        """Test with relative links"""
        text = "Check [this page](/about) out"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("this page", TextType.LINK, "/about"),
            TextNode(" out", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_bold_and_image_and_link(self):
        """Test with bold, image, and link"""
        text = "**important** ![image](img.jpg) [click here](url.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("important", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.jpg"),
            TextNode(" ", TextType.TEXT),
            TextNode("click here", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiline(self):
        """Test with multiline text"""
        text = "First line **bold**\nSecond line _italic_\nThird line `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("First line ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("\nSecond line ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("\nThird line ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_emphasis_in_emphasis(self):
        """Test that nested delimiters don't create nested formatting"""
        # Note: Our parser applies delimiters sequentially to TEXT nodes only.
        # Non-TEXT nodes (like BOLD) are not further split by subsequent delimiters.
        text = "This **has _both_ styles** here"
        nodes = text_to_textnodes(text)
        # The ** is processed first, creating a BOLD node
        # Then _ is processed, but it only affects TEXT nodes, not the BOLD node
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("has _both_ styles", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_link_with_image_alt_text(self):
        """Test that image alt text is correctly parsed"""
        text = "Image with ![multiple words as alt](url.jpg)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Image with ", TextType.TEXT),
            TextNode("multiple words as alt", TextType.IMAGE, "url.jpg"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_complex_sentence(self):
        """Test complex sentence with mixed formatting"""
        text = "Please visit [our site](https://example.com) and read the **documentation** or check out our _blog_."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Please visit ", TextType.TEXT),
            TextNode("our site", TextType.LINK, "https://example.com"),
            TextNode(" and read the ", TextType.TEXT),
            TextNode("documentation", TextType.BOLD),
            TextNode(" or check out our ", TextType.TEXT),
            TextNode("blog", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_image_at_start(self):
        """Test with image at the start"""
        text = "![header](img.jpg) followed by text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("header", TextType.IMAGE, "img.jpg"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_link_at_end(self):
        """Test with link at the end"""
        text = "Text followed by [link](url.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text followed by ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()
