import pyautogui
import win32gui
import win32con
import time
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from PIL import Image
import os
from pathlib import Path

from db_manage import saveDatabase

from dearpygui.dearpygui import *


def saveTool():

    hwnd = win32gui.FindWindow(None, "Sketch2Pose")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
    im = pyautogui.screenshot(region=(x, y, x1, y1))
    file_path = asksaveasfilename(title="Sketch2Pose save image window",
                                  initialfile="New Sketch2Pose",
                                  filetypes=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png"),
                                             ("Sketch2Pose File (*.db)", "*.db")],
                                  defaultextension="*.jpg")

    if file_path:

        if file_path[-3:] == ".db":
            saveDatabase(file_path)

        else:
            im.save(file_path)
            im = Image.open(file_path)
            im = im.crop((360, 50, get_viewport_width() - 16, get_viewport_height() - 70))
            im.save(file_path)


def autoSaveTool():

    hwnd = win32gui.FindWindow(None, "Sketch2Pose")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
    im = pyautogui.screenshot(region=(x, y, x1, y1))

    file_path = os.getcwd() + "\\temp\\temp_file.png"

    if file_path:
        im.save(file_path)
        im = Image.open(file_path)
        im = im.crop((360, 50, get_viewport_width() - 16, get_viewport_height() - 70))
        im.save(file_path)
    else:
        pass
