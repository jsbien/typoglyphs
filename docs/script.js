console.log("script.js loaded (gallery + detail toggle)");

const gallery = document.getElementById("gallery");

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
  img.alt = entry["glyph_id"];
  img.style.cursor = "pointer";

  const label = document.createElement("div");
  label.textContent = entry["glyph_id"];
  label.className = "glyph-label";

  // Clicking either image or label opens detail view
  img.onclick = () => showDetail(entry);
  label.onclick = () => showDetail(entry);

  div.appendChild(img);
  div.appendChild(label);
  gallery.appendChild(div);
}

function showDetail(entry) {
  // Hide gallery, show detail view
  document.getElementById("gallery").style.display = "none";
  const detailView = document.getElementById("detail-view");
  detailView.style.display = "block";

  // Show enlarged image
  const detailImage = document.getElementById("detail-image");
  detailImage.innerHTML = `
    <img src="https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}" 
         alt="${entry["glyph_id"]}">
  `;

  // Load description
  loadMarkdown(entry);
}

async function loadMarkdown(entry) {
  const descContent = document.getElementById("desc-content");
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

// Back button
document.getElementById("back-button").onclick = () => {
  document.getElementById("detail-view").style.display = "none";
  document.getElementById("gallery").style.display = "grid";
};

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
