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

hwnd = find_all_hwnds_by_substr("ALABAMA")[0]
win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
win32gui.SetForegroundWindow(hwnd)