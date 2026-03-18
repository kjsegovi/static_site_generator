from textnode import TextNode, TextType


def main():
    link = TextType.LINKS
    textnode = TextNode("This is anchor text", link, "https://boot.dev")
    print(textnode)


if __name__ == "__main__":
    main()
