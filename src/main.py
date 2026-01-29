"""Main entry point for desktop-file-maker TUI application."""

import sys
import os
from src.tui.app import DesktopFileMakerApp


def is_running_in_terminal():
    """Check if the application is running in a proper terminal."""
    # Check if stdout is connected to a terminal
    if not sys.stdout.isatty():
        return False
    
    # Check if we have TERM environment variable (indicates terminal)
    if not os.environ.get('TERM'):
        return False
        
    return True


def show_terminal_required_popup():
    """Show a popup dialog explaining how to run the application properly."""
    
    message = """Desktop File Maker is a Terminal Application

This application must be run from a command line terminal.

How to run properly:

1. Open a terminal (Ctrl+Alt+T)
2. Navigate to this file's location  
3. Run: ./DesktopFileMaker-0.1.2-x86_64.AppImage

Or drag this file into an open terminal window.

The application provides a text-based interface within your terminal."""
    
    import subprocess
    import shutil
    
    # Use zenity (GTK) - best native appearance
    if shutil.which('zenity'):
        try:
            subprocess.run([
                'zenity', '--info',
                '--title=Terminal Required',
                '--text=' + message,
                '--width=450',
                '--height=250',
                '--icon-name=dialog-information'
            ], check=True)
            return
        except subprocess.CalledProcessError:
            pass
    
    # Fallback options if zenity isn't available
    # Try kdialog (KDE)
    if shutil.which('kdialog'):
        try:
            subprocess.run([
                'kdialog', '--msgbox', message,
                '--title', 'Terminal Required'
            ], check=True)
            return
        except subprocess.CalledProcessError:
            pass
    
    # Try xmessage (basic but always available)
    if shutil.which('xmessage'):
        try:
            subprocess.run([
                'xmessage', '-center',
                '-title', 'Terminal Required',
                message
            ], check=True)
            return
        except subprocess.CalledProcessError:
            pass
    
    # Final fallback - print to stderr
    print("ERROR: This is a terminal application!", file=sys.stderr)
    print("Please run from a terminal: ./DesktopFileMaker-0.1.0-x86_64.AppImage", file=sys.stderr)


def main():
    """Run the desktop file maker application."""
    if not is_running_in_terminal():
        show_terminal_required_popup()
        sys.exit(1)
    
    app = DesktopFileMakerApp()
    app.run()


if __name__ == "__main__":
    main()
