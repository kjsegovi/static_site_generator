import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is not a similar text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("https://www.boot.dev", TextType.LINKS, True)
        node2 = TextNode("https://www.boot.dev", TextType.LINKS, True)
        self.assertEqual(node, node2)

    def test_dif_url(self):
        node = TextNode("https://www.google.com", TextType.LINKS, True)
        node2 = TextNode("https://www.boot.dev", TextType.LINKS, True)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
