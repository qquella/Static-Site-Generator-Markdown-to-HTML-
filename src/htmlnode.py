from functools import reduce


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return reduce(
            lambda acc, item: acc + " " + item[0] + '="' + item[1] + '"',
            self.props.items(),
            "",
        )

    def __repr__(self):
        return (
            f"HTMLNode({self.tag}, {self.value}, "
            f"{[ch for ch in (self.children or [])]},"
            f"{[f'{k}: {v}' for k,v in (self.props or {}).items()]})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{ self.props_to_html() }>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag")
        elif self.children is None:
            raise ValueError("no child")
        else:
            return f"<{self.tag}{self.props_to_html()}>{reduce(lambda acc, child: acc + child.to_html(), self.children, '')}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
