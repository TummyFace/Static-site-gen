import unittest
from block_type import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        """Test extracting a simple h1 header"""
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_extract_title_with_content(self):
        """Test extracting h1 header with content after it"""
        markdown = "# Welcome to My Static Site\n\nThis is some content."
        self.assertEqual(extract_title(markdown), "Welcome to My Static Site")
    
    def test_extract_title_with_whitespace(self):
        """Test extracting h1 header with extra whitespace"""
        markdown = "#   Hello   \n\nContent"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_extract_title_no_h1_header(self):
        """Test that exception is raised when no h1 header exists"""
        markdown = "## Subtitle\n### Another Title\nSome content"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found")
    
    def test_extract_title_h1_not_first(self):
        """Test extracting h1 header when it's not the first line"""
        markdown = "Some content\n# Main Title\nMore content"
        self.assertEqual(extract_title(markdown), "Main Title")
    
    def test_extract_title_empty_string(self):
        """Test that exception is raised for empty string"""
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found")
    
    def test_extract_title_only_hash(self):
        """Test that a line with only # doesn't match"""
        markdown = "#\nNo valid h1"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == '__main__':
    unittest.main()
