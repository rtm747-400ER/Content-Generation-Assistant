def count_words(text: str) -> int:
    """Return number of words in given text."""
    return len(text.split())


def count_chars(text: str) -> int:
    """Return number of characters in given text (excluding spaces)."""
    return len(text.replace(" ", ""))
