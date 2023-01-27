from dearpygui.dearpygui import *
import time
import math
from db_manage import *
from PIL import Image

import pyautogui
import win32gui
import win32con
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def imageTool(pad_name, file):

    # button_id = -1
    # is_release = False

    # def isMouseButtonLeftReleased():
    #     nonlocal button_id
    #     nonlocal is_release
    #     if is_release and mvMouseButton_Left == button_id:
    #         is_release = False
    #         return True
        
    #     return False

    # def isMouseButtonRightReleased():
    #     nonlocal button_id
    #     nonlocal is_release
    #     if is_release and mvMouseButton_Right == button_id:
    #         is_release = False
    #         return True
        
    #     return False

    # def _event_handler(sender, data):
    #     nonlocal button_id
    #     nonlocal is_release
    #     type = get_item_info(sender)["type"]
    #     if type == "mvAppItemType::mvMouseReleaseHandler":
    #         button_id = data
    #         is_release = True

    # for handler in get_item_children("mouse handler", 1):
    #     set_item_callback(handler, _event_handler)

    # image = Image.open(file)
    pad_width = 1025.0
    pad_height = 654.0
    pad_ratio = pad_width / pad_height

    image = load_image(file)
    width, height, value = image[0], image[1], image[3]
    aspect_ratio = width / height

    first_point = [0, 0]
    second_point = [width, height]
    
    add_static_texture(width=width, height=height, default_value=value, tag=f"load image texture {tools.image_count}", parent="global texture")

    if aspect_ratio <= pad_ratio:
        temp_height = aspect_ratio * pad_height
        adjust = (pad_width - temp_height) / 2

        second_point = [temp_height, pad_height]
        first_point[0] += adjust
        second_point[0] += adjust
    else:
        temp_width = pad_width / aspect_ratio
        adjust = (pad_height - temp_width) / 2

        second_point = [pad_width, temp_width]
        first_point[1] += adjust
        second_point[1] += adjust

    draw_image(
        texture_tag=f"load image texture {tools.image_count}",
        pmin=first_point,
        pmax=second_point,
        parent="Pad",
        tag=f"image {tools.image_count}",
    )

    write_db(tool="image tool", point_1=str(first_point), point_2=str(second_point), image=file, tag=f"image {tools.image_count}")

    tools.image_count += 1

    # time.sleep(0.1)

    # while True:
    #     # Begin drawing when left mouse button is released
    #     if isMouseButtonLeftReleased():

    #         # If mouse is clicked outside the Drawing Pad, exit the tool.
    #         if get_active_window() != "Drawing Pad":
    #             break

    #         # Continue if clicked on the drawing pad
    #         mouse_position = get_drawing_mouse_pos()
    #         time.sleep(0.01)

    #         while True:
    #             point2 = get_drawing_mouse_pos()

    #             if is_key_down(mvKey_Shift):
    #                 if point2[0] < mouse_position[0]:
    #                     # Check if in second quadrant
    #                     if point2[1] < mouse_position[1]:
    #                         first_point = mouse_position
    #                         width = aspect_ratio * (mouse_position[1] - point2[1])
    #                         second_point = [mouse_position[0] - width, point2[1]]
    #                         draw_image(
    #                             texture_tag="load image",
    #                             pmin=first_point,
    #                             pmax=second_point,
    #                             parent=pad_name,
    #                             tag=f"image {tools.image_count}",
    #                         )

    #                     # Check if in third quadrant
    #                     else:
    #                         first_point = mouse_position
    #                         width = aspect_ratio * (point2[1] - mouse_position[1])
    #                         second_point = [mouse_position[0] - width, point2[1]]
    #                         draw_image(
    #                             texture_tag="load image",
    #                             pmin=first_point,
    #                             pmax=second_point,
    #                             parent=pad_name,
    #                             tag=f"image {tools.image_count}",
    #                         )

    #                 # Check if in first quadrant
    #                 elif get_drawing_mouse_pos()[1] < mouse_position[1]:
    #                     first_point = mouse_position
    #                     width = aspect_ratio * (mouse_position[1] - point2[1])
    #                     second_point = [mouse_position[0] + width, point2[1]]
    #                     draw_image(
    #                         texture_tag="load image",
    #                         pmin=first_point,
    #                         pmax=second_point,
    #                         parent=pad_name,
    #                         tag=f"image {tools.image_count}",
    #                     )

    #                 # Check if in fourth quadrant
    #                 else:
    #                     first_point = mouse_position
    #                     width = aspect_ratio * (point2[1] - mouse_position[1])
    #                     second_point = [mouse_position[0] + width, point2[1]]
    #                     draw_image(
    #                         texture_tag="load image",
    #                         pmin=first_point,
    #                         pmax=second_point,
    #                         parent=pad_name,
    #                         tag=f"image {tools.image_count}",
    #                     )

    #             else:
    #                 first_point = mouse_position
    #                 second_point = point2
    #                 draw_image(
    #                     texture_tag="load image",
    #                     pmin=first_point,
    #                     pmax=second_point,
    #                     parent=pad_name,
    #                     tag=f"image {tools.image_count}",
    #                 )

    #             time.sleep(0.01)

    #             # Check if user wants to select the second point of the line
    #             if isMouseButtonLeftReleased():
    #                 # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
    #                 if get_active_window() != "Drawing Pad":
    #                     delete_item(f"image {tools.image_count}")
    #                     break

    #                 write_db(tool="image tool", point_1=str(first_point), point_2=str(second_point), image=file, tag=f"image {tools.image_count}")
    #                 tools.image_count += 1
    #                 time.sleep(0.01)
    #                 break

    #             # Check if user wants to exit the line tool
    #             if isMouseButtonRightReleased():
    #                 delete_item(f"image {tools.image_count}")
    #                 break

    #             # Check if user wants to exit the line tool
    #             if is_key_down(mvKey_Escape):
    #                 delete_item(f"image {tools.image_count}")
    #                 break

    #             # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
    #             delete_item(f"image {tools.image_count}")

# def get_angle(first_position, second_position):

#     if second_position[0] == first_position[0]:
#         return 0

#     else:
#         return abs(math.degrees(math.atan((second_position[1] - first_position[1]) / (second_position[0] - first_position[0]))))

def searchImage():
    Tk().withdraw()

    hwnd = win32gui.FindWindow(None, "Sketch2Pose")

    file_path = askopenfilename(title="Sketch2Pose select image window",
                                filetypes=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")],
                                defaultextension=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")])

    win32gui.SetForegroundWindow(hwnd)

    if file_path:
        set_value("##imagePath", file_path)