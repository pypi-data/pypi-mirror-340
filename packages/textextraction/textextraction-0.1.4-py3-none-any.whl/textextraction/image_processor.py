import os
import logging
from PIL import Image
import numpy as np
import re


from ._markdown_output import MarkdownOutput


# Lazy loading function for OCR engines
def get_ocr_engine(engine_name):
    if engine_name == "tesseract":
        import pytesseract

        return pytesseract
    elif engine_name == "easyocr":
        import easyocr

        return easyocr.Reader
    else:
        raise ValueError(f"Unsupported OCR engine: {engine_name}")


# Lazy loading function for NLTK
def get_nltk_words():
    from nltk.corpus import words as nltk_words

    return nltk_words


class ImageText:
    """
    Class for extracting text from images.
    Supports both Tesseract and EasyOCR engines.
    """

    def __init__(self, ocr_engine="easyocr", dictionary=False, add_metadata=True):
        """
        Initialize the ImageText processor.

        Args:
            ocr_engine (str): OCR engine to use ('tesseract' or 'easyocr').
            dictionary (bool): Whether to filter out non-English words.
            add_metadata (bool): Whether to add metadata to the markdown output.
        """
        self.ocr_engine = ocr_engine.lower()
        self.dictionary = dictionary
        self.add_metadata = add_metadata

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize markdown output processor
        self.markdown_output = MarkdownOutput(add_metadata=self.add_metadata)

        # Download NLTK English words dictionary if not already present and if we need to filter words
        if self.dictionary:
            try:
                get_nltk_words().words()
            except LookupError:
                self.logger.info("Downloading NLTK words dictionary")
                get_nltk_words().download("words", quiet=True)
            self.english_words = set(w.lower() for w in get_nltk_words().words())

        if self.ocr_engine == "easyocr":
            try:
                self.reader = get_ocr_engine("easyocr")(["en"])
                self.logger.info("EasyOCR initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing EasyOCR: {e}")
                self.logger.info("Falling back to Tesseract OCR")
                self.ocr_engine = "tesseract"
                self.reader = None  # Initialize reader as None for Tesseract
        else:
            self.reader = None  # Initialize reader as None for Tesseract

    def _filter_non_english_words(self, text):
        """
        Filter out non-English words from the extracted text.

        Args:
            text (str): The text to filter.

        Returns:
            str: The filtered text containing only English words.
        """
        if not self.dictionary:
            return text

        # Ensure english_words is initialized if dictionary was initially False but dictionary=True is passed
        if not hasattr(self, "english_words"):
            try:
                get_nltk_words().words()
            except LookupError:
                self.logger.info("Downloading NLTK words dictionary")
                get_nltk_words().download("words", quiet=True)
            self.english_words = set(w.lower() for w in get_nltk_words().words())

        words = re.findall(r"\b[a-zA-Z]+\b", text)
        english_words = [word for word in words if word.lower() in self.english_words]
        return " ".join(english_words)

    def extract_from_pil_image(self, image, dictionary=False):
        """
        Extract text from a PIL Image object.

        Args:
            image: PIL Image object or numpy array
            dictionary (bool): If True, filter out non-English words.

        Returns:
            str: The extracted text.
        """
        # Set dictionary based on dictionary parameter
        self.dictionary = dictionary

        try:
            if self.ocr_engine == "tesseract":
                text = get_ocr_engine(engine_name="tesseract").image_to_string(image)
            else:  # easyocr
                # EasyOCR requires numpy array
                if isinstance(image, Image.Image):
                    image_np = np.array(image)
                else:
                    image_np = image

                result = self.reader.readtext(image_np)
                text = " ".join([entry[1] for entry in result])

            if self.dictionary:
                text = self._filter_non_english_words(text)

            return text

        except Exception as e:
            self.logger.error(f"Error extracting text from image: {e}")
            return ""

    def extract_from_image(self, image_path, dictionary=False):
        """
        Extract text from an image file.

        Args:
            image_path (str): Path to the image file.
            dictionary (bool): If True, filter out non-English words.

        Returns:
            str: The extracted text.
        """
        if not os.path.exists(image_path):
            self.logger.error(f"Image file not found: {image_path}")
            return ""

        try:
            image = Image.open(image_path)
            return self.extract_from_pil_image(image, dictionary)

        except Exception as e:
            self.logger.error(f"Error loading image file: {e}")
            return ""

    def process(self, input_path, output_path=None, dictionary=False):
        """
        Process an image file and extract text.

        Args:
            input_path (str): Path to the image file.
            output_path (str, optional): Path to save the extracted text. If None, text is not saved.
            dictionary (bool): If True, filter out non-English words.

        Returns:
            str: The extracted text.
        """
        text = self.extract_from_image(input_path, dictionary)

        if output_path:
            # Use the markdown output utility to save the text
            self.markdown_output.save_markdown(
                text=text,
                output_path=output_path,
                title=f"Extracted Text from {os.path.basename(input_path)}",
                source_file=input_path,
            )

        return text
