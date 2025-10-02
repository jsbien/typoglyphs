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
      fields.push(""); // fill missing trailing fields
    }
    return Object.fromEntries(fields.map((v, i) => [headers[i], fields[i]]));
  });
}

function createGalleryItem(entry) {
  console.log("Parsed entry:", entry); // 🔍 Debugging log

  const div = document.createElement("div");
  div.className = "item";

  const img = document.createElement("img");
  img.src = `https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}`;
  img.alt = entry["glyph_id"];

  const label = document.createElement("div");
  label.textContent = entry["glyph_id"];

  div.appendChild(img);
  div.appendChild(label);

  // On click → show description + lightbox
  div.onclick = () => {
    loadMarkdown(entry);
    openLightbox(entry);
  };

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

/* 🔍 Lightbox functions */
function openLightbox(entry) {
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxCaption = document.getElementById("lightbox-caption");

  lightboxImg.src = `https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}`;
  lightboxImg.alt = entry["glyph_id"];
  lightboxCaption.textContent = entry["glyph_id"];

  lightbox.style.display = "flex";
}

document.getElementById("lightbox-close").onclick = () => {
  document.getElementById("lightbox").style.display = "none";
};

document.getElementById("lightbox").onclick = (e) => {
  if (e.target.id === "lightbox") {
    document.getElementById("lightbox").style.display = "none";
  }
};

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
