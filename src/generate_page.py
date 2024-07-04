import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown_file):

    file_obj = open(markdown_file)
    file_content = file_obj.read()
    file_obj.close()
    file_content_lines = file_content.split('\n')
    for line in file_content_lines:
        if line.startswith('# '):
            return line[2: ]
    raise Exception(" All pages need a single h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = ""
    with open(from_path) as file:
        markdown = file.read()
    
    template = ""
    with open(template_path) as file:
        template = file.read()
    
    html_nodes = markdown_to_html_node(markdown)
    html = html_nodes.to_html()

    title = extract_title(from_path)

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)

    folder_name = dest_path.split('/')[-2]
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    
    # filename = from_pathsplit('/')[-1].split('.')[0] + ".html"
    # filename = os.path.join(dest_path, filename)

    with open(dest_path, 'w') as file:
        file.write(template)
    




    

    
    