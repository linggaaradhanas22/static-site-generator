import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        # Testing a single attribute
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        # Testing multiple attributes and order (dictionaries maintain order in modern Python)
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_values(self):
        # Testing that values are correctly assigned to the object
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        # Testing that the repr looks clean for debugging
        node = HTMLNode("a", "Click me", None, {"href": "https://boot.dev"})
        self.assertEqual(
            repr(node), 
            "HTMLNode(a, Click me, children: None, {'href': 'https://boot.dev'})"
        )

if __name__ == "__main__":
    unittest.main()