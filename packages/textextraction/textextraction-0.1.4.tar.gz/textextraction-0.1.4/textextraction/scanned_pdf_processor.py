import os
import logging

from ._table_utils import TableUtils
from ._markdown_output import MarkdownOutput


class ScannedPdfText:
    """
    Class for extracting text from scanned PDFs.
    Supports both Tesseract and EasyOCR engines and table detection.
    """

    def __init__(
        self,
        ocr_engine="easyocr",
        add_page_number=False,
        dictionary=False,
        table_detection=True,
        add_metadata=True,
    ):
        """
        Initialize the ScannedPdfText processor.

        Args:
            ocr_engine (str): OCR engine to use ('tesseract' or 'easyocr').
            add_page_number (bool): Whether to add page numbers to the output.
            dictionary (bool): Whether to filter out non-English words.
            table_detection (bool): Whether to detect tables in the PDF.
            add_metadata (bool): Whether to add metadata to the markdown output.
        """
        self.ocr_engine = ocr_engine.lower()
        self.add_page_number = add_page_number
        self.dictionary = dictionary
        self.table_detection = table_detection
        self.add_metadata = add_metadata

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Initialize components lazily as needed
        self.image_processor = None
        self.table_utils = None
        self.markdown_output = MarkdownOutput(add_metadata=self.add_metadata)

    def _init_image_processor(self):
        """Lazy load the ImageText class for OCR processing."""
        from .image_processor import ImageText

        self.image_processor = ImageText(
            ocr_engine=self.ocr_engine, dictionary=self.dictionary
        )
        return self.image_processor

    def _init_table_utils(self):
        """Initialize TableUtils for table detection and extraction."""
        # Initialize table processor first
        if not hasattr(self, "table_processor") or self.table_processor is None:
            self.table_processor = self._init_table_processor()

        # Only proceed with TableUtils initialization if table processor is ready
        if self.table_processor is not None:
            self.table_utils = TableUtils(
                ocr_engine=self.ocr_engine, table_detection=self.table_detection
            )
            # Set the table processor in TableUtils
            self.table_utils.set_table_processor(self.table_processor)
            return self.table_utils
        else:
            self.logger.error("Failed to initialize table processor")
            return None

    def _init_table_processor(self):
        """Initialize the table processor for extracting table content."""
        from .image_processor import ImageText

        # Always create a new ImageText instance with easyocr for tables
        table_processor = ImageText(ocr_engine="easyocr")

        # Ensure the reader is properly initialized
        if not hasattr(table_processor, "reader") or table_processor.reader is None:
            self.logger.error("Failed to initialize table processor")
            return None

        self.table_processor = table_processor
        return self.table_processor

    def extract_from_pdf(self, pdf_path, start_page=0, end_page=None, dictionary=None):
        """
        Extract text from a scanned PDF file.

        Args:
            pdf_path (str): Path to the PDF file.
            start_page (int): Page to start extraction from (0-indexed).
            end_page (int): Page to end extraction at (inclusive, 0-indexed).
            dictionary (bool): If True, filter out non-English words.

        Returns:
            str: The extracted text.
        """
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return ""

        # Use the provided dictionary value or fallback to the instance value
        dictionary = self.dictionary if dictionary is None else dictionary

        # Initialize the image processor if needed
        if self.image_processor is None:
            self._init_image_processor()

        try:
            # Lazy import fitz and pdf2image
            import fitz
            import pdf2image

            # Open the PDF file
            pdf_doc = fitz.open(pdf_path)
            total_pages = len(pdf_doc)

            # Validate page range
            if end_page is None or end_page >= total_pages:
                end_page = total_pages - 1

            if start_page < 0:
                start_page = 0

            if start_page > end_page:
                self.logger.error("Start page cannot be greater than end page")
                return ""

            # Convert PDF pages to images
            self.logger.info(
                f"Converting PDF pages {start_page+1} to {end_page+1} to images"
            )
            pages = pdf2image.convert_from_path(
                pdf_path,
                first_page=start_page + 1,  # pdf2image is 1-indexed
                last_page=end_page + 1,
            )

            extracted_text = []

            # Process each page
            for i, page in enumerate(pages):
                # Use sequential page numbers (1, 2, 3, etc.) instead of document page numbers
                page_num = start_page + i
                self.logger.info(f"Processing page {page_num+1}")

                # Check if page contains a table
                is_table = False
                if self.table_detection:
                    # Initialize table utils if needed
                    if self.table_utils is None:
                        self.table_utils = self._init_table_utils()
                        if self.table_utils is None:
                            self.logger.warning(
                                "Table detection disabled due to initialization failure"
                            )
                            self.table_detection = False

                    # Detect tables only if initialization was successful
                    if self.table_utils is not None:
                        is_table = self.table_utils.detect_table(page)
                        self.logger.info(
                            f"Table detection result for page {page_num+1}: {is_table}"
                        )

                # Extract text from the page
                if is_table and self.table_utils is not None:
                    text = self.table_utils.extract_table(page)
                    self.logger.info(f"Table extracted from page {page_num+1}")
                else:
                    text = self.image_processor.extract_from_pil_image(page, dictionary)
                    self.logger.info(f"Text extracted from page {page_num+1}")

                # Add page numbers if requested
                if self.add_page_number:
                    page_header = f"\n\n## Page {page_num + 1}\n\n"
                    extracted_text.append(page_header + text)
                else:
                    extracted_text.append(text)

            return "\n".join(extracted_text)

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
        text = self.extract_from_pdf(input_path, start_page, end_page, self.dictionary)

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

    def _extract_table(self, image):
        """
        Extract table content from an image using OCR.

        Args:
            image: PIL Image object.

        Returns:
            str: Extracted table in markdown format.
        """
        try:
            # First try to use camelot-py for table extraction if available
            try:
                import camelot
                import tempfile
                import os

                # Save the image as a temporary PDF
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as temp_pdf:
                    temp_pdf_path = temp_pdf.name

                # Convert PIL image to PDF
                image.save(temp_pdf_path, "PDF")

                # Extract tables using camelot
                tables = camelot.read_pdf(temp_pdf_path, pages="1", flavor="lattice")

                # Clean up temporary file
                os.unlink(temp_pdf_path)

                if len(tables) > 0:
                    # Convert the first table to markdown
                    table = tables[0]
                    markdown_table = table.df.to_markdown(index=False)
                    return markdown_table
            except ImportError:
                self.logger.info(
                    "camelot-py not available, falling back to OCR-based extraction"
                )
            except Exception as e:
                self.logger.warning(f"Error using camelot for table extraction: {e}")

            # Fall back to OCR-based extraction if camelot fails or is not available
            if self.ocr_engine == "tesseract":
                # Use Tesseract OCR
                import pytesseract
                import numpy as np

                # Convert PIL Image to numpy array
                img_array = np.array(image)

                # Extract text with table structure
                text = pytesseract.image_to_string(img_array, config="--psm 6")

                # Process the text to create a markdown table
                lines = text.strip().split("\n")
                if len(lines) < 2:
                    return text  # Not enough lines for a table

                # Find the header row (usually the first non-empty line)
                header_row = None
                for line in lines:
                    if line.strip():
                        header_row = line.strip()
                        break

                if not header_row:
                    return text  # No header row found

                # Create markdown table
                markdown_table = f"| {header_row} |\n"
                markdown_table += (
                    f"| {' | '.join(['---' for _ in header_row.split()])} |\n"
                )

                # Add data rows
                for line in lines[1:]:
                    if line.strip():
                        markdown_table += f"| {line.strip()} |\n"

                return markdown_table
            else:
                # Use EasyOCR
                if (
                    not hasattr(self.table_processor, "reader")
                    or self.table_processor.reader is None
                ):
                    self.logger.error("OCR reader not initialized")
                    return "Error: OCR reader not initialized"

                # Convert PIL Image to numpy array
                import numpy as np

                img_array = np.array(image)

                # Extract text with EasyOCR
                results = self.table_processor.reader.readtext(img_array)

                # Process the results to create a markdown table
                if not results:
                    return "No text detected in the table"

                # Group text by y-coordinate to identify rows
                rows = {}
                for bbox, text, prob in results:
                    y_coord = bbox[0][1]  # Top-left y-coordinate
                    # Round to nearest 10 pixels to group text on the same line
                    y_group = round(y_coord / 10) * 10
                    if y_group not in rows:
                        rows[y_group] = []
                    rows[y_group].append((bbox[0][0], text))  # x-coordinate and text

                # Sort rows by y-coordinate
                sorted_rows = sorted(rows.items(), key=lambda x: x[0])

                # Create markdown table
                markdown_table = ""
                for i, (_, row_items) in enumerate(sorted_rows):
                    # Sort items in the row by x-coordinate
                    sorted_items = sorted(row_items, key=lambda x: x[0])
                    row_text = " | ".join([item[1] for item in sorted_items])

                    if i == 0:
                        # Header row
                        markdown_table += f"| {row_text} |\n"
                        # Separator row
                        markdown_table += f"| {' | '.join(['---' for _ in row_text.split(' | ')])} |\n"
                    else:
                        # Data row
                        markdown_table += f"| {row_text} |\n"

                return markdown_table

        except Exception as e:
            self.logger.error(f"Error extracting table: {e}")
            return f"Error extracting table: {str(e)}"
