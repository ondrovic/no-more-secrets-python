"""Tests for the main NMS effect."""

from __future__ import annotations

import io
import sys
from unittest.mock import MagicMock, patch

import pytest

from no_more_secrets.core.char_attr import CharAttr
from no_more_secrets.core.colors import Colors
from no_more_secrets.effects.nms_effect import NMSEffect


class TestNMSEffect:
    """Test the main NMS effect class."""
    
    def test_initialization(self):
        """Test NMSEffect initialization."""
        effect = NMSEffect()
        
        assert not effect.auto_decrypt
        assert not effect.mask_blank
        assert not effect.clear_screen
        assert effect.foreground_color == Colors.BLUE
        assert effect.custom_hex_color is None
        assert not effect.preserve_colors
    
    def test_set_auto_decrypt(self):
        """Test setting auto-decrypt mode."""
        effect = NMSEffect()
        
        effect.set_auto_decrypt(True)
        assert effect.auto_decrypt
        
        effect.set_auto_decrypt(False)
        assert not effect.auto_decrypt
    
    def test_set_mask_blank(self):
        """Test setting mask blank mode."""
        effect = NMSEffect()
        
        effect.set_mask_blank(True)
        assert effect.mask_blank
        
        effect.set_mask_blank(False)
        assert not effect.mask_blank
    
    def test_set_clear_screen(self):
        """Test setting clear screen mode."""
        effect = NMSEffect()
        
        effect.set_clear_screen(True)
        assert effect.clear_screen
        
        effect.set_clear_screen(False)
        assert not effect.clear_screen
    
    def test_set_foreground_color(self):
        """Test setting foreground color."""
        effect = NMSEffect()
        
        # Test valid colors
        effect.set_foreground_color('red')
        assert effect.foreground_color == Colors.RED
        assert effect.custom_hex_color is None
        
        effect.set_foreground_color('GREEN')  # Test case insensitive
        assert effect.foreground_color == Colors.GREEN
        
        # Test invalid color (should default to blue)
        effect.set_foreground_color('invalid_color')
        assert effect.foreground_color == Colors.BLUE
        assert effect.custom_hex_color is None
    
    def test_set_hex_color(self):
        """Test setting custom hex color."""
        effect = NMSEffect()
        
        # Test valid hex colors
        effect.set_hex_color('FF0000')
        assert effect.custom_hex_color == 'FF0000'
        
        effect.set_hex_color('#00FF00')
        assert effect.custom_hex_color == '00FF00'
        
        effect.set_hex_color('0000ff')  # Test lowercase
        assert effect.custom_hex_color == '0000ff'
        
        # Test invalid hex colors
        with patch('sys.stderr', new_callable=io.StringIO):
            effect.set_hex_color('INVALID')
            assert effect.custom_hex_color is None
            
            effect.set_hex_color('GG0000')  # Invalid characters
            assert effect.custom_hex_color is None
            
            effect.set_hex_color('FF00')  # Too short
            assert effect.custom_hex_color is None
    
    def test_set_preserve_colors(self):
        """Test setting preserve colors mode."""
        effect = NMSEffect()
        
        effect.set_preserve_colors(True)
        assert effect.preserve_colors
        
        effect.set_preserve_colors(False)
        assert not effect.preserve_colors
    
    def test_prepare_text_simple(self):
        """Test preparing simple text without ANSI codes."""
        effect = NMSEffect()
        effect.set_preserve_colors(False)
        
        text = "Hello World"
        char_attrs = effect.prepare_text(text)
        
        assert len(char_attrs) == len(text)
        
        # Check that space is preserved correctly
        space_attr = char_attrs[5]  # Space between "Hello" and "World"
        assert space_attr.source == ' '
        assert space_attr.is_space
        
        # Check that non-space characters have masks
        h_attr = char_attrs[0]  # 'H'
        assert h_attr.source == 'H'
        assert not h_attr.is_space
        # The mask should be a single character from the charset
        assert isinstance(h_attr.mask, str)
        assert len(h_attr.mask) == 1
        # Don't check specific characters since charset includes Unicode
    
    def test_prepare_text_with_ansi(self):
        """Test preparing text with ANSI codes."""
        effect = NMSEffect()
        
        # Test with preserve colors
        effect.set_preserve_colors(True)
        text = "\033[31mRed\033[0m Text"
        char_attrs = effect.prepare_text(text)
        
        # Should only have characters, not ANSI codes
        sources = [attr.source for attr in char_attrs]
        expected_sources = list("Red Text")
        assert sources == expected_sources
        
        # Check color preservation
        r_attr = char_attrs[0]  # 'R' should have red color
        assert r_attr.original_color == "\033[31m"
        
        # Test without preserve colors
        effect.set_preserve_colors(False)
        char_attrs = effect.prepare_text(text)
        
        # Should still parse correctly but not preserve colors
        sources = [attr.source for attr in char_attrs]
        assert sources == expected_sources
        
        # Should not preserve colors
        r_attr = char_attrs[0]
        assert r_attr.original_color == ""
    
    def test_parse_ansi_text(self):
        """Test ANSI text parsing specifically."""
        effect = NMSEffect()
        
        # Test complex ANSI sequence (like from tree command)
        text = "\033[1;34m.\033[0m\n\033[1;90m├── \033[0mfile"
        
        effect.set_preserve_colors(True)
        char_attrs = effect.parse_ansi_text(text)
        
        sources = [attr.source for attr in char_attrs]
        expected = list(".\n├── file")
        assert sources == expected
        
        # Check that color codes are preserved for non-reset sequences
        dot_attr = char_attrs[0]  # '.'
        if effect.preserve_colors:
            assert dot_attr.original_color == "\033[1;34m"
    
    def test_clustering_effect(self):
        """Test that clustering is applied to character attributes."""
        effect = NMSEffect()
        
        # Create a longer text to test clustering
        text = "This is a longer text to test clustering"
        char_attrs = effect.prepare_text(text)
        
        # Check that reveal times vary (indicating clustering)
        reveal_times = [attr.reveal_time for attr in char_attrs if not attr.is_space]
        
        # Should have some variation in reveal times
        assert len(set(reveal_times)) > 1  # Not all the same
        
        # Should be within expected range
        for time in reveal_times:
            assert 1000 <= time <= 6000
    
    def test_mask_blank_setting(self):
        """Test mask blank space setting."""
        effect = NMSEffect()
        
        text = "A B C"
        
        # Test with mask_blank = False (default)
        effect.set_mask_blank(False)
        char_attrs = effect.prepare_text(text)
        
        space_attrs = [attr for attr in char_attrs if attr.source == ' ']
        for attr in space_attrs:
            assert attr.is_space  # Spaces should be preserved
            assert attr.mask == ' '
        
        # Test with mask_blank = True
        effect.set_mask_blank(True)
        char_attrs = effect.prepare_text(text)
        
        space_attrs = [attr for attr in char_attrs if attr.source == ' ']
        for attr in space_attrs:
            assert not attr.is_space  # Spaces should not be preserved
            assert attr.mask != ' '  # Should have a random mask
    
    def test_execute_empty_text(self):
        """Test executing effect with empty text."""
        effect = NMSEffect()
        
        result = effect.execute("")
        assert result == ""
        
        result = effect.execute("   ")  # Whitespace only
        assert result == ""
    
    @patch('no_more_secrets.effects.nms_effect.enable_ansi_colors')
    @patch('sys.stdout')
    @patch('time.sleep')
    def test_execute_basic(self, mock_sleep, mock_stdout, mock_enable_ansi):
        """Test basic execution of the effect."""
        effect = NMSEffect()
        effect.set_auto_decrypt(True)  # Skip keypress waiting
        
        with patch.object(effect, '_wait_for_keypress'):
            result = effect.execute("Hi")
            assert result == ""
        
        # Should have called enable_ansi_colors
        mock_enable_ansi.assert_called_once()
    
    @patch('no_more_secrets.core.terminal.Terminal.get_platform')
    @patch('time.sleep')
    def test_wait_for_keypress_windows(self, mock_sleep, mock_get_platform):
        """Test wait for keypress on Windows."""
        mock_get_platform.return_value = 'windows'
        effect = NMSEffect()
        
        # Since msvcrt is imported inside the method, we need to mock it at the system level
        with patch('builtins.__import__') as mock_import:
            mock_msvcrt = MagicMock()
            def import_side_effect(name, *args, **kwargs):
                if name == 'msvcrt':
                    return mock_msvcrt
                return __import__(name, *args, **kwargs)
            mock_import.side_effect = import_side_effect
            
            effect._wait_for_keypress()
            # Should not call sleep since msvcrt is available
            mock_sleep.assert_not_called()
    
    @patch('no_more_secrets.core.terminal.Terminal.get_platform')
    @patch('time.sleep')
    def test_wait_for_keypress_unix(self, mock_sleep, mock_get_platform):
        """Test wait for keypress on Unix."""
        mock_get_platform.return_value = 'unix'
        effect = NMSEffect()
        
        # Mock the import and usage
        with patch('builtins.__import__') as mock_import:
            mock_termios = MagicMock()
            mock_tty = MagicMock()
            
            def import_side_effect(name, *args, **kwargs):
                if name == 'termios':
                    return mock_termios
                elif name == 'tty':
                    return mock_tty
                return __import__(name, *args, **kwargs)
            mock_import.side_effect = import_side_effect
            
            with patch('sys.stdin') as mock_stdin:
                mock_stdin.fileno.return_value = 0
                mock_termios.tcgetattr.return_value = "mock_settings"
                mock_stdin.read.return_value = 'a'
                
                effect._wait_for_keypress()
                # Should not call sleep since termios is available
                mock_sleep.assert_not_called()
    
    @patch('time.sleep')
    def test_wait_for_keypress_fallback(self, mock_sleep):
        """Test wait for keypress fallback."""
        effect = NMSEffect()
        
        # Mock to raise exception to trigger fallback
        with patch('no_more_secrets.core.terminal.Terminal.get_platform', side_effect=Exception):
            effect._wait_for_keypress()
            mock_sleep.assert_called_with(2)
    
    def test_complex_ansi_sequences(self):
        """Test handling of complex ANSI sequences like tree output."""
        effect = NMSEffect()
        
        # Simulate tree command output
        tree_output = (
            "\033[1;34m.\033[0m\n"
            "\033[1;90m├── \033[0m\033[34mfolder\033[0m\n"
            "\033[1;90m└── \033[0mfile.txt"
        )
        
        char_attrs = effect.prepare_text(tree_output)
        sources = [attr.source for attr in char_attrs]
        
        # Should extract just the text content
        expected = list(".\n├── folder\n└── file.txt")
        assert sources == expected
    
    def test_unicode_handling(self):
        """Test handling of Unicode characters."""
        effect = NMSEffect()
        
        # Test various Unicode characters
        unicode_text = "Hello 世界 café ñoño"
        char_attrs = effect.prepare_text(unicode_text)
        
        sources = [attr.source for attr in char_attrs]
        expected = list(unicode_text)
        assert sources == expected
        
        # All should have reasonable widths
        for attr in char_attrs:
            assert attr.width >= 1
    
    def test_reveal_time_clustering(self):
        """Test that reveal time clustering works correctly."""
        effect = NMSEffect()
        
        # Use a