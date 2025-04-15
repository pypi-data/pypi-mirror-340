"""
Text Extraction Package

This package provides functionality for extracting text from various document formats,
including PDFs, images, and scanned documents.
"""

# Define the public API
__all__ = ["PdfText", "ScannedPdfText", "PdfUnlocker", "ImageText"]

# Package metadata
__version__ = "0.1.4"
__author__ = "Nikhil K Singh"


# Lazy loading of modules
def __getattr__(name):
    if name == "PdfText":
        from .pdf_processor import PdfText

        return PdfText
    elif name == "ImageText":
        from .image_processor import ImageText

        return ImageText
    elif name == "ScannedPdfText":
        from .scanned_pdf_processor import ScannedPdfText

        return ScannedPdfText
    elif name == "PdfUnlocker":
        from .pdf_unlocker import PdfUnlocker

        return PdfUnlocker
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
