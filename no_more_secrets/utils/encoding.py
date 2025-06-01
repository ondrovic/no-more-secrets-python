"""Encoding utilities and character width calculations."""

from __future__ import annotations

import unicodedata


def fix_encoding_issues(text: str) -> str:
    """Fix common encoding issues with tree characters."""
    # Common Windows encoding issues with box-drawing characters
    replacements = {
        'Γö£ΓöÇΓöÇ': '├──',  # ├──
        'ΓööΓöÇΓöÇ': '└──',  # └──
        'Γöé': '│',           # │
        'ΓöÇ': '─',           # ─
        'Γö£': '├',           # ├
        'Γöö': '└',           # └
        'Γöé   ': '│   ',     # │ with spaces
        'â"œâ"€â"€': '├──',      # Alternative encoding
        'â"‚': '│',            # │
        'â""â"€â"€': '└──',      # └──
        'â"€': '─',            # ─
        'â"œ': '├',            # ├
        'â""': '└',            # └
    }
    
    # Apply replacements
    for garbled, correct in replacements.items():
        text = text.replace(garbled, correct)
    
    return text


def get_char_width(char: str) -> int:
    """Get display width of a character."""
    try:
        # Handle common box-drawing and tree characters
        if ord(char) >= 0x2500 and ord(char) <= 0x257F:  # Box drawing block
            return 1
        elif ord(char) >= 0x2580 and ord(char) <= 0x259F:  # Block elements
            return 1
        elif ord(char) >= 0x25A0 and ord(char) <= 0x25FF:  # Geometric shapes
            return 1
        elif ord(char) >= 0xE000 and ord(char) <= 0xF8FF:  # Private use area (icons)
            return 2  # Many terminal icons are double-width
        
        # Use unicodedata for standard classification
        width = unicodedata.east_asian_width(char)
        if width in ('F', 'W'):  # Full-width or Wide
            return 2
        elif width in ('H', 'Na', 'N'):  # Half-width, Narrow, or Neutral
            return 1
        else:
            return 1
    except (ValueError, TypeError):
        return 1


def safe_char_decode(char: str) -> str:
    """Safely decode a character, handling Unicode errors."""
    try:
        # Check if this is a multi-byte UTF-8 sequence
        char_bytes = char.encode('utf-8')
        if len(char_bytes) > 1:
            # This is a multi-byte character, Python handles this automatically
            return char
        return char
    except (UnicodeDecodeError, UnicodeEncodeError):
        return '?'  # Fallback for problematic characters