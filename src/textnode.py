import re
from enum import Enum
from functools import reduce

from htmlnode import *


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {str(self.url)})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGES:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if delimiter not in node.text:
            result.append(node)
            continue

        chunks = node.text.split(delimiter)

        for i, chunk in enumerate(chunks):
            if chunk:
                if i % 2 == 0:  # the delimiter is not in even chunks
                    result.append(TextNode(chunk, node.text_type))
                else:  # delimiter is in odd chunks
                    result.append(TextNode(chunk, text_type))
    return result


def extract_markdown_images(text):
    return reduce(
        lambda acc, str: acc
        + [
            (match.group(1), match.group(2))
            for match in [re.search(r"([.+?])(\(.+?\))", str)]
            if match
        ],
        text,
        [],
    )
