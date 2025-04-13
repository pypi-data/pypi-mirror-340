"""OCR engines package."""

from .base import OCREngine

# Define the public API
__all__ = ["OCREngine", "TesseractEngine", "EasyOCREngine"]


# Lazy imports
def __getattr__(name):
    """Lazy import of OCR engine classes.

    This function allows for lazy importing of the OCR engine classes.
    The classes are only imported when they are first accessed.

    Args:
        name (str): Name of the attribute to import.

    Returns:
        object: The imported class.

    Raises:
        AttributeError: If the requested attribute is not a valid class name.
    """
    if name == "TesseractEngine":
        from .tesseract import TesseractEngine

        return TesseractEngine
    elif name == "EasyOCREngine":
        from .easyocr import EasyOCREngine

        return EasyOCREngine
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
