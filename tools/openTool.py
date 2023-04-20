import win32gui
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

from db_manage import open_db

from dearpygui.dearpygui import *

file_path = ''


def openTool():
    global file_path

    Tk().withdraw()

    hwnd = win32gui.FindWindow(None, "Sketch2Pose")

    file_path = askopenfilename(title="Sketch2Pose open drawing window",
                                filetypes=[("Sketch2Pose File (*.db)", "*.db")],
                                defaultextension=[("Sketch2Pose File (*.db)", "*.db")])

    win32gui.SetForegroundWindow(hwnd)

    if file_path:
        open_db(file_path)
