from pdf2image import convert_from_path
from nltk.corpus import words
import nltk
import re
from .engines import TesseractEngine, EasyOCREngine


class ScannedPdfText:
    def __init__(self, ocr_engine="easyocr", line_height=20):
        """Initialize the ScannedPdfText processor.
        
        Args:
            ocr_engine (str, optional): The OCR engine to use.
                Options: "tesseract" or "easyocr". Defaults to "easyocr".
            line_height (int, optional): The minimum height of a line of text in pixels.
                Defaults to 20.
        """
        # Initialize NLTK words corpus
        self.valid_words = set(words.words())
        # Download required NLTK data (run once)
        try:
            nltk.data.find("corpora/words")
        except LookupError:
            nltk.download("words")
        
        # Initialize OCR engine
        self.ocr_engine = self._get_ocr_engine(ocr_engine, line_height)

    def _get_ocr_engine(self, engine_name, line_height):
        """Factory method to get the appropriate OCR engine.
        
        Args:
            engine_name (str): Name of the OCR engine to use.
            line_height (int): The minimum height of a line of text in pixels.
            
        Returns:
            OCREngine: An instance of the requested OCR engine.
            
        Raises:
            ValueError: If the specified engine is not supported.
        """
        engines = {
            "tesseract": TesseractEngine(line_height=line_height),
            "easyocr": EasyOCREngine(line_height=line_height)
        }
        if engine_name not in engines:
            raise ValueError(f"Unsupported OCR engine: {engine_name}. Supported engines: {list(engines.keys())}")
        return engines[engine_name]

    def extract_from_pdf(self, pdf_path):
        """Extract text from a scanned PDF using OCR with line breaks preserved.
        
        Args:
            pdf_path (str): Path to the PDF file.
            
        Returns:
            str: The extracted text with page breaks and line breaks preserved.
        """
        print(f"\nProcessing PDF: {pdf_path}")
        
        # Convert PDF to images
        print("Converting PDF to images...")
        images = convert_from_path(pdf_path)
        total_pages = len(images)
        print(f"Found {total_pages} pages")

        # Extract text from each page image using OCR
        extracted_text = ""
        
        for i, image in enumerate(images, 1):
            print(f"\rProcessing page {i}/{total_pages}...", end="", flush=True)
            
            # Use selected OCR engine to extract text
            page_text = self.ocr_engine.extract_text(image)
            
            # Add page header and preserve line breaks
            extracted_text += f"\n--- Page {i} ---\n{page_text}\n\n"
            
            # Free up memory
            del image
        
        print("\nDone processing PDF!")
        return extracted_text.strip()

    def filter_english_words(self, text):
        """Filter text to include valid English words and proper nouns.
        
        Args:
            text (str): The text to filter.
            
        Returns:
            str: The filtered text containing only valid English words and proper nouns.
        """
        print("\nFiltering text...")
        lines = text.splitlines()
        filtered_lines = []

        for line in lines:
            # Simple word tokenization
            words_in_line = re.findall(r"\b\w+\b", line)

            # Keep words that are either in the dictionary or look like proper nouns
            filtered_words = []
            for word in words_in_line:
                word_lower = word.lower()
                # Keep if it's a valid English word
                if word_lower in self.valid_words:
                    filtered_words.append(word)
                # Also keep words that look like proper nouns (capitalized)
                elif re.match(r"^[A-Z][a-z]+$", word):
                    filtered_words.append(word)
                # Keep words with at least 3 characters that appear to be technical terms
                elif len(word) >= 3 and re.match(r"^[A-Za-z]+$", word):
                    filtered_words.append(word)

            filtered_lines.append(" ".join(filtered_words))

        print("Done filtering!")
        return "\n".join(filtered_lines)

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

    def process_pdf(self, pdf_path, output_path=None, filter_words=True):
        """Process a scanned PDF and convert to markdown.
        
        Args:
            pdf_path (str): Path to the PDF file.
            output_path (str, optional): Path to save the output markdown file.
                If None, the output is not saved to a file.
            filter_words (bool, optional): Whether to filter out non-English words.
                Defaults to True.
                
        Returns:
            str: The processed text in markdown format.
        """
        # Extract text from PDF
        extracted_text = self.extract_from_pdf(pdf_path)

        # Filter if requested
        if filter_words:
            filtered_text = self.filter_english_words(extracted_text)
        else:
            filtered_text = extracted_text

        # Format as markdown
        print("\nFormatting as markdown...")
        markdown_text = self.to_markdown(filtered_text)

        # Save to file if output path is provided
        if output_path:
            print(f"Saving to {output_path}...")
            with open(output_path, "w") as md_file:
                md_file.write(markdown_text)
            print("Done!")

        return markdown_text
