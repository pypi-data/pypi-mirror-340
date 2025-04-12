import random
import re
import os
import json
import datetime
from pathlib import Path
from art import text2art, ART_NAMES, FONT_NAMES, ASCII_FONTS
from art.params import SMALL_WIZARD_FONT, MEDIUM_WIZARD_FONT, LARGE_WIZARD_FONT, XLARGE_WIZARD_FONT
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.syntax import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress
from rich import box
from rich.markdown import Markdown

FONTSY = ["smslant","twin_cob","bolger","tarty4"]
SUBTITLE = ["fancy67","bold_script","fancy141","fancy112"]

# Import pyperclip for clipboard functionality
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

def main() -> None:
    console = Console()

    # If clipboard functionality isn't available, show installation instructions
    if not CLIPBOARD_AVAILABLE:
        console.print("[yellow]Clipboard functionality requires 'pyperclip' package.[/yellow]")
        console.print("[yellow]Install it with: pip install pyperclip[/yellow]")
        console.print("[yellow]Then restart the application to enable clipboard features.[/yellow]")

    # Using the art library's built-in font categories
    font_categories = {
        "standard": FONT_NAMES,  # All fonts
        "small": SMALL_WIZARD_FONT,
        "medium": MEDIUM_WIZARD_FONT,
        "large": LARGE_WIZARD_FONT,
        "xlarge": XLARGE_WIZARD_FONT,
        "ascii_only": ASCII_FONTS,  # Only fonts with ASCII characters
        "3d": [f for f in FONT_NAMES if "3d" in f.lower() or "3-d" in f.lower()],
        "block": [f for f in FONT_NAMES if "block" in f.lower()],
        "banner": [f for f in FONT_NAMES if "banner" in f.lower()],
        "bubble": [f for f in FONT_NAMES if "bubble" in f.lower()],
        "digital": [f for f in FONT_NAMES if "digital" in f.lower()],
        "script": [f for f in FONT_NAMES if "script" in f.lower()],
        "slant": [f for f in FONT_NAMES if "slant" in f.lower()],
        "shadow": [f for f in FONT_NAMES if "shadow" in f.lower()],
        "fancy": [f for f in FONT_NAMES if "fancy" in f.lower()],
        "graffiti": [f for f in FONT_NAMES if "graffiti" in f.lower()],
    }

    # Available font styles
    available_styles = list(font_categories.keys())

    # Colors for the fonts - using a wider range of colors
    colors = [
        "bright_red", "bright_green", "bright_blue", "bright_magenta", 
        "bright_cyan", "bright_yellow", "orange3", "purple", "gold1", 
        "turquoise2", "deep_pink3", "spring_green1", "dodger_blue1", 
        "light_sea_green", "dark_orange3", "yellow3", "magenta", "cyan"
    ]

    # File to save favorites
    favorites_file = os.path.join(os.path.expanduser("~"), ".ascii_art_favorites.json")

    # Create exports directory if it doesn't exist
    exports_dir = Path(os.path.expanduser("~")) / "ascii_art_exports"
    exports_dir.mkdir(exist_ok=True)

    # Load favorites from file if it exists
    favorite_fonts = set()

    # Function to save favorites to disk
    def save_favorites():
        try:
            with open(favorites_file, 'w') as f:
                json.dump(list(favorite_fonts), f)
            return True
        except Exception as e:
            console.print(f"[yellow]Error saving favorites: {e}[/yellow]")
            return False

    # Function to export the current display to various formats
    def export_display(format_type, fonts_to_export, display_text):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"ascii_art_{display_text[:20].replace(' ', '_')}_{timestamp}"

        if format_type == "text":
            filename = exports_dir / f"{filename_base}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Fontsy ASCII Art Export for '{display_text}'\n")
                f.write(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                for i, font in enumerate(fonts_to_export):
                    try:
                        art = text2art(display_text, font=font)
                        f.write(f"Font {i+1}: {font}\n")
                        f.write(f"{art}\n")
                        f.write("-" * 80 + "\n\n")
                    except Exception:
                        f.write(f"Font {i+1}: {font} - Rendering failed\n\n")

            console.print(f"[green]Exported to text file: [bold]{filename}[/bold][/green]")
            return filename

        elif format_type == "html":
            filename = exports_dir / f"{filename_base}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fontsy ASCII Art Export for '{display_text}'</title>
    <style>
        body {{ font-family: monospace; background-color: #1e1e1e; color: #f0f0f0; padding: 20px; }}
        h1, h2 {{ color: #3aa8c1; }}
        .font-container {{ margin-bottom: 30px; border: 1px solid #444; padding: 15px; border-radius: 5px; }}
        .font-name {{ color: #e9950c; font-weight: bold; margin-bottom: 5px; display: flex; justify-content: space-between; align-items: center; }}
        .ascii-art {{ white-space: pre; background-color: #252525; padding: 15px; border-radius: 3px; }}
        .favorite {{ color: #ff9900; }}
        .copy-btn {{ background-color: #2d5e6c; color: white; border: none; border-radius: 3px; padding: 3px 10px; 
                   cursor: pointer; font-family: sans-serif; font-size: 12px; }}
        .copy-btn:hover {{ background-color: #3aa8c1; }}
        footer {{ margin-top: 50px; color: #888; text-align: center; font-size: 0.8em; }}
        .copy-feedback {{ position: fixed; top: 20px; right: 20px; background-color: #3aa8c1; color: white; 
                        padding: 10px 20px; border-radius: 4px; display: none; transition: opacity 0.5s; }}
    </style>
</head>
<body>
    <h1>Fontsy ASCII Art Export for '{display_text}'</h1>
    <p>Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <div id="copyFeedback" class="copy-feedback">Copied to clipboard!</div>
    
    <script>
        function copyToClipboard(text) {{
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            
            // Show feedback
            const feedback = document.getElementById('copyFeedback');
            feedback.style.display = 'block';
            setTimeout(() => {{
                feedback.style.opacity = '0';
                setTimeout(() => {{
                    feedback.style.display = 'none';
                    feedback.style.opacity = '1';
                }}, 500);
            }}, 1500);
        }}
    </script>
""")

                for i, font in enumerate(fonts_to_export):
                    try:
                        art = text2art(display_text, font=font)
                        star = "★ " if font in favorite_fonts else ""
                        favorite_class = " favorite" if font in favorite_fonts else ""

                        f.write(f"""    <div class="font-container">
        <div class="font-name{favorite_class}">
            <span>{i+1}. {star}{font}</span>
            <button class="copy-btn" onclick="copyToClipboard(`{art.replace('`', '\\`')}`)">Copy to Clipboard</button>
        </div>
        <pre class="ascii-art">{art}</pre>
    </div>
""")
                    except Exception:
                        f.write(f"""    <div class="font-container">
        <div class="font-name">{i+1}. {font}</div>
        <div class="ascii-art">Rendering failed</div>
    </div>
""")

                f.write(f"""    <footer>
        Created with FontsyASCII Art Font Explorer 
    </footer>
</body>
</html>""")

            console.print(f"[green]Exported to HTML file: [bold]{filename}[/bold][/green]")
            return filename

        elif format_type == "md":
            filename = exports_dir / f"{filename_base}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Fontsy ASCII Art Export for '{display_text}'\n\n")
                f.write(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                for i, font in enumerate(fonts_to_export):
                    try:
                        art = text2art(display_text, font=font)
                        star = "★ " if font in favorite_fonts else ""
                        f.write(f"## {i+1}. {star}{font}\n\n")
                        f.write("```\n")
                        f.write(f"{art}\n")
                        f.write("```\n\n")
                        f.write("---\n\n")
                    except Exception:
                        f.write(f"## {i+1}. {font}\n\n")
                        f.write("Rendering failed\n\n")
                        f.write("---\n\n")

                f.write(f"\n\n*Created with Fontsy ASCII Art Font Explorer *")

            console.print(f"[green]Exported to Markdown file: [bold]{filename}[/bold][/green]")
            return filename

        else:
            console.print(f"[yellow]Unknown export format: {format_type}[/yellow]")
            return None

    # Function to display the title screen
    def show_title_screen():
        # Clear the console
        console.clear()
        
        # Generate random fonts for title elements
        title_font = random.choice(FONTSY)
        subtitle_font = random.choice(SUBTITLE)
        welcome_font = random.choice(SUBTITLE)
        
        # Create ASCII art text
        title_art = text2art("Fontsy", font=title_font)
        subtitle_art = text2art("ASCII Art Font Explorer v0.1.7", font=subtitle_font)
        welcome_art = text2art("Welcome to Fontsy! Find your perfect style!", font=welcome_font)

        # Create styled rich text objects
        title_text = Text(title_art, style="bold green")
        subtitle_text = Text(subtitle_art, style="cyan")
        welcome_text = Text(welcome_art, style="bold yellow")
        
        # Display font info at the bottom
        font_info = f"[dim]Title Font: [bold cyan]{title_font}[/bold cyan] | Subtitle Font: [bold magenta]{subtitle_font}[/bold magenta][/dim]"
        
        # Combine all elements
        welcome_content = title_text + Text("\n") + subtitle_text
        
        welcome_panel = Panel(
            welcome_content,
            border_style="bright_blue", 
            title="[yellow]✨ Welcome ✨[/yellow]",
            title_align="center",
        )
        console.print(welcome_panel)
        console.print(font_info)
        
        console.line()
        
        console.print(welcome_text)
        
        # Simple instructions instead of full help
        console.print("\n[bold cyan]Enter text to see it in different ASCII art fonts[/bold cyan]")
        console.print("[dim]Type [bold]help[/bold] for a list of all commands[/dim]")
        console.print("[dim]Type [bold]quit[/bold] to exit[/dim]\n")

    # Display the title screen when starting the app
    show_title_screen()
    
    if os.path.exists(favorites_file):
        try:
            with open(favorites_file, 'r') as f:
                favorite_fonts = set(json.load(f))
            console.print(f"[green]Loaded {len(favorite_fonts)} favorites from disk.[/green]")
        except Exception as e:
            console.print(f"[yellow]Error loading favorites: {e}[/yellow]")
    

    # Prepare help text but don't display it initially
    help_text = "\n".join([
        "[bold white]Available commands:[/bold white]",
        "- Type your [bold]text[/bold] and press Enter to see it in different fonts",
        "- Press [bold]Enter[/bold] with empty input to see new fonts for the same text",
        "- Type a [bold]font category[/bold] to filter fonts:",
        f"  {', '.join(sorted(available_styles))}",
        "- Type [bold]grid[/bold] to show fonts in a grid layout (easier comparison)",
        "- Type [bold]list[/bold] to show fonts in list layout (more detail)",
        "- Type [bold]showcase[/bold] to see your text in ALL fonts (in a scrollable view)",
        "  • [bold]showcase [category][/bold] (e.g. 'showcase small')",
        "  • [bold]showcase [number][/bold] (e.g. 'showcase 20' for 20 random fonts)",
        "  • [bold]showcase [range][/bold] (e.g. 'showcase 10-30' for fonts 10 to 30)",
        "- Type a [bold]number[/bold] (e.g. '3') to favorite the font with that number",
        "- Type [bold]clipboard [number][/bold] (e.g. 'clipboard 5') to copy a font to clipboard",
        "- Type [bold]favorite [font_name][/bold] to mark a specific font as favorite",
        "- Type [bold]favorites[/bold] to see only your favorite fonts",
        "- Type [bold]clear[/bold] to clear all your favorites",
        "- Type [bold]title[/bold] to show the welcome screen again",
        "- Type [bold]input [number][/bold] (e.g. 'input 3') to enter real-time typing mode with the font at position 3 in current view",
        "  • Type [bold]exit[/bold] or press Ctrl+C while in typing mode to return to main menu",
        "- Export commands:",
        "  • [bold]export html[/bold] - Export last view as HTML",
        "  • [bold]export text[/bold] - Export last view as plain text",
        "  • [bold]export md[/bold] - Export last view as Markdown",
        "- Type [bold]help[/bold] to show this help message",
        "- Type [bold]quit[/bold] to exit"
    ])

    last_input = ""
    used_fonts = set()
    current_category = "standard"
    display_mode = "list"  # Default display mode
    current_fonts = []  # Keep track of currently displayed fonts
    showcase_fonts = []  # Keep track of fonts displayed in showcase mode

    # Function to toggle favorite status
    def toggle_favorite(font_name):
        if font_name in favorite_fonts:
            favorite_fonts.remove(font_name)
            console.print(f"[yellow]Removed [bold]{font_name}[/bold] from favorites[/yellow]")
        else:
            favorite_fonts.add(font_name)
            console.print(f"[green]Added [bold]{font_name}[/bold] to favorites![/green]")
        save_favorites()

    # Function to handle the showcase command with various options
    def handle_showcase(command):
        if not last_input:
            console.print("[yellow]Please enter some text first.[/yellow]")
            return

        # Default is to show all fonts
        fonts_to_show = sorted(FONT_NAMES)
        title_prefix = "ALL"

        # Check for category option (e.g., "showcase small")
        if len(command) > 1 and command[1] in available_styles:
            category = command[1]
            if category == "favorites":
                if not favorite_fonts:
                    console.print("[yellow]You don't have any favorite fonts yet.[/yellow]")
                    return
                fonts_to_show = sorted(favorite_fonts)
                title_prefix = "FAVORITE"
            else:
                fonts_to_show = sorted(font_categories[category])
                title_prefix = category.upper()

        # Check for random sample option (e.g., "showcase 20")
        elif len(command) > 1 and command[1].isdigit():
            sample_size = min(int(command[1]), len(FONT_NAMES))
            fonts_to_show = random.sample(FONT_NAMES, sample_size)
            title_prefix = f"{sample_size} RANDOM"

        # Check for range option (e.g., "showcase 10-30")
        elif len(command) > 1 and re.match(r'^\d+-\d+$', command[1]):
            try:
                start, end = map(int, command[1].split('-'))
                if start < 1:
                    start = 1
                if end > len(FONT_NAMES):
                    end = len(FONT_NAMES)
                if start > end:
                    start, end = end, start

                # Get fonts in the specified range (from sorted list)
                all_fonts_sorted = sorted(FONT_NAMES)
                fonts_to_show = all_fonts_sorted[start-1:end]
                title_prefix = f"RANGE {start}-{end}"
            except ValueError:
                console.print("[yellow]Invalid range format. Use 'showcase 10-30' format.[/yellow]")
                return

        console.print(f"[bold green]Generating showcase of {title_prefix} fonts for '[bold white]{last_input}[/bold white]'...[/bold green]")
        console.print("[yellow]This might take a moment. Press Ctrl+C to cancel.[/yellow]")

        # Store the showcase fonts for favoriting by number
        nonlocal showcase_fonts
        showcase_fonts = fonts_to_show.copy()

        # Create a colorful table with the selected fonts
        table = Table(
            title=f"[bold]{title_prefix} Font Showcase[/bold] for '{last_input}'", 
            box=box.ROUNDED, 
            header_style="bold magenta",
            title_style="bold cyan",
            border_style="bright_blue"
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Font Name", style="cyan")
        table.add_column("Preview")

        # Add progress bar for large operations
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Rendering {len(fonts_to_show)} fonts...", total=len(fonts_to_show))

            for i, font in enumerate(fonts_to_show):
                try:
                    art = text2art(last_input, font=font)
                    is_favorite = "★ " if font in favorite_fonts else ""

                    # Assign a color to the font preview randomly
                    color = random.choice(colors)
                    colored_art = f"[{color}]{art}[/{color}]"

                    table.add_row(str(i+1), f"{is_favorite}{font}", colored_art)
                except Exception:
                    table.add_row(str(i+1), font, "[red](Font rendering failed)[/red]")
                progress.update(task, advance=1)

        console.print(table)
        console.print("[dim]Type a number to favorite/unfavorite a font from this showcase.[/dim]")
        console.print("[dim]Type 'export html', 'export text', or 'export md' to save this view.[/dim]")

    # Function to copy a font to clipboard
    def copy_font_to_clipboard(font_number, fonts_list):
        if not CLIPBOARD_AVAILABLE:
            console.print("[yellow]Clipboard functionality requires 'pyperclip' package.[/yellow]")
            console.print("[yellow]Install it with: pip install pyperclip[/yellow]")
            return False

        if 1 <= font_number <= len(fonts_list):
            font_name = fonts_list[font_number - 1]
            try:
                art = text2art(last_input, font=font_name)
                pyperclip.copy(art)
                console.print(f"[green]Copied font [bold]{font_name}[/bold] to clipboard![/green]")
                return True
            except Exception as e:
                console.print(f"[yellow]Error copying font: {e}[/yellow]")
                return False
        else:
            console.print(f"[yellow]No font with number {font_number} in current view.[/yellow]")
            return False

    while True:
        user_input = Prompt.ask("\n[bold cyan]Enter text or command[/bold cyan]")

        if user_input.lower() == 'quit':
            # Save favorites before exiting
            if save_favorites():
                console.print(f"[green]Saved {len(favorite_fonts)} favorites to disk.[/green]")
            console.print("[bold green]Thanks for using ASCII Art Font Explorer! Come back soon![/bold green]")
            break

        if user_input.lower() == 'help':
            console.print(Panel(help_text, title="[bold]Commands & Tips[/bold]", border_style="green"))
            
            # Information about increasing terminal buffer
            terminal_help = "\n".join([
                "[bold white]Tip: Increase your terminal scrollback buffer[/bold white]",
                "[dim]If you want to see more output history, you can increase your terminal's scrollback buffer:[/dim]",
                "",
                "[bold yellow]VSCode:[/bold yellow]",
                "  Settings > search for 'terminal  scrollback' (e.g., 10000 lines)",
                "",
                "",
                "[dim]This allows you to scroll back and see more fonts when using showcase mode.[/dim]"
            ])
            console.print(Panel(terminal_help, title="[bold]Terminal Scrollback Help[/bold]", border_style="blue"))
            continue
            
        if user_input.lower() == 'title':
            show_title_screen()
            continue

        if user_input.lower() == 'grid':
            display_mode = 'grid'
            console.print("[yellow]Switched to grid display mode[/yellow]")
            continue
        
        if user_input.lower() == 'list':
            display_mode = 'list'
            console.print("[yellow]Switched to list display mode[/yellow]")
            continue

        # Handle clipboard command
        if user_input.lower().startswith('clipboard '):
            try:
                font_number = int(user_input.split()[1])
                # Determine which fonts list to use
                if showcase_fonts:
                    copy_font_to_clipboard(font_number, showcase_fonts)
                elif current_fonts:
                    copy_font_to_clipboard(font_number, current_fonts)
                else:
                    console.print("[yellow]No fonts to copy. Please display some fonts first.[/yellow]")
            except (IndexError, ValueError):
                console.print("[yellow]Please specify a valid font number: 'clipboard 5'[/yellow]")
            continue

        if user_input.lower() == 'favorites':
            if not favorite_fonts:
                console.print("[yellow]You haven't marked any fonts as favorites yet.[/yellow]")
                continue

            current_category = "favorites"
            used_fonts = set()
            console.print(f"[bold yellow]Showing your favorite fonts[/bold yellow]")
            if last_input:
                console.print(f"[dim]Using previous text: '{last_input}'[/dim]")
                user_input = last_input
            else:
                console.print("[dim]Please enter some text to convert.[/dim]")
                continue

        if user_input.lower() == 'clear':
            favorite_fonts.clear()
            save_favorites()
            console.print("[yellow]All favorites cleared and saved to disk.[/yellow]")
            continue

        # Handle export commands
        if user_input.lower().startswith('export '):
            export_format = user_input.lower().split()[1] if len(user_input.lower().split()) > 1 else None

            if not export_format:
                console.print("[yellow]Please specify an export format: html, text, or md[/yellow]")
                continue

            if not last_input:
                console.print("[yellow]Please display some fonts first before exporting.[/yellow]")
                continue

            # Determine which fonts to export
            if showcase_fonts:
                fonts_to_export = showcase_fonts
            elif current_fonts:
                fonts_to_export = current_fonts
            else:
                console.print("[yellow]No fonts to export. Please display some fonts first.[/yellow]")
                continue

            if export_format in ['html', 'text', 'md', 'markdown']:
                if export_format == 'markdown':
                    export_format = 'md'
                export_display(export_format, fonts_to_export, last_input)
            else:
                console.print(f"[yellow]Unknown export format: {export_format}. Please use html, text, or md.[/yellow]")
            continue

        # Handle showcase commands with options
        if user_input.lower().startswith('showcase'):
            command_parts = user_input.lower().split()
            handle_showcase(command_parts)
            continue
        
        # Handle input command
        if user_input.lower().startswith('input '):
            try:
                font_number = int(user_input.split()[1])
                
                # Determine which font list to use (current view, showcase, or favorites)
                if showcase_fonts and 1 <= font_number <= len(showcase_fonts):
                    font_name = showcase_fonts[font_number - 1]
                elif current_fonts and 1 <= font_number <= len(current_fonts):
                    font_name = current_fonts[font_number - 1]
                else:
                    console.print(f"[yellow]No font with number {font_number} in current view.[/yellow]")
                    continue
                
                # Import required packages for character-by-character input
                try:
                    import sys
                    import termios
                    import tty
                    import select
                    char_by_char_available = True
                except ImportError:
                    char_by_char_available = False
                
                # Clear screen
                console.clear()
                console.print(f"[bold green]Interactive typing mode with font: [bold white]{font_name}[/bold white][/bold green]")
                console.print("[yellow]Type anything and see it rendered instantly in real-time.[/yellow]")
                console.print("[yellow]Type 'exit' or press Ctrl+C to return to main menu.[/yellow]")
                
                if char_by_char_available:
                    # Save terminal settings
                    old_settings = termios.tcgetattr(sys.stdin)
                    
                    try:
                        # Change terminal settings for character-by-character input
                        tty.setcbreak(sys.stdin.fileno())
                        
                        current_text = ""
                        backspace_char = chr(127)  # ASCII for backspace
                        
                        # Interactive typing loop - character by character
                        while True:
                            # Check if there's input available
                            if select.select([sys.stdin], [], [], 0)[0]:
                                char = sys.stdin.read(1)
                                
                                # Check for Ctrl+C (ASCII 3) to exit
                                if ord(char) == 3:
                                    raise KeyboardInterrupt
                                
                                # Handle backspace
                                if char == backspace_char and current_text:
                                    current_text = current_text[:-1]
                                # Only add printable characters
                                elif char.isprintable():
                                    current_text += char
                                
                                # Clear screen and redraw
                                console.clear()
                                console.print(f"[bold green]Interactive typing mode with font: [bold white]{font_name}[/bold white][/bold green]")
                                console.print("[yellow]Type anything and see it rendered instantly in real-time.[/yellow]")
                                console.print("[yellow]Type 'exit' or press Ctrl+C to return to main menu.[/yellow]")
                                console.print(f"[dim]Current text: {current_text}[/dim]")
                                
                                # Check if user typed "exit" to quit
                                if current_text.lower() == "exit":
                                    break
                                
                                if current_text:
                                    try:
                                        art = text2art(current_text, font=font_name)
                                        color = random.choice(colors)
                                        console.print(f"[{color}]{art}[/{color}]")
                                    except Exception as e:
                                        console.print(f"[red]Error rendering text: {e}[/red]")
                    finally:
                        # Restore terminal settings before returning
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                else:
                    # Fallback method if character-by-character input isn't available
                    try:
                        current_text = ""
                        while True:
                            typed_text = Prompt.ask("\n[dim]Type something (or 'exit' to quit)[/dim]")
                            
                            # Check if user wants to exit
                            if typed_text.lower() == "exit":
                                break
                                
                            current_text = typed_text
                            console.clear()
                            console.print(f"[bold green]Interactive typing mode with font: [bold white]{font_name}[/bold white][/bold green]")
                            console.print("[yellow]Type anything and see it rendered (type 'exit' or press Ctrl+C to quit).[/yellow]")
                            
                            try:
                                art = text2art(current_text, font=font_name)
                                color = random.choice(colors)
                                console.print(f"[{color}]{art}[/{color}]")
                            except Exception as e:
                                console.print(f"[red]Error rendering text: {e}[/red]")
                    except KeyboardInterrupt:
                        pass
                
                # Exit handling
                console.clear()
                console.print("[yellow]Exited interactive typing mode.[/yellow]")
                show_title_screen()
                
                continue
            except (IndexError, ValueError):
                console.print("[yellow]Please specify a valid font number: 'input 5'[/yellow]")
                continue

        # Check if user is trying to favorite a font by number
        if user_input.isdigit():
            font_number = int(user_input)

            # Check if we're in showcase mode and use showcase_fonts
            if showcase_fonts and 1 <= font_number <= len(showcase_fonts):
                font_name = showcase_fonts[font_number - 1]
                toggle_favorite(font_name)
            # Otherwise use the current view fonts
            elif current_fonts and 1 <= font_number <= len(current_fonts):
                font_name = current_fonts[font_number - 1]
                toggle_favorite(font_name)
            else:
                console.print(f"[yellow]No font with number {font_number} in current view.[/yellow]")
            continue

        if user_input.lower().startswith('favorite '):
            font_name = user_input[9:].strip()
            if font_name in FONT_NAMES:
                toggle_favorite(font_name)
            else:
                console.print(f"[yellow]Font [bold]{font_name}[/bold] not found. Please check the name.[/yellow]")
            continue

        # Check if user wants to switch font category
        if user_input.lower() in available_styles:
            current_category = user_input.lower()
            used_fonts = set()  # Reset used fonts when changing category
            console.print(f"[bold yellow]Switched to {current_category.upper()} fonts[/bold yellow]")
            # Reset showcase mode
            showcase_fonts = []
            if last_input:
                console.print(f"[dim]Using previous text: '{last_input}'[/dim]")
                user_input = last_input
            else:
                console.print("[dim]Please enter some text to convert.[/dim]")
                continue

        # If user just pressed Enter, use the last input
        if not user_input.strip() and last_input:
            user_input = last_input
            console.print(f"[dim]Using previous text: '{user_input}'[/dim]")
            # Reset showcase mode when showing new fonts
            showcase_fonts = []
        elif not user_input.strip():
            console.print("[yellow]Please enter some text to convert.[/yellow]")
            continue
        else:
            # Save the new input if it's not a command
            last_input = user_input
            # Reset showcase mode when entering new text
            showcase_fonts = []
            if current_category != "standard":
                # Keep the current category when entering new text
                pass
            else:
                used_fonts = set()

        # Determine which fonts to use based on current category
        if current_category == "favorites":
            available_fonts = [f for f in favorite_fonts if f not in used_fonts]
        else:
            available_fonts = [f for f in font_categories[current_category] if f not in used_fonts]

        # If we've shown all fonts or not enough left, reset the used fonts
        if len(available_fonts) < 10:
            if current_category == "favorites":
                console.print(f"[yellow]You've seen all your favorite fonts. Starting over.[/yellow]")
                used_fonts = set()
                available_fonts = list(favorite_fonts)
            else:
                console.print(f"[yellow]You've seen most of the available {current_category.upper()} fonts. Starting over.[/yellow]")
                used_fonts = set()
                available_fonts = font_categories[current_category]

        # Select 10 random fonts or less if not enough available
        num_fonts = min(10, len(available_fonts))
        selected_fonts = random.sample(available_fonts, num_fonts)

        # Store currently displayed fonts for favoriting by number
        current_fonts = selected_fonts.copy()

        # Add selected fonts to used fonts
        used_fonts.update(selected_fonts)

        category_count = len(favorite_fonts) if current_category == "favorites" else len(font_categories[current_category])
        title = f"[bold]'{user_input}'[/bold] in {num_fonts} {current_category.upper()} fonts ({len(used_fonts)}/{category_count} shown)"
        console.print(Panel(title, border_style="blue"))

        # Create font previews based on display mode
        if display_mode == 'grid':
            # Grid display - more compact with multiple columns
            grid_items = []

            for i, font in enumerate(selected_fonts):
                try:
                    art = text2art(user_input, font=font)
                    # Select a random color for each font
                    color = random.choice(colors)
                    is_favorite = "★ " if font in favorite_fonts else ""
                    panel = Panel(
                        Text(art, style=color),
                        title=f"[bold white]{i+1}. {is_favorite}{font}[/bold white]",
                        subtitle="Type number to favorite/unfavorite",
                        border_style=color,
                        expand=False
                    )
                    grid_items.append(panel)
                except Exception as e:
                    grid_items.append(Panel(f"Error: {e}", title=f"{i+1}. {font}", border_style="red"))

            # Display in columns (adjust the number based on terminal width)
            columns = Columns(grid_items, equal=True, expand=True)
            console.print(columns)

        else:
            # List display - more detailed with each font on its own
            for i, font in enumerate(selected_fonts):
                try:
                    art = text2art(user_input, font=font)
                    # Select a random color for each font
                    color = random.choice(colors)
                    banner_text = Text(art, style=f"bold {color}")

                    # Show a star for favorite fonts
                    is_favorite = "★ " if font in favorite_fonts else ""
                    fav_status = "unfavorite" if font in favorite_fonts else "favorite"

                    # Create panel with the font name and art
                    panel = Panel(
                        banner_text,
                        title=f"[bold white]{i+1}. {is_favorite}{font}[/bold white]",
                        subtitle=f"Type {i+1} to {fav_status}",
                        border_style=color
                    )
                    console.print(panel)
                except Exception as e:
                    console.print(Panel(f"Error: {e}", title=f"{i+1}. Font: {font}", border_style="red"))

        favorite_status = f" | Favorites: {len(favorite_fonts)}" if favorite_fonts else ""
        console.print("\n[dim]Press Enter to see more fonts, or type new text, or 'quit' to exit.[/dim]")
        console.print("[dim]Type 'export html', 'export text', or 'export md' to save this view.[/dim]")
        console.print(f"[dim]Mode: {display_mode.upper()} | Category: {current_category.upper()}{favorite_status}[/dim]")

        

if __name__ == "__main__":
    main()
