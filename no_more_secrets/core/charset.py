"""Character set for the scrambling effect using complete CP437 (IBM PC) character set."""

from __future__ import annotations

import random

# Complete CP437 (IBM PC) character set - all 256 characters
# Characters 0-31 are control characters with special glyphs in CP437
# Characters 32-126 are standard ASCII printable characters  
# Characters 127-255 are extended characters including international, box drawing, and mathematical symbols
CHARSET = [
    # Control characters with CP437 glyphs (0-31)
    "☺", "☻", "♥", "♦", "♣", "♠", "•", "◘", "○", "◙", "♂", "♀", "♪", "♫", "☼", "►",
    "◄", "↕", "‼", "¶", "§", "▬", "↨", "↑", "↓", "→", "←", "∟", "↔", "▲", "▼",
    
    # Standard ASCII printable characters (32-126)
    " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
    "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_",
    "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~",
    
    # CP437 house symbol (127)
    "⌂",
    
    # International characters (128-175)
    "Ç", "ü", "é", "â", "ä", "à", "å", "ç", "ê", "ë", "è", "ï", "î", "ì", "Ä", "Å",
    "É", "æ", "Æ", "ô", "ö", "ò", "û", "ù", "ÿ", "Ö", "Ü", "¢", "£", "¥", "₧", "ƒ",
    "á", "í", "ó", "ú", "ñ", "Ñ", "ª", "º", "¿", "⌐", "¬", "½", "¼", "¡", "«", "»",
    
    # Box drawing characters (176-223)
    "░", "▒", "▓", "│", "┤", "╡", "╢", "╖", "╕", "╣", "║", "╗", "╝", "╜", "╛", "┐",
    "└", "┴", "┬", "├", "─", "┼", "╞", "╟", "╚", "╔", "╩", "╦", "╠", "═", "╬", "╧",
    "╨", "╤", "╥", "╙", "╘", "╒", "╓", "╫", "╪", "┘", "┌", "█", "▄", "▌", "▐", "▀",
    
    # Mathematical and Greek symbols (224-255)
    "α", "ß", "Γ", "π", "Σ", "σ", "µ", "τ", "Φ", "Θ", "Ω", "δ", "∞", "φ", "ε", "∩",
    "≡", "±", "≥", "≤", "⌠", "⌡", "÷", "≈", "°", "∙", "·", "√", "ⁿ", "²", "■", " "
]


def get_random_char() -> str:
    """Get a random character from the complete CP437 charset."""
    return random.choice(CHARSET)


def get_random_char_excluding_control() -> str:
    """Get a random character from CP437 charset excluding control characters (0-31)."""
    # Start from index 31 (space character) to exclude control characters
    return random.choice(CHARSET[31:])


def get_random_printable_char() -> str:
    """Get a random character from standard ASCII printable range (32-126)."""
    return random.choice(CHARSET[31:127])


def get_random_extended_char() -> str:
    """Get a random character from CP437 extended range (128-255)."""
    return random.choice(CHARSET[128:])


def get_random_box_drawing_char() -> str:
    """Get a random box drawing character from CP437 (176-223)."""
    return random.choice(CHARSET[176:224])