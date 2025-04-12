from PIL import Image
from nltk.corpus import words
import nltk
import re
from .engines import TesseractEngine, EasyOCREngine

class ImageText:
    """
        Class for extracting and processing text from images.
        This class provides functionality to extract text from images using
        different OCR engines, filter the extracted text, and convert it to
        markdown format.
        
        Attributes:
        valid_words (set): Set of valid English words for filtering.
        ocr_engine (OCREngine): The OCR engine instance used for text extraction.
    """
    def __init__(self, ocr_engine="easyocr", line_height=20):
        """
            Initialize the ImageText processor.
        
            Args:
                ocr_engine (str, optional): The OCR engine to use.
                    Options: "tesseract" or "easyocr". Defaults to "easyocr".
                line_height (int, optional): Maximum vertical distance between
                    text elements to be considered part of the same line.
                    Defaults to 20 pixels.
        """
        # Initialize NLTK words corpus
        try:
            self.valid_words = set(words.words())
        except LookupError:
            nltk.download('words')
            self.valid_words = set(words.words())
            
        # Initialize OCR engine
        self.ocr_engine = self._get_ocr_engine(ocr_engine, line_height)
    
    def _get_ocr_engine(self, engine_name, line_height):
        """Get an OCR engine instance.
        
        Args:
            engine_name (str): Name of the OCR engine to use.
            line_height (int): Maximum vertical distance between text elements
                to be considered part of the same line.
                
        Returns:
            OCREngine: An instance of the requested OCR engine.
            
        Raises:
            ValueError: If the specified engine is not supported.
        """
        engines = {
            "tesseract": TesseractEngine,
            "easyocr": EasyOCREngine
        }
        if engine_name not in engines:
            raise ValueError(f"Unsupported OCR engine: {engine_name}. Supported engines: {list(engines.keys())}")
        return engines[engine_name](line_height=line_height)
    
    def extract_from_image(self, image_path):
        """Extract text from an image file.
        
        Args:
            image_path (str): Path to the image file.
            
        Returns:
            str: The extracted text.
        """
        image = Image.open(image_path)
        return self.ocr_engine.extract_text(image)
    
    def filter_english_words(self, text):
        """Filter text to keep only valid English words.
        
        Args:
            text (str): The text to filter.
            
        Returns:
            str: The filtered text containing only valid English words.
        """
        # Split text into words
        words = text.split()
        
        # Filter words
        filtered_words = []
        for word in words:
            # Clean the word
            clean_word = re.sub(r'[^a-zA-Z]', '', word.lower())
            
            # Check if it's a valid English word
            if clean_word and clean_word in self.valid_words:
                filtered_words.append(word)
        
        return ' '.join(filtered_words)
    
    def to_markdown(self, text, title="Extracted Text"):
        """Convert text to markdown format.
        
        Args:
            text (str): The text to convert.
            title (str, optional): The title for the markdown document.
                Defaults to "Extracted Text".
                
        Returns:
            str: The text in markdown format.
        """

        # for now we are just returning the text in markdown format
        # we can also add more formatting options to the markdown

        return f"# {title}\n\n{text}"
    
    def process_image(self, image_path, output_path=None, filter_words=True):
        """Process an image file to extract and optionally filter text.
        
        Args:
            image_path (str): Path to the image file.
            output_path (str, optional): Path to save the output markdown file.
                If None, the output is not saved to a file.
            filter_words (bool, optional): Whether to filter out non-English words.
                Defaults to True.
                
        Returns:
            str: The processed text in markdown format.
        """
        # Extract text
        text = self.extract_from_image(image_path)
        
        # Filter words if requested
        if filter_words:
            text = self.filter_english_words(text)
        
        # Convert to markdown
        markdown = self.to_markdown(text)
        
        # Save to file if output path is provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(markdown)
        
        return markdown
