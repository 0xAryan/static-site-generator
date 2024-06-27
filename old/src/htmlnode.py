class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        s = ""
        for key, value in self.props.items():
            s += f' {key}="{value}"'

        return s
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, children: {self.children}, props: {self.props}"
    

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag = tag, value = value, props = props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Cannot initialize leafnode without value")
        
        if self.tag == None:
            return self.value
        

        href = self.props_to_html()

        if href != "":
            return f'<{self.tag}{href}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children=children, props=props)
        
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: no tags")
        
        if self.children == None or len(self.children) == 0:
            raise ValueError("Invalid HTML: no children")
        
        children_html = ""
        for child in self.children:
                children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
