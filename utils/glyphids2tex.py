#!/usr/bin/env python3
"""
glyphids2tex.py

Generate a LaTeX file (glyphids.tex) from the glyph-ids listed
in the index file of a directory created by extract_typoglyphs.py.

Specification: glyphids2texORIG.md
"""

import csv
from pathlib import Path
import sys

VERSION = "1.0.0"

def main(extract_dir):
    extract_dir = Path(extract_dir)
    if not extract_dir.is_dir():
        print(f"❌ {extract_dir} is not a valid directory")
        sys.exit(1)

    # Index file is named after the directory
    index_file = extract_dir / f"{extract_dir.name}.csv"
    if not index_file.exists():
        print(f"❌ Index file {index_file} not found")
        sys.exit(1)

    # Output LaTeX file
    tex_file = extract_dir / "glyphids.tex"

    # Read glyph-ids from index
    glyph_ids = []
    with open(index_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 1:
                continue
            glyph_id = row[0].strip()
            if glyph_id:
                glyph_ids.append(glyph_id)

    if not glyph_ids:
        print("⚠️ No glyph-ids found in index file")
        sys.exit(1)

    # Write LaTeX output
    with open(tex_file, "w", encoding="utf-8") as tex:
        tex.write("\\glpismo\n")
        for i, gid in enumerate(glyph_ids, start=1):
            tex.write(f"% {i}\n")
            tex.write(f"\\PTglyphid{{{gid}}}\n")
        tex.write("// \\endgl \\xe\n")
        tex.write("%%% Local Variables:\n")
        tex.write("%%% mode: latex\n")
        tex.write("%%% TeX-engine: luatex\n")
        tex.write("%%% TeX-master: shared\n")
        tex.write("%%% End:\n")

    print(f"✅ Generated {tex_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python glyphids2tex.py <extract_output_directory>")
        sys.exit(1)

    print(f"📦 glyphids2tex v{VERSION}")
    main(sys.argv[1])
