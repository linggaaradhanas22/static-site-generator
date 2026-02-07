import os
import shutil
from block_markdown import markdown_to_html_node, extract_title

def copy_static_to_public(src, dst):
    # Base case: if the destination doesn't exist, create it
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
            # Recursively call for subdirectories
            copy_static_to_public(source_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read Markdown
    with open(from_path, "r") as f:
        markdown_content = f.read()
        
    # Read Template
    with open(template_path, "r") as f:
        template = f.read()
        
    # Convert Markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    content_html = html_node.to_html()
    
    # Extract Title
    title = extract_title(markdown_content)
    
    # Inject into Template
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    
    # Ensure directory exists
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
        
    # Write output
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Iterate over every item in the content directory
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(from_path):
            # We only care about markdown files
            if from_path.endswith(".md"):
                # Change the extension from .md to .html for the destination
                dest_html_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_html_path)
        else:
            # It's a directory! Recursively call this function
            generate_pages_recursive(from_path, template_path, dest_path)

def main():
    source_dir = "./static"
    dest_dir = "./public"
    content_dir = "./content"
    template_path = "template.html"

    # 1. Clean the destination
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # 2. Copy static assets
    print("Copying static assets...")
    copy_static_to_public(source_dir, dest_dir)

    # 3. Generate all pages recursively
    print("Generating pages...")
    generate_pages_recursive(content_dir, template_path, dest_dir)

if __name__ == "__main__":
    main()