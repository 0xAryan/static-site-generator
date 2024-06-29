

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag= tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        prop_string = ""
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"'
        return prop_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None or self.value == '':
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        prop_string = self.props_to_html()
        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag == '':
            raise ValueError("Invalid Html: No tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Invalid parent node: no children")
        children_html = ''
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children={self.children}, {self.props})"

