#!/usr/bin/env python3
"""
Command-line interface for the textextraction package.
"""

import argparse
import logging
import sys
from .pdf_unlocker import PdfUnlocker


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def main():
    """Main function to parse arguments and process commands."""
    parser = argparse.ArgumentParser(description="Text Extraction Tools")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # PDF Unlock command
    unlock_parser = subparsers.add_parser(
        "unlock", help="Unlock a password-protected PDF"
    )
    unlock_parser.add_argument(
        "input_file", help="Path to the password-protected PDF file"
    )
    unlock_parser.add_argument("password", help="Password to unlock the PDF")
    unlock_parser.add_argument(
        "-o", "--output", help="Path to save the unlocked PDF (optional)"
    )

    args = parser.parse_args()

    if args.command == "unlock":
        logger = setup_logging()
        logger.info(f"Unlocking PDF: {args.input_file}")

        unlocker = PdfUnlocker()
        result = unlocker.unlock(args.input_file, args.password, args.output)

        if result:
            logger.info(f"Successfully unlocked PDF. Output saved to: {result}")
            return 0
        else:
            logger.error("Failed to unlock PDF.")
            return 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
