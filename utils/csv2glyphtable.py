#!/usr/bin/env python3
r"""
Convert a CSV file with glyph metadata into LaTeX table rows using \glyphcell.

Input CSV format (no header expected):
GlyphID,ImageFile,DescriptionFile,Flag,OptionalExtra

Example:
Au-01_0334,t01_l03g34.png,t01_l03g34.md,0,
Au-01_0603,t01_l06g03.png,t01_l06g03.md,0,
Au-01_0604,t01_l06g04.png,t01_l06g04.md,1,t01_l06g04.md

Only the first two fields are used:
  - GlyphID   →  second argument of \glyphcell (label, TeX-escaped)
  - ImageFile →  first argument of \glyphcell
"""

import sys
import csv
import argparse
import os


def latex_escape(s: str) -> str:
    """Escape minimal set of characters that may appear in glyph IDs."""
    # Adjust if your IDs can contain more special chars
    s = s.replace("\\", r"\textbackslash{}")
    s = s.replace("_", r"\_")
    s = s.replace("%", r"\%")
    s = s.replace("&", r"\&")
    s = s.replace("#", r"\#")
    s = s.replace("{", r"\{")
    s = s.replace("}", r"\}")
    return s


def read_rows(csv_file):
    """Read (image_path, label) pairs from CSV."""
    reader = csv.reader(csv_file)
    result = []
    for row in reader:
        if not row:
            continue
        # allow comments starting with '#'
        if row[0].strip().startswith("#"):
            continue
        # expect at least two fields
        if len(row) < 2:
            continue
        glyph_id = row[0].strip()
        image_file = row[1].strip()
        if not glyph_id or not image_file:
            continue
        result.append((image_file, glyph_id))
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate LaTeX \\glyphcell table rows from a CSV file."
    )
    parser.add_argument(
        "csv",
        help='input CSV file (use "-" for stdin)',
    )
    parser.add_argument(
        "-n",
        "--columns",
        type=int,
        default=4,
        help="number of columns per row (default: 4)",
    )
    parser.add_argument(
        "--image-dir",
        default="",
        help="optional path prefix for image files in LaTeX output",
    )
    parser.add_argument(
        "--with-env",
        action="store_true",
        help="wrap output in \\begin{tabular}{...} ... \\end{tabular}",
    )

    args = parser.parse_args()

    # Open CSV
    if args.csv == "-":
        csv_f = sys.stdin
    else:
        csv_f = open(args.csv, newline="", encoding="utf-8")

    try:
        rows = read_rows(csv_f)
    finally:
        if csv_f is not sys.stdin:
            csv_f.close()

    # Prepare (image path, escaped label) pairs
    processed = []
    for image_file, glyph_id in rows:
        label = latex_escape(glyph_id)
        if args.image_dir:
            image_path = os.path.join(args.image_dir, image_file)
        else:
            image_path = image_file
        processed.append((image_path, label))

    cols = args.columns
    if cols <= 0:
        cols = 1

    # Optionally print tabular environment header
    if args.with_env:
        col_spec = "c" * cols
        print(f"\\begin{{tabular}}{{{col_spec}}}")

    # Print rows in chunks of `cols`
    for i in range(0, len(processed), cols):
        chunk = processed[i : i + cols]
        cells = [
            f"\\glyphcell{{{img}}}{{{label}}}"
            for (img, label) in chunk
        ]
        line = "  " + " & ".join(cells) + r" \\"
        print(line)
        # blank line between rows for readability (LaTeX ignores it)
        if i + cols < len(processed):
            print()

    if args.with_env:
        print("\\end{tabular}")


if __name__ == "__main__":
    main()
