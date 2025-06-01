"""Main CLI entry point for the nms command."""

from __future__ import annotations

import argparse
import re
import sys

from no_more_secrets.utils.ansi import has_ansi_codes

from ..effects.nms_effect import NMSEffect
from ..utils.input_handler import get_input


def test_colors() -> None:
    """Test color output and exit."""
    print("Testing colors...")
    print("White: \033[1;37mWHITE\033[0m")
    print("Red: \033[1;31mRED\033[0m")
    print("Green: \033[1;32mGREEN\033[0m")
    print("Blue: \033[1;34mBLUE\033[0m")
    print("Yellow: \033[1;33mYELLOW\033[0m")
    print("Magenta: \033[1;35mMAGENTA\033[0m")
    print("Cyan: \033[1;36mCYAN\033[0m")
    print("Custom Orange: \033[1;38;2;255;102;0mORANGE\033[0m")
    print("Custom Purple: \033[1;38;2;128;0;128mPURPLE\033[0m")
    print("\nTo test with original colors, try:")
    print("  ls --color=always | nms -a -o")
    print("  tree -C | nms -a -o")


def check_for_ansi_colors(text: str) -> bool:
    """Check if text contains ANSI color codes."""
    ansi_pattern = re.compile(r'\033\[[0-9;]*m')
    return bool(ansi_pattern.search(text))


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Recreate the famous data decryption effect from the 1992 movie Sneakers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  echo "Hello World" | nms
  cat file.txt | nms -a -f green
  nms "Secret message"
  echo "Custom color" | nms -a -x FF6600
  ls --color=always | nms -a -o  # Force colors through pipe
        """
    )
    
    parser.add_argument('-a', '--auto', action='store_true',
                       help='Auto-decrypt flag (no keypress required)')
    parser.add_argument('-s', '--mask-spaces', action='store_true',
                       help='Mask blank space characters')
    parser.add_argument('-f', '--foreground', default='blue',
                       choices=['white', 'yellow', 'black', 'magenta', 'blue', 'green', 'red', 'cyan'],
                       help='Foreground color of decrypted text (default: blue)')
    parser.add_argument('-x', '--hex', dest='hex_color', metavar='RRGGBB',
                       help='Use custom hex color (e.g., FF0000 for red, 00FF00 for green)')
    parser.add_argument('-o', '--original', action='store_true',
                       help='Preserve original terminal colors from command output')
    parser.add_argument('--test-colors', action='store_true',
                       help='Test color output and exit')
    parser.add_argument('-v', '--version', action='version', version='nms-python 1.0.0')
    parser.add_argument('text', nargs='?', help='Text to process (if not using pipe)')
    
    return parser


def main() -> None:
    """Main function."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Test colors if requested
    if args.test_colors:
        test_colors()
        return
    
    # Get input text
    if args.text:
        text = args.text
    else:
        text = get_input("Enter text: " if sys.stdin.isatty() else None)
    
    # Show helpful message if -o flag used but no colors detected
    if args.original:
        if not has_ansi_codes(text):
            print("⚠️  No colors detected in input. To force colors through pipes:", file=sys.stderr)
            print("   ls --color=always | nms -a -o", file=sys.stderr)
            print("   tree -C | nms -a -o", file=sys.stderr)
            print("   Get-ChildItem | Out-String -Stream | nms -a -o", file=sys.stderr)
            print("", file=sys.stderr)
    
    if not text.strip():
        print("Error: No input provided.", file=sys.stderr)
        sys.exit(1)
    
    # Create effect instance
    effect = NMSEffect()
    effect.set_auto_decrypt(args.auto)
    effect.set_mask_blank(args.mask_spaces)
    effect.set_preserve_colors(args.original)
    
    # Set color - original colors take priority, then hex, then foreground
    if not args.original:
        if args.hex_color:
            # Clean up hex color input (remove quotes, spaces, etc.)
            hex_color = args.hex_color.strip('\'"').strip()
            effect.set_hex_color(hex_color)
        else:
            effect.set_foreground_color(args.foreground)
    
    # Execute effect
    try:
        effect.execute(text)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()