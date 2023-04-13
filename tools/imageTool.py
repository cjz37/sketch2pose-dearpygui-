from dearpygui.dearpygui import *
import time
import math
from db_manage import *
from PIL import Image

from tkinter import Tk
from tkinter.filedialog import askopenfilename


def imageTool(pad_name, file):

    pad_width = get_viewport_width() - 375
    pad_height = get_viewport_height() - 118
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
    print(first_point, second_point)

    write_db(tool="image tool", point_1=str(first_point), point_2=str(second_point), image=file, tag=f"image {tools.image_count}")

    tools.image_count += 1


def searchImage():
    Tk().withdraw()

    file_path = askopenfilename(title="Sketch2Pose select image window",
                                filetypes=[("ALL FILES (*.jpg, *.jpeg, *.png)", "*.jpg *.jpeg *.png"), ("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")],
                                defaultextension=[("ALL FILES (*.jpg, *.jpeg, *.png)", "*.jpg *.jpeg *.png"), ("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")])

    if file_path:
        set_value("##imagePath", file_path)
