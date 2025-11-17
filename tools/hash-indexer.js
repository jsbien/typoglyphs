// Offline image indexer using blockhash-core
// Run with: node tools/hash-indexer.js > perceptual-search/image-index.json

const fs = require('fs');
const path = require('path');
const blockhash = require('blockhash-core');
const { createCanvas, loadImage } = require('canvas');

const GLYPH_DIR = path.join(__dirname, '../typoglyphs');
const SUBDIR_PATTERN = /^\d{2}_glyphs$/;
const IMAGE_EXT = ['.png'];

async function hashImage(imgPath) {
  try {
    const img = await loadImage(imgPath);
    const canvas = createCanvas(img.width, img.height);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const hash = blockhash.bmvbhash(canvas, 8); // 8x8 bits
    return hash;
  } catch (err) {
    console.error(`❌ Failed to process ${imgPath}: ${err.message}`);
    return null;
  }
}

async function indexImages() {
  const index = [];

  const folders = fs.readdirSync(GLYPH_DIR).filter(name => SUBDIR_PATTERN.test(name));

  for (const folder of folders) {
    const fullDir = path.join(GLYPH_DIR, folder);
    const files = fs.readdirSync(fullDir).filter(f => IMAGE_EXT.includes(path.extname(f)));

    for (const file of files) {
      const relPath = `typoglyphs/${folder}/${file}`;
      const fullPath = path.join(GLYPH_DIR, folder, file);
      const hash = await hashImage(fullPath);
      if (hash) index.push({ path: relPath, hash });
    }
  }

  console.log(JSON.stringify(index, null, 2));
}

indexImages();