from blocks import markdown_to_blocks, block_to_block_type, BlockType
from delimiter import text_to_textnodes
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = html_node_from_type(block, block_type)
        html_nodes.append(html_node)
    return ParentNode("div", html_nodes)

def html_node_from_type(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        block = block.replace("\n", " ")
        children = text_to_children(block)
        return ParentNode("p", children)
    elif block_type == BlockType.HEADING:
        total = 0
        for char in block:
            if char == "#":
                total += 1
            else:
                break
        block = block[total+1:]
        children = text_to_children(block)
        return ParentNode(f"h{total}", children)
    elif block_type == BlockType.CODE:
        block = block.removeprefix("```").removesuffix("```").lstrip("\n")
        text_node = TextNode(block, TextType.TEXT)
        code_leaf = text_node_to_html_node(text_node)
        code_node = ParentNode("code", [code_leaf])
        return ParentNode("pre", [code_node])
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        stripped = [line.lstrip("> ") for line in lines]
        joined = " ".join(stripped)
        children = text_to_children(joined)
        return ParentNode("blockquote", children)
    elif block_type == BlockType.UNORDERED_LIST:
        item_list = block.split("\n")
        all_items = []
        for line in item_list:
            new_line = line[2:]
            li_children = text_to_children(new_line)
            li_node = ParentNode("li", li_children)
            all_items.append(li_node)
        return ParentNode("ul", all_items)
    elif block_type == BlockType.ORDERED_LIST:
        item_list = block.split("\n")
        all_items = []
        for i, line in enumerate(item_list):
            new_line = line[line.index(". ") + 2:]
            li_children = text_to_children(new_line)
            li_node = ParentNode("li", li_children)
            all_items.append(li_node)
        return ParentNode("ol", all_items)
    return None


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def main():
    pass


if __name__ == "__main__":
    main()
