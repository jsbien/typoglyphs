console.log("script.js loaded (gallery + always-visible metadata)");

const gallery = document.getElementById("gallery");
const detailImage = document.getElementById("detail-image");
const descContent = document.getElementById("desc-content");

async function loadCSV() {
  const res = await fetch("typoglyphs.txt");
  const text = await res.text();
  return parseCSV(text);
}

function parseCSV(csv) {
  const rows = csv.trim().split("\n");
  const headers = ['glyph_id', 'image_path', 'keyword_path', 'has_description', 'description_path'];
  return rows.map(line => {
    const fields = line.split(",");
    while (fields.length < headers.length) {
      fields.push("");
    }
    return Object.fromEntries(fields.map((v, i) => [headers[i], fields[i].trim()]));
  });
}

function createGalleryItem(entry) {
  const div = document.createElement("div");
  div.className = "item";

  const img = document.createElement("img");
  img.src = `https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}`;
  img.alt = entry.glyph_id;

  // clicking loads metadata
  img.onclick = () => showDetail(entry);
  // zoom overlay
  makeZoomable(img);

  const label = document.createElement("div");
  label.textContent = entry.glyph_id;
  label.className = "glyph-label";

  // clicking label also loads metadata
  label.onclick = () => showDetail(entry);

  div.appendChild(img);
  div.appendChild(label);
  gallery.appendChild(div);
}

function showDetail(entry) {
  // Show enlarged image in metadata panel
  detailImage.innerHTML = `
    <img src="https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}" 
         alt="${entry["glyph_id"]}">
  `;
  loadMarkdown(entry);
}

async function loadMarkdown(entry) {
  descContent.innerHTML = `<div class="loading">Loading description for <strong>${entry["glyph_id"]}</strong>...</div>`;

  const tryPath = entry["has_description"].trim() === "1"
    ? entry["description_path"]
    : entry["keyword_path"];

  if (!tryPath) {
    descContent.innerHTML = `<div class="loading">No description found.</div>`;
    return;
  }

  const url = `https://raw.githubusercontent.com/jsbien/typoglyphs/main/${tryPath}`;

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("Not found");
    const md = await res.text();
    descContent.innerHTML = marked.parse(md);
  } catch (err) {
    descContent.innerHTML = `<div class="loading">No description found.</div>`;
    console.error("Failed to load markdown for", entry["glyph_id"], tryPath, err);
  }
}

async function initGallery() {
  try {
    const data = await loadCSV();
    console.log("Loaded CSV entries:", data.length);
    data.forEach(createGalleryItem);
  } catch (err) {
    gallery.innerHTML = `<div class="loading">Failed to load CSV index.</div>`;
    console.error("CSV load error:", err);
  }
}

initGallery();

function makeZoomable(img) {
  img.addEventListener("click", () => {
    const overlay = document.createElement("div");
    overlay.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.9);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 500;
    `;

    const zoomed = document.createElement("img");
    zoomed.src = img.src;
    zoomed.alt = img.alt;
    zoomed.style.cssText = `
      max-width: 95%;
      max-height: 95%;
      object-fit: contain;
      cursor: zoom-out;
    `;

    overlay.appendChild(zoomed);

    /* append inside the nearest .gallery container */
    const galleryContainer = img.closest(".gallery");
    (galleryContainer || document.body).appendChild(overlay);

    overlay.addEventListener("click", () => overlay.remove());
  });
}

