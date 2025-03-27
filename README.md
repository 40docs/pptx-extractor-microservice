# PPTX Extractor Microservice

This microservice extracts **slide images** and **presenter notes** from `.pptx` files. It's built with Python, Flask, LibreOffice, and `pdf2image`.

---

## 🚀 Features

- Converts `.pptx` → `.pdf` → `.png` (1 image per slide)
- Extracts presenter notes per slide
- Returns a JSON summary with slide/notes/image mappings

---

## 📦 How to Run (via Docker)

### 1. Pull the Container

```bash
docker pull ghcr.io/40docs/pptx-extractor:latest
```

### 2. Run the Container

```bash
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/slides:/app/slides \
  ghcr.io/<your-org>/pptx-extractor:latest
```

This maps:
- Flask app to `localhost:5000`
- Local `uploads/` and `slides/` directories for viewing results

---

## 🧪 Sample Test

A sample PowerPoint file is included in the repo under `sample/shapes.pptx`.

```bash
curl -X POST http://localhost:5001/extract \
  -F "file=@sample/shapes.pptx"
```

---

## 📝 Notes

- Input `.pptx` files are stored temporarily in `/uploads`
- Output slide images are saved in `/slides`
- Output presenter notes are saved in `/notes`

---

## 🙋‍♂️ Questions?

Open an issue or contact the maintainer.
