#!/usr/bin/env python3

import os
import re
import csv
import argparse
import shutil
from pathlib import Path

VERSION = "1.0.1"

GLYPH_ID_PATTERN = re.compile(r'glyph-id\s*=\s*["\'](.+?)["\']')

def is_valid_file(file_path):
    name = os.path.basename(file_path)
    return not name.startswith('.') and name not in {'.DS_Store', 'Thumbs.db'}

def scan_directory(base_path, extension):
    for root, _, files in sorted(os.walk(base_path)):
        for filename in sorted(files):
            if not is_valid_file(filename):
                continue
            if filename.endswith(extension):
                yield os.path.join(root, filename)

def extract_glyph_id(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = GLYPH_ID_PATTERN.search(line)
            if match:
                return match.group(1)
    raise ValueError(f"Missing or malformed glyph-id in {md_path}")

def backup_csv(csv_path):
    backup_path = csv_path.with_suffix('.bak')
    shutil.copy2(csv_path, backup_path)
    print(f"🔄 Backed up existing CSV to {backup_path}")

def main(root_path, dry_run=False):
    print(f"📦 Typoglyphs Index Generator v{VERSION}")
    print(f"📁 Root: {root_path}")
    if dry_run:
        print("💡 Dry-run mode: no files will be written\n")

    typoglyphs_dir = os.path.join(root_path, 'typoglyphs')
    keywords_dir = os.path.join(root_path, 'keywords')
    descriptions_dir = os.path.join(root_path, 'descriptions')
    csv_path = Path(root_path) / 'typoglyphs.csv'

    total_images = 0
    missing_keywords = 0
    missing_descriptions = 0
    indexed_rows = []

    print("🔍 Scanning for images...\n")
    for png_path in scan_directory(typoglyphs_dir, '.png'):
        rel_png = os.path.relpath(png_path, root_path)
        base_name = os.path.splitext(os.path.basename(png_path))[0]

        # 🔎 Match keyword file
        keyword_md_path = None
        for md_path in scan_directory(keywords_dir, '.md'):
            if os.path.splitext(os.path.basename(md_path))[0] == base_name:
                keyword_md_path = md_path
                break

        if not keyword_md_path:
            print(f"❌ ERROR: No keyword file for image: {rel_png}")
            missing_keywords += 1
            continue

        try:
            glyph_id = extract_glyph_id(keyword_md_path)
        except Exception as e:
            print(f"❌ ERROR: {e}")
            continue

        # 🔎 Match description file
        desc_md_path = None
        for d_path in scan_directory(descriptions_dir, '.md'):
            if os.path.splitext(os.path.basename(d_path))[0] == base_name:
                desc_md_path = d_path
                break

        if desc_md_path:
            try:
                with open(desc_md_path, 'r', encoding='utf-8') as f:
                    if not f.read().strip():
                        raise ValueError("Description file is empty")
            except Exception as e:
                print(f"❌ ERROR: Problem with description file {desc_md_path} — {e}")
                continue
        else:
            missing_descriptions += 1

        # ✅ Final row
        has_description = 1 if desc_md_path else 0
        rel_keyword = os.path.relpath(keyword_md_path, root_path)
        rel_desc = os.path.relpath(desc_md_path, root_path) if desc_md_path else ""

        indexed_rows.append([
            glyph_id,
            rel_png,
            rel_keyword,
            has_description,
            rel_desc
        ])
        total_images += 1

    print("\n📊 Summary:")
    print(f"✔️ Indexed: {len(indexed_rows)} image(s)")
    print(f"❗ Missing keyword files: {missing_keywords}")
    print(f"ℹ️  Missing descriptions: {missing_descriptions}")

    if dry_run:
        print("\n💡 Dry run complete — no CSV written.")
    else:
        if csv_path.exists():
            backup_csv(csv_path)

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(indexed_rows)

        print(f"\n✅ CSV written to {csv_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate typoglyphs index CSV.")
    parser.add_argument("root", help="Path to the root of the repository")
    parser.add_argument("--dry-run", action="store_true", help="Run without writing CSV")
    args = parser.parse_args()

    main(args.root, dry_run=args.dry_run)
