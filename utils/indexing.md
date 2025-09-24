## 📄 `indexing.md` — Typoglyphs Index Generator Specification

### 🌟 Purpose

This script generates or refreshes a CSV index file named `typoglyphs.csv` in the root of the repository.  
Its purpose is to catalog all typoglyph image files along with their associated keyword and (optional) description files.

---

### 🚀 Usage

```bash
python generate_typoglyphs_index.py <path_to_repo_root> [--dry-run]
```

- `path_to_repo_root`: The root directory of the repository (where `typoglyphs.csv` will be created).
- `--dry-run`: Optional flag to preview the process without writing the CSV file.

---

### 📦 Output: `typoglyphs.csv`

Each row in the CSV contains the following fields:

| Field             | Description                                                    |
|-------------------|----------------------------------------------------------------|
| `glyph-id`        | Extracted from the keyword `.md` file                          |
| `image_path`      | Relative path to the `.png` image file                         |
| `keyword_path`    | Relative path to the corresponding keyword `.md` file          |
| `has_description` | `1` if description file exists and is valid, otherwise `0`     |
| `description_path`| Relative path to the description file if it exists, else empty |

---

### 🧱 Directory Scanning

The script recursively scans the following subdirectories under `<root>`:

- `typoglyphs/`: for `.png` image files
- `keywords/`: for `.md` keyword files
- `descriptions/`: for `.md` description files

All directories and files are processed **in alphabetical order**.

---

### 🔗 File Matching Rules

- `.png` files are matched to `.md` files in `keywords/` and `descriptions/` by **filename only**, ignoring directory structure.
  - Example: `typoglyphs/foo/bar.png` ⇔ `keywords/baz/bar.md`
- File matching is **case-sensitive** — case mismatches are reported as errors.

---

### 🏷️ `glyph-id` Extraction

- The `glyph-id` must appear in the body of the keyword `.md` file in the format:  
  ```text
  glyph-id="Some-ID"
  ```
- Only one `glyph-id` should appear per file.
- Missing, malformed, or duplicated `glyph-id` fields result in a **fatal error**.

---

### ⚙️ Processing Behavior

- If a `.png` file has:
  - ✅ A matching keyword file → process it.
  - ❌ No matching keyword file → report error, skip entry.
- If a matching description file:
  - ✅ Exists and is **non-empty** → include it.
  - ❌ Does not exist or is empty → set `has_description = 0` and leave path empty.
- Hidden/system files like `.DS_Store` and files starting with `.` are ignored.

---

### 💾 CSV Writing

- If `typoglyphs.csv` already exists:
  - A backup is created as `typoglyphs.bak`
  - The entire index is regenerated from scratch
- CSV entries are sorted by image discovery order (alphabetical by path)

---

### 📊 Progress and Summary

- Summary statistics are printed after processing:
  - Total indexed images
  - Number of missing keyword files
  - Number of missing descriptions
- Progress messages are printed per directory (not per file)

---

### 🧪 Dry Run Mode

- Use `--dry-run` to simulate the process without modifying or creating `typoglyphs.csv`
- Useful for validating new entries or testing changes to directory structure

---

### 🔢 Version

The script includes a version string (e.g. `v1.0.1`) reported at the beginning of each run for traceability.
