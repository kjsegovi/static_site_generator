from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "link"
    IMAGES = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    tag = ""
    if text_node.text_type == TextType.TEXT:
        tag = None
    elif text_node.text_type == TextType.BOLD:
        tag = "b"
    elif text_node.text_type == TextType.ITALIC:
        tag = "i"
    elif text_node.text_type == TextType.CODE:
        tag = "code"
    elif text_node.text_type == TextType.LINKS:
        tag = "a"
    elif text_node.text_type == TextType.IMAGES:
        tag = "img"

    url = None
    if text_node.url:
        if tag == "img":
            url = {"src": text_node.url}
        else:
            url = {"href": text_node.url}
    html_node = LeafNode(tag, text_node.text, url)
    return html_node
