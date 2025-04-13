from .utils import get_valid_words, filter_english_words
import numpy as np
import cv2

# PyMuPDF is imported as fitz, but we'll import it inside methods with error handling
from PIL import Image
import io


class ScannedPdfText:
    def __init__(
        self,
        ocr_engine="easyocr",
        line_height=20,
        table_detection=True,
        filter_words=False,
        add_page_number=False,
    ):
        """Initialize the ScannedPdfText processor.

        Args:
            ocr_engine (str, optional): The OCR engine to use.
                Options: "tesseract" or "easyocr". Defaults to "easyocr".
            line_height (int, optional): Maximum vertical distance between
                text elements to be considered part of the same line.
                Defaults to 20 pixels.
            table_detection (bool, optional): Whether to enable table detection.
                Defaults to True.
            filter_words (bool, optional): Whether to filter out non-English words.
                Defaults to False.
            add_page_number (bool, optional): Whether to add page numbers to extracted text.
                Defaults to False.
        """
        # Initialize valid words set
        self.valid_words = get_valid_words()
        self.table_detection = table_detection
        self.ocr_engine_name = ocr_engine
        self.filter_words = filter_words
        self.add_page_number = add_page_number

        # Table detection works best with EasyOCR
        self.table_detection_engine = "easyocr"

        # Initialize OCR engine
        self.ocr_engine = self._get_ocr_engine(ocr_engine, line_height)

        # If table detection is enabled and using Tesseract, also initialize EasyOCR for tables
        if self.table_detection and ocr_engine == "tesseract":
            self.table_ocr_engine = self._get_ocr_engine("easyocr", line_height)
        else:
            self.table_ocr_engine = self.ocr_engine

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
        # Use absolute imports instead of relative imports
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

        # Only pass table_detection parameter to EasyOCR engine
        if engine_name == "easyocr":
            return engine_class(
                line_height=line_height, table_detection=self.table_detection
            )
        else:
            return engine_class(line_height=line_height)

    def extract_from_pdf(self, pdf_path, start_page=None, end_page=None):
        """Extract text from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.
            start_page (int, optional): First page to extract (1-indexed). Defaults to None.
            end_page (int, optional): Last page to extract (1-indexed). Defaults to None.

        Returns:
            str: Extracted text.
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF is required for PDF processing. "
                "Please install it with 'pip install pymupdf'"
            )

        import cv2
        import numpy as np
        from PIL import Image
        import os
        import time

        pdf_document = fitz.open(pdf_path)

        # Normalize page range
        start_page = max(1, start_page or 1)
        end_page = min(pdf_document.page_count, end_page or pdf_document.page_count)

        # Adjust for 0-indexed pages in PyMuPDF
        start_page -= 1
        end_page -= 1

        print(
            f"Extracting text from PDF: {pdf_path} (pages {start_page+1} to {end_page+1})"
        )

        full_text = []

        for page_num in range(start_page, end_page + 1):
            print(f"Processing page {page_num+1}/{end_page+1}")

            current_page = pdf_document[page_num]

            # Convert page to an image
            pix = current_page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Extract text using selected OCR engine for the whole page
            print(f"  Extracting text with {self.ocr_engine_name} OCR")

            # Convert to numpy array for processing if table detection is enabled
            if self.table_detection:
                np_img = np.array(img)
                gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
                # Analyze image for table-like structures
                regions = self._analyze_page_structure(gray, img.width, img.height)

                if regions:
                    print(
                        f"  Detected {len(regions['tables'])} potential tables and {len(regions['text'])} text regions"
                    )
                    page_text = self._process_structured_page(img, np_img, regions)
                else:
                    # No tables detected, process as regular text
                    page_text = self.ocr_engine.extract_text(img)
            else:
                # No table detection, just extract text normally
                page_text = self.ocr_engine.extract_text(img)

            # Apply word filtering if requested and we have text to filter
            if self.filter_words and page_text:
                page_text = filter_english_words(page_text)

            # Add page number if requested
            if self.add_page_number:
                page_text = f"# Page {page_num+1}\n\n{page_text}"

            full_text.append(page_text)

        # Close the PDF document
        pdf_document.close()

        return "\n\n".join(full_text)

    def _analyze_page_structure(self, gray_img, width, height):
        """Analyze page structure to identify text and table regions.

        Args:
            gray_img: Grayscale image (numpy array)
            width: Image width
            height: Image height

        Returns:
            dict: Dictionary with 'tables' and 'text' regions
        """
        import cv2

        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY_INV)

        # Detect tables
        tables = []

        # Detect line segments that could form tables
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

        # Detect horizontal and vertical lines
        horizontal_lines = cv2.morphologyEx(
            binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
        )
        vertical_lines = cv2.morphologyEx(
            binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2
        )

        # Combine lines
        table_mask = cv2.bitwise_or(horizontal_lines, vertical_lines)

        # Dilate to connect nearby lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(table_mask, kernel, iterations=2)

        # Find contours of potential table regions
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Minimum table size (2% of page)
        min_table_area = width * height * 0.02

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            aspect_ratio = w / float(h) if h > 0 else 0

            # Tables typically have reasonable aspect ratio and size
            if area > min_table_area and 0.2 < aspect_ratio < 10:
                # Further analyze to confirm it's a table
                roi = binary[y : y + h, x : x + w]

                # Check for grid-like structure (multiple h/v lines)
                h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(w / 10), 1))
                v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(h / 10)))

                h_lines = cv2.morphologyEx(roi, cv2.MORPH_OPEN, h_kernel)
                v_lines = cv2.morphologyEx(roi, cv2.MORPH_OPEN, v_kernel)

                # Count lines
                h_contours, _ = cv2.findContours(
                    h_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )
                v_contours, _ = cv2.findContours(
                    v_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                # Require at least 2 horizontal and 2 vertical lines for a table
                if len(h_contours) >= 2 and len(v_contours) >= 2:
                    tables.append((x, y, w, h))
                    print(f"    Table detected: x={x}, y={y}, w={w}, h={h}")

        # Find text regions (if any) - exclude table regions
        text_regions = []

        # If there are tables, consider gaps between tables as text regions
        if tables:
            # Sort tables by y-coordinate
            tables.sort(key=lambda t: t[1])

            # Text above first table
            if tables[0][1] > 50:  # At least 50px from top
                text_regions.append((0, 0, width, tables[0][1]))

            # Text between tables
            for i in range(len(tables) - 1):
                t1_bottom = tables[i][1] + tables[i][3]
                t2_top = tables[i + 1][1]

                if t2_top - t1_bottom > 50:  # At least 50px gap
                    text_regions.append((0, t1_bottom, width, t2_top - t1_bottom))

            # Text after last table
            last_table_bottom = tables[-1][1] + tables[-1][3]
            if height - last_table_bottom > 50:  # At least 50px to bottom
                text_regions.append(
                    (0, last_table_bottom, width, height - last_table_bottom)
                )
        else:
            # No tables, the entire page is text
            text_regions.append((0, 0, width, height))

        return {"tables": tables, "text": text_regions}

    def _process_structured_page(self, img, np_img, regions):
        """Process a page with identified structure (text and table regions).

        Args:
            img: PIL Image
            np_img: NumPy array of image
            regions: Dict with 'tables' and 'text' regions

        Returns:
            str: Processed text with tables in markdown format
        """
        # Process each region in order by y-coordinate
        all_regions = []

        # Add text regions with type
        for x, y, w, h in regions["text"]:
            all_regions.append(("text", x, y, w, h))

        # Add table regions with type
        for x, y, w, h in regions["tables"]:
            all_regions.append(("table", x, y, w, h))

        # Sort by y-coordinate
        all_regions.sort(key=lambda r: r[2])

        # Process each region
        processed_parts = []

        for region_type, x, y, w, h in all_regions:
            # Extract region
            region_img = img.crop((x, y, x + w, y + h))

            if region_type == "text":
                # Process as text with the primary OCR engine
                text = self.ocr_engine.extract_text(region_img)
                processed_parts.append(text)
            else:
                # Process as table with the table OCR engine (EasyOCR)
                print(f"    Processing table region: {w}x{h}")
                # Always use the table OCR engine (EasyOCR) for tables
                table_markdown = self._process_table_region(region_img)
                if table_markdown:
                    processed_parts.append(table_markdown)

        # Join all parts with appropriate spacing
        return "\n\n".join(processed_parts)

    def _process_table_region(self, image):
        """Process a potential table region and extract text in a table format.

        Args:
            image: PIL image containing a potential table region

        Returns:
            str: Markdown formatted table or empty string if no table was detected
        """
        # Always use EasyOCR for table detection as it produces better results
        return self._process_table_region_easyocr(image)

    def _process_table_region_with_engine(self, image, engine_name):
        """Process a table region using the specified engine.

        This is a fallback method to process tables with either engine if needed.

        Args:
            image: PIL image containing a potential table region
            engine_name: Name of the OCR engine to use

        Returns:
            str: Markdown formatted table
        """
        if engine_name == "tesseract":
            return self._process_table_region_tesseract(image)
        else:
            return self._process_table_region_easyocr(image)

    def _process_table_region_tesseract(self, image):
        """Process a table region using Tesseract with specific optimizations.

        Args:
            image: PIL image containing a potential table region

        Returns:
            str: Markdown formatted table
        """
        import cv2
        import numpy as np

        # Convert PIL image to OpenCV format
        img_np = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Invert for line detection (white lines on black background)
        thresh_inv = cv2.bitwise_not(thresh)

        # Detect horizontal and vertical lines
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image.width / 10), 1))
        v_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (1, int(image.height / 10))
        )

        h_lines = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, h_kernel, iterations=1)
        v_lines = cv2.morphologyEx(thresh_inv, cv2.MORPH_OPEN, v_kernel, iterations=1)

        # Combine horizontal and vertical lines
        table_structure = cv2.bitwise_or(h_lines, v_lines)

        # Find contours of the table cells
        contours, _ = cv2.findContours(
            table_structure, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        # If we found cell contours, extract text from each cell
        if len(contours) > 4:  # At least enough contours for a 2x2 table
            # Extract table cells (bounding boxes)
            cells = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # Filter out very small boxes or boxes that are likely the table border
                if (
                    w > 20
                    and h > 20
                    and w < image.width * 0.9
                    and h < image.height * 0.9
                ):
                    cells.append((x, y, w, h))

            # If we don't have enough cells, use grid-based approach
            if len(cells) < 4:
                # Fall back to analyzing the whole region without grid detection
                return self._extract_table_without_grid_tesseract(image)

            # Sort cells by y-coordinate to group into rows
            cells.sort(key=lambda cell: cell[1])

            # Group cells into rows
            rows = []
            current_row = [cells[0]]
            row_top = cells[0][1]

            for cell in cells[1:]:
                # If this cell is approximately on the same row
                if abs(cell[1] - row_top) < image.height * 0.05:  # 5% tolerance
                    current_row.append(cell)
                else:
                    # Sort this row's cells by x-coordinate
                    current_row.sort(key=lambda cell: cell[0])
                    rows.append(current_row)
                    # Start a new row
                    current_row = [cell]
                    row_top = cell[1]

            # Add the last row
            if current_row:
                current_row.sort(key=lambda cell: cell[0])
                rows.append(current_row)

            # Now extract text from each cell
            table_data = []
            for row in rows:
                row_data = []
                for x, y, w, h in row:
                    # Extract cell image
                    cell_img = image.crop((x, y, x + w, y + h))

                    try:
                        # Call with config as a keyword argument
                        ocr_config = "--psm 6"  # Assume a single uniform block of text
                        cell_text = self.ocr_engine.extract_text(
                            cell_img, config=ocr_config
                        )
                        # Clean up the text
                        cell_text = cell_text.strip().replace("\n", " ")
                        row_data.append(cell_text)
                    except Exception as e:
                        # In case of error, add empty cell
                        print(f"Error processing cell: {e}")
                        row_data.append("")

                if row_data:
                    table_data.append(row_data)

            return self._format_to_markdown_table(table_data)
        else:
            # Fall back to analyzing the whole region without grid detection
            return self._extract_table_without_grid_tesseract(image)

    def _extract_table_without_grid_tesseract(self, image):
        """Extract a table without relying on grid detection, optimized for Tesseract.

        Args:
            image: PIL image of table region

        Returns:
            str: Markdown table
        """
        import numpy as np
        import cv2
        import pytesseract

        # Apply preprocessing to improve OCR quality for tables
        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Enhance image for better OCR
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Apply light denoising
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)

        # Convert back to PIL for OCR
        enhanced_pil = Image.fromarray(denoised)

        # Use Tesseract's built-in table extraction capability directly
        try:
            # Try to use the Tesseract data API to get table structure
            data = pytesseract.image_to_data(
                enhanced_pil, output_type=pytesseract.Output.DICT
            )

            # Group text by y-coordinates (rows)
            rows = {}
            line_height = 10  # Minimum height difference to consider a new row

            # Filter out empty text entries
            filtered_indices = [
                i for i, text in enumerate(data["text"]) if text.strip()
            ]

            for i in filtered_indices:
                y = data["top"][i]
                text = data["text"][i].strip()
                x = data["left"][i]

                # Find the row this text belongs to
                matched = False
                for row_y in list(rows.keys()):
                    if abs(row_y - y) < line_height:
                        rows[row_y].append((x, text))
                        matched = True
                        break

                if not matched:
                    rows[y] = [(x, text)]

            # Sort rows by y position
            sorted_y = sorted(rows.keys())

            if len(sorted_y) <= 1:
                # Not enough rows, try other method
                return self._extract_table_using_text_layout(enhanced_pil)

            # For each row, sort text by x-coordinate
            table_data = []
            for y in sorted_y:
                row_texts = [
                    text for _, text in sorted(rows[y], key=lambda item: item[0])
                ]
                if row_texts:
                    table_data.append(row_texts)

            # For very simple cases, try to improve column detection
            if all(len(row) == 1 for row in table_data):
                # Only single column detected - try splitting by spaces
                improved_table = []
                for row in table_data:
                    text = row[0]
                    parts = text.split()
                    # Simple heuristic: if we have 2-6 parts, treat as separate columns
                    if 2 <= len(parts) <= 6:
                        improved_table.append(parts)
                    else:
                        improved_table.append(row)

                if any(len(row) > 1 for row in improved_table):
                    table_data = improved_table

            # Normalize table (make all rows have same number of columns)
            max_cols = max(len(row) for row in table_data) if table_data else 0
            for i in range(len(table_data)):
                while len(table_data[i]) < max_cols:
                    table_data[i].append("")

            return self._format_to_markdown_table(table_data)

        except Exception as e:
            # Fall back to basic text parsing
            print(f"Tesseract table API error: {e}")
            return self._extract_table_using_text_layout(enhanced_pil)

    def _extract_table_using_text_layout(self, image):
        """Extract table data by analyzing text layout patterns.

        Args:
            image: PIL image of a table region

        Returns:
            str: Markdown formatted table
        """
        # Get raw text
        text = self.ocr_engine.extract_text(image)

        # Split into lines and remove empty ones
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if not lines:
            return ""

        # Try to detect if the table has grid lines (indicated by '|' characters)
        has_separators = any("|" in line for line in lines)

        table_data = []

        if has_separators:
            # Process as a table with separators
            for line in lines:
                # Split by pipe character
                cells = [cell.strip() for cell in line.split("|")]
                # Remove empty cells at beginning/end (artifacts of split)
                if cells and not cells[0]:
                    cells = cells[1:]
                if cells and not cells[-1]:
                    cells = cells[:-1]

                if cells:
                    table_data.append(cells)
        else:
            # More aggressive splitting by whitespace
            import re

            for line in lines:
                # Try to split based on multiple spaces
                cells = [
                    cell.strip() for cell in re.split(r"\s{2,}", line) if cell.strip()
                ]

                # If that didn't work well (only one cell), try tokenizing
                if len(cells) <= 1:
                    words = line.split()
                    # If we have multiple words, try to split into reasonable columns
                    if len(words) >= 2:
                        # Here we could implement more advanced column detection based on content types
                        # For simplicity, we'll just check if there are 2-6 words and use them as columns
                        if 2 <= len(words) <= 6:
                            cells = words

                if cells:
                    table_data.append(cells)

        # If we still don't have a proper table, return the original text
        if not table_data or all(len(row) <= 1 for row in table_data):
            return ""

        # Normalize table (make all rows have same number of columns)
        max_cols = max(len(row) for row in table_data)
        for i in range(len(table_data)):
            while len(table_data[i]) < max_cols:
                table_data[i].append("")

        return self._format_to_markdown_table(table_data)

    def _process_table_region_easyocr(self, image):
        """Process a table region using EasyOCR with specific optimizations.

        Args:
            image: PIL image containing a potential table region

        Returns:
            str: Markdown formatted table
        """
        import cv2
        import numpy as np

        # Convert to numpy array
        img_np = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Detect horizontal and vertical lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

        horizontal_lines = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
        )
        vertical_lines = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2
        )

        # Combine lines
        grid_mask = cv2.bitwise_or(horizontal_lines, vertical_lines)

        # Find contours to get the grid cells
        contours, _ = cv2.findContours(
            cv2.bitwise_not(grid_mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        # Check if we have a grid
        grid_cells = []
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            # Filter out very small boxes and the whole image
            area_ratio = (w * h) / (image.width * image.height)
            if area_ratio < 0.8 and area_ratio > 0.005 and w > 30 and h > 20:
                grid_cells.append((x, y, w, h))

        # If we found grid cells, extract text from each
        if len(grid_cells) > 3:  # At least a 2x2 table minus header
            # Group cells into rows
            # Sort by y-coordinate first
            grid_cells.sort(key=lambda c: c[1])

            # Find row boundaries
            rows = []
            current_row = [grid_cells[0]]
            current_y = grid_cells[0][1]

            for cell in grid_cells[1:]:
                # If this cell is approximately aligned with current row
                if abs(cell[1] - current_y) < image.height * 0.05:  # 5% tolerance
                    current_row.append(cell)
                else:
                    # Sort cells in current row by x-coordinate
                    current_row.sort(key=lambda c: c[0])
                    rows.append(current_row)
                    # Start new row
                    current_row = [cell]
                    current_y = cell[1]

            # Add the last row
            if current_row:
                current_row.sort(key=lambda c: c[0])
                rows.append(current_row)

            # Extract text from each cell
            table_data = []
            for row in rows:
                row_data = []
                for x, y, w, h in row:
                    # Extract the cell image
                    cell_img = image.crop((x, y, x + w, y + h))
                    # Use EasyOCR to extract text
                    cell_text = self.ocr_engine.extract_text(cell_img).strip()
                    row_data.append(cell_text)

                if row_data:
                    table_data.append(row_data)

            return self._format_to_markdown_table(table_data)

        # No grid found or too few cells, use direct OCR
        else:
            # Perform OCR on the whole region with EasyOCR
            detected_text = self.ocr_engine.extract_text(image)

            # Check if EasyOCR already returned markdown table format
            if "| " in detected_text and " |" in detected_text:
                return detected_text

            # Otherwise, parse the text and construct a table
            lines = [line.strip() for line in detected_text.split("\n") if line.strip()]
            table_data = []

            # Find lines that look like rows
            for line in lines:
                # Look for column separators
                if "|" in line:
                    # Use the pipe symbols as separators
                    cells = [cell.strip() for cell in line.split("|")]
                    # Remove empty cells from start and end if they're just artifacts of split
                    if cells and not cells[0]:
                        cells = cells[1:]
                    if cells and not cells[-1]:
                        cells = cells[:-1]

                    if cells:
                        table_data.append(cells)
                else:
                    # Try a heuristic approach to identify columns
                    # Split by multiple spaces or tabs
                    import re

                    cells = [
                        cell.strip()
                        for cell in re.split(r"\s{2,}|\t", line)
                        if cell.strip()
                    ]
                    if len(cells) > 1:
                        table_data.append(cells)

            # If we found table data, format it
            if table_data:
                # Normalize number of columns
                max_cols = max([len(row) for row in table_data])
                for i in range(len(table_data)):
                    while len(table_data[i]) < max_cols:
                        table_data[i].append("")

                return self._format_to_markdown_table(table_data)

            return ""

    def _format_to_markdown_table(self, table_data):
        """Format structured data as a Markdown table.

        Args:
            table_data: List of lists representing rows and cells

        Returns:
            str: Markdown formatted table
        """
        if not table_data or not table_data[0]:
            return ""

        # Determine column count from first row
        column_count = len(table_data[0])

        # Ensure all rows have the same number of columns
        for i in range(len(table_data)):
            # Pad with empty strings if needed
            while len(table_data[i]) < column_count:
                table_data[i].append("")

        # Build table header
        md_table = []

        # First row is the header
        header = " | ".join(table_data[0])
        md_table.append(f"| {header} |")

        # Add separator row
        separator = " | ".join(["---"] * column_count)
        md_table.append(f"| {separator} |")

        # Add data rows
        for row in table_data[1:]:
            row_str = " | ".join(row)
            md_table.append(f"| {row_str} |")

        # Return the formatted table with blank lines around it
        return "\n\n" + "\n".join(md_table) + "\n\n"

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
        # If the text already contains Markdown tables, we need to preserve them
        import re

        # Split text into table and non-table sections
        parts = []
        lines = text.split("\n")
        in_table = False
        current_part = []

        for line in lines:
            # Table line detection (starts and ends with pipe)
            is_table_line = line.strip().startswith("|") and line.strip().endswith("|")

            if is_table_line and not in_table:  # Table start
                if current_part:
                    parts.append(("text", "\n".join(current_part)))
                    current_part = []
                in_table = True
                current_part.append(line)
            elif not is_table_line and in_table:  # Table end
                if current_part:
                    parts.append(("table", "\n".join(current_part)))
                    current_part = []
                in_table = False
                current_part.append(line)
            else:  # Continue current part
                current_part.append(line)

        # Add last part
        if current_part:
            part_type = "table" if in_table else "text"
            parts.append((part_type, "\n".join(current_part)))

        # Format each part
        formatted_parts = []
        for part_type, content in parts:
            if part_type == "table":
                # Preserve table as is
                formatted_parts.append(content)
            else:
                # Format regular text - replace consecutive empty lines
                formatted_parts.append(re.sub(r"\n\s*\n", "\n\n&nbsp;\n\n", content))

        # Join all parts
        formatted_text = "\n\n".join(formatted_parts)

        return f"# {title}\n\n{formatted_text}"

    def process_pdf(
        self,
        pdf_path,
        output_path=None,
        filter_words=None,
        start_page=None,
        end_page=None,
    ):
        """Process a scanned PDF and convert to markdown.

        Args:
            pdf_path (str): Path to the PDF file.
            output_path (str, optional): Path to save the output markdown file.
                If None, the output is not saved to a file.
            filter_words (bool, optional): Whether to filter out non-English words.
                If None, uses the instance's filter_words setting.
            start_page (int, optional): First page to extract (1-indexed). Defaults to None.
            end_page (int, optional): Last page to extract (1-indexed). Defaults to None.

        Returns:
            str: The processed text in markdown format.
        """
        # Use instance filter_words setting if not specified
        if filter_words is None:
            filter_words = self.filter_words

        # Extract text from PDF
        extracted_text = self.extract_from_pdf(
            pdf_path, start_page=start_page, end_page=end_page
        )

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


if __name__ == "__main__":
    # This handles the case when the file is run directly
    print("This module is not meant to be run directly.")
    print("Use it as part of the textextraction package:")
    print("from textextraction import ScannedPdfText")
    print("")
    print("To test table extraction, use example_tables.py in the project root.")
