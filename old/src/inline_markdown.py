from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
import re


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

def extract_markdown_images(txt):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", txt)
    return matches

def extract_markdown_links(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
	return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    l = []
    for node in old_nodes:
        link_tup = extract_markdown_links(node.text)
        total_link_count = len(link_tup)
        if total_link_count == 0:
            if node.text != "":
                l.append(TextNode(node.text, text_type_text))
                continue
            else:
                continue
        
        i = 0
        while i != total_link_count:
            link_tag = link_tup[i][0]
            link_link = link_tup[i][1]
            split_list = node.text.split(f"[{link_tag}]({link_link})", 1)
            index = node.text.index(')')
            node.text = node.text[index + 1:]
            l.append(TextNode(split_list[0], node.text_type))
            l.append(TextNode(link_tag, text_type_link, link_link))
            i += 1

        if len(node.text) != 0:
            l.append(TextNode(node.text, node.text_type))
    
    return l


# def text_to_textnodes(text):
#     nodes = [TextNode(text, text_type_text)]
#     nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
#     nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
#     nodes = split_nodes_delimiter(nodes, '`', text_type_code)
#     nodes = split_nodes_image(nodes)
#     nodes = split_nodes_link(nodes)
#     return nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes