import unittest
from markdown_to_html import markdown_to_html_node


class TestHTMLConversionExtra(unittest.TestCase):

    def test_headings(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

    def test_heading_levels(self):
        md = """# H1

## H2

### H3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "## This is **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is <b>bold</b> heading</h2></div>",
        )

    def test_unordered_list(self):
        md = """- Item one
- Item two
- Item three"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First
2. Second
3. Third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_blockquote(self):
        md = ">This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>",
        )

    def test_list_with_inline_markdown(self):
        md = """- This is **bold**
- This is _italic_
- This has `code`"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bold</b></li><li>This is <i>italic</i></li><li>This has <code>code</code></li></ul></div>",
        )

    def test_full_document(self):
        md = """# My Document

This is a paragraph with **bold** and _italic_ text.

- List item one
- List item two

> A wise quote

```
some code here
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>My Document</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>", html)
        self.assertIn("<ul><li>List item one</li><li>List item two</li></ul>", html)
        self.assertIn("<blockquote>A wise quote</blockquote>", html)
        self.assertIn("<pre><code>some code here\n</code></pre>", html)
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))

