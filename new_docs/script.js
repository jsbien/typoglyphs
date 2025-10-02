function createGalleryItem(entry) {
  console.log("Parsed entry:", entry);

  const div = document.createElement("div");
  div.className = "item";

  const img = document.createElement("img");
  img.src = `https://raw.githubusercontent.com/jsbien/typoglyphs/main/${entry.image_path}`;
  img.alt = entry["glyph_id"];

  const label = document.createElement("div");
  label.textContent = entry["glyph_id"];
  label.style.cursor = "pointer";

  // 🔍 Clicking image opens fullscreen
  img.onclick = (e) => {
    e.stopPropagation();
    openLightbox(entry);
  };

  // 📖 Clicking label loads metadata panel
  label.onclick = (e) => {
    e.stopPropagation();
    loadMarkdown(entry);
  };

  div.appendChild(img);
  div.appendChild(label);

  gallery.appendChild(div);
}

