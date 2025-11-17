## Perceptual Hashing-Based Image Search for `typoglyphs`

### 📌 Objective
To extend the existing simple search engine at
https://jsbien.github.io/typoglyphs/ by enabling an additional option
for the user, namely a visual search for glyphs. All the existing
features, in particular previews and live image zoom, should be
preserved.

To the present site we add the buton "Beta" redirecting to the
extended version, containing an additional field "Simple visual
search" (to be supplemented later by another, MobileNet-based ML,
visual search field), which uses using perceptual hashing, entirely on
the client-side.



There are several thousands of the glyph images to be searched.
---

### 🧱 Technology Stack
- **Frontend-only** (runs in the browser)
- **Perceptual hashing** using [blockhash.js](https://github.com/commonsmachinery/blockhash-js)
- **Static `image-index.json`** storing precomputed image hashes
- **GitHub Pages-compatible** (works without a backend)

---

### 🔍 Search Algorithm (Overview)
1. Each image from `typoglyphs/01_glyphs` to `typoglyphs/81_glyphs` will be processed offline.
2. A perceptual hash (using blockhash) will be computed for each image.
3. These hashes and filenames will be stored in `image-index.json`.
4. On the website:
   - User uploads or selects an input image
   - Its hash is computed in the browser
   - Compared against all stored hashes
   - Matches are ranked by Hamming distance

---

### 🗂️ Glyph images
This version will support images from:
- `typoglyphs/01_glyphs`
- to
- `typoglyphs/81_glyphs`

Assuming images are in `.png` format (can be extended).

---

### ⚡ Performance Expectations
- Fast (few milliseconds per comparison)
- Works even on low-end devices
- Does not require external services

---

### 📦 Output Format (`image-index.json`)
```json
[
  {
    "path": "typoglyphs/01_glyphs/example1.png",
    "hash": "ffaf2c9a91e3..."
  },
  {
    "path": "typoglyphs/02_glyphs/example2.png",
    "hash": "ab89bc39c1d7..."
  }
  // ... more entries
]
```

---

### 🧭 Future Extensions
- Add MobileNet-based ML search (user-selectable)

---

### 🛠️ Tools to Use
- [blockhash.js](https://github.com/commonsmachinery/blockhash-js)
- Image processing script (Node.js or Python offline script - PLEASE ELABORATE)

---

### 📁 File Structure (in `search-dev` branch)

The site is served from `docs`, so appropriate redirection should be provided.

```
search-dev/
├── design-docs/
│   └── perceptual-search-design.md  ← this file
├── perceptual-search/
│   ├── index.html
│   ├── search.js
│   └── image-index.json
```

---

### 📌 Status
✅ Design completed — implementation phase can begin.
