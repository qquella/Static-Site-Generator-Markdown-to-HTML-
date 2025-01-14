from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node1 = TextNode('This is a text node', TextType.BOLD, 'https://www.boot.dev')
    print(text_node1)

if __name__ == "__main__":
        main()
