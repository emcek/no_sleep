import tkinter as tk
from ctypes import windll
from datetime import datetime, timedelta
from os import kill, getpid
from pathlib import Path
from signal import SIGINT
from sys import argv
from threading import Timer

from PIL import Image
from pystray import MenuItem, Icon

# Informs the system that the state being set should remain in effect until the next call that uses ES_CONTINUOUS
# and one of the other state flags is cleared.
ES_CONTINUOUS = 0x80000000
# Forces the display to be on by resetting the display idle timer.
ES_SYSTEM_REQUIRED = 0x00000001
# Forces the system to be in the working state by resetting the system idle timer.
ES_DISPLAY_REQUIRED = 0x00000002
ICON_FILE = Path(__file__).resolve().with_name('no_sleep.ico')
__version__ = '1.0.2'


class NoSleepGui(tk.Frame):

    def __init__(self, master: tk.Tk, sys_tray: bool = False) -> None:
        super().__init__(master)
        self.master: tk.Tk = master
        self.sys_tray = sys_tray
        self.status_txt = tk.StringVar()
        self.shutdown_time = tk.IntVar()

        self.shutdown_time.set(60)
        self.status_txt.set(f'ver: {__version__}')

        l_shutdown = tk.Label(master=self.master, text='Minutes:')
        l_shutdown.grid(row=0, column=0, sticky=tk.W + tk.E, padx=7)
        entry_shutdown = tk.Entry(master=self.master, textvariable=self.shutdown_time, width=7)
        entry_shutdown.grid(row=0, column=1, sticky=tk.W, padx=7)
        btn_shutdown = tk.Button(self.master, text='Set Shutdown', command=self.set_shutdown)
        btn_shutdown.grid(row=0, column=3, sticky=tk.W + tk.E, padx=7)

        btn_stay_on = tk.Button(self.master, text='Stay On', command=self.stay_on)
        btn_stay_on.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E, padx=7)
        btn_quit = tk.Button(self.master, text='Quit', command=self.exit)
        btn_quit.grid(row=1, column=2, columnspan=2, sticky=tk.W + tk.E, padx=7)

        status = tk.Label(master=self.master, textvariable=self.status_txt)
        status.grid(row=2, column=0, columnspan=4, sticky=tk.SE, padx=7)

        if self.sys_tray:
            self.sys_tray_icon = self._setup_system_tray()
            self.sys_tray_icon.run_detached()
            self.sys_tray_icon.notify('Running in background.', 'NoSleep')

    def _setup_system_tray(self) -> Icon:
        icon = Image.open(ICON_FILE)
        menu = (MenuItem('Show', self._show_gui), MenuItem('Quit', self.exit))
        self.master.protocol('WM_DELETE_WINDOW', self._withdraw_gui)
        return Icon('no_sleep', icon, 'NoSleep', menu)

    def _withdraw_gui(self) -> None:
        if self.sys_tray:
            self.sys_tray_icon.notify('Still running at system tray.', 'NoSleep')
        self.master.withdraw()

    def _show_gui(self) -> None:
        self.master.after(0, self.master.deiconify)

    def stay_on(self):
        self.status_txt.set('Will stay on')
        windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)

    def exit(self):
        self.status_txt.set(f'Quitting')
        if self.sys_tray:
            self.sys_tray_icon.visible = False
        windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        kill(getpid(), SIGINT)

    def set_shutdown(self):
        timer = self.shutdown_time.get() * 60
        shut_time = datetime.now() + timedelta(seconds=timer)
        self.status_txt.set(f'Stay on until: {shut_time.strftime("%H:%M")}')
        timer_th = Timer(timer, self.exit)
        timer_th.name = 'timer_thread'
        timer_th.start()


def run(sys_tray: bool = False, start_min: bool = False):
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
