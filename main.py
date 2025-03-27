from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from note_extractor import extract_notes
from image_extractor import convert_pptx_to_images
from pathlib import Path

SLIDES_DIR = Path("slides")
SLIDES_DIR.mkdir(exist_ok=True)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    pptx_path = UPLOAD_DIR / filename
    file.save(pptx_path)

    try:
        notes = extract_notes(pptx_path)
        image_paths = convert_pptx_to_images(pptx_path, SLIDES_DIR)

        # Build response by matching slide number to image
        slides_data = []
        for note in notes:
            slide_num = note["slide"]
            image_file = f"slide_{slide_num}.png"
            slides_data.append({
                "slide": slide_num,
                "notes": note["notes"],
                "image": image_file
            })

        return jsonify({
            "status": "ok",
            "pptx": filename,
            "slides": slides_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
