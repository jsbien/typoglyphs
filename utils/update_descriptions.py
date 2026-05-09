#!/usr/bin/env python3

import argparse
import re
import shutil
from pathlib import Path

# Matches:
#   t01_l03g27.md
#   t23_l03g38.md
#
# Captures:
#   01
#   23
PATTERN = re.compile(r"^t(\d+)_.*\.md$", re.IGNORECASE)


def target_dir_for(filename: str) -> str:
    """
    Determine target subdirectory from filename.

    Example:
        t01_l03g27.md -> 01_descriptions
        t23_l03g38.md -> 23_descriptions
    """
    match = PATTERN.match(filename)

    if not match:
        raise ValueError(
            f"Cannot infer target directory from filename: {filename}"
        )

    number = match.group(1)  # preserve leading zeros
    return f"{number}_descriptions"


def process_files(description_root: Path, flat_md_dir: Path, dry_run: bool):
    md_files = sorted(flat_md_dir.glob("*.md"))

    if not md_files:
        print("No .md files found.")
        return

    copied = 0
    skipped = 0

    for md_file in md_files:
        try:
            target_subdir = target_dir_for(md_file.name)
        except ValueError as err:
            print(f"SKIP: {err}")
            skipped += 1
            continue

        destination_dir = description_root / target_subdir
        destination_file = destination_dir / md_file.name

        if dry_run:
            print(f"DRY RUN:")
            print(f"  source      : {md_file}")
            print(f"  destination : {destination_file}")
            print()
            copied += 1
            continue

        destination_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(md_file, destination_file)

        print(f"COPIED:")
        print(f"  source      : {md_file}")
        print(f"  destination : {destination_file}")
        print()

        copied += 1

    print("Summary")
    print("-------")
    print(f"Processed : {copied}")
    print(f"Skipped   : {skipped}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Distribute flat Markdown files into typoglyphs "
            "description subdirectories."
        )
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show operations without copying files",
    )

    parser.add_argument(
        "description_root",
        help="Root directory of the description tree",
    )

    parser.add_argument(
        "flat_md_dir",
        help="Directory containing flat .md files",
    )

    args = parser.parse_args()

    description_root = Path(args.description_root)
    flat_md_dir = Path(args.flat_md_dir)

    if not description_root.is_dir():
        raise SystemExit(
            f"Description root does not exist: {description_root}"
        )

    if not flat_md_dir.is_dir():
        raise SystemExit(
            f"Flat md directory does not exist: {flat_md_dir}"
        )

    process_files(
        description_root=description_root,
        flat_md_dir=flat_md_dir,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
