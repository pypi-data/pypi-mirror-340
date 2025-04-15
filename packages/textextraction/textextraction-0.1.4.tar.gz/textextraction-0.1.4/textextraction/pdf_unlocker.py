"""
PDF Unlocker module for the textextraction package.

This module provides functionality to remove password protection from PDF files
while maintaining compatibility with the textextraction package structure.
"""

import os
import logging
from pathlib import Path


class PdfUnlocker:
    """Class to handle unlocking of password-protected PDF files."""

    def __init__(self):
        """Initialize the PDF unlocker."""
        self.logger = logging.getLogger(__name__)

    def unlock(self, input_path, password, output_path=None):
        """
        Unlock a password-protected PDF file.

        Args:
            input_path (str): Path to the password-protected PDF file.
            password (str): Password to unlock the PDF.
            output_path (str, optional): Path to save the unlocked PDF. If None,
                                        will use the input filename with '_unlocked' suffix.

        Returns:
            str: Path to the unlocked PDF file, or None if operation failed.
        """
        # Validate input file
        if not os.path.exists(input_path):
            self.logger.error(f"Input file not found: {input_path}")
            return None

        # Determine output path if not provided
        if output_path is None:
            input_file = Path(input_path)
            output_path = str(
                input_file.parent / f"{input_file.stem}_unlocked{input_file.suffix}"
            )

        try:
            # Try using PyPDF2 first (simpler, faster)
            try:
                from PyPDF2 import PdfReader, PdfWriter

                self.logger.info(f"Attempting to unlock PDF using PyPDF2: {input_path}")
                reader = PdfReader(input_path)

                # Check if the PDF is encrypted
                if not reader.is_encrypted:
                    self.logger.warning("The PDF is not password-protected.")
                    return input_path

                # Try to decrypt with the provided password
                try:
                    reader.decrypt(password)
                    self.logger.info("Successfully decrypted the PDF.")
                except Exception as e:
                    self.logger.error(
                        f"Failed to decrypt PDF with provided password: {e}"
                    )
                    return None

                # Create a new PDF writer
                writer = PdfWriter()

                # Add all pages from the reader to the writer
                for page in reader.pages:
                    writer.add_page(page)

                # Write the output file
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

                self.logger.info(f"Unlocked PDF saved to: {output_path}")
                return output_path

            except ImportError:
                self.logger.warning("PyPDF2 not available, falling back to pypdfium2")

            # Fall back to pypdfium2 if PyPDF2 is not available
            try:
                import pypdfium2 as pdfium

                self.logger.info(
                    f"Attempting to unlock PDF using pypdfium2: {input_path}"
                )

                # Load the PDF with password
                pdf = pdfium.PdfDocument(input_path, password=password)

                # Save the PDF without password
                pdf.save(output_path)

                self.logger.info(f"Unlocked PDF saved to: {output_path}")
                return output_path

            except ImportError:
                self.logger.error(
                    "Neither PyPDF2 nor pypdfium2 is available. Please install one of them."
                )
                return None

        except Exception as e:
            self.logger.error(f"Error unlocking PDF: {e}")
            return None
