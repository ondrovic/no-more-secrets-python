"""ANSI code utilities for parsing and stripping color codes."""

from __future__ import annotations

import re


# More comprehensive ANSI pattern that handles complex sequences
ANSI_PATTERN = re.compile(r'\033\[[0-9;]*[a-zA-Z]')


def strip_ansi_codes(text: str) -> str:
    """Strip all ANSI escape codes from text."""
    return ANSI_PATTERN.sub('', text)


def has_ansi_codes(text: str) -> bool:
    """Check if text contains ANSI escape codes."""
    return bool(ANSI_PATTERN.search(text))


def extract_ansi_codes(text: str) -> list[str]:
    """Extract all ANSI codes from text."""
    return ANSI_PATTERN.findall(text)