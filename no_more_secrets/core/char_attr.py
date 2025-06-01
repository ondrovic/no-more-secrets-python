"""Character attribute classes for the NMS effect."""

from __future__ import annotations


class CharAttr:
    """Character attributes for the decryption effect."""
    
    def __init__(
        self, 
        source: str, 
        mask: str, 
        width: int, 
        is_space: bool, 
        reveal_time: int, 
        original_color: str = ""
    ) -> None:
        """Initialize character attributes.
        
        Args:
            source: Original character
            mask: Scrambled character to display
            width: Display width of character
            is_space: Whether character is whitespace
            reveal_time: Time in milliseconds before character is revealed
            original_color: Original ANSI color code (if preserving colors)
        """
        self.source = source
        self.mask = mask
        self.width = width
        self.is_space = is_space
        self.reveal_time = reveal_time
        self.is_revealed = False
        self.original_color = original_color
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"CharAttr(source={self.source!r}, mask={self.mask!r}, "
            f"width={self.width}, is_space={self.is_space}, "
            f"reveal_time={self.reveal_time}, is_revealed={self.is_revealed})"
        )