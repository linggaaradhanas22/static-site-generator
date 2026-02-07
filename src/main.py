import os
import shutil

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

def main():
    source_dir = "./static"
    dest_dir = "./public"

    # 1. Clean the destination directory
    if os.path.exists(dest_dir):
        print(f"Cleaning {dest_dir}...")
        shutil.rmtree(dest_dir)

    # 2. Start the copy process
    print(f"Starting copy from {source_dir} to {dest_dir}...")
    copy_static_to_public(source_dir, dest_dir)
    print("Copy complete!")

if __name__ == "__main__":
    main()