# No More Secrets - Python

A Python recreation of the famous data decryption effect from the 1992 hacker movie "Sneakers".

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-GPL--3.0-green.svg)

## Quick Start

### Installation

```bash
# Install with pip
pip install no-more-secrets

# Or install from source
git clone https://github.com/ondrovic/no-more-secrets-python.git
cd no-more-secrets-python
poetry install
```

### Basic Usage

```bash
# Pipe text to nms
echo "Hello World" | nms

# Auto-decrypt with green color
echo "Secret message" | nms -a -f green

# Custom hex color
echo "Custom color" | nms -a -x FF6600

# Preserve original colors
ls --color=always | nms -a -o

# Recreate the Sneakers movie scene
sneakers
```

## Features

- **Pipe Support**: Works with piped data from other commands
- **Color Options**: Multiple foreground colors including custom hex colors
- **Auto-decrypt**: Optional automatic decryption without keypress
- **UTF-8 Support**: Handles Unicode characters properly
- **Color Preservation**: Can preserve original terminal colors
- **Cross-platform**: Works on Linux, macOS, and Windows

## Command Line Options

| Option | Description |
|--------|-------------|
| `-a, --auto` | Auto-decrypt flag (no keypress required) |
| `-s, --mask-spaces` | Mask blank space characters |
| `-f COLOR` | Set foreground color (white, yellow, black, magenta, blue, green, red, cyan) |
| `-x RRGGBB` | Use custom hex color (e.g., FF0000 for red) |
| `-o, --original` | Preserve original terminal colors |
| `--test-colors` | Test color output and exit |

## Examples

### System Administration
```bash
# Show system info with effect
uname -a | nms -f green

# Display directory listing with preserved colors
ls -la --color=always | nms -a -o

# Show network configuration
ifconfig | nms -f cyan
```

### Creative Uses
```bash
# Birthday surprise
echo "Happy Birthday!" | nms -f yellow

# Make log files look like movie hacking
tail /var/log/syslog | nms -f green -a

# Custom orange color for warnings
echo "Warning: System breach detected!" | nms -x FF6600
```

## Technical Details

### Character Set
Uses the CP437 character set (original IBM PC) for the scrambling effect, including:
- Standard ASCII characters
- Extended ASCII symbols  
- Box drawing characters
- Mathematical symbols
- Greek letters

### Effect Timing
- **Typing Effect**: 4ms per character
- **Jumble Duration**: 2 seconds
- **Reveal Speed**: 50ms between updates
- **Random Reveal Time**: 0-6000ms per character

## Requirements

- Python 3.10 or higher
- Terminal that supports ANSI escape sequences
- Optional: colorama for enhanced Windows support

## Credits

- Original C implementation by [Brian Barto](https://github.com/bartobri/no-more-secrets)
- Movie "Sneakers" (1992) for the inspiration
- Python implementation for educational and compatibility purposes

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/ondrovic/no-more-secrets-python/blob/main/LICENSE) file for details.