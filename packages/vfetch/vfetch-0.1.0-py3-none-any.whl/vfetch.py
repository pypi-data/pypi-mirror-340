#!/usr/bin/env python3
"""
vfetch - A Python-based system information fetching tool
Similar to neofetch but with enhanced visuals and functionality
"""

import argparse
import os
import time
import platform
import logging
from collections import OrderedDict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.box import DOUBLE_EDGE, ROUNDED, HEAVY
from rich.text import Text
from rich.columns import Columns

import ascii_art
import system_info
import formatters
import themes

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="vfetch_debug.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="vfetch - An enhanced system information display tool"
    )
    parser.add_argument(
        "-t", "--theme",
        choices=list(themes.THEMES.keys()),
        help="Color theme to use for display (required)"
    )
    parser.add_argument(
        "-a", "--ascii",
        choices=list(ascii_art.ASCII_OPTIONS.keys()),
        help="ASCII art to display (required)"
    )
    parser.add_argument(
        "-c", "--compact",
        action="store_true",
        help="Display information in compact mode"
    )
    parser.add_argument(
        "-p", "--performance",
        action="store_true",
        help="Include performance metrics (CPU load, memory usage, etc.)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    parser.add_argument(
        "--refresh",
        type=float,
        default=0,
        help="Refresh data every N seconds (0 for no refresh)"
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="List available color themes"
    )
    parser.add_argument(
        "--list-ascii",
        action="store_true",
        help="List available ASCII art options"
    )
    parser.add_argument(
        "--demo-mode",
        action="store_true",
        help="Cycle through themes and ASCII art"
    )
    return parser.parse_args()


def display_system_info(args, console):
    """Display system information with the specified options"""
    # Add theme name to theme dict for reference
    theme_data = themes.THEMES[args.theme].copy()
    theme_data["name"] = args.theme
    
    ascii_logo = ascii_art.ASCII_OPTIONS[args.ascii]
    
    # Get system information
    start_time = time.time()
    try:
        logging.info(f"Gathering system info with performance={args.performance}")
        system_data = system_info.gather_system_info(args.performance)
    except Exception as e:
        logging.error(f"Error gathering system info: {e}")
        # Create a fallback with minimal information
        system_data = OrderedDict()
        try:
            system_data["Host"] = OrderedDict([("User", os.getlogin() if hasattr(os, 'getlogin') else "unknown")])
            system_data["OS"] = OrderedDict([("System", platform.system())])
        except Exception as inner_e:
            logging.error(f"Error creating fallback system info: {inner_e}")
            system_data["Error"] = OrderedDict([("Message", "Failed to gather system information")])
    
    end_time = time.time()
    
    # Create layout
    layout = Layout()
    layout.split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=2)
    )
    
    # Format ASCII art with theme colors
    formatted_ascii = formatters.format_ascii(ascii_logo, theme_data, not args.no_color)
    
    # Determine appropriate box style for this theme
    box_style = formatters.BOX_STYLES.get(args.theme, ROUNDED)
    
    # Add ASCII art to left panel with nice borders
    layout["left"].update(
        Panel(
            Align.center(formatted_ascii),
            border_style=theme_data["border"] if not args.no_color else "white",
            box=box_style,
            padding=(1, 2),
            title="vfetch" if args.ascii != "default" else None,
            title_align="center"
        )
    )
    
    # Create information table for right panel
    try:
        info_table = formatters.create_info_table(
            system_data, 
            theme_data, 
            not args.no_color, 
            args.compact
        )
        
        # Add processing time if performance metrics requested
        if args.performance:
            # Create a nice footer with processing time
            processing_time = f"Fetch time: {(end_time - start_time):.3f}s"
            if not args.no_color:
                processing_time = Text(processing_time)
                processing_time.stylize(theme_data["accent"])
            info_table.add_row("", "")
            info_table.add_row("Performance", processing_time)
        
        layout["right"].update(info_table)
    except Exception as e:
        logging.error(f"Error creating info table: {e}")
        console.print(f"[red]Error creating info table: {e}[/red]")
        # Fallback to simple text
        layout["right"].update(
            Panel(
                f"Error displaying system information:\n{str(e)}",
                border_style="red"
            )
        )
    
    # Clear screen and display layout
    console.clear()
    
    # Add a header with theme and ASCII info if not in compact mode
    if not args.compact:
        header = Text()
        header.append(f"Theme: ", style="dim")
        header.append(args.theme, style=theme_data["primary"] if not args.no_color else None)
        header.append(" • ", style="dim")
        header.append(f"ASCII: ", style="dim")
        header.append(args.ascii, style=theme_data["secondary"] if not args.no_color else None)
        console.print(header, justify="center")
    
    # Display main layout
    console.print(layout)
    
    # Add a footer with available commands if not in compact mode
    if not args.compact:
        footer = Text()
        footer.append("Press Ctrl+C to exit", style="dim")
        if args.refresh > 0:
            footer.append(" • ", style="dim")
            footer.append(f"Refreshing every {args.refresh}s", style="dim")
        console.print(footer, justify="center")


