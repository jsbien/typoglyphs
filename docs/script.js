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
  return rows.map((line, idx) => {
    const fields = line.split(",");
    if (fields.length !== 5) {
      console.warn(`Line ${idx} has ${fields.length} fields:`, fields);
    }
    return {
      glyph_id: fields[0]?.trim() || "",
      image_path: fields[1]?.trim() || "",
      keyword_path: fields[2]?.trim() || "",
      has_description: fields[3]?.trim() || "",
      description_path: fields[4]?.trim() || "",
    };
  });
}

function createGalleryItem(entry) {
  const div = document.createElement("div");
  div.className = "item";
  div.dataset.glyphId = entry.glyph_id;
  div.dataset.imagePath = entry.image_path;

  const img = document.createElement("img");
  img.src = `https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}`;
  img.alt = entry.glyph_id;

  img.onclick = () => showDetail(entry);
  makeZoomable(img);

  const label = document.createElement("div");
  label.textContent = entry.glyph_id;
  label.className = "glyph-label";

  label.onclick = () => showDetail(entry);

  div.appendChild(img);
  div.appendChild(label);
  gallery.appendChild(div);
}


function showDetail(entry) {
  // Show enlarged image in metadata panel
  detailImage.innerHTML = `
    <img src="https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}"
         alt="${entry.glyph_id}"
         class="detail-img">
  `;

  // Make the metadata image zoomable too
  const detailImg = detailImage.querySelector("img");
  if (detailImg) makeZoomable(detailImg);

  // ✅ Load the markdown text into the description panel
  loadMarkdown(entry);
}

function getBaseUrl() {
  const here = window.location.origin;
  // Local dev (file:// or localhost) → use relative paths
  if (here === "null" || here.includes("localhost")) {
    return ""; // relative to docs/
  }
  // Otherwise assume production on GitHub Pages
  return "https://raw.githubusercontent.com/jsbien/typoglyphs/main/";
}

async function loadMarkdown(entry) {
  descContent.innerHTML =
    `<div class="loading">Loading description for <strong>${entry["glyph_id"]}</strong>...</div>`;

  const hasDescription = String(entry["has_description"] || "").trim() === "1";
  const descPath = (entry["description_path"] || "").trim();
  const keywordPath = (entry["keyword_path"] || "").trim();
  const chosenPath = hasDescription && descPath ? descPath : keywordPath;

  if (!chosenPath) {
    descContent.innerHTML = `<div class="loading">No description found.</div>`;
    return;
  }

  const url = getBaseUrl() + chosenPath;
  console.log("Fetching:", url);

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Not found: ${url}`);
    const md = await res.text();
    descContent.innerHTML = marked.parse(md);
  } catch (err) {
    descContent.innerHTML = `<div class="loading">No description found.</div>`;
    console.error("Failed to load markdown for", entry["glyph_id"], url, err);
  }
}

async function initGallery() {
  try {
    const data = await loadCSV();
    console.log("Loaded CSV entries:", data.length);
    data.forEach(createGalleryItem);
    enableFiltering(); // activate the filter after loading
  } catch (err) {
    gallery.innerHTML = `<div class="loading">Failed to load CSV index.</div>`;
    console.error("CSV load error:", err);
  }
}
function loadFilterHistory() {
  const list = document.getElementById("filter-history");
  if (!list) return;
  const saved = JSON.parse(localStorage.getItem("filter-history") || "[]");
  list.innerHTML = "";
  saved.forEach(q => {
    const opt = document.createElement("option");
    opt.value = q;
    list.appendChild(opt);
  });
  return saved;
}

function saveFilterToHistory(query) {
  query = query.trim();
  if (!query) return;
  let saved = JSON.parse(localStorage.getItem("filter-history") || "[]");
  if (saved.includes(query)) return;
  saved.unshift(query);
  if (saved.length > 10) saved = saved.slice(0, 10);
  localStorage.setItem("filter-history", JSON.stringify(saved));
}


function enableFiltering() {
  const filterInput = document.getElementById("filter-input");
  loadFilterHistory();
  if (!filterInput) return;

    saveFilterToHistory(query);
  filterInput.addEventListener("input", e => {
    const query = e.target.value.toLowerCase().trim();
    const items = gallery.querySelectorAll(".item");

    items.forEach(item => {
      // we stored entry data as dataset attributes for convenience
      const glyphId = item.dataset.glyphId?.toLowerCase() || "";
      const imagePath = item.dataset.imagePath?.toLowerCase() || "";

      item.style.display =
        glyphId.includes(query) || imagePath.includes(query)
          ? ""
          : "none";
    });
  });
}


initGallery();



function makeZoomable(img) {
  img.addEventListener("click", () => {
    const overlay = document.createElement("div");
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.9);
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      cursor: grab;
      z-index: 9999;
    `;

    const zoomed = document.createElement("img");
    zoomed.src = img.src;
    zoomed.alt = img.alt;
    zoomed.style.cssText = `
      transform-origin: center center;
      transition: transform 0.2s ease;
      cursor: grab;
      user-select: none;
    `;

    overlay.appendChild(zoomed);
    document.body.appendChild(overlay);

    // --- Interactive zoom and pan ---
    let scale = 1;
    let isDragging = false;
    let startX, startY, offsetX = 0, offsetY = 0;

    function updateTransform() {
      zoomed.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
    }

    overlay.addEventListener("wheel", e => {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 0.2 : -0.2;
      scale = Math.min(Math.max(0.5, scale + delta), 6);
      updateTransform();
    });

    zoomed.addEventListener("mousedown", e => {
      isDragging = true;
      startX = e.clientX - offsetX;
      startY = e.clientY - offsetY;
      overlay.style.cursor = "grabbing";
    });

    overlay.addEventListener("mouseup", () => {
      isDragging = false;
      overlay.style.cursor = "grab";
    });

    overlay.addEventListener("mouseleave", () => {
      isDragging = false;
      overlay.style.cursor = "grab";
    });

    overlay.addEventListener("mousemove", e => {
      if (!isDragging) return;
      offsetX = e.clientX - startX;
      offsetY = e.clientY - startY;
      updateTransform();
    });

    // click background (not image) to close
    overlay.addEventListener("click", e => {
      if (e.target === overlay) overlay.remove();
    });

    // initial fit
    updateTransform();
  });
}
