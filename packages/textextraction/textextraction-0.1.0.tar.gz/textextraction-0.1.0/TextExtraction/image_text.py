from PIL import Image
import pytesseract
from nltk.corpus import words
import nltk
import re


class ImageText:
    def __init__(self):
        # Initialize the nltk words corpus
        self.valid_words = set(words.words())
        # Download required NLTK data (run once)
        try:
            nltk.data.find("corpora/words")
        except LookupError:
            nltk.download("words")

    def extract_from_image(self, image_path):
        """Extract text from an image file with line breaks preserved"""
        image = Image.open(image_path)
        # Extract text with line breaks
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text

    def filter_english_words(self, text):
        """Filter text to include valid English words and proper nouns"""
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

        return "\n".join(filtered_lines)

    def to_markdown(self, text, title="Extracted Text"):
        """Convert text to markdown format"""
        return f"# {title}\n\n{text}"

    def process_image(self, image_path, output_path=None, filter_words=True):
        """Process an image and convert to markdown"""
        # Extract text from image
        extracted_text = self.extract_from_image(image_path)

        # Filter if requested
        if filter_words:
            filtered_text = self.filter_english_words(extracted_text)
        else:
            filtered_text = extracted_text

        # Format as markdown
        markdown_text = self.to_markdown(filtered_text)

        # Save to file if output path is provided
        if output_path:
            with open(output_path, "w") as md_file:
                md_file.write(markdown_text)

        return markdown_text
