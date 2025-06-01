"""ANSI color and terminal escape code utilities."""

from __future__ import annotations


class Colors:
    """ANSI escape codes for terminal colors and cursor control."""
    
    # Terminal control codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CLEAR_SCREEN = "\033[2J"
    CURSOR_HOME = "\033[H"
    CURSOR_HIDE = "\033[?25l"
    CURSOR_SHOW = "\033[?25h"
    SCREEN_SAVE = "\033[?47h"
    SCREEN_RESTORE = "\033[?47l"
    CURSOR_SAVE = "\033[s"
    CURSOR_RESTORE = "\033[u"
    
    # Foreground color codes
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    
    @staticmethod
    def fg(color_code: int) -> str:
        """Generate foreground color escape sequence."""
        return f"\033[{color_code}m"
    
    @staticmethod
    def move_cursor(row: int, col: int) -> str:
        """Generate cursor movement escape sequence."""
        return f"\033[{row};{col}H"


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_ansi(r: int, g: int, b: int) -> str:
    """Convert RGB values to ANSI 24-bit color code."""
    return f"\033[1;38;2;{r};{g};{b}m"


def get_color_map() -> dict[str, int]:
    """Get mapping of color names to color codes."""
    return {
        'white': Colors.WHITE,
        'yellow': Colors.YELLOW,
        'black': Colors.BLACK,
        'magenta': Colors.MAGENTA,
        'blue': Colors.BLUE,
        'green': Colors.GREEN,
        'red': Colors.RED,
        'cyan': Colors.CYAN,
    }


def get_color_prefix(color_name: str | None = None, hex_color: str | None = None) -> str:
    """Get ANSI color prefix for given color name or hex value."""
    if hex_color:
        r, g, b = hex_to_rgb(hex_color)
        return rgb_to_ansi(r, g, b)
    
    color_map = get_color_map()
    color_codes = {
        Colors.WHITE: "\033[1;37m",
        Colors.YELLOW: "\033[1;33m", 
        Colors.BLACK: "\033[1;30m",
        Colors.MAGENTA: "\033[1;35m",
        Colors.BLUE: "\033[1;34m",
        Colors.GREEN: "\033[1;32m",
        Colors.RED: "\033[1;31m",
        Colors.CYAN: "\033[1;36m"
    }
    
    if color_name and color_name.lower() in color_map:
        color_code = color_map[color_name.lower()]
        return color_codes.get(color_code, "\033[1;34m")  # Default to blue
    
    return "\033[1;34m"  # Default blue