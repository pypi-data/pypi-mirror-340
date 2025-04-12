"""
formatters.py - Formatting functionality for vfetch
"""

import re
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED, DOUBLE_EDGE, HEAVY, SIMPLE

# Enhanced box styles for different themes
BOX_STYLES = {
    "default": ROUNDED,
    "matrix": SIMPLE,
    "dracula": DOUBLE_EDGE,
    "sunset": ROUNDED,
    "ocean": DOUBLE_EDGE,
    "monochrome": SIMPLE,
    "retro": HEAVY,
    "forest": ROUNDED,
    "replit": DOUBLE_EDGE,
    "neon": HEAVY,
    "cyberpunk": DOUBLE_EDGE,
    "space": ROUNDED,
    "fire": HEAVY,
    "ice": SIMPLE
}

def format_ascii(ascii_art, theme, colored=True):
    """Format ASCII art with theme colors"""
    if not colored:
        return ascii_art
    
    # Apply primary color to ASCII art
    text = Text(ascii_art)
    text.stylize(theme["primary"])
    return text

def create_info_table(system_data, theme, colored=True, compact=False):
    """Create a formatted table with system information"""
    # Determine box style based on theme
    box_style = BOX_STYLES.get(theme.get("name", "default"), ROUNDED)
    
    # Create table with borders
    table = Table(
        show_header=False,
        show_lines=False,
        box=box_style,
        expand=True,
        padding=(0, 1)
    )
    
    # Add columns
    table.add_column("Category", style=theme["primary"] if colored else "white")
    table.add_column("Information", style=theme["secondary"] if colored else "white")
    
    # Process system information
    for category, data in system_data.items():
        if isinstance(data, dict):
            # Create section header
            table.add_row("", "")
            table.add_row(
                Text(category, style=f"bold {theme['primary' if colored else 'white']}"),
                ""
            )
            
            # Add items in this category
            for key, value in data.items():
                # Colorize numbers in the value
                if colored:
                    formatted_value = colorize_number(str(value), theme, colored)
                else:
                    formatted_value = str(value)
                
                if compact:
                    table.add_row(f"  {key}", formatted_value)
                else:
                    table.add_row(f"  {key}", formatted_value)
    
    return table

def colorize_number(text, theme, colored=True):
    """Colorize numbers in text"""
    if not colored:
        return text
    
    # Regular expression to match numbers
    pattern = r'\b\d+\.?\d*\b'
    
    def repl(match):
        number = match.group(0)
        colored_number = Text(number)
        colored_number.stylize(theme["accent"])
        return colored_number
    
    # Use Text object to create rich formatted text
    result = Text()
    last_end = 0
    
    for match in re.finditer(pattern, text):
        start, end = match.span()
        
        # Add text before the match
        if start > last_end:
            result.append(text[last_end:start])
        
        # Add colored number
        number_text = Text(match.group(0))
        number_text.stylize(theme["accent"])
        result.append(number_text)
        
        last_end = end
    
    # Add any remaining text
    if last_end < len(text):
        result.append(text[last_end:])
    
    return result or text  # Fallback to original text if no replacements made

def create_header(text, theme, colored=True):
    """Create a formatted header with a theme color"""
    if colored:
        header = Text(text)
        header.stylize(f"bold {theme['primary']}")
        return header
    else:
        return text