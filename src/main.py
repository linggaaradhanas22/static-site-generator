import os
import sys
import shutil
from static_generator import copy_static_to_public, generate_pages_recursive

def main():
    # Grab basepath from CLI argument, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    static_path = "./static"
    # GitHub Pages uses the /docs directory
    docs_path = "./docs"
    content_path = "./content"
    template_path = "./template.html"

    print("Cleaning docs directory...")
    if os.path.exists(docs_path):
        shutil.rmtree(docs_path)

    print("Copying static files...")
    copy_static_to_public(static_path, docs_path)

    print("Generating pages...")
    generate_pages_recursive(content_path, template_path, docs_path, basepath)

if __name__ == "__main__":
    main()