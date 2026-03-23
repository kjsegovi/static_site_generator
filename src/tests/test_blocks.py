from blocks import markdown_to_blocks, block_to_block_type, BlockType
import unittest

class TestSplitNodesLink(unittest.TestCase):

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_only_whitespace_lines(self):
        md = "\n\n\t\n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block_no_splits(self):
        md = "Just a single paragraph with no blank lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with no blank lines"])

    def test_strips_leading_tabs_on_continuation_lines(self):
        md = "# Heading\n\nSome text\n\twith a tabbed continuation\n\t\tand double tabbed\n\nAnother block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Some text\nwith a tabbed continuation\nand double tabbed",
                "Another block",
            ],
        )

    def test_multiple_blank_lines_between_blocks(self):
        md = "Block one\n\n\n\nBlock two\n\n\n\n\nBlock three"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two", "Block three"])


    def test_heading_single_hash(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_six_hashes(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_code_block_multiline(self):
        self.assertEqual(block_to_block_type("```\nline 1\nline 2\n```"), BlockType.CODE)

    def test_code_block_missing_closing(self):
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)


    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> a quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)

    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        self.assertEqual(block_to_block_type("- one\n- two\n- three"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_is_not_list(self):
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. only item"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        self.assertEqual(block_to_block_type("2. starts at two"), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_order(self):
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)

    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text"), BlockType.PARAGRAPH)

    def test_paragraph_with_newlines(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)