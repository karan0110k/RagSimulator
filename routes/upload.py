from flask import Blueprint, request, jsonify
from utils.pdf_parser import extract_text_and_images
from utils.chunking import chunk_text
from services.embedding_service import generate_embeddings
from services.vector_store import create_text_index, create_image_index
from services.image_analyzer import analyze_image

import numpy as np
import os

upload_bp = Blueprint("upload", __name__)

ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")


@upload_bp.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename.lower()

    # ===============================
    # 🟢 CASE 1 — IMAGE UPLOAD
    # ===============================
    if filename.endswith(ALLOWED_IMAGE_EXTENSIONS):

        image_path = "temp_image.jpg"
        file.save(image_path)

        # Analyze image using Groq Vision
        image_description = analyze_image(image_path)

        # Chunk image caption
        chunks = chunk_text(image_description)

        # Generate embeddings
        embeddings = generate_embeddings(chunks)

        # Create vector index
        parents = [image_description]
        mapping = {i: 0 for i in range(len(chunks))}
        create_text_index(np.array(embeddings), chunks, parents, mapping)

        return jsonify({
            "message": "Image processed and indexed successfully.",
            "type": "image",
            "chunks_created": len(chunks)
        })


    # ===============================
    # 🟢 CASE 2 — PDF UPLOAD
    # ===============================
    elif filename.endswith(".pdf"):

        pdf_path = "temp.pdf"
        file.save(pdf_path)

        # Extract text + images
        text, image_paths = extract_text_and_images(pdf_path)

        image_descriptions = []

        # Analyze each extracted image
        for img_path in image_paths:
            try:
                description = analyze_image(img_path)
                image_descriptions.append(description)
            except Exception as e:
                print(f"Image analysis failed for {img_path}: {e}")

        # Combine text + image captions
        combined_content = text + "\n\n" + "\n\n".join(image_descriptions)

        # Chunk combined content
        chunks = chunk_text(combined_content)

        # Generate embeddings
        embeddings = generate_embeddings(chunks)

        # Create vector index
        parents = [combined_content]
        mapping = {i: 0 for i in range(len(chunks))}
        create_text_index(np.array(embeddings), chunks, parents, mapping)

        return jsonify({
            "message": f"PDF processed successfully.",
            "type": "pdf",
            "text_length": len(text),
            "images_found": len(image_paths),
            "chunks_created": len(chunks)
        })


    # ===============================
    # 🔴 Unsupported File
    # ===============================
    else:
        return jsonify({
            "error": "Unsupported file type. Please upload PDF or image (PNG/JPG)."
        }), 400