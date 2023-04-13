from dearpygui.dearpygui import *
import time
import numpy as np
from scipy import interpolate
import scipy.interpolate as si

from db_manage import *

def draw_spline(
        p1,
        p2,
        p3,
        p4,
        color,
        thickness,
        parent):
    x = [p1[0], p1[0], p1[0], p2[0], p3[0], p4[0], p4[0]]
    y = [p1[1], p1[1], p1[1], p2[1], p3[1], p4[1], p4[1]]

    t = range(len(x))
    knots = [2, 3, 4]
    ipl_t = np.linspace(0.0, len(x) - 1, 100)

    x_tup = si.splrep(t, x, k=3, t=knots)
    y_tup = si.splrep(t, y, k=3, t=knots)
    x_i = si.splev(ipl_t, x_tup)
    y_i = si.splev(ipl_t, y_tup)

    for i in range(len(x_i) - 1):
        draw_line(
            p1=[x_i[i], y_i[i]],
            p2=[x_i[i + 1], y_i[i + 1]],
            color=color,
            thickness=thickness,
            parent=parent,
        )


def curveTool(pad_name, lineColor, lineThickness):

    button_id = -1
    is_release = False

    def isMouseButtonLeftReleased():
        nonlocal button_id
        nonlocal is_release
        if is_release and mvMouseButton_Left == button_id:
            is_release = False
            return True

        return False

    def isMouseButtonRightReleased():
        nonlocal button_id
        nonlocal is_release
        if is_release and mvMouseButton_Right == button_id:
            is_release = False
            return True

        return False

    def _event_handler(sender, data):
        nonlocal button_id
        nonlocal is_release
        mouse_type = get_item_info(sender)["type"]
        if mouse_type == "mvAppItemType::mvMouseReleaseHandler":
            button_id = data
            is_release = True

    for handler in get_item_children("mouse handler", 1):
        set_item_callback(handler, _event_handler)

    lines_count = 0
    pre_last_point = [0., 0.]

    while True:

        temp_count = 0
        spline_points = [[0., 0.], [0., 0.], [0., 0.], [0., 0.]]

        if isMouseButtonLeftReleased():

            if get_active_window() != "Drawing Pad":
                return

            spline_points[temp_count] = get_drawing_mouse_pos()
            draw_circle(
                center=spline_points[temp_count],
                radius=3,
                fill=[255, 0, 0, 255],
                tag=f"temp_point {temp_count}",
                parent=pad_name,
            )
            # print("[FIRST click]: temp_count = {}, pos = {}".format(temp_count, spline_points[temp_count]))
            temp_count += 1

            while True:

                if isMouseButtonLeftReleased():
                    spline_points[temp_count] = get_drawing_mouse_pos()
                    draw_circle(
                        center=spline_points[temp_count],
                        radius=3,
                        fill=[255, 0, 0, 255],
                        tag=f"temp_point {temp_count}",
                        parent=pad_name,
                    )
                    # print("[FIRST click]: temp_count = {}, pos = {}".format(temp_count, spline_points[temp_count]))
                    temp_count += 1

                    if temp_count > 3:
                        draw_spline(
                            p1=spline_points[0],
                            p2=spline_points[1],
                            p3=spline_points[2],
                            p4=spline_points[3],
                            color=lineColor,
                            thickness=lineThickness,
                            parent=pad_name,
                        )
                        print('[Draw]: {}; lineID = {}'.format(spline_points, lines_count))
                        tools.spline_count += 1

                        for count in range(temp_count + 1):
                            delete_item(f"temp_point {count}")

                        break

        if isMouseButtonRightReleased() or is_key_down(mvKey_Escape):
            break


