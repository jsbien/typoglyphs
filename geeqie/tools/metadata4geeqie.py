import os
import shutil
import sys

SCRIPT_VERSION = "1.1"

def move_xmp_files(input_dir, working_dir):
    total_moved = 0

    for entry in os.listdir(working_dir):
        subdir_path = os.path.join(working_dir, entry)
        if not os.path.isdir(subdir_path) or not entry.endswith('_glyphs'):
            continue

        # Extract the 2-digit prefix from the directory name (e.g., "01" from "01_glyphs")
        prefix_number = entry.split('_')[0]
        xmp_prefix = f"t{prefix_number}_"

        metadata_path = os.path.join(subdir_path, '.metadata')
        os.makedirs(metadata_path, exist_ok=True)

        moved_count = 0
        for file_name in os.listdir(input_dir):
            if file_name.startswith(xmp_prefix) and file_name.endswith('.xmp'):
                src = os.path.join(input_dir, file_name)
                dst = os.path.join(metadata_path, file_name)
                shutil.move(src, dst)
                moved_count += 1

        total_moved += moved_count
        print(f"📂 {entry}: {moved_count} files moved")

    print(f"\n✅ Done. Total .xmp files moved: {total_moved}")

if __name__ == "__main__":
    print(f"\n🛠️ metadata4geeqie.py v{SCRIPT_VERSION}")

    if len(sys.argv) != 3:
        print("Usage: python metadata4geeqie.py <input_dir> <working_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    working_dir = sys.argv[2]

    if not os.path.isdir(input_dir):
        print(f"❌ Input directory not found: {input_dir}")
        sys.exit(1)

    if not os.path.isdir(working_dir):
        print(f"❌ Working directory not found: {working_dir}")
        sys.exit(1)

    move_xmp_files(input_dir, working_dir)
