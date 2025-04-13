"""Tesseract OCR engine implementation."""

import pytesseract
import numpy as np
from PIL import Image
from .base import OCREngine


class TesseractEngine(OCREngine):
    """Tesseract OCR engine implementation.

    This class provides text extraction functionality using the Tesseract OCR engine.
    """

    def __init__(self, line_height=20):
        """Initialize the Tesseract OCR engine.

        Args:
            line_height (int, optional): The minimum height of a line of text in pixels.
                Defaults to 20.
        """
        self.line_height = line_height

        # Check if Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            raise RuntimeError(
                "Tesseract is not installed. Please install it first:\n"
                "macOS: brew install tesseract\n"
                "Ubuntu/Debian: sudo apt-get install tesseract-ocr\n"
                "Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki"
            )

    def extract_text(self, image, **kwargs):
        """Extract text from an image using Tesseract.

        Args:
            image (PIL.Image): The image to extract text from.
            **kwargs: Additional configuration parameters
                config (str): Tesseract configuration string
                lang (str): OCR language

        Returns:
            str: The extracted text with line breaks preserved.
        """
        # Convert image to RGB if it's not
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Get configuration parameters
        config = kwargs.get("config", "")
        lang = kwargs.get("lang", "eng")

        # First try to detect if the image contains a table and no config is specified
        if not config and self._detect_table(image):
            return self._process_table(image)

        # Standard text extraction
        text = pytesseract.image_to_string(image, lang=lang, config=config)
        return text

    def _detect_table(self, image):
        """Detect if the image contains a table structure.

        Args:
            image (PIL.Image): The image to check for table structure.

        Returns:
            bool: True if a table is detected, False otherwise.
        """
        # Get detailed data from Tesseract
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        # Look for structured horizontal alignment which suggests a table
        if len(data["left"]) <= 5:  # Not enough elements to form a table
            return False

        # Group text by similar y-coordinates (possible rows)
        y_coords = data["top"]
        rows = {}

        for i, y in enumerate(y_coords):
            if not data["text"][i].strip():
                continue

            # Group with tolerance for y position
            for row_y in list(rows.keys()):
                if abs(row_y - y) <= self.line_height:
                    rows[row_y].append((data["left"][i], data["text"][i]))
                    break
            else:
                rows[y] = [(data["left"][i], data["text"][i])]

        # Check if we have multiple rows with aligned text
        if len(rows) < 2:
            return False

        # Check for column alignment
        x_positions = []
        for row_data in rows.values():
            for x, _ in row_data:
                x_positions.append(x)

        # Count frequency of x positions with some tolerance
        x_clusters = {}
        tolerance = 20

        for x in x_positions:
            matched = False
            for center in list(x_clusters.keys()):
                if abs(center - x) <= tolerance:
                    x_clusters[center] += 1
                    matched = True
                    break
            if not matched:
                x_clusters[x] = 1

        # If we have multiple columns (x positions that appear frequently), likely a table
        frequent_columns = [x for x, count in x_clusters.items() if count >= 2]
        return len(frequent_columns) >= 2

    def _process_table(self, image):
        """Process an image containing a table into Markdown format.

        Args:
            image (PIL.Image): The image containing a table.

        Returns:
            str: Markdown formatted table.
        """
        # Get detailed data from Tesseract
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        # Group text by similar y-coordinates (rows)
        y_coords = data["top"]
        rows = {}

        for i, y in enumerate(y_coords):
            if not data["text"][i].strip():
                continue

            # Group with tolerance for y position
            for row_y in list(rows.keys()):
                if abs(row_y - y) <= self.line_height:
                    rows[row_y].append((data["left"][i], data["text"][i].strip()))
                    break
            else:
                rows[y] = [(data["left"][i], data["text"][i].strip())]

        # Sort rows by y-coordinate (top to bottom)
        sorted_rows = [rows[y] for y in sorted(rows.keys())]

        # For each row, sort by x-coordinate (left to right)
        for i, row in enumerate(sorted_rows):
            sorted_rows[i] = [text for _, text in sorted(row, key=lambda item: item[0])]

        # Create Markdown table
        if not sorted_rows:
            return ""

        # Build markdown table
        markdown_table = []

        # Add table rows
        for i, row in enumerate(sorted_rows):
            if not row:  # Skip empty rows
                continue

            markdown_row = "| " + " | ".join(row) + " |"
            markdown_table.append(markdown_row)

            # Add separator row after the header (first row)
            if i == 0:
                separator = "|" + "|".join(["---"] * len(row)) + "|"
                markdown_table.append(separator)

        # Return the complete table
        return "\n".join(markdown_table)
