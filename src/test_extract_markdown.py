import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images_single_image(self):
        """Test extracting a single markdown image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple_images(self):
        """Test extracting multiple markdown images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_images(self):
        """Test with text containing no images"""
        text = "This is plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt_text(self):
        """Test image with empty alt text"""
        matches = extract_markdown_images("![](https://i.imgur.com/test.png)")
        self.assertListEqual([("", "https://i.imgur.com/test.png")], matches)

    def test_extract_markdown_images_complex_url(self):
        """Test image with complex URL containing query parameters"""
        text = "![alt](https://example.com/image.jpg?size=large&format=webp)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("alt", "https://example.com/image.jpg?size=large&format=webp")], matches
        )

    def test_extract_markdown_images_with_surrounding_text(self):
        """Test image extraction from text with various surrounding content"""
        text = "Start text ![image1](url1) middle text ![image2](url2) end text"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image1", "url1"), ("image2", "url2")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_single_link(self):
        """Test extracting a single markdown link"""
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple_links(self):
        """Test extracting multiple markdown links"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_links(self):
        """Test with text containing no links"""
        text = "This is plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_relative_url(self):
        """Test link with relative URL"""
        text = "Check out [this page](/about)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this page", "/about")], matches)

    def test_extract_markdown_links_with_fragment(self):
        """Test link with URL fragment"""
        text = "Go to [section](https://example.com#section)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("section", "https://example.com#section")], matches)

    def test_extract_markdown_links_complex_anchor_text(self):
        """Test link with special characters in anchor text"""
        text = "[Click here!!!](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Click here!!!", "https://example.com")], matches)

    def test_extract_markdown_links_with_surrounding_text(self):
        """Test link extraction from text with various surrounding content"""
        text = "Start [link1](url1) middle [link2](url2) end"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)


class TestExtractMarkdownMixed(unittest.TestCase):
    def test_extract_both_images_and_links_in_same_text(self):
        """Test that links function doesn't match images"""
        text = "![image](img.jpg) and [link](url.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertListEqual([("image", "img.jpg")], images)
        self.assertListEqual([("link", "url.com")], links)

    def test_links_dont_match_images(self):
        """Verify that extract_markdown_links doesn't match image syntax"""
        text = "![this should not match](https://example.com/image.jpg)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_images_dont_match_links(self):
        """Verify that extract_markdown_images doesn't match link syntax"""
        text = "[this should not match](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()
