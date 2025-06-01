# API Reference

This page provides detailed documentation of the No More Secrets Python package.

## Main Classes

### NMSEffect

The main class for creating the "No More Secrets" decryption effect.

::: no_more_secrets.effects.nms_effect.NMSEffect

## Core Components

### Colors

ANSI color utilities and escape code generation.

::: no_more_secrets.core.colors

### Terminal

Cross-platform terminal manipulation utilities.

::: no_more_secrets.core.terminal.Terminal

### CharAttr

Character attribute class for tracking character state during the effect.

::: no_more_secrets.core.char_attr.CharAttr

## Utilities

### Encoding

Text encoding and character width utilities.

::: no_more_secrets.utils.encoding

### ANSI

ANSI escape sequence parsing and manipulation.

::: no_more_secrets.utils.ansi

### Input Handler

Input handling from pipes and user input.

::: no_more_secrets.utils.input_handler

## Command Line Interface

### Main CLI

The main `nms` command implementation.

::: no_more_secrets.cli.main

### Sneakers

The `sneakers` command for movie scene recreation.

::: no_more_secrets.cli.sneakers

## Example Usage

### Basic Effect

```python
from no_more_secrets import NMSEffect

# Create effect instance
effect = NMSEffect()

# Configure the effect
effect.set_foreground_color('green')
effect.set_auto_decrypt(True)

# Execute the effect
effect.execute("Hello, World!")
```

### Custom Hex Color

```python
from no_more_secrets import NMSEffect

effect = NMSEffect()
effect.set_hex_color('FF6600')  # Orange color
effect.execute("Custom colored text")
```

### Preserve Original Colors

```python
from no_more_secrets import NMSEffect

effect = NMSEffect()
effect.set_preserve_colors(True)

# This will preserve any ANSI colors in the input text
colored_text = "\033[31mRed\033[0m and \033[32mGreen\033[0m text"
effect.execute(colored_text)
```

## Error Handling

The library handles various error conditions gracefully:

- **Platform-specific modules**: Gracefully degrades when platform-specific modules (termios, msvcrt) are unavailable
- **Unicode handling**: Safely processes Unicode characters and handles encoding issues
- **Terminal compatibility**: Works across different terminal types and sizes
- **Keyboard interrupts**: Properly handles Ctrl+C and restores terminal state

## Performance Considerations

- The effect uses sleep delays for timing, which means it's not CPU-intensive
- Large text inputs will take proportionally longer to complete
- Auto-decrypt mode (`-a`) skips user input waiting for faster execution
- Terminal size is automatically detected and handled

## Cross-Platform Support

The library works across different platforms:

- **Linux/Unix**: Full functionality with termios support
- **macOS**: Full functionality with termios support  
- **Windows**: Full functionality with msvcrt and colorama support
- **Other platforms**: Basic functionality with graceful degradation