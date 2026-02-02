import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    # Test that two identical nodes are equal
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    # Test that nodes with different text content are NOT equal
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    # Test that nodes with different text types are NOT equal
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    # Test that nodes with different URLs (one None, one string) are NOT equal
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    # Test that the default URL value is indeed None
    def test_url_default_none(self):
        node = TextNode("Testing default URL", TextType.TEXT)
        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()