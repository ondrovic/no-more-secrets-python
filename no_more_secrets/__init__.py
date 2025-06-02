"""No More Secrets - Python Implementation.

A Python recreation of the famous data decryption effect from the 1992 movie Sneakers.
"""

from __future__ import annotations
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("no-more-secrets")  # This should match your package name in pyproject.toml
except PackageNotFoundError:
    __version__ = "unknown"

__author__ = "Chris Ondrovic"
__email__ = "ondrovic@gmail.com"

from .effects.nms_effect import NMSEffect

__all__ = ["NMSEffect"]