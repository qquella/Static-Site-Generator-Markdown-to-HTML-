import os
import shutil
from os.path import isfile

from genpage import generate_page
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import *


def main():
    text_node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node1)

    copy_from_src_dir("./static/", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")


# if os.path.exists("./public"):
#     shutil.rmtree("./public")
# os.makedirs("./public")


def copy_from_src_dir(from_path, to_path):
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Source path '{from_path}' does not exist.")
    if os.path.exists(to_path):
        shutil.rmtree(to_path)  # Clear the destination directory
    os.makedirs(to_path)

    fdirs = os.listdir(from_path)

    for item in fdirs:
        src_item = os.path.join(from_path, item)
        dst_item = os.path.join(to_path, item)

        if os.path.isfile(src_item):
            print(f"copying file: {os.path.join(from_path, item)}.")
            shutil.copy(src_item, dst_item)
        elif os.path.isdir(src_item):
            print(f"copying dir: {os.path.join(from_path, item)}.")
            os.makedirs(dst_item, exist_ok=True)
            copy_from_src_dir(src_item, dst_item)


if __name__ == "__main__":
    main()
