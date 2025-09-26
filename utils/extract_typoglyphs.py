#!/usr/bin/env python3
"""
extract_typoglyphs.py

Copy glyph-related files for a list of glyph IDs into a flat output directory
and generate an auxiliary CSV index.

Specification: extracting.md
"""

import os
import csv
import shutil
import argparse
from pathlib import Path

VERSION = "1.0.0"

def read_id_list(id_file):
    ids = []
    seen = set()
    with open(id_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "#" in line:
                line = line.split("#", 1)[0].strip()
            if line in seen:
                print(f"❌ ERROR: Duplicate glyph-id in list: {line}")
                continue
            seen.add(line)
            ids.append(line)
    return ids

def read_typoglyphs_csv(csv_path):
    records = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 5:
                continue
            glyph_id, image, keyword, has_desc, desc = row
            records[glyph_id] = {
                "image": image,
                "keyword": keyword,
                "has_desc": int(has_desc),
                "desc": desc,
            }
    return records

def backup_output_dir(out_dir):
    backup_dir = out_dir.with_suffix(".bak")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    shutil.move(str(out_dir), str(backup_dir))
    print(f"🔄 Existing output directory moved to {backup_dir}")
    return backup_dir

def copy_file(src, dest_dir, dry_run=False):
    if not src or not os.path.exists(src):
        return None
    dest_path = Path(dest_dir) / Path(src).name
    if dry_run:
        print(f"💡 Would copy {src} → {dest_path}")
    else:
        shutil.copy2(src, dest_path)
    return dest_path

def main(root_path, id_file, output_dir, dry_run=False):
    print(f"📦 Extract Typoglyphs v{VERSION}")
    print(f"📁 Root: {root_path}")
    print(f"📄 ID list: {id_file}")
    print(f"📂 Output: {output_dir}")
    if dry_run:
        print("💡 Dry-run mode: no files will be written\n")

    root = Path(root_path)
    csv_path = root / "typoglyphs.csv"
    if not csv_path.exists():
        print(f"❌ ERROR: {csv_path} not found")
        return

    glyph_records = read_typoglyphs_csv(csv_path)
    glyph_ids = read_id_list(id_file)

    out_dir = Path(output_dir)
    if out_dir.exists() and not dry_run:
        backup_output_dir(out_dir)
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    failed = 0

    for gid in glyph_ids:
        if gid not in glyph_records:
            print(f"❌ ERROR: glyph-id {gid} not found in typoglyphs.csv")
            failed += 1
            continue

        rec = glyph_records[gid]
        row = [gid, "", "", rec["has_desc"], ""]
        success = True

        # image
        img_path = root / rec["image"]
        copied_img = copy_file(img_path, out_dir, dry_run)
        if copied_img:
            row[1] = copied_img.name
        else:
            print(f"❌ ERROR: Missing image for {gid}")
            success = False

        # keyword
        kw_path = root / rec["keyword"]
        copied_kw = copy_file(kw_path, out_dir, dry_run)
        if copied_kw:
            row[2] = copied_kw.name
        else:
            print(f"❌ ERROR: Missing keyword file for {gid}")
            success = False

        # description
        if rec["has_desc"]:
            desc_path = root / rec["desc"]
            copied_desc = copy_file(desc_path, out_dir, dry_run)
            if copied_desc:
                row[3] = 1
                row[4] = copied_desc.name
            else:
                print(f"❌ ERROR: Missing description for {gid}")
                success = False

        if success:
            copied.append(row)
        else:
            failed += 1

   # ... unchanged parts above ...

    # write auxiliary CSV
    copied.sort(key=lambda r: r[0])
    aux_csv_path = out_dir / "index.csv"
    if dry_run:
        print(f"💡 Would write auxiliary CSV to {aux_csv_path}")
    else:
        with open(aux_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(copied)
        print(f"✅ Auxiliary CSV written to {aux_csv_path}")

    print("\n📊 Summary:")
    print(f"✔️ Total glyphs listed: {len(glyph_ids)}")
    print(f"✔️ Successfully copied: {len(copied)}")
    print(f"❌ Failed or skipped: {failed}")
    if out_dir.exists() and not dry_run:
        print(f"📂 Output directory: {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract typoglyphs by glyph-id list")
    parser.add_argument("root", help="Path to repository root (with typoglyphs.csv)")
    parser.add_argument("id_file", help="File with list of glyph-ids to extract")
    parser.add_argument("output", help="Output directory path")
    parser.add_argument("--dry-run", action="store_true", help="Run without writing files")
    args = parser.parse_args()

    main(args.root, args.id_file, args.output, dry_run=args.dry_run)
