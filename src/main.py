import os
import shutil
from static_generator import copy_static_to_public, generate_pages_recursive

def main():
    source_dir = "./static"
    dest_dir = "./public"
    content_dir = "./content"
    template_path = "template.html"

    # 1. Clean the destination
    if os.path.exists(dest_dir):
        print(f"Cleaning existing {dest_dir} directory...")
        shutil.rmtree(dest_dir)

    # 2. Copy static assets
    print("Copying static assets...")
    copy_static_to_public(source_dir, dest_dir)

    # 3. Generate all pages recursively
    print("Generating pages...")
    generate_pages_recursive(content_dir, template_path, dest_dir)

if __name__ == "__main__":
    main()