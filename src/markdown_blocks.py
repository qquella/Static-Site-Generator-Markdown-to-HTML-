import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes


def markdown_to_blocks(markdown):
    texts = markdown.split("\n\n")
    return list(filter(lambda t: t != "", list(map(lambda text: text.strip(), texts))))


def block_to_block_type(md):
    segs = md.split()

    if "#" in segs[0]:
        n = len(segs[0])
        if n <= 6:
            return f"<h{n}>{' '.join(segs[1:])}</h{n}>"

    elif "*" == md[0] or "-" == md[0]:
        return f"<ul>{[f"<li>{s[2:]}</li>" for s in segs]}</ul>"

    elif re.search(r"\d\.\s", md) is not None:
        return f"<ol>{[f"<li>{s[2:]}</li>" for s in segs]}</ol>"

    elif md[0] == ">":
        return f"<blockquote>{md}</blockquote>"

    elif md[:2] == "```":
        return f"<code>{md}</code>"

    else:
        return f"<p>{md}</p>"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    hnode = None
    children = []

    for block in blocks:
        segs = block.split()

        if "#" in segs[0]:
            n = len(segs[0])
            if n <= 6:
                hnode = LeafNode(f"h{n}", block[n + 1 :])

        # elif "*" == block[0] or "-" == block[0]:
        #    hnode = LeafNode("ul", f"{[f"<li>{s[2:]}</li>" for s in segs]}")

        #  elif re.search(r"\d\.\s", block) is not None:
        #      hnode = LeafNode("ol", f"{[f"<li>{s[2:]}</li>" for s in segs]}")
        elif "*" == block[0] or "-" == block[0]:
            items = block.split("\n")
            list_items = "".join([f"<li>{item[2:].strip()}</li>" for item in items])
            hnode = LeafNode("ul", list_items)

        elif re.search(r"\d\.\s", block):
            items = block.split("\n")
            list_items = "".join([f"<li>{item[3:].strip()}</li>" for item in items])
            hnode = LeafNode("ol", list_items)

        elif block[0] == ">":
            hnode = LeafNode("blockquote", block[2:].strip())

        #   elif block[:2] == "```":
        #       hnode = LeafNode("code", block[3:])

        elif block[:2] == "```":
            nodes = text_to_textnodes(block)
            # content = "".join([node.to_html() for node in nodes])
            [children.append(text_node_to_html_node(node)) for node in nodes]
        else:
            hnode = LeafNode("p", block)

        children.append(hnode)

    return ParentNode("div", children)
