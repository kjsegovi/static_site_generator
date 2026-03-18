class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""

        html = ""

        for prop in self.props:
            html += f"{prop}={self.props[prop]} "

        return html

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if not value:
            raise ValueError("All leaf nodes must have a value")
        super().__init__(tag, value, None ,props)

    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        else:
            front_tag = f"<{self.tag}"
            back_tag = f"</{self.tag}>"
            props = ""
            for prop in self.props:
                props += f" {prop}=\"{self.props[prop]}\""

            front_tag += props + ">"

            return front_tag + self.value + back_tag
