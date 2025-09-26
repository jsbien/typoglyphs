## 📄 `extracting.md` — Typoglyphs Extraction Script Specification

### 🌟 Purpose

This script uses a glyph-id list to copy the corresponding glyph images, keyword files, and optional description files into a flat output directory.  
Additionally, it creates an auxiliary CSV index with references to the copied files.  
File information is obtained from the `typoglyphs.csv` index in the root of the repository.

---

### 🚀 Usage

```bash
python extract_typoglyphs.py <path_to_repo_root> <id_list> <path_to_output_directory> [--dry-run]
```

- `path_to_repo_root`: Root directory of the repository containing `typoglyphs.csv`.  
- `id_list`: A text file listing glyph IDs (e.g., `Au-01_0101`), one per line.  
  - Blank lines are ignored.  
  - Lines may include comments, starting with `#` or trailing after the ID.  
  - Duplicate IDs are reported as errors and ignored.  
- `path_to_output_directory`: Directory where the files will be copied.  
- `--dry-run`: Optional flag to simulate the process without creating files.

---

### 📦 Output

- If the output directory exists, rename it to `<output_dir>.bak`.  
  - If `<output_dir>.bak` already exists, it will be **overwritten**.  
- The new output directory is created flat: all `.png` and `.md` files are placed at the same level.  
- An auxiliary CSV index is created **inside the output directory**, named `index.csv`.  
  - Same structure as `typoglyphs.csv`.  
  - Paths are relative to the output directory.  

Auxiliary index fields:

| Field             | Description                                                    |
|-------------------|----------------------------------------------------------------|
| `glyph-id`        | Extracted from the keyword `.md` file                          |
| `image_path`      | Relative path to the `.png` image file                         |
| `keyword_path`    | Relative path to the corresponding keyword `.md` file          |
| `has_description` | `1` if description file exists and is valid, otherwise `0`     |
| `description_path`| Relative path to the description file if it exists, else empty |

---

### ⚙️ Processing Behavior

- For each glyph ID in the list:
  - Copy the corresponding image, keyword file, and description file (if present).  
  - If a file is missing, report a **non-fatal error** and continue with the next ID.  
- If two glyph IDs reference the same file, the later copy will **overwrite** the earlier one.

---

### 📊 Progress and Summary

- At the end, print a summary:
  - Total glyphs processed  
  - Total glyphs successfully copied  
  - Number of skipped or failed glyphs  
  - Backup location of any previous output directory  

No per-file progress messages are required.

---

### 🧪 Dry Run Mode

- When run with `--dry-run`, the script simulates the process:
  - Does not create or overwrite files.  
  - Reports what would have been done (including backup).  

---

### 🔤 Encoding

- All files (`typoglyphs.csv`, Markdown files, and the glyph ID list) are assumed to be UTF-8 encoded.

---

### 🔢 Version

The script includes a version string (e.g., `v1.0.0`) reported at the start of execution for traceability.
