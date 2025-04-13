"""EasyOCR engine implementation."""

import easyocr
import numpy as np
from .base import OCREngine


class EasyOCREngine(OCREngine):
    """EasyOCR engine implementation.

    This class provides text extraction functionality using the EasyOCR engine.
    The EasyOCR reader is shared across instances to avoid reinitializing.
    """

    # Class-level reader instance (shared across all instances)
    _reader = None

    def __init__(self, line_height=20, paragraph_gap=40, table_detection=True):
        """Initialize the EasyOCR engine.

        Args:
            line_height (int, optional): The minimum height of a line of text in pixels.
                Defaults to 20.
            paragraph_gap (int, optional): The minimum vertical gap in pixels to consider as a paragraph break.
                Defaults to 40.
            table_detection (bool, optional): Whether to detect and preserve tables.
                Defaults to True.
        """
        self.line_height = line_height
        self.paragraph_gap = paragraph_gap
        self.table_detection = table_detection
        if EasyOCREngine._reader is None:
            print("Initializing EasyOCR (this may take a moment)...")
            EasyOCREngine._reader = easyocr.Reader(["en"])

    def extract_text(self, image, **kwargs):
        """Extract text from an image using EasyOCR.

        Args:
            image (PIL.Image): The image to extract text from.
            **kwargs: Additional configuration parameters (not used in EasyOCR)

        Returns:
            str: The extracted text with line breaks preserved.
        """
        # Convert image to RGB if it's not
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Convert to numpy array
        img_array = np.array(image)

        # Use EasyOCR to read text
        results = self._reader.readtext(img_array)

        # Process results
        if self.table_detection and self._detect_potential_table(results):
            # Process as table
            return self._process_as_table(results)

        # Process as regular text with standard EasyOCR processing
        # Sort results by y-coordinate (top to bottom)
        results.sort(key=lambda x: x[0][0][1])  # Sort by y-coordinate of first point

        # Group text by lines based on y-coordinates
        lines = []
        current_line = []
        current_y = None

        for bbox, text, prob in results:
            # Get the y-coordinate of the text box
            y = bbox[0][1]  # y-coordinate of top-left point

            # If this is the first text or if the text is on a new line
            if current_y is None or abs(y - current_y) > self.line_height:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [text]
                current_y = y
            else:
                current_line.append(text)

        # Add the last line if there is one
        if current_line:
            lines.append(" ".join(current_line))

        # Join lines with newlines
        return "\n".join(lines)

    def _detect_potential_table(self, results):
        """Detect if the text potentially contains a table by analyzing text alignment.

        Args:
            results (list): List of text results from EasyOCR.

        Returns:
            bool: True if a potential table is detected, False otherwise.
        """
        if len(results) < 4:  # Need at least a few lines to form a table
            return False

        # Sort by y-coordinate (top to bottom)
        results_by_y = sorted(results, key=lambda x: x[0][0][1])

        # Group by similar y-coordinates (rows)
        rows = []
        current_row = [results_by_y[0]]
        current_y = results_by_y[0][0][0][1]

        for result in results_by_y[1:]:
            y = result[0][0][1]
            if abs(y - current_y) <= self.line_height:
                current_row.append(result)
            else:
                rows.append(current_row)
                current_row = [result]
                current_y = y

        if current_row:
            rows.append(current_row)

        # Check if we have at least 2 rows with multiple elements
        multi_element_rows = [row for row in rows if len(row) > 1]
        if len(multi_element_rows) < 2:
            return False

        # For table detection, check for consistent number of elements in rows
        # and alignment in x-positions
        if len(rows) >= 2:
            # Check element counts
            element_counts = [len(row) for row in rows if len(row) > 1]
            if max(element_counts) - min(element_counts) <= 1:  # Allow 1 difference
                return True

            # Collect x-positions of all text boxes
            all_x_positions = []
            for row in rows:
                for item in row:
                    all_x_positions.append(item[0][0][0])  # left-most x coordinate

            # Group x-positions by similarity
            x_clusters = {}
            tolerance = self.line_height  # Use line height as horizontal tolerance too

            for x in sorted(all_x_positions):
                matched = False
                for center in list(x_clusters.keys()):
                    if abs(center - x) <= tolerance:
                        x_clusters[center].append(x)
                        matched = True
                        break
                if not matched:
                    x_clusters[x] = [x]

            # Check if we have multiple consistent columns
            strong_columns = [
                col for col, items in x_clusters.items() if len(items) >= 2
            ]
            if len(strong_columns) >= 2:
                return True

        return False

    def _process_as_table(self, results):
        """Process and format text as a Markdown table.

        Args:
            results (list): List of text results from EasyOCR.

        Returns:
            str: Formatted Markdown table.
        """
        # Sort by y-coordinate (top to bottom)
        results_by_y = sorted(results, key=lambda x: x[0][0][1])

        # Group by similar y-coordinates (rows)
        rows = []
        tolerance = self.line_height

        # First, determine the row centers
        y_positions = [r[0][0][1] for r in results_by_y]
        y_clusters = {}

        for y in y_positions:
            matched = False
            for center in list(y_clusters.keys()):
                if abs(center - y) <= tolerance:
                    y_clusters[center].append(y)
                    matched = True
                    break
            if not matched:
                y_clusters[y] = [y]

        # Sort the cluster centers by y-coordinate
        row_centers = sorted(y_clusters.keys())

        # Now assign text boxes to rows based on their proximity to row centers
        row_contents = {y: [] for y in row_centers}

        for result in results_by_y:
            y = result[0][0][1]
            # Find closest row center
            closest_center = min(row_centers, key=lambda c: abs(c - y))
            row_contents[closest_center].append(result)

        # Get the x-positions of all text boxes for column detection
        all_x_positions = []
        for result in results_by_y:
            all_x_positions.append(result[0][0][0])  # left-most x coordinate

        # Determine column boundaries
        x_clusters = {}
        x_tolerance = tolerance

        for x in sorted(all_x_positions):
            matched = False
            for center in list(x_clusters.keys()):
                if abs(center - x) <= x_tolerance:
                    x_clusters[center].append(x)
                    matched = True
                    break
            if not matched:
                x_clusters[x] = [x]

        # Sort column centers
        column_centers = sorted(x_clusters.keys())

        # Process each row to organize by columns
        final_rows = []
        max_columns = len(column_centers)

        for center in row_centers:
            row_data = row_contents[center]
            # For each column, find the closest text box
            row_cells = [""] * max_columns

            for result in row_data:
                x = result[0][0][0]
                # Find closest column center
                closest_col_idx = min(
                    range(len(column_centers)), key=lambda i: abs(column_centers[i] - x)
                )
                # If cell already has content, append with space
                if row_cells[closest_col_idx]:
                    row_cells[closest_col_idx] += " " + result[1]
                else:
                    row_cells[closest_col_idx] = result[1]

            final_rows.append(row_cells)

        # Create Markdown table, ensuring it has at least 2 rows
        if len(final_rows) < 2:
            # If we only have one row, duplicate it and make the first one the header
            if len(final_rows) == 1:
                final_rows.append(final_rows[0].copy())
            else:
                return ""  # No valid rows

        # Build the markdown table
        markdown_table = []

        # Add table rows
        for i, row in enumerate(final_rows):
            markdown_row = "| " + " | ".join(row) + " |"
            markdown_table.append(markdown_row)

            # Add separator after header
            if i == 0:
                separator = "|" + "|".join(["---"] * len(row)) + "|"
                markdown_table.append(separator)

        # Return the complete table with a newline before and after
        return "\n" + "\n".join(markdown_table) + "\n"
