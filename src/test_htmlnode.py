import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlnode = HTMLNode(props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', 
            htmlnode.props_to_html()
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_grandchildren(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Paragraph 1 text"),
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "List item 1"),
                        LeafNode("li", "List item 2"),
                    ]
                ),
                LeafNode("p", "Paragraph 2 text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div><p>Paragraph 1 text</p><ul><li>List item 1</li><li>List item 2</li></ul><p>Paragraph 2 text</p></div>'
        )

if __name__ == "__main__":
    unittest.main()