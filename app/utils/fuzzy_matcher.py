import difflib


def fuzzy_compare(s1: str, s2: str) -> dict:
    """
    Compare two strings using difflib's SequenceMatcher for fuzzy logic.
    Returns a dict with similarity ratio (0-1) and is_fuzzy_match (True if ratio > 0.85).
    """
    ratio = difflib.SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
    is_fuzzy_match = ratio > 0.85
    return {
        'ratio': ratio,
        'is_fuzzy_match': is_fuzzy_match
    }
