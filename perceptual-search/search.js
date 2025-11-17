// perceptual-search/search.js
// Frontend image search using perceptual hashing

import initBlockhash from 'https://cdn.skypack.dev/blockhash-core?min';

const fileInput = document.getElementById('imageUpload');
const resultsContainer = document.getElementById('results');
const statusDisplay = document.getElementById('status');

async function loadImageIndex() {
  const res = await fetch('image-index.json');
  return await res.json();
}

function loadImage(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = URL.createObjectURL(file);
  });
}

function imageToData(img) {
  const canvas = document.createElement('canvas');
  canvas.width = img.width;
  canvas.height = img.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  return ctx.getImageData(0, 0, canvas.width, canvas.height);
}

function hammingDistance(a, b) {
  let dist = 0;
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) dist++;
  }
  return dist;
}

function displayResults(matches) {
  resultsContainer.innerHTML = '';
  for (const match of matches.slice(0, 20)) {
    const img = document.createElement('img');
    img.src = `../${match.path}`;
    img.title = `Distance: ${match.distance}`;
    img.width = 100;
    resultsContainer.appendChild(img);
  }
}

fileInput.addEventListener('change', async () => {
  const file = fileInput.files[0];
  if (!file) return;

  statusDisplay.textContent = '⏳ Loading image and computing hash...';

  try {
    const [blockhash, index] = await Promise.all([
      initBlockhash(),
      loadImageIndex(),
    ]);

    const img = await loadImage(file);
    const imgData = imageToData(img);
    const queryHash = blockhash.bmvbhash(imgData.data, img.width, img.height, 8);

    const matches = index.map(entry => ({
      path: entry.path,
      distance: hammingDistance(entry.hash, queryHash)
    })).sort((a, b) => a.distance - b.distance);

    displayResults(matches);
    statusDisplay.textContent = `✅ Found similar images.`;
  } catch (err) {
    statusDisplay.textContent = `❌ Error: ${err.message}`;
    console.error(err);
  }
});
