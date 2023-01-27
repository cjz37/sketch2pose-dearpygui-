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

file_path = ''


def saveTool():
    global file_path

    delete_item("cursor circle")
    delete_item("cursor node")

    Tk().withdraw()

    hwnd = win32gui.FindWindow(None, "Sketch2Pose")
    win32gui.SetForegroundWindow(hwnd)
    # win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
    time.sleep(0.1)
    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
    im = pyautogui.screenshot(region=(x, y, x1, y1))
    file_path = asksaveasfilename(title="Sketch2Pose save image window",
                                  initialfile="New Sketch2Pose",
                                  filetypes=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png"),
                                             ("PDF (*.pdf)", "*.pdf"), ("Sketch2Pose File (*.db)", "*.db")],
                                  defaultextension=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png"),
                                                    ("PDF (*.pdf)", "*.pdf"), ("Sketch2Pose File (*.db)", "*.sdw")])

    win32gui.SetForegroundWindow(hwnd)

    if file_path:

        if file_path[-3:] == ".db":
            saveDatabase(file_path)

        elif file_path[-4:] == ".pdf":
            im.save(f"{file_path[:-4]}.png")
            im = Image.open(f"{file_path[:-4]}.png")
            im = im.crop((335, 80, 1352, 683))
            im.save(f"{file_path[:-4]}.png")
            im = im.convert('RGB')
            im.save(fr'{file_path}')
            os.remove(f"{file_path[:-4]}.png")

        else:
            im.save(file_path)
            im = Image.open(file_path)
            im = im.crop((360, 80, 1352, 702))
            im.save(file_path)


def autoSaveTool():
    global file_path

    delete_item("cursor circle")
    delete_item("cursor node")

    Tk().withdraw()

    hwnd = win32gui.FindWindow(None, "Sketch2Pose")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    x, y, x1, y1 = win32gui.GetClientRect(hwnd)
    x, y = win32gui.ClientToScreen(hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
    im = pyautogui.screenshot(region=(x, y, x1, y1))

    win32gui.SetForegroundWindow(hwnd)

    file_path = os.getcwd() + "\\temp\\temp_file.png"

    if file_path:
        im.save(file_path)
        im = Image.open(file_path)
        im = im.crop((360, 80, 1352, 702))
        im.save(file_path)
