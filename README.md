# PPTX Extractor Microservice

This microservice extracts **slide images** and **presenter notes** from PowerPoint (`.pptx`) files. Built with Python, Flask, LibreOffice, and pdf2image for containerized deployment.

## 🚀 Features

- **Multi-Step Conversion**: PPTX → PDF (LibreOffice) → PNG images (pdf2image)
- **Note Extraction**: Extracts presenter notes from each slide using python-pptx
- **RESTful API**: Simple JSON API with health check and file processing endpoints
- **File Organization**: Automatic output organization with numbered slide files
- **Container Ready**: Fully containerized with conda environment management

## 🏗️ Architecture

### Processing Pipeline
1. **File Upload**: Secure file handling with werkzeug utilities
2. **Note Extraction**: Parallel extraction of presenter notes to individual text files
3. **Image Conversion**: Two-step conversion process via LibreOffice headless mode
4. **Response Generation**: JSON response mapping slides to notes and images

### Directory Structure
```
/app
├── uploads/          # Temporary PPTX file storage
├── notes/           # Individual note files (slide_01.txt, slide_02.txt, ...)
├── slides/          # PNG images (slide_01.png, slide_02.png, ...)
└── sample/          # Sample PowerPoint files for testing
```

## 📦 Quick Start

### Docker Deployment (Recommended)

```bash
# Pull the latest container
docker pull ghcr.io/40docs/pptx-extractor:latest

# Run with volume mounts for output access
docker run -p 5000:5000 \
  -v $(pwd)/notes:/app/notes \
  -v $(pwd)/slides:/app/slides \
  ghcr.io/40docs/pptx-extractor:latest
```

### Local Development

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install -y libreoffice poppler-utils

# Create conda environment
conda env create -f environment.yml
conda activate pptx_extractor_env

# Run Flask application
python main.py
```

## 🧪 API Usage

### Health Check
```bash
curl http://localhost:5000/health
# Returns: {"status": "ok"}
```

### Extract Presentation
```bash
# Using included sample file
curl -X POST http://localhost:5000/extract \
  -F "file=@sample/shapes.pptx"

# Using your own file
curl -X POST http://localhost:5000/extract \
  -F "file=@path/to/your/presentation.pptx"
```

### Response Format
```json
{
  "status": "ok",
  "pptx": "presentation.pptx",
  "slides": [
    {
      "slide": 1,
      "notes": "Presenter notes for slide 1",
      "image": "slide_01.png"
    },
    {
      "slide": 2,
      "notes": "Presenter notes for slide 2", 
      "image": "slide_02.png"
    }
  ]
}
```

## 🔧 Dependencies

### System Requirements
- **LibreOffice**: Headless PPTX to PDF conversion
- **poppler-utils**: PDF processing utilities for pdf2image

### Python Dependencies
- **Python 3.11**: Base runtime environment
- **Flask**: Web framework and API server
- **python-pptx**: PowerPoint file parsing and note extraction
- **pdf2image**: PDF to PNG image conversion
- **Pillow**: Image processing library
- **PyMuPDF**: Alternative PDF processing (backup)

## 🐳 Container Details

Built on `continuumio/miniconda3` with:
- Conda environment for dependency isolation
- System package installation (LibreOffice, poppler-utils)
- Exposed port 5000 for Flask application
- Activated conda environment for runtime

## 🛠️ Development

### Testing Changes
```bash
# Build local container
docker build -t pptx-extractor:dev .

# Test with sample file
docker run --rm -p 5000:5000 pptx-extractor:dev &
curl -X POST http://localhost:5000/extract \
  -F "file=@sample/shapes.pptx"
```

### Adding Features
- Modify extraction logic in `note_extractor.py` or `image_extractor.py`
- Update API endpoints in `main.py`
- Add new dependencies to `environment.yml`
- Test both local and containerized deployments

## 📝 File Processing Notes

- **Input Validation**: Files are processed using `secure_filename()` for security
- **Temporary Storage**: Uploaded files are temporarily stored in `/uploads`
- **Output Organization**: 
  - Slide images: `/slides/slide_NN.png` (zero-padded numbering)
  - Presenter notes: `/notes/slide_NN.txt` (UTF-8 encoded text files)
- **Cleanup**: Consider implementing cleanup routines for production deployments

## 🚨 Production Considerations

- **Resource Limits**: LibreOffice conversion can be memory-intensive
- **File Size Limits**: Configure appropriate upload size limits in Flask
- **Temporary File Cleanup**: Implement periodic cleanup of `/uploads` directory
- **Error Logging**: Enhance logging for production monitoring
- **Security**: Validate file types and implement additional security measures

## 🔍 Troubleshooting

### Common Issues

**LibreOffice Conversion Fails**
```bash
# Check LibreOffice installation
libreoffice --version

# Test manual conversion
libreoffice --headless --convert-to pdf sample/shapes.pptx
```

**PDF to Image Conversion Fails**
```bash
# Verify poppler-utils installation
pdftoppm -h

# Check Python dependencies
conda list pdf2image pillow
```

**Container Issues**
```bash
# Check container logs
docker logs <container-id>

# Verify volume mounts
docker run -it --entrypoint /bin/bash ghcr.io/40docs/pptx-extractor:latest
```

## 📚 Additional Resources

- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [pdf2image GitHub](https://github.com/Belval/pdf2image)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [LibreOffice Headless Mode](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html)
