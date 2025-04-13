"""Common utilities for text extraction and processing."""

import re
from functools import lru_cache
from nltk.corpus import words
import nltk


@lru_cache(maxsize=1)
def get_valid_words():
    """Get the set of valid English words, cached for performance.

    Returns:
        set: Set of valid English words.
    """
    try:
        return set(words.words())
    except LookupError:
        nltk.download("words")
        return set(words.words())


def clean_text(text):
    """Clean text by removing excessive newlines while preserving structure.

    Args:
        text (str): Text to clean.

    Returns:
        str: Cleaned text.
    """
    return re.sub(r"\n{3,}", "\n\n", text)


def filter_english_words(text, valid_words):
    """Filter text to keep only valid English words while preserving special formatting.

    Args:
        text (str): Text to filter.
        valid_words (set): Set of valid English words.

    Returns:
        str: Filtered text with preserved formatting.
    """
    # Check if text contains table markers
    has_tables = "|" in text and "\n|" in text

    if not has_tables:
        # Regular text processing
        words_list = text.split()
        filtered_words = []

        for word in words_list:
            clean_word = re.sub(r"[^a-zA-Z]", "", word.lower())
            if clean_word and clean_word in valid_words:
                filtered_words.append(word)

        return " ".join(filtered_words)
    else:
        # Split text into lines
        lines = text.split("\n")
        filtered_lines = []

        for line in lines:
            # Detect table rows (lines starting and ending with |)
            if line.strip().startswith("|") and line.strip().endswith("|"):
                # Preserve table row formatting
                if "---" in line:
                    # This is a separator row, keep as is
                    filtered_lines.append(line)
                else:
                    # This is a data row, filter text within cells
                    cells = line.split("|")
                    filtered_cells = []

                    for cell in cells:
                        if not cell.strip():
                            # Empty cell or edge of row
                            filtered_cells.append(cell)
                            continue

                        # Filter cell text
                        cell_words = cell.split()
                        filtered_cell_words = []

                        for word in cell_words:
                            clean_word = re.sub(r"[^a-zA-Z]", "", word.lower())
                            if clean_word and clean_word in valid_words:
                                filtered_cell_words.append(word)

                        # Preserve cell even if no words match
                        if not filtered_cell_words and cell_words:
                            filtered_cell_words = [cell_words[0]]

                        filtered_cells.append(" ".join(filtered_cell_words))

                    filtered_lines.append("|".join(filtered_cells))
            else:
                # Regular text line
                words_list = line.split()
                filtered_words = []

                for word in words_list:
                    clean_word = re.sub(r"[^a-zA-Z]", "", word.lower())
                    if clean_word and clean_word in valid_words:
                        filtered_words.append(word)

                filtered_lines.append(" ".join(filtered_words))

        return "\n".join(filtered_lines)
