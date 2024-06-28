import unittest
from htmlnode import(
    HTMLNode,
    LeafNode,
    ParentNode,
)


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
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
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            node.to_html()
        )
    
    def test_to_html_parentnode_nested(self):
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
            "<div><p>Paragraph 1 text</p><ul><li>List item 1</li><li>List item 2</li></ul><p>Paragraph 2 text</p></div>",
            node.to_html()
        )


if __name__ == "__main__":
    unittest.main()