'''
Author: Crange 839704627@qq.com
Date: 2023-01-24 00:14:27
LastEditors: Crange 839704627@qq.com
LastEditTime: 2023-01-24 16:29:40
'''
from dearpygui.dearpygui import *
from db_manage import reset_db

def resetPad(pad_name):
    # Erase all lines from the drawing pad
    # clear_drawing(pad_name)
    delete_item(pad_name, children_only=True)
    # set_item_color("Drawing Pad", style=mvGuiCol_WindowBg, color=[255, 255, 255])
    reset_db()
