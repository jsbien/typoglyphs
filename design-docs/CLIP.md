 # CLIP-Based Visual Search Design for Typoglyphs
 
 ## 🧠 What is CLIP?
 CLIP (Contrastive Language–Image Pretraining), developed by OpenAI, is a neural network that learns visual concepts from natural language supervision. Unlike traditional classifiers, CLIP jointly learns from images and their associated text descriptions.
 
 This allows us to perform:
 - Image-to-image similarity
 - Text-to-image retrieval (e.g., "gothic lowercase A")
 
 ## 🎯 Goal
 Enhance the glyph search experience in Typoglyphs by adding a CLIP-based search option that:
 1. Extracts high-dimensional feature vectors from input glyph images.
 2. Compares them with precomputed glyph embeddings.
 3. Returns the most visually or semantically similar glyphs.
 
 ## 🧰 Tools & Libraries
 - **Model**: OpenAI CLIP (ViT-B/32 preferred)
 - **In-Browser Execution**: Via [Transformers.js](https://github.com/xenova/transformers.js) or [ONNX Runtime Web](https://onnxruntime.ai/)
 - **Indexing**: Precompute CLIP vectors for all glyphs offline
 - **Search**: Compute cosine similarity between query and indexed vectors
 
 ## 🛠️ Implementation Plan
 
 ### Step 1: Preprocessing Glyphs (Offline)
 - Use a Python or Node.js script to:
   - Resize/normalize all glyph images
   - Run them through CLIP image encoder
   - Save each vector in a JSON file alongside the glyph filename
 
 ### Step 2: Search UI Update
 - Add search mode switch in UI:
   - "Fast (Hash-Based)"
   - "Accurate (CLIP-Based)"
 - On image upload:
   - If CLIP is selected, encode uploaded image
   - Compare with precomputed glyph vectors
   - Return top-N closest matches by cosine similarity
 
 ### Step 3: In-Browser Inference
 - Use `Transformers.js` to load CLIP image model
 - Resize uploaded image to 224×224, normalize to model's expected format
 - Run encoder and retrieve feature vector
 - Perform cosine similarity in JS against indexed vectors
 
 ### Step 4: Optimization
 - Store vector index in chunks (per folder or compressed)
 - Consider WebAssembly or WebGPU acceleration if slow
 - Lazy-load vectors on demand
 
 ## 🧪 Testing Strategy
 - Validate that identical images return top match
 - Test with similar handwritten glyphs from different folders
 - Compare results from CLIP vs hash vs pixel difference
 
 ## 🔄 Fallback
 - If browser doesn't support CLIP inference:
   - Alert user with message
   - Fallback to fast hash-based search
 
 ## 📂 Output Format Example
 ```json
 [
   {
     "path": "typoglyphs/33_glyphs/t33_l03g21.png",
     "vector": [0.13, -0.04, 0.22, ..., -0.09]
   },
   ...
 ]
 ```
 
 ## 📌 Notes
 - Embedding extraction can take several seconds in-browser
 - Ensure consistent preprocessing for both query and index
 - CLIP is robust to minor distortions, so ideal for glyph classification
 
 ---
 Created for `search-dev` branch by AskTheCode companion.
