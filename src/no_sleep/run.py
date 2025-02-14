import tkinter as tk
from argparse import ArgumentParser

from no_sleep.gui import ICON_FILE, NoSleepGui, __version__


def run() -> None:
    """Run the app."""
    parser = ArgumentParser(description='no more sleep')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s version: ' + __version__)
    parser.add_argument('-t', '--tray', action='store_true', dest='tray', help='show tray icon')
    parser.add_argument('-m', '--minimized', action='store_true', dest='minimized', help='start minimized')
    args = parser.parse_args()

    root = tk.Tk()
    width, height = 220, 75
    root.geometry(f'{width}x{height}')
    root.minsize(width=width, height=height)
    root.iconbitmap(ICON_FILE)
    root.title('NoSleep')
    NoSleepGui(master=root, cli_args=args)
    if args.minimized:
        root.withdraw()
    root.mainloop()


if __name__ == '__main__':
    run()
