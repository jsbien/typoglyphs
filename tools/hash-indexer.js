// Offline image indexer using blockhash-core
// Run with: node tools/hash-indexer.js > perceptual-search/image-index.json

const fs = require('fs');
const path = require('path');
const { createCanvas, loadImage } = require('canvas');
const blockhash = require('blockhash-core');

const GLYPH_DIR = path.join(__dirname, '../typoglyphs');
const SUBDIR_PATTERN = /^\d{2}_glyphs$/;
const IMAGE_EXT = ['.png'];

async function hashImage(imgPath) {
  try {
    const img = await loadImage(imgPath);
    const canvas = createCanvas(img.width, img.height);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const imageData = ctx.getImageData(0, 0, img.width, img.height);
    const hash = blockhash.bmvbhash(imageData.data, img.width, img.height, 8);
    return hash;
  } catch (err) {
    console.error(`❌ Failed to process ${imgPath}: ${err.message}`);
    return null;
  }
}

async function indexImages() {
  const index = [];

  const folders = fs
    .readdirSync(GLYPH_DIR)
    .filter((name) => SUBDIR_PATTERN.test(name));

  for (const folder of folders) {
    const fullDir = path.join(GLYPH_DIR, folder);
    const files = fs
      .readdirSync(fullDir)
      .filter((f) => IMAGE_EXT.includes(path.extname(f)));

    for (const file of files) {
      const relPath = `typoglyphs/${folder}/${file}`;
      const fullPath = path.join(fullDir, file);
      const hash = await hashImage(fullPath);
      if (hash) {
        index.push({ path: relPath, hash });
        console.log(`✅ Hashed: ${relPath}`);
      }
    }
  }

  console.error(`✅ Indexed ${index.length} images.`);
  console.log(JSON.stringify(index, null, 2));
}

indexImages();
