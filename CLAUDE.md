# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python Flask microservice that extracts slide images and presenter notes from PowerPoint (.pptx) files. The service converts presentations through a multi-step process: PPTX → PDF (via LibreOffice) → PNG images (via pdf2image), while simultaneously extracting presenter notes.

## Architecture

The microservice follows a simple modular architecture:

- **main.py**: Flask web server with `/health` and `/extract` endpoints
- **note_extractor.py**: Extracts presenter notes using python-pptx library
- **image_extractor.py**: Handles PPTX→PDF→PNG conversion pipeline using LibreOffice and pdf2image
- **environment.yml**: Conda environment with Python 3.11 and required dependencies

## Development Commands

### Local Development Setup
```bash
# Create conda environment
conda env create -f environment.yml
conda activate pptx_extractor_env

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install libreoffice poppler-utils

# Run the Flask application
python main.py
```

### Docker Development
```bash
# Build container
docker build -t pptx-extractor:latest .

# Run container with volume mounts for output
docker run -p 5000:5000 \
  -v $(pwd)/notes:/app/notes \
  -v $(pwd)/slides:/app/slides \
  pptx-extractor:latest

# Test with sample file
curl -X POST http://localhost:5000/extract \
  -F "file=@sample/shapes.pptx"
```

### Testing
```bash
# Health check
curl http://localhost:5000/health

# Extract from sample PPTX
curl -X POST http://localhost:5000/extract \
  -F "file=@sample/shapes.pptx"
```

## Key Implementation Details

### File Processing Pipeline
1. **Upload**: Files saved to `/uploads` directory using secure_filename()
2. **Note Extraction**: Uses python-pptx to read presenter notes from each slide
3. **Image Conversion**: Two-step process via LibreOffice headless mode:
   - PPTX → PDF using LibreOffice command line
   - PDF → PNG images using pdf2image library
4. **Output Structure**: JSON response mapping slide numbers to notes and image filenames

### Directory Structure
- `/uploads`: Temporary storage for uploaded PPTX files
- `/notes`: Individual text files for presenter notes (slide_01.txt, slide_02.txt, etc.)
- `/slides`: PNG images for each slide (slide_01.png, slide_02.png, etc.)

### Dependencies
- **System**: LibreOffice (headless conversion), poppler-utils (PDF processing)
- **Python**: Flask, python-pptx, pdf2image, Pillow, PyMuPDF
- **Environment**: Python 3.11 via Conda

## Error Handling Patterns

The service implements basic error handling:
- File upload validation in Flask endpoint
- LibreOffice conversion failure detection via subprocess return codes
- Exception catching with JSON error responses (500 status)
- File existence validation after PDF conversion

## API Endpoints

- `GET /health`: Returns `{"status": "ok"}` for health checks
- `POST /extract`: Accepts multipart file upload, returns JSON with slide data

Expected response format:
```json
{
  "status": "ok",
  "pptx": "filename.pptx",
  "slides": [
    {
      "slide": 1,
      "notes": "presenter notes text",
      "image": "slide_01.png"
    }
  ]
}
```

## Container Configuration

The Dockerfile uses continuumio/miniconda3 base image and:
- Installs LibreOffice and poppler-utils system packages
- Creates conda environment from environment.yml
- Exposes port 5000
- Runs Flask app in activated conda environment

This microservice is designed for containerized deployment with volume mounts for accessing generated output files.