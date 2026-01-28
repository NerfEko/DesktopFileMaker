"""Main entry point for desktop-file-maker TUI application."""

from src.tui.app import DesktopFileMakerApp


def main():
    """Run the desktop file maker application."""
    app = DesktopFileMakerApp()
    app.run()


if __name__ == "__main__":
    main()
