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
    pattern = r"!\[(.+?)\]\((.+?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.+?)\]\((.+?)\)"
    matches = re.findall(pattern, text)
    return matches


# def split_nodes_link(old_nodes):
#    nodes = []
#    pattern = r"([^\[\]]*?)\[(.+?)\]\((.+?)\)([^\[\]]*?)"
#
#    for node in old_nodes:
#        matches = re.findall(pattern, node.text)
#
#        for text1, alt, link, text2 in matches:
#            ns = [
#                TextNode(text1, TextType.NORMAL),
#                TextNode(alt, TextType.LINKS, link),
#                TextNode(text2, TextType.NORMAL),
#            ]
#            nodes.extend(ns)
#    return nodes


def split_nodes_link(old_nodes):
    nodes = []
    pattern = r"(.*?)(?:\[(.+?)\]\((.+?)\))(.*)"

    for node in old_nodes:
        text = node.text
        while True:
            match = re.search(pattern, text)
            if not match:
                # Add the remaining text as a normal node if no more matches
                if text:
                    nodes.append(TextNode(text, node.text_type))
                break

            text1, alt, link, text2 = match.groups()
            if text1:
                nodes.append(TextNode(text1, node.text_type))
            nodes.append(TextNode(alt, TextType.LINKS, link))
            text = text2  # Continue parsing remaining text

    return nodes


def split_nodes_image(old_nodes):
    nodes = []
    pattern = r"(.*?)(?:!\[(.+?)\]\((.+?)\))(.*)"

    for node in old_nodes:
        text = node.text
        while True:
            match = re.search(pattern, text)
            if not match:
                # Add the remaining text as a normal node if no more matches
                if text:
                    nodes.append(TextNode(text, node.text_type))
                break

            text1, alt, link, text2 = match.groups()
            if text1:
                nodes.append(TextNode(text1, node.text_type))  # Add leading text
            nodes.append(TextNode(alt, TextType.IMAGES, link))  # Add image node
            text = text2  # Continue parsing remaining text

    return nodes


def text_to_textnodes(text):

    text_node = TextNode(text, TextType.NORMAL)
    nodes = [text_node]

    # Apply transformations in the correct order
    nodes = split_nodes_image(nodes)  # Extract images first
    nodes = split_nodes_link(nodes)  # Extract links next
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # Extract code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # Extract bold
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)  # Extract italic
    return nodes
