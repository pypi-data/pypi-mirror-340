"""Tesseract OCR engine implementation."""

import pytesseract
from PIL import Image
from .base import OCREngine

class TesseractEngine(OCREngine):
    """Tesseract OCR engine implementation.
    
    This class provides text extraction functionality using the Tesseract OCR engine.
    """
    
    def __init__(self, line_height=20):
        """Initialize the Tesseract OCR engine.
        
        Args:
            line_height (int, optional): The minimum height of a line of text in pixels.
                Defaults to 20.
        """
        self.line_height = line_height
        
        # Check if Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            raise RuntimeError(
                "Tesseract is not installed. Please install it first:\n"
                "macOS: brew install tesseract\n"
                "Ubuntu/Debian: sudo apt-get install tesseract-ocr\n"
                "Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki"
            )
    
    def extract_text(self, image):
        """Extract text from an image using Tesseract.
        
        Args:
            image (PIL.Image): The image to extract text from.
            
        Returns:
            str: The extracted text with line breaks preserved.
        """
        # Convert image to RGB if it's not
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Extract text using Tesseract
        text = pytesseract.image_to_string(image)
        return text 