// tools/hash-indexer.js
import fs from 'fs';
import path from 'path';
import { createCanvas, loadImage } from 'canvas';
import blockhash from 'blockhash-core';

const BASE_DIR = 'typoglyphs';
const OUTPUT_DIR = 'perceptual-search/index';
const GLYPH_DIRS = fs.readdirSync(BASE_DIR).filter(name => /^\d{2}_glyphs$/.test(name));

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function hashImage(imgPath) {
  try {
    const img = await loadImage(imgPath);
    const canvas = createCanvas(img.width, img.height);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const imgData = ctx.getImageData(0, 0, img.width, img.height);
    const hash = blockhash.bmvbhash(imgData.data, img.width, img.height, 8);
    return hash;
  } catch (err) {
    console.error(`❌ Failed to process ${imgPath}: ${err.message}`);
    return null;
  }
}

async function processDirectory(dir) {
  const dirPath = path.join(BASE_DIR, dir);
  const files = fs.readdirSync(dirPath).filter(file => file.toLowerCase().endsWith('.png'));
  const results = [];

  for (const file of files) {
    const fullPath = path.join(dirPath, file);
    const hash = await hashImage(fullPath);
    if (hash) {
      results.push({
        path: path.join(BASE_DIR, dir, file),
        hash
      });
    }
  }

  const outputPath = path.join(OUTPUT_DIR, `index-${dir}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`✅ Saved ${results.length} hashes to ${outputPath}`);
}

async function main() {
  for (const dir of GLYPH_DIRS) {
    await processDirectory(dir);
  }
}

main();
