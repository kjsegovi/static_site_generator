import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_no_tag_raises(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_multiple_children(self):
        parent_node = ParentNode("div", [
            LeafNode("b", "bold"),
            LeafNode("i", "italic"),
            LeafNode("span", "normal"),
        ])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>bold</b><i>italic</i><span>normal</span></div>"
        )

    def test_parent_with_props(self):
        child_node = LeafNode("p", "Hello")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        html = parent_node.to_html()
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertIn("<p>Hello</p>", html)

    def test_deeply_nested(self):
        parent_node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode("b", "deep")
                ])
            ])
        ])
        self.assertEqual(
            parent_node.to_html(),
            "<div><section><p><b>deep</b></p></section></div>"
        )

    def test_parent_mixed_leaf_and_parent_children(self):
        parent_node = ParentNode("div", [
            LeafNode("span", "first"),
            ParentNode("p", [LeafNode("b", "bold text")]),
            LeafNode("span", "last"),
        ])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><p><b>bold text</b></p><span>last</span></div>"
        )



if __name__ == "__main__":
    unittest.main()


"""
HTMLNode(p, This is a paragraph, None, None) 
HTMLNode(p, This is a paragraph, None, None)

"""
