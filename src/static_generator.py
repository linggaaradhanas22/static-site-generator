import os
import shutil
from block_markdown import markdown_to_html_node, extract_title

def copy_static_to_public(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in os.listdir(src):
        source_path = os.path.join(src, item)
        dest_path = os.path.join(dst, item)
        
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            copy_static_to_public(source_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
        
    with open(template_path, "r") as f:
        template = f.read()
        
    html_node = markdown_to_html_node(markdown_content)
    content_html = html_node.to_html()
    
    title = extract_title(markdown_content)
    
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
        
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                # Use os.path.join and splitext for cleaner extension replacement
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_html_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")
                generate_page(from_path, template_path, dest_html_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)