from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "bold"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    markdown_blocks = [re.sub(r"\n[ \t]+", "\n", b).strip() for b in markdown_blocks]
    string_blocks = [b for b in markdown_blocks if b != ""]

    return string_blocks

def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    elif re.match(r"```\n.*\n```", markdown, re.DOTALL):
        return BlockType.CODE
    elif markdown[0] == ">":
        return BlockType.QUOTE
    elif re.match(r"^(- .+\n)*- .+$", markdown):
        return BlockType.UNORDERED_LIST
    else:
        lines = markdown.split("\n")
        is_ordered = True
        for i, line in enumerate(lines, 1):
            if not line.startswith(f"{i}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH


if __name__ == "__main__":
    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
    blocks = markdown_to_blocks(md)
    print(blocks)