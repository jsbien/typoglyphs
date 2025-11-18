// tools/clip-indexer.js

import fs from 'fs/promises';
import path from 'path';
import { pipeline } from '@xenova/transformers';
import { createCanvas, loadImage } from 'canvas';

const GLYPH_ROOT = 'typoglyphs';
const OUTPUT_DIR = 'perceptual-search/clip-index';

async function embedImage(imagePath, extractor) {
  try {
    const img = await loadImage(imagePath);
    const canvas = createCanvas(img.width, img.height);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const embedding = await extractor(canvas, { pooling: 'mean', normalize: true });
    return embedding.data;
  } catch (e) {
    console.warn(`❌ Failed to process ${imagePath}: ${e.message}`);
    return null;
  }
}

async function main() {
  console.log('⏳ Loading CLIP model...');
  const extractor = await pipeline('feature-extraction', 'Xenova/clip-vit-base-patch32');
  console.log('✅ Model loaded.');

  await fs.mkdir(OUTPUT_DIR, { recursive: true });
  const subdirs = (await fs.readdir(GLYPH_ROOT, { withFileTypes: true }))
    .filter(dirent => dirent.isDirectory() && dirent.name.endsWith('_glyphs'))
    .map(dirent => dirent.name);

  for (const subdir of subdirs) {
    const dirPath = path.join(GLYPH_ROOT, subdir);
    const files = (await fs.readdir(dirPath)).filter(f => f.toLowerCase().endsWith('.png'));

    const index = [];

    for (const file of files) {
      const fullPath = path.join(dirPath, file);
      const embedding = await embedImage(fullPath, extractor);
      if (!embedding) continue;

      index.push({
        path: path.join(GLYPH_ROOT, subdir, file),
        embedding
      });
    }

    const outPath = path.join(OUTPUT_DIR, `${subdir}.json`);
    await fs.writeFile(outPath, JSON.stringify(index));
    console.log(`✅ Saved ${outPath} (${index.length} entries)`);
  }

  console.log('🎉 Done.');
}

main();
