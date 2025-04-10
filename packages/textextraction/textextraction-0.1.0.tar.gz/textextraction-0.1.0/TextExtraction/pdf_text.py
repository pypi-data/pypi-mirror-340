from pdfminer.high_level import extract_text
from nltk.corpus import words
import nltk
import re


class PdfText:
    def __init__(self):
        # Initialize the nltk words corpus
        self.valid_words = set(words.words())
        # Download required NLTK data (run once)
        try:
            nltk.data.find("corpora/words")
        except LookupError:
            nltk.download("words")

    def extract_from_pdf(self, pdf_path):
        """Extract text from a PDF file preserving original line breaks"""
        # Use pdfminer.six to extract text with better layout preservation
        extracted_text = extract_text(pdf_path)

        # Clean up excessive newlines while preserving paragraph structure
        # Replace 3 or more consecutive newlines with just 2
        cleaned_text = re.sub(r"\n{3,}", "\n\n", extracted_text)

        return cleaned_text

    def filter_english_words(self, text):
        """Filter text to include valid English words and proper nouns while preserving line breaks"""
        lines = text.splitlines()
        filtered_lines = []

        for line in lines:
            # If line is empty, preserve it
            if not line.strip():
                filtered_lines.append("")
                continue

            # Simple word tokenization
            words_in_line = re.findall(r"\b\w+\b", line)

            if not words_in_line:
                # If no words were found, preserve the line structure
                filtered_lines.append("")
                continue

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

        # Preserve all line breaks
        return "\n".join(filtered_lines)

    def to_markdown(self, text, title="Extracted Text"):
        """Convert text to markdown format while preserving line breaks"""
        # Replace consecutive empty lines with a special marker
        formatted_text = re.sub(r"\n\s*\n", "\n\n&nbsp;\n\n", text)

        return f"# {title}\n\n{formatted_text}"

    def process_pdf(self, pdf_path, output_path=None, filter_words=True):
        """Process a PDF and convert to markdown"""
        # Extract text from PDF
        extracted_text = self.extract_from_pdf(pdf_path)

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
