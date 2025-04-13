from .utils import get_valid_words, clean_text, filter_english_words


class PdfText:
    def __init__(self, table_detection=True):
        """Initialize the PDF text processor.

        Args:
            table_detection (bool, optional): Whether to detect and preserve tables.
                Defaults to True.
        """
        # Initialize the valid words set
        self.valid_words = get_valid_words()
        self.table_detection = table_detection

    def extract_from_pdf(self, pdf_path):
        """Extract text from a PDF file preserving original line breaks and detecting tables.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: The extracted text with preserved structure.
        """
        # Import pdfminer only when needed
        from pdfminer.high_level import extract_text

        # Extract text with better layout preservation
        extracted_text = extract_text(pdf_path)

        # If table detection is enabled, try to detect and format tables
        if self.table_detection:
            tables = self._detect_tables(pdf_path)
            if tables:
                # Replace table regions in the extracted text with markdown tables
                return self._merge_text_with_tables(extracted_text, tables)

        return clean_text(extracted_text)

    def _detect_tables(self, pdf_path):
        """Detect tables in the PDF document.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            list: List of detected tables with their position information.
        """
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextBoxHorizontal, LTRect, LTLine

        tables = []

        # Extract page layouts
        for page_num, page_layout in enumerate(extract_pages(pdf_path), 1):
            # Collect horizontal and vertical lines
            h_lines = []
            v_lines = []
            text_boxes = []

            # First pass: collect lines and text boxes
            for element in page_layout:
                if isinstance(element, LTRect) and (
                    element.width > 3 * element.height
                    or element.height > 3 * element.width
                ):
                    # This is likely a line rather than a small rectangle
                    if element.width > element.height:
                        h_lines.append((element.x0, element.y0, element.x1, element.y1))
                    else:
                        v_lines.append((element.x0, element.y0, element.x1, element.y1))
                elif isinstance(element, LTLine):
                    if element.x1 - element.x0 > element.y1 - element.y0:
                        h_lines.append((element.x0, element.y0, element.x1, element.y1))
                    else:
                        v_lines.append((element.x0, element.y0, element.x1, element.y1))
                elif isinstance(element, LTTextBoxHorizontal):
                    text_boxes.append(element)

            # If we have both horizontal and vertical lines, we might have a table
            if len(h_lines) >= 2 and len(v_lines) >= 2:
                # Group lines that might form a table grid
                table_regions = self._identify_table_regions(h_lines, v_lines)

                for region in table_regions:
                    x0, y0, x1, y1 = region

                    # Collect text elements within this region
                    table_elements = []
                    for text_box in text_boxes:
                        if (
                            text_box.x0 >= x0
                            and text_box.x1 <= x1
                            and text_box.y0 >= y0
                            and text_box.y1 <= y1
                        ):
                            table_elements.append(
                                (text_box.x0, text_box.y1, text_box.get_text().strip())
                            )

                    if table_elements:
                        # Process table elements into a structured table
                        table_data = self._structure_table(
                            table_elements, h_lines, v_lines, region
                        )
                        if table_data and len(table_data) > 1:  # Ensure we have rows
                            tables.append(
                                {"page": page_num, "region": region, "data": table_data}
                            )

        return tables

    def _identify_table_regions(self, h_lines, v_lines):
        """Identify regions that might contain tables based on line intersections.

        Args:
            h_lines (list): List of horizontal lines.
            v_lines (list): List of vertical lines.

        Returns:
            list: List of regions (x0, y0, x1, y1) that might contain tables.
        """
        # Group lines that are close to each other
        h_groups = self._group_lines(h_lines, "horizontal")
        v_groups = self._group_lines(v_lines, "vertical")

        # Find potential table boundaries based on line intersections
        regions = []

        # Look for regions formed by at least 2 horizontal and 2 vertical lines
        if len(h_groups) >= 2 and len(v_groups) >= 2:
            # Sort groups by position
            h_groups.sort(key=lambda g: -g[0][1])  # Sort by y (top to bottom)
            v_groups.sort(key=lambda g: g[0][0])  # Sort by x (left to right)

            for i in range(len(h_groups) - 1):
                for j in range(len(v_groups) - 1):
                    # Define a region
                    x0 = v_groups[j][0][0]
                    y0 = h_groups[i + 1][0][1]
                    x1 = v_groups[j + 1][0][0]
                    y1 = h_groups[i][0][1]

                    # Check if region is reasonable
                    if x1 - x0 > 20 and y1 - y0 > 20:  # Minimum size
                        regions.append((x0, y0, x1, y1))

        return regions

    def _group_lines(self, lines, direction):
        """Group lines that are close to each other.

        Args:
            lines (list): List of lines to group.
            direction (str): Line direction ('horizontal' or 'vertical').

        Returns:
            list: List of line groups.
        """
        if not lines:
            return []

        # Sort lines
        if direction == "horizontal":
            lines.sort(key=lambda line: -line[1])  # Sort by y (top to bottom)
        else:
            lines.sort(key=lambda line: line[0])  # Sort by x (left to right)

        # Group lines that are close
        tolerance = 5  # 5 points tolerance
        groups = [[lines[0]]]

        for line in lines[1:]:
            if direction == "horizontal":
                # Group by y-coordinate
                if abs(line[1] - groups[-1][-1][1]) <= tolerance:
                    groups[-1].append(line)
                else:
                    groups.append([line])
            else:
                # Group by x-coordinate
                if abs(line[0] - groups[-1][-1][0]) <= tolerance:
                    groups[-1].append(line)
                else:
                    groups.append([line])

        return groups

    def _structure_table(self, elements, h_lines, v_lines, region):
        """Structure table elements into rows and columns.

        Args:
            elements (list): List of text elements (x, y, text).
            h_lines (list): Horizontal lines.
            v_lines (list): Vertical lines.
            region (tuple): Table region (x0, y0, x1, y1).

        Returns:
            list: Structured table data as rows and columns.
        """
        # If no elements, return empty
        if not elements:
            return []

        # Get region boundaries
        x0, y0, x1, y1 = region

        # Group elements by y-coordinate (rows)
        elements.sort(key=lambda e: -e[1])  # Sort by y (top to bottom)

        # Identify row boundaries using horizontal lines
        h_positions = [y0, y1]  # Include region boundaries
        for line in h_lines:
            if line[1] >= y0 and line[1] <= y1:
                h_positions.append(line[1])
        h_positions = sorted(list(set(h_positions)))

        # Group elements into rows
        rows = []
        for i in range(len(h_positions) - 1):
            row_elements = []
            for elem in elements:
                if elem[1] <= h_positions[i] and elem[1] >= h_positions[i + 1]:
                    row_elements.append(elem)
            if row_elements:
                rows.append(row_elements)

        # If we couldn't detect rows using lines, try grouping by proximity
        if not rows:
            tolerance = 10  # 10 points tolerance
            current_row = [elements[0]]
            current_y = elements[0][1]

            for elem in elements[1:]:
                if abs(elem[1] - current_y) <= tolerance:
                    current_row.append(elem)
                else:
                    rows.append(current_row)
                    current_row = [elem]
                    current_y = elem[1]

            if current_row:
                rows.append(current_row)

        # Process each row to organize columns
        table_data = []
        for row in rows:
            # Sort elements in row by x-coordinate (left to right)
            row.sort(key=lambda e: e[0])

            # Extract text from each element
            row_data = [elem[2] for elem in row]
            if row_data:
                table_data.append(row_data)

        return table_data

    def _merge_text_with_tables(self, text, tables):
        """Merge the extracted text with detected tables in Markdown format.

        Args:
            text (str): Extracted text.
            tables (list): Detected tables.

        Returns:
            str: Text with tables in Markdown format.
        """
        if not tables:
            return text

        # Convert tables to Markdown
        markdown_tables = []
        for table in tables:
            md_table = []

            for i, row in enumerate(table["data"]):
                # Add table row
                md_table.append("| " + " | ".join(row) + " |")

                # Add separator after header
                if i == 0:
                    md_table.append("|" + "|".join(["---"] * len(row)) + "|")

            markdown_tables.append("\n".join(md_table))

        # For now, just append the tables to the text
        # In a more sophisticated implementation, we could replace table regions in the text
        result = clean_text(text)

        for i, md_table in enumerate(markdown_tables):
            result += f"\n\n**Table {i+1}**:\n\n{md_table}\n\n"

        return result

    def filter_english_words(self, text):
        """Filter text to keep only valid English words.

        Args:
            text (str): The text to filter.

        Returns:
            str: The filtered text containing only valid English words.
        """
        return filter_english_words(text, self.valid_words)

    def to_markdown(self, text, title="Extracted Text"):
        """Convert text to markdown format while preserving line breaks"""
        # Import re only when needed
        import re

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
