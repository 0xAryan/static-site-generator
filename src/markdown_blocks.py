block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

from htmlnode import(
    ParentNode,
)
from itertools import takewhile
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
    node = ParentNode("div", children)
    return node

def block_to_html_node(block):
    type = block_to_block_type(block)
    if type == block_type_quote:
        return quote_block_to_htmlnode(block)
    if type == block_type_unordered_list:
        return unordered_list_block_to_htmlnode(block)
    if type == block_type_ordered_list:
        return ordered_list_block_to_htmlnode(block)
    if type == block_type_code:
        return code_block_to_htmlnode(block)
    if type == block_type_heading:
        return heading_block_to_html(block)
    if type == block_type_paragraph:
        return paragraph_block_to_html(block)
    raise ValueError("Invalid Block type")

def block_to_block_type(block):
    lines = block.split('\n')

    if (
        block.startswith('# ')
        or block.startswith('## ')
        or block.startswith('### ')
        or block.startswith('#### ')
        or block.startswith('##### ')
        or block.startswith('###### ')
    ):
        return block_type_heading
    elif len(lines) > 1 and lines[0].startswith('```') and lines[-1].startswith('```'):
        return block_type_code
    elif block.startswith('>'):
        for line in lines:
            if not line.startswith(">"):
                return block_type_heading
            return block_type_quote
    elif block.startswith('* '):
        for line in lines:
            if not line.startswith('* '):
                return block_type_heading

        return block_type_unordered_list
    elif block.startswith('- '):
        for line in lines:
            if not line.startswith('- '):
                return block_type_heading

        return block_type_unordered_list
    elif block.startswith('1. '):
        index = 1
        for line in lines:
            if not line.startswith(f'{index}. '):
                return block_type_paragraph
            index += 1
        return block_type_ordered_list
    else:
        return block_type_paragraph


def text_to_child(text):
    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        htmlnode = text_node_to_html_node(textnode)
        children.append(htmlnode)
    return children



def quote_block_to_htmlnode(block):
    lines = block.split('\n')
    text = []
    for line in lines:
        if not line.startswith("> "):
            raise ValueError("Invalid quote block") 
        text.append(line.lstrip('>').strip())
    
    filtered_text = ' '.join(text)
    children = text_to_child(filtered_text)
    return ParentNode("blockquote", children)

def unordered_list_block_to_htmlnode(block):
    list_of_list_items = []
    lines = block.split('\n')
    for line in lines:
        line = line[2:]
        child = text_to_child(line)
        item = ParentNode("li", child)
        list_of_list_items.append(item)
    return ParentNode("ul", list_of_list_items)

def ordered_list_block_to_htmlnode(block):
    list_of_list_items = []
    lines = block.split('\n')
    for line in lines:
        line = line[3:]
        child = text_to_child(line)
        item = ParentNode("li", child)
        list_of_list_items.append(item)
    return ParentNode("ol", list_of_list_items)

def code_block_to_htmlnode(block):
    if not block.startswith('```') or not block.endswith('```'):
        raise ValueError("Invalid code block")
    lines = block[4:-3]
    c = text_to_child(lines)
    child = ParentNode("code", c)
    return ParentNode("pre", [child])

def count_leading_characters(string, char):
    return sum(1 for _ in takewhile(lambda x: x == char, string))
 

def heading_block_to_html(block):
    no = count_leading_characters(block, '#')
    if no + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[no+1:]
    children = text_to_child(text)
    return ParentNode(f'h{no}', children)

def paragraph_block_to_html(block):
    lines = block.split('\n')
    lines = ' '.join(lines)

    child = text_to_child(lines)
    node = ParentNode('p', child)
    return node



