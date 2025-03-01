from htmlnode import *
import unittest
class Test_htmlnodes(unittest.TestCase):
    def test_htmlnode_1(self):
        node = HTMLNode(None, None, None, None)
        assert node.props_to_html() == ""
    def test_htmlnode_2(self):
        node = HTMLNode(None, None, None, {"bear": "grizzly"})
        assert node.props_to_html() == ' bear="grizzly"'
    def test_htmlnode_3(self):
        node = HTMLNode(None, None, None, {"wizard": "magical", "honey": "sweet"})
        assert node.props_to_html() == ' wizard="magical" honey="sweet"'
    def test_leafnode_with_none_value(self):
        node = LeafNode("b", None)
        # unittest's way of testing for exceptions
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_2(self):
        node = LeafNode("b", "Oh no, a bear")
        assert node.to_html() == "<b>Oh no, a bear</b>"
    def test_leafnode_1(self):
        props = {"href": "https://example.com"}
        node = LeafNode("a", "Click here!", props)
        assert node.to_html() == '<a href="https://example.com">Click here!</a>'

    def test_parentnode_1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "first bold test"),
                LeafNode(None, " followed by some words"),
                LeafNode("i", " and a pointed end."),
            ],
        )
        assert node.to_html() == "<p><b>first bold test</b> followed by some words<i> and a pointed end.</i></p>"

    def test_mixed_children_types(self):
        parent = ParentNode("div", [
        LeafNode("span", "leaf child"),
        ParentNode("section", [LeafNode("p", "grandchild")]),
        LeafNode(None, "text without tag")
        ])
        assert parent.to_html() == "<div><span>leaf child</span><section><p>grandchild</p></section>text without tag</div>"

    def test_parent_with_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "test")]).to_html()

    def test_parent_with_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()


    def test_deeply_nested_structure(self):
        level3 = LeafNode("b", "deep")
        level2 = ParentNode("i", [level3])
        level1 = ParentNode("u", [level2])
        root = ParentNode("div", [level1])
        assert root.to_html() == "<div><u><i><b>deep</b></i></u></div>"
    def test_textnode_to_htmlnode_test_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