def display_theme_list(console):
    """Display a visually appealing list of available themes"""
    console.print("[bold]Available Themes:[/bold]", style="bright_white")
    
    # Create a table for theme display
    table = Table(
        show_header=False,
        box=DOUBLE_EDGE,
        expand=False,
        padding=(0, 2)
    )
    
    # Add columns with even spacing
    num_columns = 3
    for i in range(num_columns):
        table.add_column(f"col{i}")
    
    # Add rows with colored theme names
    theme_names = list(themes.THEMES.keys())
    rows = []
    row = []
    
    for i, theme_name in enumerate(theme_names):
        # Color the theme name using its primary color
        theme_text = Text(f"• {theme_name}")
        theme_text.stylize(themes.THEMES[theme_name]["primary"])
        
        row.append(theme_text)
        
        # Create a new row after filling the columns
        if (i + 1) % num_columns == 0 or i == len(theme_names) - 1:
            # Pad the row if it's not full
            while len(row) < num_columns:
                row.append("")
            
            rows.append(row)
            row = []
    
    # Add rows to the table
    for row in rows:
        table.add_row(*row)
    
    console.print(table)


def display_ascii_list(console):
    """Display a visually appealing list of available ASCII art options"""
    console.print("[bold]Available ASCII Art Options:[/bold]", style="bright_white")
    
    # We'll show examples of the ASCII art
    for art_name, art in ascii_art.ASCII_OPTIONS.items():
        # Preview panel for the ASCII art
        preview = Panel(
            art[:8].strip(),  # Show just the first few lines
            title=art_name,
            border_style="bright_cyan",
            box=ROUNDED,
            padding=(0, 1),
            title_align="center"
        )
        console.print(preview)
        console.print()


def demo_mode(args, console):
    """Cycle through various themes and ASCII art combinations"""
    original_theme = args.theme
    original_ascii = args.ascii
    
    try:
        console.print("[bold cyan]Starting Demo Mode - Press Ctrl+C to exit[/bold cyan]")
        time.sleep(1)
        
        # Use a selection of the best theme and ASCII combinations
        demo_themes = ["cyberpunk", "neon", "matrix", "forest", "replit", "ocean", "fire"]
        demo_ascii = ["dragon", "fox", "keycap", "cube", "tiger", "circuit", "pixel", "owl"]
        
        # If no themes or ASCII art are selected, choose some good ones for the demo
        if not demo_themes:
            demo_themes = list(themes.THEMES.keys())[:5]
        if not demo_ascii:
            demo_ascii = list(ascii_art.ASCII_OPTIONS.keys())[:5]
            
        for theme_name in demo_themes:
            for ascii_name in demo_ascii:
                args.theme = theme_name
                args.ascii = ascii_name
                
                # Display current theme and ASCII combination
                display_system_info(args, console)
                
                # Wait before showing the next one
                time.sleep(1.5)
    except KeyboardInterrupt:
        pass
    finally:
        # Restore original settings
        args.theme = original_theme
        args.ascii = original_ascii
        console.print("[bold cyan]Demo Mode Finished[/bold cyan]")


