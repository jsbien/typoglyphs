// search.js

import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.5.1';

// Load CLIP pipeline (image encoder)
let extractor = null;
let loaded = false;

const status = document.getElementById('status');
const results = document.getElementById('results');
const preview = document.getElementById('input-preview');

async function loadModel() {
  status.textContent = '⏳ Loading CLIP model... (may take a moment)';
  extractor = await pipeline('feature-extraction', 'Xenova/clip-vit-base-patch32');
  loaded = true;
  status.textContent = '✅ CLIP model loaded.';
}

function showPreview(file) {
  const img = document.createElement('img');
  img.src = URL.createObjectURL(file);
  img.style.maxHeight = '200px';
  preview.innerHTML = '';
  preview.appendChild(img);
  return img;
}

function cosineSimilarity(vecA, vecB) {
  const dot = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
  const magA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
  const magB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
  return dot / (magA * magB);
}

async function embedImageFromFile(file) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = async () => {
      const embedding = await extractor(img, { pooling: 'mean', normalize: true });
      resolve(embedding.data);
    };
    img.src = URL.createObjectURL(file);
  });
}

async function loadIndexChunks() {
  const basePath = 'image-index';
  const subdirs = ['01_glyphs', '02_glyphs', '03_glyphs', '04_glyphs', '05_glyphs']; // Extend this
  const index = [];

  for (const dir of subdirs) {
    try {
      const res = await fetch(`${basePath}/${dir}.json`);
      const data = await res.json();
      index.push(...data);
    } catch (e) {
      console.warn(`❌ Could not load ${dir}: ${e}`);
    }
  }

  return index;
}

async function handleSearch(file) {
  if (!loaded) await loadModel();
  showPreview(file);
  status.textContent = '📷 Processing image...';

  const inputEmbedding = await embedImageFromFile(file);
  const index = await loadIndexChunks();

  const scored = index.map(entry => {
    const score = cosineSimilarity(inputEmbedding, entry.embedding);
    return { ...entry, score };
  });

  scored.sort((a, b) => b.score - a.score);
  displayResults(scored.slice(0, 24));
}

function displayResults(topHits) {
  results.innerHTML = '';
  for (const hit of topHits) {
    const img = document.createElement('img');
    img.src = hit.path;
    img.title = `Score: ${hit.score.toFixed(4)}`;
    img.style.maxHeight = '100px';
    results.appendChild(img);
  }

  status.textContent = `✅ Found ${topHits.length} similar glyphs.`;
}

// Wire input
document.getElementById('imageUpload').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) handleSearch(file);
});
