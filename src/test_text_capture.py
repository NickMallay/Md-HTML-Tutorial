import unittest
from textnode import *
from text_capture import *
from block_type import *
from main import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_delimiter(self):
        # Test with a single bold section
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_multiple_bold_sections(self):
        # Test with multiple bold sections
        node = TextNode("This has **two** bold **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        for i, node in enumerate(new_nodes):
            print(f"Node {i}: '{node.text}' (Type: {node.text_type})")

        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This has ")
        self.assertEqual(new_nodes[1].text, "two")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " bold ")
        self.assertEqual(new_nodes[3].text, "words")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_edge_cases_links(self):
        # Test with no links
        node = TextNode("This text has no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
        # Test with link at the beginning
        node = TextNode("[First link](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First link", TextType.LINK, "https://example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )
        
        # Test with link at the end
        node = TextNode("Text followed by [last link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text followed by ", TextType.TEXT),
                TextNode("last link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **bold** with a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        assert len(nodes) == 4
        
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        
        assert nodes[2].text == " with a "
        assert nodes[2].text_type == TextType.TEXT
        
        assert nodes[3].text == "link"
        assert nodes[3].text_type == TextType.LINK
        assert nodes[3].url == "https://boot.dev"
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_with_extras(self):
        md = """


    This is a **bold** paragraph with some text

        This paragraph has extra spaces before this line
        And even more
        


    - This is a list point with indentation
            - And some extra spaces in a sub-point



    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a **bold** paragraph with some text",
                "This paragraph has extra spaces before this line\nAnd even more",
                "- This is a list point with indentation\n- And some extra spaces in a sub-point",
            ],
        )
    def test_paragraph(self):
        block = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        block = "This is a multi-line\nparagraph with no\nspecial formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        # Test all heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Test invalid headings
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space after hash"), BlockType.PARAGRAPH)
    def test_code_block(self):
        # Single-line code block (already stripped)
        self.assertEqual(block_to_block_type("```print('hello')```"), BlockType.CODE)

        # Multi-line code block (already stripped)
        self.assertEqual(block_to_block_type("```\ndef hello():\n    print('Hi')\n```"), BlockType.CODE)

        # Edge Case: Multi-line code block with extra spaces inside (but input is already stripped)
        self.assertEqual(block_to_block_type("```\n   print('test')\n   ```"), BlockType.CODE)
    def test_quote(self):
        # Simple quote (already stripped)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

        # Multi-line quote (already stripped)
        self.assertEqual(block_to_block_type("> This is a quote\n> on multiple lines"), BlockType.QUOTE)

        # Edge Case: Quote with extra spaces **inside the text** (but input is already stripped)
        self.assertEqual(block_to_block_type(">    This is a quote with extra spaces inside"), BlockType.QUOTE)
    def test_unordered_list(self):
        # Simple unordered list (pre-stripped)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)

        # Edge Case: Unordered list with spaces inside (not at the beginning)
        self.assertEqual(block_to_block_type("-    Item 1\n-  Item 2"), BlockType.UNORDERED_LIST)
    def test_ordered_list(self):
        # Standard ordered list (pre-stripped)
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), BlockType.ORDERED_LIST)

        # Edge Case: Ordered list with internal spaces (not at the beginning)
        self.assertEqual(block_to_block_type("1.    Item one\n2.   Item two"), BlockType.ORDERED_LIST)
    def test_mixed_unordered_list(self):
        # Standard unordered list (each line starts with "- " and follows the rule)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)

        # Edge Case: Nested unordered list (should be a paragraph because indentation isn't allowed)
        self.assertEqual(block_to_block_type("- Item 1\n  - Nested Item"), BlockType.PARAGRAPH)

        # Edge Case: Incorrectly formatted unordered list (missing space after "-")
        self.assertEqual(block_to_block_type("-Item 1\n-Item 2"), BlockType.PARAGRAPH)

        # Edge Case: An unordered list where one line is invalid (should be a paragraph)
        self.assertEqual(block_to_block_type("- Item 1\nItem without dash\n- Item 2"), BlockType.PARAGRAPH)

    def test_mixed_ordered_list(self):
        # Standard ordered list (each line starts with "X. " and increments correctly)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)

        # Edge Case: Nested ordered list (should be a paragraph because indentation isn't allowed)
        self.assertEqual(block_to_block_type("1. Item 1\n  2. Nested Item"), BlockType.PARAGRAPH)

        # Edge Case: Ordered list that does NOT start at 1 (should be a paragraph)
        self.assertEqual(block_to_block_type("2. Item 1\n3. Item 2"), BlockType.PARAGRAPH)

        # Edge Case: Ordered list that skips a number (should be a paragraph)
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 2"), BlockType.PARAGRAPH)

        # Edge Case: Incorrectly formatted ordered list (missing space after ".")
        self.assertEqual(block_to_block_type("1.Item 1\n2.Item 2"), BlockType.PARAGRAPH)

        # Edge Case: An ordered list where one line is invalid (should be a paragraph)
        self.assertEqual(block_to_block_type("1. Item 1\nNot a list item\n2. Item 2"), BlockType.PARAGRAPH)


    def test_edge_cases(self):
        # Empty block should default to paragraph
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

        # Random characters should be a paragraph
        self.assertEqual(block_to_block_type("@#$%^&*()_+!"), BlockType.PARAGRAPH)
    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )