"""EasyOCR engine implementation."""

import easyocr
import numpy as np
from .base import OCREngine

class EasyOCREngine(OCREngine):
    """EasyOCR engine implementation.
    
    This class provides text extraction functionality using the EasyOCR engine.
    The EasyOCR reader is shared across instances to avoid reinitializing.
    """
    
    # Class-level reader instance (shared across all instances)
    _reader = None
    
    def __init__(self, line_height=20, paragraph_gap=40):
        """Initialize the EasyOCR engine.
        
        Args:
            line_height (int, optional): The minimum height of a line of text in pixels.
                Defaults to 20.
            paragraph_gap (int, optional): The minimum vertical gap in pixels to consider as a paragraph break.
                Defaults to 40.
        """
        self.line_height = line_height
        self.paragraph_gap = paragraph_gap
        if EasyOCREngine._reader is None:
            print("Initializing EasyOCR (this may take a moment)...")
            EasyOCREngine._reader = easyocr.Reader(['en'])
    
    def extract_text(self, image):
        """Extract text from an image using EasyOCR.
        
        Args:
            image (PIL.Image): The image to extract text from.
            
        Returns:
            str: The extracted text with line breaks and paragraph breaks preserved.
        """
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Extract text using EasyOCR
        results = self._reader.readtext(img_array)
        
        # Sort results by y-coordinate (top to bottom)
        results.sort(key=lambda x: x[0][0][1])  # Sort by y-coordinate of first point
        
        # Group text by lines based on y-coordinates
        lines = []
        current_line = []
        current_y = None
        
        for (bbox, text, prob) in results:
            # Get the y-coordinate of the text box
            y = bbox[0][1]  # y-coordinate of top-left point
            
            # If this is the first text or if the text is on a new line
            if current_y is None or abs(y - current_y) > self.line_height:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [text]
                current_y = y
            else:
                current_line.append(text)
        
        # Add the last line if there is one
        if current_line:
            lines.append(' '.join(current_line))
        
        # Now group lines into paragraphs based on vertical spacing
        paragraphs = []
        current_paragraph = []
        
        for i, line in enumerate(lines):
            current_paragraph.append(line)
            
            # Check if this is the last line or if there's a paragraph break
            if i < len(lines) - 1:
                # Get the y-coordinates of the current and next line
                current_y = results[i][0][0][1]  # y-coordinate of first point of current line
                next_y = results[i+1][0][0][1]  # y-coordinate of first point of next line
                
                # If there's a significant gap, treat it as a paragraph break
                if next_y - current_y > self.paragraph_gap:
                    paragraphs.append('\n'.join(current_paragraph))
                    current_paragraph = []
        
        # Add the last paragraph if there is one
        if current_paragraph:
            paragraphs.append('\n'.join(current_paragraph))
        
        # Join paragraphs with double newlines to create clear paragraph breaks
        return '\n\n'.join(paragraphs) 