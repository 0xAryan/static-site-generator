import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node1 = TextNode("This is a text node 1", text_type_bold)
        node2 = TextNode("This is a second node", text_type_italic)
        self.assertNotEqual(node1, node2)

    def test_not_eq2(self):
        node1 = TextNode("This is a text node 1", text_type_bold)
        node2 = TextNode("This is a second node", text_type_bold)
        self.assertNotEqual(node1, node2)
    
    def check_url(self):
        node1 = TextNode("test node", text_type_bold, "www.google.com")
        node2 = TextNode("test node", text_type_bold, "www.google.com")
        self.assertEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "www.google.com")
        self.assertEqual(
            "TextNode(This is a text node, text, www.google.com)", repr(node)
        )
    

if __name__ == "__main__":
    unittest.main()
