import os
import re
import logging

from ._markdown_output import MarkdownOutput


class PdfText:
    """
    Class for extracting text from regular PDFs (not scanned PDFs).
    Uses pdfplumber for text and table extraction.
    """

    def __init__(
        self,
        add_page_number=False,
        dictionary=False,
        add_metadata=True,
        table_detection=True,
    ):
        """
        Initialize the PdfText processor.

        Args:
            add_page_number (bool): Whether to add page numbers to the output.
            dictionary (bool): Whether to filter out non-English words.
            add_metadata (bool): Whether to add metadata to the markdown output.
            table_detection (bool): Whether to detect and extract tables from the PDF.
        """
        self.add_page_number = add_page_number
        self.dictionary = dictionary
        self.add_metadata = add_metadata
        self.table_detection = table_detection

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Initialize markdown output processor
        self.markdown_output = MarkdownOutput(add_metadata=self.add_metadata)

        # English dictionary will be lazy loaded when needed
        self.english_words = None

    def _load_dictionary(self):
        """
        Lazy load the NLTK dictionary only when needed.

        Returns:
            set: A set of lowercase English words.
        """
        if self.english_words is None:
            self.logger.info("Loading English dictionary")

            try:
                from nltk.corpus import words as nltk_words
                import nltk

                try:
                    nltk.data.find(resource_name="words/english")
                except LookupError:
                    self.logger.info("Downloading NLTK words dictionary")
                    nltk.download(info_or_id="words", quiet=True)

                self.english_words = set(w.lower() for w in nltk_words.words())
                self.logger.info(f"Loaded {len(self.english_words)} English words")
            except Exception as e:
                self.logger.error(f"Error loading dictionary: {e}")
                self.english_words = set()  # Empty set as fallback

        return self.english_words

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

        # Ensure dictionary is loaded
        english_words = self._load_dictionary()
        if not english_words:
            self.logger.warning("Dictionary is empty, returning original text")
            return text

        self.logger.info("Filtering non-English words")
        words = re.findall(r"\b[a-zA-Z]+\b", text)
        english_words_only = [word for word in words if word.lower() in english_words]

        if not english_words_only:
            self.logger.warning("No English words found after filtering")
            return text  # Return original if no words left after filtering

        self.logger.info(
            f"Filtered {len(words) - len(english_words_only)} non-English words"
        )
        return " ".join(english_words_only)

    def _extract_tables_from_page(self, page):
        """
        Extract tables from a page using pdfplumber.

        Args:
            page: pdfplumber page object.

        Returns:
            list: List of tables in markdown format.
        """
        try:
            tables = page.extract_tables()
            if not tables:
                return []

            markdown_tables = []
            for i, table in enumerate(tables):
                # Convert table to markdown format
                if not table:
                    continue

                markdown_rows = []
                # Add header row
                markdown_rows.append(
                    "| " + " | ".join([str(cell or "") for cell in table[0]]) + " |"
                )

                # Add separator row
                markdown_rows.append(
                    "| " + " | ".join(["---" for _ in table[0]]) + " |"
                )

                # Add data rows
                for row in table[1:]:
                    markdown_rows.append(
                        "| " + " | ".join([str(cell or "") for cell in row]) + " |"
                    )

                table_markdown = "\n".join(markdown_rows)
                markdown_tables.append(f"\n\n{table_markdown}\n\n")

            return markdown_tables

        except Exception as e:
            self.logger.error(f"Error extracting tables: {e}")
            return []

    def extract_from_pdf(self, pdf_path, start_page=0, end_page=None, dictionary=None):
        """
        Extract text from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.
            start_page (int): Page to start extraction from (0-indexed).
            end_page (int): Page to end extraction at (inclusive, 0-indexed).
            dictionary (bool): If True, filter out non-English words.

        Returns:
            str: The extracted text.
        """
        # Validate input
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return ""

        # Use provided dictionary parameter or fallback to instance property
        use_dictionary = self.dictionary if dictionary is None else dictionary

        try:
            # Import pdfplumber lazily
            import pdfplumber

            self.logger.info(f"Opening PDF: {pdf_path}")
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                self.logger.info(f"PDF has {total_pages} pages")

                # Validate page range
                if end_page is None or end_page >= total_pages:
                    end_page = total_pages - 1

                if start_page < 0:
                    start_page = 0

                if start_page > end_page:
                    self.logger.error(
                        f"Invalid page range: start_page ({start_page}) > end_page ({end_page})"
                    )
                    return ""

                self.logger.info(f"Extracting pages {start_page+1} to {end_page+1}")
                extracted_text = []

                # Process each page
                for page_num in range(start_page, end_page + 1):
                    self.logger.info(f"Processing page {page_num+1}")
                    page = pdf.pages[page_num]

                    # Extract tables from the page if table_detection is enabled
                    tables = []
                    if self.table_detection:
                        tables = self._extract_tables_from_page(page)

                    # Extract text from the page
                    text = page.extract_text() or ""

                    # Filter out non-English words if requested
                    if use_dictionary:
                        text = self._filter_non_english_words(text)

                    # Add page numbers if requested
                    if self.add_page_number:
                        page_header = f"\n\n## Page {page_num + 1}\n\n"
                        page_content = page_header + text
                    else:
                        page_content = text

                    # Add tables to the page content if table_detection is enabled
                    if tables:
                        self.logger.info(
                            f"Found {len(tables)} tables on page {page_num+1}"
                        )
                        page_content += "\n" + "".join(tables)

                    extracted_text.append(page_content)

                self.logger.info(
                    f"Extraction complete: {len(extracted_text)} pages processed"
                )
                return "\n".join(extracted_text)

        except ImportError as e:
            self.logger.error(f"Required library not installed: {e}")
            return f"Error: Required library not installed: {e}"
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {e}")
            return f"Error extracting text: {str(e)}"

    def process(self, input_path, output_path=None, start_page=0, end_page=None):
        """
        Process a PDF file and extract text with improved markdown formatting.

        Args:
            input_path (str): Path to the PDF file.
            output_path (str, optional): Path to save the extracted text. If None, text is not saved.
            start_page (int): Page to start extraction from (0-indexed).
            end_page (int): Page to end extraction at (inclusive, 0-indexed).

        Returns:
            str: The extracted text.
        """
        # Extract text from the PDF
        text = self.extract_from_pdf(input_path, start_page, end_page)

        # Clean up the text for better markdown formatting
        if text:
            # Improve table formatting
            # Remove any empty table rows (rows with only | characters)
            lines = text.split("\n")
            formatted_lines = []
            for line in lines:
                # Skip empty table rows (rows with only | characters and spaces)
                if line.strip().startswith("|") and line.strip().endswith("|"):
                    # Check if the row is empty (contains only |, spaces, and -)
                    content = line.strip()[1:-1].strip()
                    if not content or all(c in "|- " for c in content):
                        continue
                formatted_lines.append(line)

            text = "\n".join(formatted_lines)

            # Ensure proper spacing around tables
            # Add a blank line before and after tables for better markdown rendering
            text = text.replace("\n\n|", "\n\n|")  # Ensure proper spacing before tables
            text = text.replace("|\n\n", "|\n\n")  # Ensure proper spacing after tables

            # Fix any double pipe characters that might have been introduced
            text = text.replace("||", "|")

        # Save to markdown file if output path is provided
        if output_path:
            self.markdown_output.save_markdown(
                text=text,
                output_path=output_path,
                title=f"Extracted Text from {os.path.basename(input_path)}",
                source_file=input_path,
            )

        return text
