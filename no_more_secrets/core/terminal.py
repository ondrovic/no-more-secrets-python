"""Terminal manipulation utilities and platform detection."""

from __future__ import annotations

import os
import sys
from typing import Any

# Platform detection and imports
PLATFORM = 'other'

# Global variables for platform-specific modules
termios = None
tty = None
select = None
msvcrt = None

# Try to determine platform and import appropriate modules
try:
    import termios as _termios  # type: ignore[import-untyped]
    import tty as _tty      # type: ignore[import-untyped] 
    import select as _select   # type: ignore[import-untyped]
    termios = _termios
    tty = _tty
    select = _select
    PLATFORM = 'unix'
except ImportError:
    try:
        import msvcrt as _msvcrt  # type: ignore[import-untyped]
        msvcrt = _msvcrt
        PLATFORM = 'windows'
        
        # Enable ANSI color support on Windows
        try:
            import ctypes
            from ctypes import wintypes
            
            # Enable ANSI escape sequence processing
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            
            STD_OUTPUT_HANDLE = -11
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            
            hout = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            if hout == -1:
                raise Exception("Failed to get stdout handle")
            
            dwMode = wintypes.DWORD()
            if kernel32.GetConsoleMode(hout, ctypes.byref(dwMode)) == 0:
                raise Exception("Failed to get console mode")
            
            dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
            if kernel32.SetConsoleMode(hout, dwMode) == 0:
                raise Exception("Failed to set console mode")
                
        except Exception:
            # Fallback: try alternative method
            try:
                os.system('')  # Initialize ANSI on older Windows
            except:
                pass
        
    except ImportError:
        PLATFORM = 'other'


class Terminal:
    """Terminal manipulation utilities."""
    
    @staticmethod
    def get_platform() -> str:
        """Get current platform type."""
        return PLATFORM
    
    @staticmethod
    def get_size() -> tuple[int, int]:
        """Get terminal size (rows, cols)."""
        try:
            import shutil
            size = shutil.get_terminal_size()
            return size.lines, size.columns
        except:
            return 24, 80  # fallback
    
    @staticmethod
    def set_raw_mode() -> Any:
        """Set terminal to raw mode (no echo, no line buffering)."""
        if PLATFORM == 'unix' and sys.stdin.isatty() and termios and tty:
            try:
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                tty.setraw(sys.stdin.fileno())
                return old_settings
            except Exception:
                return None
        return None
    
    @staticmethod
    def restore_mode(old_settings: Any) -> None:
        """Restore terminal to original mode."""
        if PLATFORM == 'unix' and old_settings and sys.stdin.isatty() and termios:
            try:
                fd = sys.stdin.fileno()
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception:
                pass
    
    @staticmethod
    def get_char() -> str:
        """Get a single character from stdin without echo."""
        if PLATFORM == 'windows' and msvcrt:
            if sys.stdin.isatty():
                try:
                    char = msvcrt.getch()
                    if isinstance(char, bytes):
                        return char.decode('utf-8', errors='ignore')
                    return str(char)
                except (KeyboardInterrupt, EOFError):
                    return '\x03'  # Ctrl+C
            else:
                try:
                    return input()
                except (KeyboardInterrupt, EOFError):
                    return '\x03'
        elif PLATFORM == 'unix' and termios and tty:
            if sys.stdin.isatty():
                try:
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(sys.stdin.fileno())
                        ch = sys.stdin.read(1)
                        return ch
                    except (KeyboardInterrupt, EOFError):
                        return '\x03'
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                except Exception:
                    try:
                        return input()
                    except (KeyboardInterrupt, EOFError):
                        return '\x03'
            else:
                try:
                    return input()
                except (KeyboardInterrupt, EOFError):
                    return '\x03'
        else:
            try:
                return input()
            except (KeyboardInterrupt, EOFError):
                return '\x03'
    
    @staticmethod
    def has_input() -> bool:
        """Check if input is available without blocking."""
        if not sys.stdin.isatty():
            return True
        
        if PLATFORM == 'windows' and msvcrt:
            try:
                return msvcrt.kbhit()
            except Exception:
                return False
        elif PLATFORM == 'unix' and select:
            try:
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    return True
            except Exception:
                return False
        
        return False
    
    @staticmethod
    def clear_input() -> None:
        """Clear any pending input."""
        if PLATFORM == 'windows' and msvcrt:
            try:
                while msvcrt.kbhit():
                    msvcrt.getch()
            except Exception:
                pass
        elif PLATFORM == 'unix' and sys.stdin.isatty() and termios:
            try:
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
            except Exception:
                pass


def enable_ansi_colors() -> None:
    """Enable ANSI colors on Windows if needed."""
    if PLATFORM == 'windows':
        try:
            import colorama  # type: ignore[import-untyped]
            colorama.init()
        except ImportError:
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                pass