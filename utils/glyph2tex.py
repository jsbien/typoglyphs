#!/usr/bin/env python3
"""
glyph2tex.py

Generate a single LaTeX file (glyphs.tex) from the PNG glyphs
listed in the index file of an output directory created by
extract_typoglyphs.py.

Usage:
    python glyph2tex.py <extract_output_directory>
"""

import csv
from pathlib import Path

VERSION = "1.3.0"

def generate_tex_file(extract_dir):
    """Generate one LaTeX file (glyphs.tex) from the directory-specific index file."""

    extract_dir = Path(extract_dir)
    if not extract_dir.is_dir():
        raise ValueError(f"{extract_dir} is not a valid directory")

    # Index file has the same base name as the directory
    index_file = extract_dir / f"{extract_dir.name}.csv"
    if not index_file.exists():
        raise FileNotFoundError(f"{index_file} not found — is this from extract_typoglyphs.py?")

    # Collect all image paths from index file
    images = []
    with open(index_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue
            _, image_path, *_ = row
            if image_path.endswith(".png"):
                images.append(image_path)

    if not images:
        print("⚠️ No .png images found in index file")
        return

    # Write glyphs.tex into the same directory
    tex_path = extract_dir / "glyphs.tex"
    with open(tex_path, "w", encoding="utf-8") as tex_file:
        tex_file.write("\\exdisplay \\bg \\gla\n")
        for i, file_name in enumerate(images, start=1):
            tex_file.write(f"% {i}\n{{\\PTglyph{{5}}{{{file_name}}}}}\n")
        tex_file.write("//\n")
        tex_file.write("%%% Local Variables:\n")
        tex_file.write("%%% mode: latex\n")
        tex_file.write("%%% TeX-engine: luatex\n")
        tex_file.write("%%% TeX-master: shared\n")
        tex_file.write("%%% End:\n")

    print(f"✅ Generated {tex_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python glyph2tex.py <extract_output_directory>")
        sys.exit(1)

    print(f"📦 glyph2tex v{VERSION}")
    generate_tex_file(sys.argv[1])
