from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
import re



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        s = old_node.text
        split_node = []
        sections = s.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("Invalid Markdown syntax, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_node.append(TextNode(sections[i], text_type_text))
            else:
                split_node.append(TextNode(sections[i], text_type))
            
        new_nodes.extend(split_node)

    return new_nodes    

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        for image_tup in images:
            sections = text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if len(sections) % 2 != 0:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
            text = sections[1]
        
        if text != '':
            new_nodes.append(TextNode(text, text_type_text))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        for link_tup in links:
            sections = text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
            text = sections[1]
        
        if text != '':
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, text_type_text)], "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes =split_nodes_link(nodes)
    return nodes
    