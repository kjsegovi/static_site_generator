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
            if self.props:
                for prop in self.props:
                    props += f" {prop}=\"{self.props[prop]}\""

            front_tag += props + ">"

            return front_tag + self.value + back_tag

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props}"

    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        ):
            return True
        else:
            return False

    def to_html(self):
        if not self.tag:
            raise ValueError("The Parent Node does not have a tag")
        if not self.children:
            raise ValueError(f"The children list is empty")

        start_tag = f"<{self.tag}"
        props = ""
        if self.props:
            for prop in self.props:
                props += f" {prop}=\"{self.props[prop]}\""
        end_tag = f"</{self.tag}>"

        child_tags = ""
        for child in self.children:
            # print(f"a child: {child}")
            child_tags += child.to_html()

        return start_tag + props + ">" + child_tags + end_tag