#!/usr/bin/env python3

import sys
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("Usage: append_md.py <appendix.md> <target_directory>")
        sys.exit(1)

    appendix_path = Path(sys.argv[1])
    target_dir = Path(sys.argv[2])

    if not appendix_path.is_file():
        print(f"Error: appendix file not found: {appendix_path}")
        sys.exit(1)

    if not target_dir.is_dir():
        print(f"Error: directory not found: {target_dir}")
        sys.exit(1)

    appendix_content = appendix_path.read_text(encoding="utf-8")

    for md_file in target_dir.glob("*.md"):
        if md_file.resolve() == appendix_path.resolve():
            continue

        original_content = md_file.read_text(encoding="utf-8")
        md_file.write_text(
            original_content.rstrip() + "\n\n" + appendix_content.lstrip(),
            encoding="utf-8"
        )

        print(f"Updated: {md_file}")

if __name__ == "__main__":
    main()
