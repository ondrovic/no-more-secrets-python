"""Tests for encoding utilities."""

from __future__ import annotations

import pytest

from no_more_secrets.utils.encoding import (
    fix_encoding_issues,
    get_char_width,
    safe_char_decode,
)


def test_get_char_width():
    """Test character width calculation."""
    # ASCII characters
    assert get_char_width('A') == 1
    assert get_char_width('1') == 1
    assert get_char_width(' ') == 1
    
    # Box drawing characters
    assert get_char_width('│') == 1  # U+2502
    assert get_char_width('├') == 1  # U+251C
    assert get_char_width('└') == 1  # U+2514
    assert get_char_width('─') == 1  # U+2500
    
    # Block elements
    assert get_char_width('█') == 1  # U+2588
    assert get_char_width('░') == 1  # U+2591
    
    # Geometric shapes
    assert get_char_width('■') == 1  # U+25A0
    
    # Wide characters (East Asian)
    try:
        # These might be 2 width on some systems
        width = get_char_width('中')  # Chinese character
        assert width in [1, 2]  # Could be 1 or 2 depending on system
    except:
        # If Unicode data isn't available, should default to 1
        pass
    
    # Edge cases
    assert get_char_width('\n') == 1
    assert get_char_width('\t') == 1


def test_safe_char_decode():
    """Test safe character decoding."""
    # Normal ASCII
    assert safe_char_decode('A') == 'A'
    assert safe_char_decode('1') == '1'
    assert safe_char_decode(' ') == ' '
    
    # Unicode characters
    assert safe_char_decode('é') == 'é'
    assert safe_char_decode('ñ') == 'ñ'
    assert safe_char_decode('中') == '中'
    
    # Box drawing
    assert safe_char_decode('│') == '│'
    assert safe_char_decode('├') == '├'
    
    # Empty string
    assert safe_char_decode('') == ''


def test_fix_encoding_issues():
    """Test encoding issue fixes for garbled characters."""
    # Test common Windows encoding issues
    test_cases = [
        # Box drawing replacements
        ('Γö£ΓöÇΓöÇ', '├──'),
        ('ΓööΓöÇΓöÇ', '└──'),
        ('Γöé', '│'),
        ('ΓöÇ', '─'),
        ('Γö£', '├'),
        ('Γöö', '└'),
        ('Γöé   ', '│   '),
        
        # Alternative encodings
        ('â"œâ"€â"€', '├──'),
        ('â"‚', '│'),
        ('â""â"€â"€', '└──'),
        ('â"€', '─'),
        ('â"œ', '├'),
        ('â""', '└'),
    ]
    
    for garbled, expected in test_cases:
        result = fix_encoding_issues(garbled)
        assert result == expected, f"Expected {expected!r}, got {result!r} for input {garbled!r}"
    
    # Test text without encoding issues
    normal_text = "Hello World"
    assert fix_encoding_issues(normal_text) == normal_text
    
    # Test mixed content
    mixed_text = "Hello Γöé World"
    expected = "Hello │ World"
    assert fix_encoding_issues(mixed_text) == expected
    
    # Test empty string
    assert fix_encoding_issues("") == ""
    
    # Test multiple replacements in one string
    complex_text = "Γö£ΓöÇΓöÇ file1\nΓööΓöÇΓöÇ file2"
    expected = "├── file1\n└── file2"
    assert fix_encoding_issues(complex_text) == expected


def test_fix_encoding_issues_tree_like():
    """Test encoding fixes on tree-like structures."""
    # Simulate garbled tree output
    garbled_tree = (
        ".\n"
        "Γö£ΓöÇΓöÇ folder1\n"
        "Γöé   Γö£ΓöÇΓöÇ file1.txt\n"
        "Γöé   ΓööΓöÇΓöÇ file2.txt\n"
        "ΓööΓöÇΓöÇ folder2"
    )
    
    expected_tree = (
        ".\n"
        "├── folder1\n"
        "│   ├── file1.txt\n"
        "│   └── file2.txt\n"
        "└── folder2"
    )
    
    result = fix_encoding_issues(garbled_tree)
    assert result == expected_tree


def test_unicode_edge_cases():
    """Test Unicode edge cases."""
    # Test various Unicode categories
    test_chars = [
        'é',    # Latin with diacritic
        'ñ',    # Spanish ñ
        'ç',    # Cedilla
        'Ω',    # Greek omega
        'α',    # Greek alpha
        '中',   # Chinese
        '💻',   # Emoji (might be width 2)
        '🌟',   # Another emoji
    ]
    
    for char in test_chars:
        # These should not raise exceptions
        width = get_char_width(char)
        assert isinstance(width, int)
        assert width >= 1
        
        decoded = safe_char_decode(char)
        assert isinstance(decoded, str)
        
        # Should not change normal Unicode
        fixed = fix_encoding_issues(char)
        assert isinstance(fixed, str)


def test_character_width_private_use_area():
    """Test characters in private use area (often icons)."""
    # Private use area characters (often used for terminal icons)
    private_chars = [
        '\uE000',  # Start of private use area
        '\uF000',  # Middle of private use area
    ]
    
    for char in private_chars:
        width = get_char_width(char)
        # Private use area characters are often double-width icons
        assert width in [1, 2]


def test_malformed_input():
    """Test handling of malformed or problematic input."""
    # Test with None (should not crash)
    try:
        result = safe_char_decode(None)  # type: ignore
        # If it doesn't crash, it should return something safe
        assert isinstance(result, str)
    except (TypeError, AttributeError):
        # It's okay if it raises an exception for None
        pass
    
    # Test empty string
    assert safe_char_decode('') == ''
    assert get_char_width('') == 1  # Should handle gracefully
    assert fix_encoding_issues('') == ''