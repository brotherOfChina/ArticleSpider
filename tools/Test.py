
from ctypes import *
import time
import win32gui
# 772,267
# 1207,594
import win32api

import win32con

def makeYin():
    for i in range(1, 1000):
        windll.user32.SetCursorPos(772, 267)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 772, 267)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 772, 267)

        time.sleep(2)
        windll.user32.SetCursorPos(1207, 594)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 1207, 594)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 1207, 594)
        time.sleep(2)
def makeJin():
    for i in range(1, 100):
        windll.user32.SetCursorPos(972, 267)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 772, 267)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 772, 267)

        time.sleep(2)
        windll.user32.SetCursorPos(1207, 594)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 1207, 594)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 1207, 594)
        time.sleep(2)
def makeTong():
    for i in range(1, 3000):
        windll.user32.SetCursorPos(544, 267)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 544, 267)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 544, 267)

        time.sleep(2)
        windll.user32.SetCursorPos(1207, 594)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 1207, 594)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 1207, 594)
        time.sleep(2)
def getPos():
    print(win32gui.GetCursorPos())

# getPos()
# makeTong()
# makeYin()
makeJin()