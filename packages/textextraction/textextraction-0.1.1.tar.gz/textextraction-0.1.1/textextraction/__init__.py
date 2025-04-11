# Import and expose the classes
from .image_text import ImageText
from .pdf_text import PdfText
from .scanned_pdf_text import ScannedPdfText

# Define the public API
__all__ = ["ImageText", "PdfText", "ScannedPdfText"]

# Package metadata
__version__ = "0.1.1"
