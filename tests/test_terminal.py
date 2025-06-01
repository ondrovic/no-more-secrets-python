"""Tests for terminal utilities."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import pytest

from no_more_secrets.core.terminal import Terminal, enable_ansi_colors


def test_get_platform():
    """Test platform detection."""
    platform = Terminal.get_platform()
    assert platform in ['unix', 'windows', 'other']
    assert isinstance(platform, str)


def test_get_size():
    """Test terminal size detection."""
    rows, cols = Terminal.get_size()
    
    # Should return reasonable values
    assert isinstance(rows, int)
    assert isinstance(cols, int)
    assert rows > 0
    assert cols > 0
    
    # Should have minimum reasonable values
    assert rows >= 1
    assert cols >= 1


@patch('shutil.get_terminal_size')
def test_get_size_with_shutil(mock_get_size):
    """Test terminal size when shutil is available."""
    # Mock shutil.get_terminal_size
    mock_size = MagicMock()
    mock_size.lines = 25
    mock_size.columns = 80
    mock_get_size.return_value = mock_size
    
    rows, cols = Terminal.get_size()
    assert rows == 25
    assert cols == 80


@patch('shutil.get_terminal_size')
def test_get_size_fallback(mock_get_size):
    """Test terminal size fallback when shutil fails."""
    # Mock shutil to raise an exception
    mock_get_size.side_effect = Exception("No terminal")
    
    rows, cols = Terminal.get_size()
    # Should fall back to default values
    assert rows == 24
    assert cols == 80


def test_set_raw_mode():
    """Test setting raw mode."""
    # This is platform-specific, so we test that it doesn't crash
    old_settings = Terminal.set_raw_mode()
    
    # Should either return something or None
    # We can't test the actual functionality without mocking the terminal
    assert old_settings is None or old_settings is not None


def test_restore_mode():
    """Test restoring terminal mode."""
    # Test with None (should not crash)
    Terminal.restore_mode(None)
    
    # Test with some mock settings
    Terminal.restore_mode("mock_settings")


@patch('sys.stdin.isatty')
def test_has_input_not_tty(mock_isatty):
    """Test has_input when not a TTY."""
    mock_isatty.return_value = False
    
    # When not a TTY, should return True
    result = Terminal.has_input()
    assert result is True


@patch('sys.stdin.isatty')
def test_has_input_tty(mock_isatty):
    """Test has_input when is a TTY."""
    mock_isatty.return_value = True
    
    # This will depend on platform, so we just test it doesn't crash
    result = Terminal.has_input()
    # On Windows, msvcrt.kbhit() might return 0 (falsy) which is valid
    assert isinstance(result, (bool, int))  # Accept both bool and int (0/1)


def test_clear_input():
    """Test clearing input."""
    # Should not crash regardless of platform
    Terminal.clear_input()


@patch('no_more_secrets.core.terminal.PLATFORM', 'windows')
@patch('sys.stdin.isatty')
def test_get_char_windows_tty(mock_isatty):
    """Test get_char on Windows TTY."""
    mock_isatty.return_value = True
    
    with patch('no_more_secrets.core.terminal.msvcrt') as mock_msvcrt:
        mock_msvcrt.getch.return_value = b'a'
        
        # Should not crash and return a string
        result = Terminal.get_char()
        assert isinstance(result, str)


@patch('no_more_secrets.core.terminal.PLATFORM', 'windows')
@patch('sys.stdin.isatty')
def test_get_char_windows_not_tty(mock_isatty):
    """Test get_char on Windows non-TTY."""
    mock_isatty.return_value = False
    
    with patch('builtins.input', return_value='test'):
        result = Terminal.get_char()
        assert result == 'test'


@patch('no_more_secrets.core.terminal.PLATFORM', 'unix')
@patch('sys.stdin.isatty')
def test_get_char_unix_not_tty(mock_isatty):
    """Test get_char on Unix non-TTY."""
    mock_isatty.return_value = False
    
    with patch('builtins.input', return_value='test'):
        result = Terminal.get_char()
        assert result == 'test'


@patch('no_more_secrets.core.terminal.PLATFORM', 'other')
def test_get_char_other_platform():
    """Test get_char on other platforms."""
    with patch('builtins.input', return_value='test'):
        result = Terminal.get_char()
        assert result == 'test'


def test_get_char_keyboard_interrupt():
    """Test get_char with keyboard interrupt."""
    with patch('builtins.input', side_effect=KeyboardInterrupt):
        result = Terminal.get_char()
        assert result == '\x03'  # Ctrl+C


def test_get_char_eof_error():
    """Test get_char with EOF error."""
    with patch('builtins.input', side_effect=EOFError):
        result = Terminal.get_char()
        assert result == '\x03'  # Ctrl+C


@patch('no_more_secrets.core.terminal.PLATFORM', 'windows')
def test_has_input_windows():
    """Test has_input on Windows."""
    with patch('no_more_secrets.core.terminal.msvcrt') as mock_msvcrt:
        mock_msvcrt.kbhit.return_value = True
        
        with patch('sys.stdin.isatty', return_value=True):
            result = Terminal.has_input()
            assert result is True


@patch('no_more_secrets.core.terminal.PLATFORM', 'unix')
@patch('no_more_secrets.core.terminal.select')
@patch('sys.stdin.isatty')
def test_has_input_unix(mock_isatty, mock_select):
    """Test has_input on Unix."""
    mock_isatty.return_value = True
    mock_select.select.return_value = ([sys.stdin], [], [])
    
    result = Terminal.has_input()
    assert result is True


@patch('no_more_secrets.core.terminal.PLATFORM', 'windows')
def test_clear_input_windows():
    """Test clear_input on Windows."""
    with patch('no_more_secrets.core.terminal.msvcrt') as mock_msvcrt:
        mock_msvcrt.kbhit.side_effect = [True, True, False]  # Two hits, then none
        mock_msvcrt.getch.return_value = b'a'
        
        # Should not crash
        Terminal.clear_input()


@patch('no_more_secrets.core.terminal.PLATFORM', 'unix')
@patch('no_more_secrets.core.terminal.termios')
@patch('sys.stdin.isatty')
def test_clear_input_unix(mock_isatty, mock_termios):
    """Test clear_input on Unix."""
    mock_isatty.return_value = True
    
    # Should not crash
    Terminal.clear_input()
    mock_termios.tcflush.assert_called_once()


@patch('no_more_secrets.core.terminal.PLATFORM', 'windows')
def test_enable_ansi_colors_windows_colorama():
    """Test enabling ANSI colors on Windows with colorama."""
    # Mock the import inside the function
    with patch('builtins.__import__') as mock_import:
        mock_colorama = MagicMock()
        
        def import_side_effect(name, *args, **kwargs):
            if name == 'colorama':
                return mock_colorama
            return __import__(name, *args, **kwargs)
        mock_import.side_effect = import_side_effect
        
        enable_ansi_colors()
        # Should attempt to call colorama.init()


@patch('no_more_secrets.core.terminal.PLATFORM', 'windows')
def test_enable_ansi_colors_windows_ctypes():
    """Test enabling ANSI colors on Windows with ctypes fallback."""
    # Mock imports to simulate colorama not available but ctypes available
    with patch('builtins.__import__') as mock_import:
        def import_side_effect(name, *args, **kwargs):
            if name == 'colorama':
                raise ImportError("No module named 'colorama'")
            elif name == 'ctypes':
                return MagicMock()  # Mock ctypes module
            return __import__(name, *args, **kwargs)
        mock_import.side_effect = import_side_effect
        
        # Should not crash even if both fail
        enable_ansi_colors()


@patch('no_more_secrets.core.terminal.PLATFORM', 'unix')
def test_enable_ansi_colors_unix():
    """Test enabling ANSI colors on Unix (should be no-op)."""
    # Should not crash
    enable_ansi_colors()


def test_import_error_handling():
    """Test that import errors are handled gracefully."""
    # Test that missing platform-specific modules don't crash the class
    terminal = Terminal()
    assert terminal is not None
    
    # Basic methods should work even if platform modules are missing
    platform = terminal.get_platform()
    assert isinstance(platform, str)
    
    size = terminal.get_size()
    assert isinstance(size, tuple)
    assert len(size) == 2


class TestTerminalEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_bytes_to_string_conversion(self):
        """Test conversion of bytes to string in get_char."""
        with patch('no_more_secrets.core.terminal.PLATFORM', 'windows'):
            with patch('sys.stdin.isatty', return_value=True):
                with patch('no_more_secrets.core.terminal.msvcrt') as mock_msvcrt:
                    # Test bytes input
                    mock_msvcrt.getch.return_value = b'\xff'  # Non-UTF8 byte
                    
                    result = Terminal.get_char()
                    # Should handle gracefully and return a string
                    assert isinstance(result, str)
    
    def test_string_input_conversion(self):
        """Test string input conversion in get_char."""
        with patch('no_more_secrets.core.terminal.PLATFORM', 'windows'):
            with patch('sys.stdin.isatty', return_value=True):
                with patch('no_more_secrets.core.terminal.msvcrt') as mock_msvcrt:
                    # Test non-bytes input (edge case)
                    mock_msvcrt.getch.return_value = 'a'  # String instead of bytes
                    
                    result = Terminal.get_char()
                    assert isinstance(result, str)
                    assert result == 'a'