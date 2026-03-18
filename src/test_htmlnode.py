import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("h1", "This is a heading")
        self.assertNotEqual(node, node2)

    def test_children(self):
        node = HTMLNode("body", None, [HTMLNode("p", "This is a body paragraph")])
        node2 = HTMLNode("body", None, [HTMLNode("p", "This is a body paragraph")])
        self.assertEqual(node, node2)

    def test_props(self):
        node = HTMLNode("img", None, None, {"href": "~/abc.png"})
        node2 = HTMLNode("img", None, None, {"href": "~/abc.png"})
        self.assertEqual(node, node2)

    # some tests for leaf node
    def test_leaf_eq(self):
        node = LeafNode("p", "Hello World!")
        node2 = LeafNode("p", "Hello World!")
        self.assertEqual(node, node2)

    def test_leaf_not_eq(self):
        node = LeafNode("p", "Hello World!")
        node2 = LeafNode("a", "Goodbye World!")
        self.assertNotEqual(node, node2)

    def test_leaf_props(self):
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        # print(node)
        self.assertEqual(node, node2)

    def test_leaf_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        test = node.to_html()
        actual = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(test, actual)


if __name__ == "__main__":
    unittest.main()


"""
HTMLNode(p, This is a paragraph, None, None) 
HTMLNode(p, This is a paragraph, None, None)

"""
