"""Sneakers - Movie Scene Recreation CLI."""

from __future__ import annotations

import sys

from ..core.terminal import Terminal
from ..effects.nms_effect import NMSEffect


def create_sneakers_display() -> str:
    """Create the display content exactly as seen in the movie."""
    
    # Get terminal dimensions
    rows, cols = Terminal.get_size()
    
    # Menu content from the movie
    head1_left = "DATANET PROC RECORD:  45-3456-W-3452"
    head1_right = "Transnet on/xc-3"
    head2_center = "FEDERAL RESERVE TRANSFER NODE"
    head3_center = "National Headquarters"
    head4_center = "************  Remote Systems Network Input Station  ************"
    head5_center = "================================================================"
    menu1 = "[1] Interbank Funds Transfer  (Code Prog: 485-GWU)"
    menu2 = "[2] International Telelink Access  (Code Lim: XRP-262)"
    menu3 = "[3] Remote Facsimile Send/Receive  (Code Tran:  2LZP-517)"
    menu4 = "[4] Regional Bank Interconnect  (Security Code:  47-B34)"
    menu5 = "[5] Update System Parameters  (Entry Auth. Req.)"
    menu6 = "[6] Remote Operator Logon/Logoff"
    foot1_center = "================================================================"
    foot2_center = "[ ] Select Option or ESC to Abort"
    
    # Build the display string with proper spacing
    display_lines = []
    
    # Header line 1 - left and right aligned
    spaces = cols - len(head1_left) - len(head1_right)
    if spaces < 0:
        spaces = 0
    line1 = head1_left + " " * spaces + head1_right
    display_lines.append(line1)
    
    # Header line 2 - centered
    spaces = (cols - len(head2_center)) // 2
    if spaces < 0:
        spaces = 0
    line2 = " " * spaces + head2_center
    display_lines.append(line2)
    
    # Empty line
    display_lines.append("")
    
    # Header line 3 - centered
    spaces = (cols - len(head3_center)) // 2
    if spaces < 0:
        spaces = 0
    line3 = " " * spaces + head3_center
    display_lines.append(line3)
    
    # Empty line
    display_lines.append("")
    
    # Header line 4 - centered
    spaces = (cols - len(head4_center)) // 2
    if spaces < 0:
        spaces = 0
    line4 = " " * spaces + head4_center
    display_lines.append(line4)
    
    # Header line 5 - centered
    spaces = (cols - len(head5_center)) // 2
    if spaces < 0:
        spaces = 0
    line5 = " " * spaces + head5_center
    display_lines.append(line5)
    
    # Empty line
    display_lines.append("")
    
    # Menu items - indented from center
    menu_indent = ((cols - len(head5_center)) // 2) + 3
    if menu_indent < 0:
        menu_indent = 0
    
    for menu_item in [menu1, menu2, menu3, menu4, menu5, menu6]:
        line = " " * menu_indent + menu_item
        display_lines.append(line)
    
    # Empty line
    display_lines.append("")
    
    # Footer line 1 - centered
    spaces = (cols - len(foot1_center)) // 2
    if spaces < 0:
        spaces = 0
    foot_line1 = " " * spaces + foot1_center
    display_lines.append(foot_line1)
    
    # Empty line
    display_lines.append("")
    
    # Footer line 2 - centered
    spaces = (cols - len(foot2_center)) // 2
    if spaces < 0:
        spaces = 0
    foot_line2 = " " * spaces + foot2_center
    display_lines.append(foot_line2)
    
    return "\n".join(display_lines)


def main() -> None:
    """Main function for the Sneakers recreation."""
    
    try:
        # Create the display content
        display_text = create_sneakers_display()
        
        # Create effect instance with movie-appropriate settings
        effect = NMSEffect()
        effect.set_clear_screen(True)  # Always clear screen for movie effect
        effect.set_foreground_color('blue')  # Classic blue color
        effect.set_auto_decrypt(False)  # Require keypress like in movie
        
        # Execute the effect
        effect.execute(display_text)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()