import pyautogui as pag
import time
import numpy as np
from pywinauto import Desktop
import win32gui
import win32con
import win32clipboard
import csv
import json
import treys

def window_management() :
	windows = Desktop(backend = "uia").windows()
	width, height, was_history, was_lobby = 500, 400, False, False
	for w in windows :
		wname = str(w).split("'")[1]
		#print(wname)
		if "Limit" in wname or 'Find Seat' in wname or 'Waiting List' in wname or 'Insufficient' in wname :
			wname = str(w).split("'")[1] + "'" + str(w).split("'")[2]
			hwnd = win32gui.FindWindow(None, wname)		
			win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)
		if 'Hand History' in wname :
			hwnd = win32gui.FindWindow(None, wname)		
			win32gui.ShowWindow(hwnd, 5)
			win32gui.SetForegroundWindow(hwnd)
			win32gui.MoveWindow(hwnd, 0, 0, 500, 1000, True)
		if 'Lobby' in wname :
			wname = str(w).split("'")[1]
			hwnd = win32gui.FindWindow(None, wname)	
			win32gui.ShowWindow(hwnd, 5)
			win32gui.SetForegroundWindow(hwnd)	
			win32gui.MoveWindow(hwnd, 500, 0, 1000, 1000, True)

window_management()   
i = 0
ys = [266, 279, 300]
while 1 :
	#table
	index = i % 3
	x = np.random.randint(550, 970)
	pag.moveTo(x, ys[index], duration = 1+ np.random.random() / 10) 
	pag.click(x, ys[index])
	#observe
	x, y = np.random.randint(1140, 1400), 830
	pag.moveTo(x, y, duration = 1+ np.random.random() / 10)
	pag.click(x, y) 
	time.sleep(5)
	window_management()   
	#scroll
	x, y = 472, 474
	pag.moveTo(x, y, duration = 1+ np.random.random() / 10)
	for n in range(5) :
		pag.click(x, y)
		time.sleep(0.1) 
	pag.dragTo(x, y + 100, duration = 1+ np.random.random() / 10)
	#last
	x, y = np.random.randint(90, 400), 472
	pag.moveTo(x, y, duration = 1+ np.random.random() / 10)
	pag.click(x, y) 
	#text
	x, y = np.random.randint(60, 400), np.random.randint(560, 840)
	pag.moveTo(x, y, duration = 1 + np.random.random() / 10)
	pag.click(x, y) 
	#copy
	time.sleep(0.2)
	pag.hotkey("ctrlleft", "a")
	time.sleep(0.3)
	pag.hotkey("ctrlleft", "c") 
	time.sleep(0.5)
	
	#save
	win32clipboard.OpenClipboard()
	data = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()
	with open('hist.txt', 'a', encoding = "utf-8") as f :
		f.write('\n' + str(data))
		f.close()
	#restart
	print(i)
	i += 1
	pag.moveTo(np.random.randint(0, 1000), np.random.randint(0, 1000), duration = 2) 
#observe x = 1140 - 1400, y = 830
#tables x = 550 - 970, y = 266, 279, 300
#scroll x = 472, y = 474 2clicks 
#last x = 90 - 400, y 472
#text x = 60 - 400, y = 560 - 840
