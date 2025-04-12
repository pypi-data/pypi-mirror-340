# textextraction

textextraction is a Python package for extracting and processing text from images, PDFs, and scanned PDFs. It converts the extracted text into Markdown format while preserving the original text structure and filtering out non-English words.

## Features

- Extract text from image files using OCR
- Extract text from regular PDF files with preserved line breaks
- Extract text from scanned PDF files using OCR
- Filter text to keep only valid English words and proper nouns
- Convert extracted text to Markdown format
- Maintain the original document structure in the output

## Installation

### 1. Install the package

```bash
pip install textextraction
```

### 2. Install system dependencies

#### For Tesseract OCR:

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
apt-get update && apt-get install -y tesseract-ocr
```

**Windows:**
- Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

#### For EasyOCR:

EasyOCR has its own dependencies that will be installed automatically when you install the package.

#### For PDF processing:

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
apt-get update && apt-get install -y poppler-utils
```

**Windows:**
- Download from: https://github.com/oschwartz10612/poppler-windows/releases/

## Usage

### Converting Images to Markdown

#### Using Tesseract OCR

```python
from textextraction import ImageText

# Initialize with Tesseract OCR
image_processor = ImageText(ocr_engine="tesseract")

# Process an image and save to markdown
image_processor.process_image(
    image_path="path/to/image.png",
    output_path="output_image_tesseract.md"
)

# Optional: Customize line height for better text grouping
image_processor = ImageText(ocr_engine="tesseract", line_height=30)
image_processor.process_image(
    image_path="path/to/image.png",
    output_path="output_image_tesseract_custom.md"
)
```

#### Using EasyOCR (default)

```python
from textextraction import ImageText

# Initialize with EasyOCR (default)
image_processor = ImageText()

# Process an image and save to markdown
image_processor.process_image(
    image_path="path/to/image.png",
    output_path="output_image_easyocr.md"
)

# Optional: Customize line height for better text grouping
image_processor = ImageText(line_height=30)
image_processor.process_image(
    image_path="path/to/image.png",
    output_path="output_image_easyocr_custom.md"
)
```

### Converting Scanned PDFs to Markdown

#### Using Tesseract OCR

```python
from textextraction import ScannedPdfText

# Initialize with Tesseract OCR
pdf_processor = ScannedPdfText(ocr_engine="tesseract")

# Process a scanned PDF and save to markdown
pdf_processor.process_pdf(
    pdf_path="path/to/scanned_document.pdf",
    output_path="output_scanned_tesseract.md"
)

# Optional: Customize line height for better text grouping
pdf_processor = ScannedPdfText(ocr_engine="tesseract", line_height=30)
pdf_processor.process_pdf(
    pdf_path="path/to/scanned_document.pdf",
    output_path="output_scanned_tesseract_custom.md"
)
```

#### Using EasyOCR (default)

```python
from textextraction import ScannedPdfText

# Initialize with EasyOCR (default)
pdf_processor = ScannedPdfText()

# Process a scanned PDF and save to markdown
pdf_processor.process_pdf(
    pdf_path="path/to/scanned_document.pdf",
    output_path="output_scanned_easyocr.md"
)

# Optional: Customize line height for better text grouping
pdf_processor = ScannedPdfText(line_height=30)
pdf_processor.process_pdf(
    pdf_path="path/to/scanned_document.pdf",
    output_path="output_scanned_easyocr_custom.md"
)
```

### Converting Regular PDFs to Markdown

```python
from textextraction import PdfText

# Initialize the PDF processor
pdf_processor = PdfText()

# Process a PDF and save to markdown
pdf_processor.process_pdf(
    pdf_path="path/to/document.pdf",
    output_path="output_pdf.md"
)
```

## Dependencies

### For Tesseract OCR:
- Python 3.6+
- pytesseract
- Pillow (PIL)
- Tesseract OCR (system dependency)

### For EasyOCR:
- Python 3.6+
- easyocr
- Pillow (PIL)
- numpy
- torch
- torchvision

### For PDF Processing:
- Python 3.6+
- pdfminer.six
- pdf2image
- Poppler (system dependency)

## License

This project is licensed under the MIT License - see the LICENSE file for details.