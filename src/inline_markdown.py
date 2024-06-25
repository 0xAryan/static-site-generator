from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    l = []
    for old_node in old_nodes:
        z = []
        if not isinstance(old_node, TextNode):
            z.append(old_node)
            continue

        split_str = old_node.text.split(delimiter)
        if len(split_str) % 2 == 0:
            raise Exception("Invalid Markdown, formatted section not closed")
        for i in range(len(split_str)):
            if split_str[i] == "":
                continue
            if i % 2 == 0:
                z.append(TextNode(split_str[i] ,old_node.text_type))
            else:
                z.append(TextNode(split_str[i], text_type))
        
        l.extend(z)

        
    return l