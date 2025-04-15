# Text Extraction

A Python package for extracting text from various document formats, including PDFs, images, and scanned documents. The package supports table detection, OCR, and password-protected PDF handling.

## Features

- Extract text from regular PDFs
- Process scanned PDFs using OCR
- Extract text from images
- Detect and extract tables from PDFs
- Remove password protection from PDFs
- Generate markdown output with proper formatting
- Support for multiple OCR engines (Tesseract, EasyOCR)
- Dictionary-based text correction

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/textextraction.git
cd textextraction

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Usage

### Basic PDF Text Extraction

```python
from textextraction import PdfText

# Initialize the PDF processor
pdf_processor = PdfText(add_page_number=True)

# Extract text from a PDF
pdf_processor.process("input.pdf", "output.md")
```

### Scanned PDF Processing

```python
from textextraction import ScannedPdfText

# Initialize the scanned PDF processor
scanned_processor = ScannedPdfText(
    add_page_number=True,
    dictionary=True,  # Enable dictionary-based correction
    add_metadata=True
)

# Process a scanned PDF
scanned_processor.process("scanned.pdf", "output.md")
```

### Image Text Extraction

```python
from textextraction import ImageText

# Initialize the image processor
image_processor = ImageText(dictionary=True)

# Extract text from an image
image_processor.process("image.jpg", "output.md")
```

### Table Extraction

```python
from textextraction import PdfText

# Initialize with table detection enabled
pdf_processor = PdfText(table_detection=True)

# Extract text and tables from a PDF
pdf_processor.process("input.pdf", "output.md")
```

### PDF Unlocking

```python
from textextraction import PdfUnlocker

# Initialize the PDF unlocker
unlocker = PdfUnlocker()

# Remove password protection
unlocker.unlock("protected.pdf", "password", "unlocked.pdf")
```

### Command Line Interface

The package also provides a command-line interface:

```bash
# Unlock a password-protected PDF
python -m textextraction unlock input.pdf password -o output.pdf

# Process a PDF with table detection
python -m textextraction process input.pdf --table-detection -o output.md

# Process a scanned PDF with OCR
python -m textextraction process scanned.pdf --scanned --ocr -o output.md
```

## Advanced Options

### PDF Processing

```python
from textextraction import PdfText

# Initialize with custom options
pdf_processor = PdfText(
    add_page_number=True,      # Add page numbers to output
    dictionary=True,           # Enable dictionary-based correction
    add_metadata=True,         # Include PDF metadata
    table_detection=True       # Enable table detection
)

# Process specific page range
pdf_processor.process(
    "input.pdf",
    "output.md",
    start_page=1,    # Start from page 1
    end_page=5       # End at page 5
)
```

### Scanned PDF Processing

```python
from textextraction import ScannedPdfText

# Initialize with OCR options
scanned_processor = ScannedPdfText(
    add_page_number=True,
    dictionary=True,
    add_metadata=True,
    table_detection=True,
    ocr_engine="easyocr"  # Choose between "tesseract" or "easyocr"
)

# Process with custom page range
scanned_processor.process(
    "scanned.pdf",
    "output.md",
    start_page=1,
    end_page=5
)
```

## Output Format

The package generates markdown output with the following features:

- Page numbers (if enabled)
- Properly formatted tables
- Preserved document structure
- Metadata (if enabled)
- Clean text formatting

Example output:
```markdown
# Document Title

## Page 1

This is the first page of the document.

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
| Data 3   | Data 4   |

## Page 2

This is the second page...
```

## Dependencies

- PyPDF2/pypdfium2 - PDF processing
- Tesseract OCR - Text recognition
- EasyOCR - Alternative OCR engine
- Pillow - Image processing
- NumPy - Numerical operations
- OpenCV - Image processing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