def display_minimal_info(args, console):
    """Display system information with minimal styling (blue text with ASCII boxes)"""
    # Get system information
    try:
        logging.info(f"Gathering system info with performance={args.performance}")
        system_data = system_info.gather_system_info(args.performance)
    except Exception as e:
        logging.error(f"Error gathering system info: {e}")
        # Create a fallback with minimal information
        system_data = OrderedDict()
        try:
            system_data["Host"] = OrderedDict([("User", os.getlogin() if hasattr(os, 'getlogin') else "unknown")])
            system_data["OS"] = OrderedDict([("System", platform.system())])
        except Exception as inner_e:
            logging.error(f"Error creating fallback system info: {inner_e}")
            system_data["Error"] = OrderedDict([("Message", "Failed to gather system information")])
    
    # Clear screen
    console.clear()
    
    # Create a title with box
    title_panel = Panel(
        "[bold blue]vfetch - System Information[/bold blue]",
        border_style="blue",
        box=ROUNDED,
        expand=False, 
        padding=(0, 2)
    )
    console.print(title_panel, justify="center")
    
    # Create a main content panel with two columns
    main_table = Table.grid(padding=1, expand=True)
    main_table.add_column(ratio=1)
    main_table.add_column(ratio=3)
    
    # Create a placeholder for where ASCII art would be
    ascii_placeholder = Panel(
        Align.center("[blue]ASCII art will appear here[/blue]\n[blue]when specified with -a/--ascii[/blue]"),
        title="vfetch",
        border_style="blue",
        box=ROUNDED,
        padding=(1, 2),
        title_align="center"
    )
    
    # Create a table for system information
    info_table = Table(
        show_header=False,
        box=ROUNDED,
        expand=True,
        border_style="blue"
    )
    info_table.add_column("Category", style="bold blue")
    info_table.add_column("Value", style="white")
    
    # Add system data to the table
    for section_name, section_data in system_data.items():
        info_table.add_row(f"[bold blue]{section_name}[/bold blue]", "")
        for key, value in section_data.items():
            # Check if the value has a visualization bar (for memory/disk)
            if isinstance(value, str) and '[' in value and ']' in value and ('■' in value or '□' in value):
                info_table.add_row(f"  [blue]{key}[/blue]", Text.from_markup(value))
            else:
                info_table.add_row(f"  [blue]{key}[/blue]", str(value))
        info_table.add_row("", "")  # Add spacing between sections
    
    # Add both panels to the main table
    main_table.add_row(ascii_placeholder, info_table)
    
    # Display the main content
    console.print(main_table)
    
    # Add a footer with help information in a box
    footer_panel = Panel(
        Text.from_markup(
            "[dim]Use -t/--theme and -a/--ascii options to enable visual styling\n"
            "Use --list-themes and --list-ascii to see available options\n"
            f"{'Refreshing every ' + str(args.refresh) + 's • ' if args.refresh > 0 else ''}Press Ctrl+C to exit[/dim]"
        ),
        border_style="blue",
        box=ROUNDED,
        expand=False,
        padding=(1, 1)
    )
    console.print(footer_panel, justify="center")

def main():
    args = parse_arguments()
    console = Console()
    
    try:
        # Handle special commands
        if args.list_themes:
            display_theme_list(console)
            return
            
        if args.list_ascii:
            display_ascii_list(console)
            return
        
        if args.demo_mode:
            demo_mode(args, console)
            return
        
        # Check if theme and ASCII art are provided
        if args.theme is None or args.ascii is None:
            # Display minimal information in blue if theme or ASCII art not provided
            if args.refresh > 0:
                try:
                    while True:
                        display_minimal_info(args, console)
                        time.sleep(args.refresh)
                except KeyboardInterrupt:
                    console.print("\n[bold]Exiting vfetch...[/bold]")
            else:
                display_minimal_info(args, console)
            return
            
        # Display system information with refresh if specified
        if args.refresh > 0:
            try:
                while True:
                    display_system_info(args, console)
                    time.sleep(args.refresh)
            except KeyboardInterrupt:
                console.print("\n[bold]Exiting vfetch...[/bold]")
        else:
            display_system_info(args, console)
    
    except Exception as e:
        logging.error(f"Unhandled exception in main: {e}")
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        raise


if __name__ == "__main__":
    main()