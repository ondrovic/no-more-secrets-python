"""Tests for color utilities."""

from __future__ import annotations

import pytest

from no_more_secrets.core.colors import (
    Colors,
    get_color_map,
    get_color_prefix,
    hex_to_rgb,
    rgb_to_ansi,
)


def test_colors_constants():
    """Test color constant values."""
    assert Colors.RED == 31
    assert Colors.GREEN == 32
    assert Colors.BLUE == 34
    assert Colors.WHITE == 37


def test_hex_to_rgb():
    """Test hex to RGB conversion."""
    assert hex_to_rgb("FF0000") == (255, 0, 0)
    assert hex_to_rgb("#00FF00") == (0, 255, 0)
    assert hex_to_rgb("0000FF") == (0, 0, 255)
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)


def test_rgb_to_ansi():
    """Test RGB to ANSI conversion."""
    result = rgb_to_ansi(255, 0, 0)
    assert result == "\033[1;38;2;255;0;0m"
    
    result = rgb_to_ansi(0, 255, 0)
    assert result == "\033[1;38;2;0;255;0m"


def test_get_color_map():
    """Test color map retrieval."""
    color_map = get_color_map()
    assert isinstance(color_map, dict)
    assert "red" in color_map
    assert "green" in color_map
    assert "blue" in color_map
    assert color_map["red"] == Colors.RED


def test_get_color_prefix():
    """Test color prefix generation."""
    # Test named color
    prefix = get_color_prefix("red")
    assert "\033[1;31m" in prefix
    
    # Test hex color
    prefix = get_color_prefix(hex_color="FF0000")
    assert "\033[1;38;2;255;0;0m" in prefix
    
    # Test default
    prefix = get_color_prefix()
    assert "\033[1;34m" in prefix  # Default blue


def test_fg_color():
    """Test foreground color generation."""
    assert Colors.fg(Colors.RED) == "\033[31m"
    assert Colors.fg(Colors.GREEN) == "\033[32m"


def test_move_cursor():
    """Test cursor movement."""
    result = Colors.move_cursor(10, 20)
    assert result == "\033[10;20H"