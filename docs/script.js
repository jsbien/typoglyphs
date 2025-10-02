const gallery = document.getElementById("gallery");
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
      fields.push(""); // fill missing trailing fields with empty string
    }
    return Object.fromEntries(fields.map((v, i) => [headers[i], fields[i]]));
  });
}

function createGalleryItem(entry) {
  const div = document.createElement("div");
  div.className = "item";

  const img = document.createElement("img");
  img.src = `https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}`;
  img.alt = entry["glyph_id"];

  const label = document.createElement("div");
  label.textContent = entry["glyph_id"];

  div.appendChild(img);
  div.appendChild(label);

  div.onclick = () => loadMarkdown(entry);
  gallery.appendChild(div);
}

async function loadMarkdown(entry) {
  descContent.innerHTML = `<div class="loading">Loading description for <strong>${entry["glyph_id"]}</strong>...</div>`;

  const tryPath = entry["has_description"].trim() === "1"
    ? entry["description_path"]
    : entry["keyword_path"];

  try {
    const res = await fetch(`https://raw.githubusercontent.com/jsbien/typoglyphs/main/${tryPath}`);
    if (!res.ok) throw new Error("Not found");
    const md = await res.text();
    descContent.innerHTML = marked.parse(md);
  } catch (err) {
    descContent.innerHTML = `<div class="loading">No description found.</div>`;
  }
}

async function initGallery() {
  try {
    const data = await loadCSV();
    data.forEach(createGalleryItem);
  } catch (err) {
    gallery.innerHTML = `<div class="loading">Failed to load CSV index.</div>`;
    console.error("CSV load error:", err);
  }
}

initGallery();
