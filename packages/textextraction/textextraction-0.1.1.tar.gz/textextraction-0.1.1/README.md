# TextExtraction

TextExtraction is a Python package for extracting and processing text from images, PDFs, and scanned PDFs. It converts the extracted text into Markdown format while preserving the original text structure and filtering out non-English words.

## Features

- Extract text from image files using OCR
- Extract text from regular PDF files with preserved line breaks
- Extract text from scanned PDF files using OCR
- Filter text to keep only valid English words and proper nouns
- Convert extracted text to Markdown format
- Maintain the original document structure in the output

## Installation

### Install from PyPI

```bash
pip install textextraction
```

Note: This package requires Tesseract OCR and Poppler to be installed on your system.

#### macOS:
```bash
brew install tesseract poppler
```

#### Ubuntu/Debian:
```bash
apt-get update && apt-get install -y tesseract-ocr poppler-utils
```

#### Windows:
- Install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki
- Install Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/

## Usage

### Basic Usage

```python
from TextExtraction import ImageText, PdfText, ScannedPdfText

# Process an image
image_processor = ImageText()
image_processor.process_image(
    image_path="path/to/image.png",
    output_path="output_image.md",
    filter_words=True
)

# Process a regular PDF
pdf_processor = PdfText()
pdf_processor.process_pdf(
    pdf_path="path/to/document.pdf",
    output_path="output_pdf.md",
    filter_words=True
)

# Process a scanned PDF
scanned_pdf_processor = ScannedPdfText()
scanned_pdf_processor.process_pdf(
    pdf_path="path/to/scanned_document.pdf",
    output_path="output_scanned.md",
    filter_words=True
)
```

### ImageText Class

The `ImageText` class extracts text from images using Optical Character Recognition (OCR).

```python
from TextExtraction import ImageText

image_text = ImageText()

# Extract text from an image
extracted_text = image_text.extract_from_image("path/to/image.png")

# Filter text to keep only valid English words
filtered_text = image_text.filter_english_words(extracted_text)

# Convert to markdown
markdown_text = image_text.to_markdown(filtered_text, title="Image Text")

# Process an image and save the result to a file
markdown_text = image_text.process_image(
    image_path="path/to/image.png",
    output_path="output.md",
    filter_words=True
)
```

### PdfText Class

The `PdfText` class extracts text from regular PDFs while preserving the document structure.

```python
from TextExtraction import PdfText

pdf_text = PdfText()

# Extract text from a PDF
extracted_text = pdf_text.extract_from_pdf("path/to/document.pdf")

# Filter text to keep only valid English words
filtered_text = pdf_text.filter_english_words(extracted_text)

# Convert to markdown
markdown_text = pdf_text.to_markdown(filtered_text, title="PDF Text")

# Process a PDF and save the result to a file
markdown_text = pdf_text.process_pdf(
    pdf_path="path/to/document.pdf",
    output_path="output.md",
    filter_words=True
)
```

### ScannedPdfText Class

The `ScannedPdfText` class extracts text from scanned PDFs using OCR.

```python
from TextExtraction import ScannedPdfText

scanned_pdf_text = ScannedPdfText()

# Extract text from a scanned PDF
extracted_text = scanned_pdf_text.extract_from_pdf("path/to/scanned_document.pdf")

# Filter text to keep only valid English words
filtered_text = scanned_pdf_text.filter_english_words(extracted_text)

# Convert to markdown
markdown_text = scanned_pdf_text.to_markdown(filtered_text, title="Scanned PDF Text")

# Process a scanned PDF and save the result to a file
markdown_text = scanned_pdf_text.process_pdf(
    pdf_path="path/to/scanned_document.pdf",
    output_path="output.md",
    filter_words=True
)
```

## Example

Here's a complete example showing how to use all three classes:

```python
from TextExtraction import ImageText, PdfText, ScannedPdfText

def process_image():
    image_text = ImageText()
    image_path = "test.png"
    output_path = "image_output.md"
    
    markdown_text = image_text.process_image(
        image_path=image_path,
        output_path=output_path,
        filter_words=True
    )
    print(f"Processed image and saved to {output_path}")

def process_pdf():
    pdf_text = PdfText()
    pdf_path = "sample.pdf"
    output_path = "pdf_output.md"
    
    markdown_text = pdf_text.process_pdf(
        pdf_path=pdf_path,
        output_path=output_path,
        filter_words=True
    )
    print(f"Processed PDF and saved to {output_path}")

def process_scanned_pdf():
    scanned_pdf_text = ScannedPdfText()
    pdf_path = "scanned_sample.pdf"
    output_path = "scanned_pdf_output.md"
    
    markdown_text = scanned_pdf_text.process_pdf(
        pdf_path=pdf_path,
        output_path=output_path,
        filter_words=True
    )
    print(f"Processed scanned PDF and saved to {output_path}")

if __name__ == "__main__":
    process_image()
    process_pdf()
    process_scanned_pdf()
```

## Notes

- The filtering process keeps valid English words, proper nouns, and technical terms with at least 3 characters.
- The Markdown output preserves the original document structure with line breaks.
- For scanned PDFs, the OCR process might not always perfectly recognize all text, especially with poor quality scans.

## Requirements

- Python 3.6+
- NLTK
- Pillow
- pdfminer.six
- pytesseract
- pdf2image
- Tesseract OCR (system dependency)
- Poppler (system dependency)

See `requirements.txt` for specific version requirements.