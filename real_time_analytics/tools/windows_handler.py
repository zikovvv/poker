import win32gui
import win32con
from pywinauto import Desktop
import itertools
import os
import time 
from pprint import pprint
import numpy as np
import win32gui
import win32con
import winxpgui

def find_all_hwnds_by_substr(substr) :
    return [win32gui.FindWindow(None, str(www).split("uiawrapper.UIAWrapper - '")[1].split("', %s" % str(www).split("', ")[-1])[0]) for www in Desktop(backend = "uia").windows() if substr in str(www)]

def move_all_holdem_windows(GAME_WINDOW_WIDTH) :
    for hwnd in HOLDEM_WINDOWS_HWNDS : 
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, GAME_WINDOW_WIDTH, GAME_WINDOW_WIDTH, 0) 
        win32gui.SetForegroundWindow(hwnd)

def pg_window_handler(WINDOW_CAPTION, width_pokerstars, height_pokerstars, PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT) :
    HWND = win32gui.FindWindow(None, WINDOW_CAPTION)
    pgwindow_x, pgwindow_y, *_ = win32gui.GetWindowRect(HWND)
    if pgwindow_x < width_pokerstars and pgwindow_y < height_pokerstars :
        if pgwindow_x / width_pokerstars > pgwindow_y / height_pokerstars :
            win32gui.SetWindowPos(HWND, win32con.HWND_TOP, width_pokerstars, pgwindow_y, PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT, 0) 
        else :
            win32gui.SetWindowPos(HWND, win32con.HWND_TOP, pgwindow_x, height_pokerstars, PG_WINDOW_WIDTH, PG_WINDOW_HEIGHT, 0) 
HOLDEM_WINDOWS_HWNDS = find_all_hwnds_by_substr("Hold'em") 
if len(HOLDEM_WINDOWS_HWNDS) == 0 : 
    print("===NO WINDOWS===")
    exit()