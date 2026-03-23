import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_basic_title(self):
        markdown = "# Hello World\nSome content"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_title_with_leading_whitespace(self):
        markdown = "\n\n# My Title\nSome text"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_no_title_heading_raises(self):
        markdown = "No heading here\nJust text"
        with self.assertRaises(Exception) as ctx:
            extract_title(markdown)
        self.assertIn("no title heading", str(ctx.exception))

    def test_empty_string_raises(self):
        markdown = ""
        with self.assertRaises(Exception) as ctx:
            extract_title(markdown)
        self.assertIn("no text", str(ctx.exception))

    def test_whitespace_only_raises(self):
        markdown = "   \n\n  "
        with self.assertRaises(Exception) as ctx:
            extract_title(markdown)
        self.assertIn("no text", str(ctx.exception))

    def test_h2_heading_raises(self):
        markdown = "## Not a title\nContent"
        with self.assertRaises(Exception) as ctx:
            extract_title(markdown)
        self.assertIn("no title heading", str(ctx.exception))

    def test_title_only_no_body(self):
        markdown = "# Just a Title"