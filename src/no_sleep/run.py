import tkinter as tk
from sys import argv

from no_sleep.gui import ICON_FILE, NoSleepGui


def run(sys_tray: bool = False, start_min: bool = False) -> None:
    """
    Run the app.

    :param sys_tray:
    :param start_min:
    """
    root = tk.Tk()
    width, height = 220, 75
    root.geometry(f'{width}x{height}')
    root.minsize(width=width, height=height)
    root.iconbitmap(ICON_FILE)
    root.title('NoSleep')
    NoSleepGui(master=root, sys_tray=sys_tray)
    if start_min:
        root.withdraw()
    root.mainloop()


if __name__ == '__main__':
    tray = False
    start_as_min = False
    if 'tray' in argv:
        tray = True
    if 'min' in argv:
        start_as_min = True
    run(sys_tray=tray, start_min=start_as_min)
