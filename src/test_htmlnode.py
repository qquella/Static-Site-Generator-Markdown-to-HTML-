import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.node = HTMLNode('a', 'Guten Tag!', props={"href": "https://www.google.com"})
        self.node2 = HTMLNode('a', 'Gute Nacht!!', [self.node], {  
                          "href": "https://www.google.com",
                          "target": "_blank", 
                         })

        self.pnode = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    ],
                )
        self.pnode2 = ParentNode(
                "h3",
                [
                    LeafNode("b", "Bold text"),
                    self.pnode,
                ],
                {
                    "class": "text-primary",
                    "id": "cool-div",
                })
        #self.pnodex = ParentNode("h3")


    @unittest.expectedFailure
    def test_to_html(self):
        node.to_html()

    def test_props(self):
        self.assertEqual(self.node2.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_none(self):
        self.assertEqual(self.node.children, None)

    def test_ln(self):
        ln1 = LeafNode("p", "This is a paragraph of text.")
        ln2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(ln1.to_html(), '<p>This is a paragraph of text.</p>')
        self.assertEqual(ln2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_pn_to_html(self):
        self.assertEqual(self.pnode.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertEqual(self.pnode2.to_html(), f"<h3 class=\"text-primary\" id=\"cool-div\"><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></h3>")

    @unittest.expectedFailure
    def test_pn_no_child(self):
        pnodex = ParentNode("h3")

    def test_repr(self):
        node = HTMLNode(
                "p",
                "What a strange world",
                None,
                {"class": "primary"},
                )
        self.assertEqual(
                node.__repr__(), "HTMLNode(p, What a strange world, [],['class: primary'])"
                )

        def test_to_html_no_children(self):
            node = LeafNode("p", "Hello, world!")
            self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        def test_to_html_no_tag(self):
            node = LeafNode(None, "Hello, world!")
            self.assertEqual(node.to_html(), "Hello, world!")

                         







if __name__ == "__main__":
    unittest.main()
