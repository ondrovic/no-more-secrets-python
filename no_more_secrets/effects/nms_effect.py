"""Main NMS (No More Secrets) effect implementation."""

from __future__ import annotations

import random
import re
import sys
import time
from typing import List

from ..core.char_attr import CharAttr
from ..core.charset import (
    get_random_char,
    get_random_char_excluding_control,
    get_random_printable_char,
    get_random_extended_char,
    get_random_box_drawing_char,
)
from ..core.colors import Colors, get_color_map, get_color_prefix, hex_to_rgb, rgb_to_ansi
from ..core.terminal import Terminal, enable_ansi_colors
from ..utils.encoding import get_char_width


class NMSEffect:
    """Main class implementing the No More Secrets effect."""
    
    def __init__(self) -> None:
        """Initialize the NMS effect with default settings."""
        self.auto_decrypt = False
        self.mask_blank = False
        self.clear_screen = False
        self.foreground_color = Colors.BLUE
        self.custom_hex_color: str | None = None
        self.preserve_colors = False
        self.charset_mode = "full"  # "full", "no_control", "printable", "extended", "box_drawing"
    
    def set_auto_decrypt(self, setting: bool) -> None:
        """Set auto-decrypt mode."""
        self.auto_decrypt = setting
    
    def set_mask_blank(self, setting: bool) -> None:
        """Set whether to mask blank spaces."""
        self.mask_blank = setting
    
    def set_clear_screen(self, setting: bool) -> None:
        """Set whether to clear screen before effect."""
        self.clear_screen = setting
    
    def set_foreground_color(self, color: str) -> None:
        """Set the foreground color for revealed text."""
        color = color.lower()
        color_map = get_color_map()
        if color in color_map:
            self.foreground_color = color_map[color]
            self.custom_hex_color = None  # Reset custom color
        else:
            self.foreground_color = Colors.BLUE
            self.custom_hex_color = None
    
    def set_hex_color(self, hex_color: str) -> None:
        """Set a custom hex color for revealed text."""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Validate hex color
        if len(hex_color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in hex_color):
            self.custom_hex_color = hex_color
        else:
            print(f"ERROR: Invalid hex color '{hex_color}'. Use format like 'FF0000' or '#00FF00'", file=sys.stderr)
            self.custom_hex_color = None
    
    def set_preserve_colors(self, setting: bool) -> None:
        """Set whether to preserve original terminal colors."""
        self.preserve_colors = setting
    
    def set_charset_mode(self, mode: str) -> None:
        """Set the character set mode for scrambling effect.
        
        Args:
            mode: One of "full", "no_control", "printable", "extended", "box_drawing"
        """
        valid_modes = ["full", "no_control", "printable", "extended", "box_drawing"]
        if mode in valid_modes:
            self.charset_mode = mode
        else:
            print(f"ERROR: Invalid charset mode '{mode}'. Valid modes: {', '.join(valid_modes)}", file=sys.stderr)
            self.charset_mode = "full"
    
    def _get_scramble_char(self) -> str:
        """Get a scrambling character based on the current charset mode."""
        if self.charset_mode == "full":
            return get_random_char()
        elif self.charset_mode == "no_control":
            return get_random_char_excluding_control()
        elif self.charset_mode == "printable":
            return get_random_printable_char()
        elif self.charset_mode == "extended":
            return get_random_extended_char()
        elif self.charset_mode == "box_drawing":
            return get_random_box_drawing_char()
        else:
            return get_random_char()  # fallback
    
    def parse_ansi_text(self, text: str) -> List[CharAttr]:
        """Parse text with ANSI codes and preserve color information."""
        char_attrs = []
        current_color = ""
        
        # More comprehensive ANSI escape sequence pattern
        ansi_pattern = re.compile(r'\033\[[0-9;]*[a-zA-Z]')
        
        i = 0
        while i < len(text):
            # Check for ANSI escape sequence
            if text[i:i+1] == '\033':
                # Find the full ANSI sequence
                match = ansi_pattern.match(text[i:])
                if match:
                    ansi_code = match.group()
                    if ansi_code == '\033[0m':
                        current_color = ""  # Reset color
                    else:
                        # Only store color if we're preserving colors
                        if self.preserve_colors:
                            current_color = ansi_code
                    i += len(ansi_code)
                    continue
            
            # Regular character
            char = text[i]
            
            # Determine if it's a space character we should preserve
            is_space = char.isspace() and (not self.mask_blank or char != ' ')
            
            # For non-space characters, use a mask based on charset mode
            if is_space:
                mask = char
            else:
                mask = self._get_scramble_char()
            
            # Get display width
            width = get_char_width(char)
            
            # Set reveal time - create clusters by grouping characters
            reveal_time = random.randint(1000, 6000)  # 1-6 seconds
            
            char_attrs.append(CharAttr(char, mask, width, is_space, reveal_time, current_color))
            i += 1
        
        # Apply clustering effect
        self._apply_clustering(char_attrs)
        
        return char_attrs
    
    def _apply_clustering(self, char_attrs: List[CharAttr]) -> None:
        """Apply clustering effect to character attributes."""
        for i in range(len(char_attrs)):
            if not char_attrs[i].is_space:
                # 30% chance to create a cluster
                if random.random() < 0.3:
                    base_time = char_attrs[i].reveal_time
                    # Cluster with 1-3 adjacent characters
                    cluster_size = random.randint(1, 3)
                    for j in range(max(0, i-cluster_size//2), min(len(char_attrs), i+cluster_size//2+1)):
                        if not char_attrs[j].is_space:
                            # Make nearby characters reveal around the same time
                            char_attrs[j].reveal_time = base_time + random.randint(-200, 200)
    
    def prepare_text(self, text: str) -> List[CharAttr]:
        """Prepare text for the decryption effect."""
        # Always parse ANSI codes to properly handle colored input
        # But only preserve colors if preserve_colors is True
        return self.parse_ansi_text(text)
    
    def _prepare_text_simple(self, text: str) -> List[CharAttr]:
        """Prepare text without ANSI parsing (original method)."""
        char_attrs = []
        
        # Handle the text character by character, including multi-byte UTF-8
        i = 0
        while i < len(text):
            char = text[i]
            
            # Handle Unicode properly - get the full character
            from ..utils.encoding import safe_char_decode
            char = safe_char_decode(char)
            
            # Determine if it's a space character we should preserve
            is_space = char.isspace() and (not self.mask_blank or char != ' ')
            
            # For non-space characters, use a mask based on charset mode
            if is_space:
                mask = char
            else:
                mask = self._get_scramble_char()
            
            # Get display width
            width = get_char_width(char)
            
            # Set reveal time - create clusters by grouping characters
            # Characters reveal in waves across the text
            reveal_time = random.randint(1000, 6000)  # 1-6 seconds
            
            char_attrs.append(CharAttr(char, mask, width, is_space, reveal_time))
            i += 1
        
        # Apply clustering effect
        self._apply_clustering(char_attrs)
        
        return char_attrs
    
    def _wait_for_keypress(self) -> None:
        """Wait for a keypress in a cross-platform way."""
        try:
            if Terminal.get_platform() == 'windows':
                try:
                    import msvcrt
                    msvcrt.getch()
                except ImportError:
                    time.sleep(2)  # Fallback if msvcrt not available
            else:
                # Unix - set terminal to raw mode temporarily
                try:
                    import termios
                    import tty
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(sys.stdin.fileno())
                        sys.stdin.read(1)
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                except ImportError:
                    time.sleep(2)  # Fallback if termios/tty not available
        except Exception:
            time.sleep(2)  # Fallback
    
    def execute(self, text: str) -> str:
        """Execute the complete NMS effect - movie style."""
        if not text.strip():
            return ""

        # Enable ANSI colors on Windows
        enable_ansi_colors()

        # Get the color prefix
        if self.custom_hex_color:
            r, g, b = hex_to_rgb(self.custom_hex_color)
            color_prefix = rgb_to_ansi(r, g, b)
        else:
            color_prefix = get_color_prefix(
                color_name=None if self.foreground_color == Colors.BLUE else 
                next((name for name, code in get_color_map().items() if code == self.foreground_color), None)
            )

        try:
            # Save current terminal state and clear screen
            print("\033[?47h", end='')  # Save screen
            print("\033[2J", end='')    # Clear screen
            print("\033[H", end='')     # Home cursor
            print("\033[?25l", end='')  # Hide cursor
            sys.stdout.flush()
            
            # Prepare character attributes
            char_attrs = self.prepare_text(text)
            
            # Phase 1: Type out scrambled text
            print("\033[H", end='')
            for attr in char_attrs:
                if attr.is_space:
                    print(attr.source, end='')
                else:
                    print(attr.mask, end='')
                sys.stdout.flush()
                time.sleep(0.004)
            
            # Wait for keypress or auto-decrypt
            if self.auto_decrypt:
                time.sleep(1)
            else:
                self._wait_for_keypress()
            
            # Phase 2: Jumble effect using charset mode
            start_time = time.time()
            while time.time() - start_time < 2.0:
                print("\033[H", end='')
                for attr in char_attrs:
                    if attr.is_space:
                        print(attr.source, end='')
                    else:
                        print(self._get_scramble_char(), end='')
                sys.stdout.flush()
                time.sleep(0.035)
            
            # Phase 3: Reveal effect with EXPLICIT color codes
            while True:
                print("\033[H", end='')  # Go to start of screen
                
                all_revealed = True
                any_changed = False
                
                for i, attr in enumerate(char_attrs):
                    if attr.is_space:
                        print(attr.source, end='')
                        continue
                    
                    # Check if this character should be revealed
                    if attr.reveal_time > 0:
                        # Still scrambled - use charset mode for scrambling
                        attr.reveal_time -= 50
                        if random.randint(0, 5) == 0:
                            attr.mask = self._get_scramble_char()
                        print(attr.mask, end='')  # WHITE/NORMAL
                        all_revealed = False
                    else:
                        # REVEAL THIS CHARACTER WITH ORIGINAL OR CHOSEN COLOR
                        if not attr.is_revealed:
                            attr.is_revealed = True
                            any_changed = True
                        
                        # Choose color based on preserve_colors setting
                        if self.preserve_colors and attr.original_color:
                            # Use original color from terminal
                            color_prefix_final = attr.original_color
                            if not color_prefix_final.endswith('m'):
                                color_prefix_final += 'm'
                            print(color_prefix_final + attr.source + "\033[0m", end='')
                        else:
                            # Use selected/custom color
                            print(color_prefix + attr.source + "\033[0m", end='')
                
                sys.stdout.flush()
                
                if all_revealed:
                    break
                    
                if any_changed:
                    time.sleep(0.15)  # Pause on reveals
                else:
                    time.sleep(0.05)
            
            # Show cursor and wait
            print("\033[?25h", end='')
            sys.stdout.flush()
            self._wait_for_keypress()
                
        except KeyboardInterrupt:
            pass
        finally:
            # Restore original terminal state
            print("\033[?25h", end='')  # Show cursor
            print("\033[?47l", end='')  # Restore screen
            sys.stdout.flush()
        
        return ""