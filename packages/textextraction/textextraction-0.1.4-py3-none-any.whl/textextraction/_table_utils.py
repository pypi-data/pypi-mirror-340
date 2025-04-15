import logging


class TableUtils:
    """
    Utility class for detecting and extracting tables from images using OpenCV.
    """

    def __init__(self, ocr_engine="easyocr", table_detection=True):
        """
        Initialize the TableUtils processor.

        Args:
            ocr_engine (str): OCR engine to use for text extraction.
            table_detection (bool): Whether to detect tables.
        """
        self.ocr_engine = ocr_engine
        self.table_detection = table_detection
        self.table_processor = None

        # Setup logging
        self.logger = logging.getLogger(__name__)

    def detect_table(self, image):
        """
        Detect if an image contains a table using OpenCV.

        Args:
            image: PIL Image object or numpy array.

        Returns:
            bool: True if a table is detected, False otherwise.
        """
        if not self.table_detection:
            return False

        # Lazy import numpy and cv2
        import numpy as np
        import cv2

        # Convert PIL Image to numpy array if needed
        from PIL import Image

        if isinstance(image, Image.Image):
            image_np = np.array(image)
        else:
            image_np = image

        # Convert to grayscale if it's a color image
        if len(image_np.shape) == 3:
            gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_np

        # Apply adaptive threshold to get binary image
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        # Detect horizontal lines
        horizontal = np.copy(binary)
        horizontalsize = int(horizontal.shape[1] / 30)
        horizontalStructure = cv2.getStructuringElement(
            cv2.MORPH_RECT, (horizontalsize, 1)
        )
        horizontal = cv2.erode(horizontal, horizontalStructure)
        horizontal = cv2.dilate(horizontal, horizontalStructure)

        # Detect vertical lines
        vertical = np.copy(binary)
        verticalsize = int(vertical.shape[0] / 30)
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
        vertical = cv2.erode(vertical, verticalStructure)
        vertical = cv2.dilate(vertical, verticalStructure)

        # Count horizontal and vertical lines
        h_lines = cv2.HoughLinesP(
            horizontal, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10
        )
        v_lines = cv2.HoughLinesP(
            vertical, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10
        )

        # Check if enough lines to constitute a table
        h_count = 0 if h_lines is None else len(h_lines)
        v_count = 0 if v_lines is None else len(v_lines)

        # Table requires at least 3 horizontal and 3 vertical lines
        return h_count >= 3 and v_count >= 3

    def extract_table(self, image):
        """
        Extract table data from an image and format as markdown.

        Args:
            image: PIL Image object or numpy array.

        Returns:
            str: Markdown formatted table.
        """
        # First try to use camelot-py for table extraction if available
        try:
            import camelot
            import tempfile
            import os

            # Save the image as a temporary PDF
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                temp_pdf_path = temp_pdf.name

            # Convert PIL Image to PDF
            from PIL import Image

            if isinstance(image, Image.Image):
                image.save(temp_pdf_path, "PDF")
            else:
                # Convert numpy array to PIL Image
                img = Image.fromarray(image)
                img.save(temp_pdf_path, "PDF")

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
        if not self.table_processor:
            self.logger.error("Table processor not initialized")
            return "Table detected but OCR processor not available"

        # Use OCR to extract text from the table
        reader = self.table_processor.reader

        # Lazy import numpy
        import numpy as np

        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image

        # Extract text with EasyOCR
        results = reader.readtext(img_array)

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
            cells = [item[1] for item in sorted_items]

            # Format the row with proper | placement
            if i == 0:
                # Header row
                markdown_table += "| " + " | ".join(cells) + " |\n"
                # Separator row
                markdown_table += "| " + " | ".join(["---" for _ in cells]) + " |\n"
            else:
                # Data row
                markdown_table += "| " + " | ".join(cells) + " |\n"

        return markdown_table

    def set_table_processor(self, processor):
        """
        Set the OCR processor for table text extraction.

        Args:
            processor: The OCR processor (ImageText instance).
        """
        self.table_processor = processor
