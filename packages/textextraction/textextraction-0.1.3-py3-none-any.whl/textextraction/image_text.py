from .utils import get_valid_words, filter_english_words


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
        # Initialize valid words set
        self.valid_words = get_valid_words()

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
            "tesseract": lambda: __import__(
                "textextraction.engines.tesseract", fromlist=["TesseractEngine"]
            ).TesseractEngine,
            "easyocr": lambda: __import__(
                "textextraction.engines.easyocr", fromlist=["EasyOCREngine"]
            ).EasyOCREngine,
        }

        if engine_name not in engines:
            raise ValueError(
                f"Unsupported OCR engine: {engine_name}. Supported engines: {list(engines.keys())}"
            )

        engine_class = engines[engine_name]()
        return engine_class(line_height=line_height)

    def extract_from_image(self, image_path):
        """Extract text from an image file.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: The extracted text.
        """
        # Import PIL.Image only when needed
        from PIL import Image

        image = Image.open(image_path)
        return self.ocr_engine.extract_text(image)

    def filter_english_words(self, text):
        """Filter text to keep only valid English words.

        Args:
            text (str): The text to filter.

        Returns:
            str: The filtered text containing only valid English words.
        """
        return filter_english_words(text, self.valid_words)

    def to_markdown(self, text, title="Extracted Text"):
        """Convert text to markdown format.

        Args:
            text (str): The text to convert.
            title (str, optional): The title for the markdown document.
                Defaults to "Extracted Text".

        Returns:
            str: The text in markdown format.
        """

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
            with open(output_path, "w") as f:
                f.write(markdown)

        return markdown
