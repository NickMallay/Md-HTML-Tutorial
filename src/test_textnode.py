import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self): # Testto see if working with no website
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_2(self): #Test to see if they are the same with a website and italics
        node = TextNode("This is test 2", TextType.ITALIC, "www.test.com")
        node2 = TextNode("This is test 2", TextType.ITALIC, "www.test.com")
        self.assertEqual(node, node2)

    def test_3(self):#Test to see if different types work
        node = TextNode("This is test 3", TextType.BOLD, "www.test.com")
        node2 = TextNode("This is test 3", TextType.ITALIC, "www.test.com")
        self.assertNotEqual(node, node2)

    def test_4(self):#Test to see how it respons to None as website
        node = TextNode("This is test 4", TextType.BOLD, None)
        node2 = TextNode("This is test 4", TextType.BOLD, None)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()