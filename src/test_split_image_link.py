import unittest
from split_nodes import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images_single(self):
        """Test extracting a single image"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        """Test extracting multiple images"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        """Test with text containing no images"""
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_at_start(self):
        """Test image at the start of text"""
        node = TextNode(
            "![start image](https://example.com/start.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        """Test image at the end of text"""
        node = TextNode(
            "Text followed by ![end image](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("end image", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        """Test with only an image, no surrounding text"""
        node = TextNode(
            "![only image](https://example.com/only.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only image", TextType.IMAGE, "https://example.com/only.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt_text(self):
        """Test image with empty alt text"""
        node = TextNode(
            "Text with ![](https://example.com/noalt.png) empty alt",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/noalt.png"),
                TextNode(" empty alt", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_complex_url(self):
        """Test image with complex URL"""
        node = TextNode(
            "![alt](https://example.com/image.jpg?size=large&format=webp)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "alt",
                    TextType.IMAGE,
                    "https://example.com/image.jpg?size=large&format=webp",
                ),
            ],
            new_nodes,
        )

    def test_split_images_non_text_node_passthrough(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        node1 = TextNode("bold", TextType.BOLD)
        node2 = TextNode(
            "Text with ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        node3 = TextNode("code", TextType.CODE)
        
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_split_images_three_images(self):
        """Test with three images"""
        node = TextNode(
            "![1](url1) middle ![2](url2) more ![3](url3) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("1", TextType.IMAGE, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("2", TextType.IMAGE, "url2"),
                TextNode(" more ", TextType.TEXT),
                TextNode("3", TextType.IMAGE, "url3"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        """Test with consecutive images"""
        node = TextNode(
            "![img1](url1)![img2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_single(self):
        """Test extracting a single link"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        """Test extracting multiple links"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        """Test with text containing no links"""
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_at_start(self):
        """Test link at the start of text"""
        node = TextNode(
            "[start link](https://example.com/start) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start link", TextType.LINK, "https://example.com/start"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        """Test link at the end of text"""
        node = TextNode(
            "Text followed by [end link](https://example.com/end)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("end link", TextType.LINK, "https://example.com/end"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        """Test with only a link, no surrounding text"""
        node = TextNode(
            "[only link](https://example.com/only)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only link", TextType.LINK, "https://example.com/only"),
            ],
            new_nodes,
        )

    def test_split_links_relative_url(self):
        """Test link with relative URL"""
        node = TextNode(
            "Check out [this page](/about)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("this page", TextType.LINK, "/about"),
            ],
            new_nodes,
        )

    def test_split_links_with_fragment(self):
        """Test link with URL fragment"""
        node = TextNode(
            "Go to [section](https://example.com#section)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("section", TextType.LINK, "https://example.com#section"),
            ],
            new_nodes,
        )

    def test_split_links_complex_anchor_text(self):
        """Test link with special characters in anchor text"""
        node = TextNode(
            "[Click here!!!](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click here!!!", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_non_text_node_passthrough(self):
        """Test that non-TEXT nodes are passed through unchanged"""
        node1 = TextNode("bold", TextType.BOLD)
        node2 = TextNode(
            "Text with [link](https://example.com)",
            TextType.TEXT,
        )
        node3 = TextNode("code", TextType.CODE)
        
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_split_links_three_links(self):
        """Test with three links"""
        node = TextNode(
            "[1](url1) middle [2](url2) more [3](url3) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("1", TextType.LINK, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("2", TextType.LINK, "url2"),
                TextNode(" more ", TextType.TEXT),
                TextNode("3", TextType.LINK, "url3"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        """Test with consecutive links"""
        node = TextNode(
            "[link1](url1)[link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_with_query_params(self):
        """Test link with query parameters"""
        node = TextNode(
            "[search](https://example.com/search?q=test&sort=date)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "search",
                    TextType.LINK,
                    "https://example.com/search?q=test&sort=date",
                ),
            ],
            new_nodes,
        )

    def test_split_links_does_not_match_images(self):
        """Test that links don't match image syntax"""
        node = TextNode(
            "This ![image](url.jpg) is not a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_mixed_with_images_text(self):
        """Test links when image markdown text is present as literal text"""
        # Note: The actual image won't be processed by split_nodes_link,
        # but if there were an image and a link, the link should be found
        node = TextNode(
            "This has [a link](url) and text mentioning ![images](are cool)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # split_nodes_link should only find the [a link] part, not the ![images] part
        self.assertListEqual(
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "url"),
                TextNode(" and text mentioning ![images](are cool)", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesEdgeCases(unittest.TestCase):
    def test_split_images_and_links_together_images_first(self):
        """Test that split functions respect content boundaries"""
        # Create an image first, then try to split for links
        node = TextNode(
            "Image: ![alt](img.png) then link: [text](url.com)",
            TextType.TEXT,
        )
        # When we split for images, we should get images
        image_nodes = split_nodes_image([node])
        # Now test that those resulting nodes work with split_nodes_link
        link_nodes = split_nodes_link(image_nodes)
        
        # The result should have both images and links processed
        expected_images = [
            TextNode("Image: ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "img.png"),
            TextNode(" then link: [text](url.com)", TextType.TEXT),
        ]
        self.assertEqual(image_nodes, expected_images)
        
        # Now split for links
        link_nodes = split_nodes_link(image_nodes)
        # The [text](url.com) part should be converted to a link
        self.assertListEqual(
            [
                TextNode("Image: ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "img.png"),
                TextNode(" then link: ", TextType.TEXT),
                TextNode("text", TextType.LINK, "url.com"),
            ],
            link_nodes,
        )

    def test_split_empty_node_list(self):
        """Test with empty node list"""
        self.assertListEqual([], split_nodes_image([]))
        self.assertListEqual([], split_nodes_link([]))

    def test_split_images_multiline_text(self):
        """Test images in multiline text"""
        node = TextNode(
            "Line 1\n![image1](url1)\nLine 2\n![image2](url2)\nLine 3",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Line 1\n", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "url1"),
                TextNode("\nLine 2\n", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "url2"),
                TextNode("\nLine 3", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiline_text(self):
        """Test links in multiline text"""
        node = TextNode(
            "Line 1\n[link1](url1)\nLine 2\n[link2](url2)\nLine 3",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Line 1\n", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("\nLine 2\n", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode("\nLine 3", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
