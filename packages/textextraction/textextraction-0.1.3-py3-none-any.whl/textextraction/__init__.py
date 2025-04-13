# Define the public API
__all__ = ["ImageText", "PdfText", "ScannedPdfText"]

# Package metadata
__version__ = "0.1.3"


# Lazy imports
def __getattr__(name):
    """Lazy import of module classes.

    This function allows for lazy importing of the main classes.
    The classes are only imported when they are first accessed.

    Args:
        name (str): Name of the attribute to import.

    Returns:
        object: The imported class.

    Raises:
        AttributeError: If the requested attribute is not a valid class name.
    """
    if name == "ImageText":
        from .image_text import ImageText

        return ImageText
    elif name == "PdfText":
        from .pdf_text import PdfText

        return PdfText
    elif name == "ScannedPdfText":
        try:
            # Check for PyMuPDF dependency
            try:
                import fitz  # PyMuPDF
                if not hasattr(fitz, "__version__"):
                    pass
            except ImportError:
                raise ImportError(
                    "PyMuPDF is required for ScannedPdfText. "
                    "Please install it with 'pip install pymupdf'"
                )

            # Check for OpenCV dependency
            try:
                import cv2
            except ImportError:
                raise ImportError(
                    "OpenCV is required for ScannedPdfText. "
                    "Please install it with 'pip install opencv-python'"
                )

            from .scanned_pdf_text import ScannedPdfText

            return ScannedPdfText
        except ImportError as e:
            # Re-raise with helpful message
            raise ImportError(f"Error importing ScannedPdfText: {str(e)}")
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
