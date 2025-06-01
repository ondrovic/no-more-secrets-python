"""Input handling utilities for reading from pipes and user input."""

from __future__ import annotations

import sys
from typing import Optional

from ..core.terminal import Terminal
from .encoding import fix_encoding_issues


def get_input(prompt: Optional[str] = None) -> str:
    """Get input from pipe or user prompt."""
    if not sys.stdin.isatty():
        # Input from pipe - handle encoding properly
        try:
            # On Windows, try different approaches to get proper UTF-8
            if Terminal.get_platform() == 'windows':
                # Method 1: Try reading as UTF-8 bytes and decode
                try:
                    input_data = sys.stdin.buffer.read()
                    # Try UTF-8 first
                    text = input_data.decode('utf-8', errors='replace')
                    
                    # Fix common encoding issues
                    text = fix_encoding_issues(text)
                    
                    return text
                except:
                    # Fallback to regular stdin and fix encoding
                    text = sys.stdin.read()
                    return fix_encoding_issues(text)
            else:
                # Unix/Linux - should handle UTF-8 properly
                input_data = sys.stdin.buffer.read()
                text = input_data.decode('utf-8', errors='replace')
                return fix_encoding_issues(text)
        except:
            # Final fallback
            text = sys.stdin.read()
            return fix_encoding_issues(text)
    elif prompt:
        # Interactive input with prompt
        return input(prompt)
    else:
        print("Error: No input provided. Use pipe or provide text.", file=sys.stderr)
        sys.exit(1)