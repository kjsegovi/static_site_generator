from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            node_list.append(old_node)
            continue

        delimit_count = old_node.text.count(delimiter)
        if delimit_count % 2 != 0:
            raise Exception(f"No closing {delimiter} found. Please double check.")

        split_nodes = old_node.text.split(delimiter)
        for i, text in enumerate(split_nodes):
            if i % 2 == 0:
                add_node = TextNode(text, TextType.TEXT)
            else:
                add_node = TextNode(text, text_type)
            node_list.append(add_node)

    return node_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_links(text)
        if not matches:
            node_list.append(node)
            continue
        text_matches = []
        i = 0
        parts = ['', text]
        for match in matches:
            parts = parts[1].split(f"[{match[0]}]({match[1]})")
            #print(parts)
            if parts[0]:
                text_node = TextNode(parts[0], TextType.TEXT)
                text_matches.append(text_node)
            link_node = TextNode(match[0], TextType.LINKS, match[1])
            text_matches.append(link_node)

        if parts[1]:
            text_node = TextNode(parts[1], TextType.TEXT)
            text_matches.append(text_node)

        # print(text_matches)
        node_list.extend(text_matches)
    # print(node_list)
    return node_list

def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_images(text)
        if not matches:
            node_list.append(node)
            continue
        text_matches = []
        i = 0
        parts = ['', text]
        for match in matches:
            parts = parts[1].split(f"![{match[0]}]({match[1]})")
            #print(parts)
            if parts[0]:
                text_node = TextNode(parts[0], TextType.TEXT)
                text_matches.append(text_node)
            link_node = TextNode(match[0], TextType.IMAGES, match[1])
            text_matches.append(link_node)

        if parts[1]:
            text_node = TextNode(parts[1], TextType.TEXT)
            text_matches.append(text_node)

        # print(text_matches)
        node_list.extend(text_matches)
    # print(node_list)
    return node_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

if __name__ == "__main__":
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    print(new_nodes)