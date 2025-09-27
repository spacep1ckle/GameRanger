import os
import shutil
import filecmp

def get_unique_filename(directory, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{name}_{counter}{ext}"
        counter += 1
    return new_filename

def copy_txt_files_to_directory(target_dir):
    if not os.path.isdir(target_dir):
        print(f"Creating directory: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)

    skipped = 0
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.txt'):
                src_path = os.path.join(root, file)
                dst_path = os.path.join(target_dir, file)
                if os.path.exists(dst_path):
                    # If files are identical, skip
                    if filecmp.cmp(src_path, dst_path, shallow=False):
                        print(f"Skipping (identical): {src_path} -> {dst_path}")
                        skipped += 1
                        continue
                    # If files are different, rename
                    unique_name = get_unique_filename(target_dir, file)
                    dst_path = os.path.join(target_dir, unique_name)
                    print(f"Copying (renamed): {src_path} -> {dst_path}")
                else:
                    print(f"Copying {src_path} -> {dst_path}")
                shutil.copy2(src_path, dst_path)
    if skipped > 0:
        print(f"{skipped} file(s) were skipped due to redundancy.")

if __name__ == "__main__":
    target_directory = input("Enter the target directory to copy .txt files into: ").strip()
    copy_txt_files_to_directory(target_directory)