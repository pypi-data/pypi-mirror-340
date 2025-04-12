"""Base class for OCR engines."""

from abc import ABC, abstractmethod
from PIL import Image

class OCREngine(ABC):
    """Abstract base class for OCR engines.
    
    This class defines the interface that all OCR engines must implement.
    It ensures consistent behavior across different OCR implementations.
    """
    
    @abstractmethod
    def extract_text(self, image):
        """Extract text from an image.
        
        Args:
            image (PIL.Image): The image to extract text from.
            
        Returns:
            str: The extracted text with line breaks preserved.
        """
        pass 