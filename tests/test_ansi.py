"""Tests for ANSI utilities."""

from __future__ import annotations

import pytest

from no_more_secrets.utils.ansi import (
    extract_ansi_codes,
    has_ansi_codes,
    strip_ansi_codes,
)


def test_strip_ansi_codes():
    """Test ANSI code stripping."""
    # Basic color codes
    text = "\033[31mRed text\033[0m"
    result = strip_ansi_codes(text)
    assert result == "Red text"
    
    # Complex tree-like output
    text = "\033[1;34m.\033[0m\n\033[1;90m├── \033[0m.gitignore"
    result = strip_ansi_codes(text)
    assert result == ".\n├── .gitignore"
    
    # No ANSI codes
    text = "Plain text"
    result = strip_ansi_codes(text)
    assert result == "Plain text"


def test_has_ansi_codes():
    """Test ANSI code detection."""
    assert has_ansi_codes("\033[31mRed\033[0m")
    assert has_ansi_codes("\033[1;34mBlue\033[0m")
    assert not has_ansi_codes("Plain text")
    assert not has_ansi_codes("")


def test_extract_ansi_codes():
    """Test ANSI code extraction."""
    text = "\033[31mRed\033[0m and \033[32mGreen\033[0m"
    codes = extract_ansi_codes(text)
    assert "\033[31m" in codes
    assert "\033[0m" in codes
    assert "\033[32m" in codes
    
    # No codes
    codes = extract_ansi_codes("Plain text")
    assert codes == []


def test_complex_ansi_sequences():
    """Test complex ANSI sequences like those from tree command."""
    # Tree command style output
    tree_output = (
        "\033[1;34m.\033[0m\n"
        "\033[1;90m├── \033[0m\033[34mfolder\033[0m\n"
        "\033[1;90m└── \033[0mfile.txt"
    )
    
    result = strip_ansi_codes(tree_output)
    expected = ".\n├── folder\n└── file.txt"
    assert result == expected
    
    assert has_ansi_codes(tree_output)
    
    codes = extract_ansi_codes(tree_output)
    assert len(codes) > 0