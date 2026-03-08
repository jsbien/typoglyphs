#!/usr/bin/env python3
"""
sync_site.py

Synchronize selected repository content into site/ without touching links or
removing files.

Copies modified files from:
- descriptions/ -> site/descriptions/
- keywords/     -> site/keywords/
- typoglyphs/   -> site/typoglyphs/

Also copies:
- typoglyphs.csv -> site/typoglyphs.txt

Behavior:
- preserves relative subdirectory structure
- copies only when destination is missing or source is newer / different size
- ignores hidden/system files such as .DS_Store and files starting with '.'
- does not delete anything from site/
- does not resolve or modify symlinks intentionally; it only writes target files
"""

import argparse
import filecmp
import os
import shutil
from pathlib import Path

VERSION = "1.0.0"
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}


def is_valid_file(path: Path) -> bool:
    return not path.name.startswith(".") and path.name not in IGNORED_NAMES


def iter_files(base_dir: Path):
    if not base_dir.exists():
        return
    for root, dirs, files in os.walk(base_dir):
        # ignore hidden directories
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for filename in sorted(files):
            src = Path(root) / filename
            if is_valid_file(src):
                yield src


def needs_copy(src: Path, dst: Path) -> bool:
    if not dst.exists():
        return True

    src_stat = src.stat()
    dst_stat = dst.stat()

    # Fast checks first
    if src_stat.st_size != dst_stat.st_size:
        return True

    # Copy if source is newer
    if src_stat.st_mtime > dst_stat.st_mtime:
        return True

    # Fallback content check for equal/older timestamps but different content
    try:
        return not filecmp.cmp(src, dst, shallow=False)
    except OSError:
        return True


def copy_tree_subset(src_root: Path, dst_root: Path, dry_run: bool = False):
    scanned = 0
    copied = 0
    skipped = 0

    if not src_root.exists():
        print(f"⚠️  Missing source directory: {src_root}")
        return scanned, copied, skipped

    print(f"🔍 Scanning {src_root} → {dst_root}")
    for src in iter_files(src_root):
        scanned += 1
        rel = src.relative_to(src_root)
        dst = dst_root / rel

        if needs_copy(src, dst):
            if dry_run:
                print(f"💡 Would copy {src} → {dst}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"✅ Copied {src} → {dst}")
            copied += 1
        else:
            skipped += 1

    return scanned, copied, skipped


def copy_single_file(src: Path, dst: Path, dry_run: bool = False):
    if not src.exists():
        print(f"❌ ERROR: Missing file: {src}")
        return 0, 0

    if needs_copy(src, dst):
        if dry_run:
            print(f"💡 Would copy {src} → {dst}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✅ Copied {src} → {dst}")
        return 1, 1

    return 1, 0


def main(root_path: str, dry_run: bool = False):
    root = Path(root_path).resolve()
    site = root / "site"

    print(f"📦 Site Sync v{VERSION}")
    print(f"📁 Root: {root}")
    if dry_run:
        print("💡 Dry-run mode: no files will be written\n")

    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")

    if not site.exists():
        raise SystemExit(f"site/ directory does not exist: {site}")

    jobs = [
        (root / "descriptions", site / "descriptions"),
        (root / "keywords", site / "keywords"),
        (root / "typoglyphs", site / "typoglyphs"),
    ]

    total_scanned = 0
    total_copied = 0
    total_skipped = 0

    for src_root, dst_root in jobs:
        scanned, copied, skipped = copy_tree_subset(src_root, dst_root, dry_run=dry_run)
        total_scanned += scanned
        total_copied += copied
        total_skipped += skipped

    print("\n🔍 Syncing index file...")
    scanned, copied = copy_single_file(
        root / "typoglyphs.csv",
        site / "typoglyphs.txt",
        dry_run=dry_run,
    )
    total_scanned += scanned
    total_copied += copied
    total_skipped += max(0, scanned - copied)

    print("\n📊 Summary:")
    print(f"✔️ Scanned: {total_scanned}")
    print(f"✅ Copied/updated: {total_copied}")
    print(f"ℹ️  Unchanged: {total_skipped}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy modified descriptions, keywords, typoglyphs, and typoglyphs.csv into site/."
    )
    parser.add_argument(
        "root",
        help="Path to repository root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without writing files",
    )
    args = parser.parse_args()

    main(args.root, dry_run=args.dry_run)
    
