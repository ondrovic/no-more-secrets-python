"""Basic tests to verify the module structure works."""

from __future__ import annotations

import pytest

from no_more_secrets import NMSEffect
from no_more_secrets.core import CharAttr, Colors, Terminal, get_random_char
from no_more_secrets.utils import get_char_width, fix_encoding_issues


def test_nms_effect_creation():
    """Test that NMSEffect can be created."""
    effect = NMSEffect()
    assert effect is not None
    assert not effect.auto_decrypt
    assert not effect.mask_blank
    assert effect.foreground_color == Colors.BLUE


def test_char_attr_creation():
    """Test CharAttr creation."""
    attr = CharAttr(
        source="A",
        mask="X", 
        width=1,
        is_space=False,
        reveal_time=1000
    )
    assert attr.source == "A"
    assert attr.mask == "X"
    assert attr.width == 1
    assert not attr.is_space
    assert attr.reveal_time == 1000
    assert not attr.is_revealed


def test_colors():
    """Test color constants."""
    assert Colors.BLUE == 34
    assert Colors.RED == 31
    assert Colors.GREEN == 32


def test_terminal():
    """Test terminal utilities."""
    rows, cols = Terminal.get_size()
    assert rows > 0
    assert cols > 0
    
    platform = Terminal.get_platform()
    assert platform in ['unix', 'windows', 'other']


def test_charset():
    """Test character set functionality."""
    char = get_random_char()
    assert isinstance(char, str)
    assert len(char) == 1


def test_encoding_utils():
    """Test encoding utilities."""
    # Test character width
    assert get_char_width('A') == 1
    assert get_char_width(' ') == 1
    
    # Test encoding fixes
    fixed_text = fix_encoding_issues("Hello World")
    assert "Hello World" in fixed_text


def test_nms_effect_configuration():
    """Test NMSEffect configuration methods."""
    effect = NMSEffect()
    
    # Test auto decrypt
    effect.set_auto_decrypt(True)
    assert effect.auto_decrypt
    
    # Test mask blank
    effect.set_mask_blank(True)
    assert effect.mask_blank
    
    # Test foreground color
    effect.set_foreground_color("red")
    assert effect.foreground_color == Colors.RED
    
    # Test hex color
    effect.set_hex_color("FF0000")
    assert effect.custom_hex_color == "FF0000"
    
    # Test preserve colors
    effect.set_preserve_colors(True)
    assert effect.preserve_colors


if __name__ == "__main__":
    pytest.main([__file__])