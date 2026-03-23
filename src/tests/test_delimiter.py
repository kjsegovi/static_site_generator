from delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType
import unittest

class TestSplitNodesLink(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold phrase** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]

    def test_multiple_delimited_sections(self):
        node = TextNode("One `code` and another `block` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [
            TextNode("One ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("block", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [TextNode("already bold", TextType.BOLD)]

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has a `broken delimiter", TextType.TEXT)
        try:
            split_nodes_delimiter([node], "`", TextType.CODE)
            assert False, "Expected an exception to be raised"
        except Exception:
            pass

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_single_link(self):
        node = TextNode(
            "Click [here](https://www.google.com) for more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINKS, "https://www.google.com"),
                TextNode(" for more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_two_links(self):
        node = TextNode(
            "Visit [Google](https://www.google.com) and [GitHub](https://www.github.com) today",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Google", TextType.LINKS, "https://www.google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINKS, "https://www.github.com"),
                TextNode(" today", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode(
            "[Home](https://example.com) is where it starts",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Home", TextType.LINKS, "https://example.com"),
                TextNode(" is where it starts", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode(
            "Check out [my site](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("my site", TextType.LINKS, "https://example.com"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("Just plain text here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Just plain text here", TextType.TEXT)],
            new_nodes,
        )


class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        node = TextNode(
            "Here is an ![alt text](https://i.imgur.com/abc.png) in text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGES, "https://i.imgur.com/abc.png"),
                TextNode(" in text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![logo](https://example.com/logo.png) welcome to the site",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGES, "https://example.com/logo.png"),
                TextNode(" welcome to the site", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "See the photo ![sunset](https://example.com/sunset.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("See the photo ", TextType.TEXT),
                TextNode("sunset", TextType.IMAGES, "https://example.com/sunset.jpg"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("No images in this text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("No images in this text", TextType.TEXT)],
            new_nodes,
        )

    def test_all_markdown_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_plain_text_only(self):
        text = "Just some plain text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("Just some plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_bold_and_italic(self):
        text = "A **bold** and _italic_ sentence"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" sentence", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_only(self):
        text = "![photo](https://example.com/photo.png)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("photo", TextType.IMAGES, "https://example.com/photo.png"),
            ],
            new_nodes,
        )

    def test_link_only(self):
        text = "[click here](https://example.com)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("click here", TextType.LINKS, "https://example.com"),
            ],
            new_nodes,
        )
