from dearpygui.dearpygui import *
import time
import numpy as np
from scipy import interpolate
import scipy.interpolate as si

import tools
from db_manage import *


def draw_spline_quadratic(
        p1,
        p2,
        p3,
        p4,
        color,
        thickness,
        parent,
        tag):
    x = [p1[0], p2[0], p3[0], p4[0]]
    y = [p1[1], p2[1], p3[1], p4[1]]

    t = range(len(x))
    ipl_t = np.linspace(0.0, len(x) - 1, 100)

    x_tup = si.splrep(t, x, k=2)
    y_tup = si.splrep(t, y, k=2)
    x_i = si.splev(ipl_t, x_tup)
    y_i = si.splev(ipl_t, y_tup)

    for i in range(99):
        draw_line(
            p1=[x_i[i], y_i[i]],
            p2=[x_i[i + 1], y_i[i + 1]],
            color=color,
            thickness=thickness,
            parent=parent,
            tag=f"{tag} line {i}"
        )


def init():
    delete_item("cursor")

    delete_item("last point")

    for count in range(tools.temp_count + 1):
        delete_item(f"temp_point {count}")

    tools.temp_count = 0


def splineTool(pad_name, lineColor, lineThickness):

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

    spline_points = [[0., 0.], [0., 0.], [0., 0.], [0., 0.]]

    while True:

        time.sleep(0.01)

        while True:

            time.sleep(0.01)

            # 结束绘制
            if isMouseButtonRightReleased() or is_key_down(mvKey_Escape):
                init()
                break

            if isMouseButtonLeftReleased():

                if get_active_window() != "Drawing Pad":
                    init()
                    return

                spline_points[tools.temp_count] = get_drawing_mouse_pos()
                draw_circle(
                    center=spline_points[tools.temp_count],
                    radius=3,
                    fill=[255, 0, 0, 255],
                    tag=f"temp_point {tools.temp_count}",
                    parent=pad_name,
                )
                # print("[FIRST click]: tools.temp_count = {}, pos = {}".format(tools.temp_count, spline_points[tools.temp_count]))
                tools.temp_count += 1

                while True:

                    time.sleep(0.01)

                    if isMouseButtonLeftReleased():

                        if get_active_window() != "Drawing Pad":
                            init()
                            return

                        spline_points[tools.temp_count] = get_drawing_mouse_pos()
                        draw_circle(
                            center=spline_points[tools.temp_count],
                            radius=3,
                            fill=[255, 0, 0, 255],
                            tag=f"temp_point {tools.temp_count}",
                            parent=pad_name,
                        )
                        tools.temp_count += 1

                        if tools.temp_count > 3:
                            draw_spline_quadratic(
                                p1=spline_points[0],
                                p2=spline_points[1],
                                p3=spline_points[2],
                                p4=spline_points[3],
                                color=lineColor,
                                thickness=lineThickness,
                                parent=pad_name,
                                tag=f"spline {tools.spline_count}"
                            )
                            delete_item("last point")
                            draw_circle(
                                center=spline_points[3],
                                radius=3,
                                fill=[255, 0, 0, 255],
                                tag="last point",
                                parent=pad_name,
                            )

                            write_db(tool="spline tool", point_1=str(spline_points[0]), point_2=str(spline_points[1]),
                                     point_3=str(spline_points[2]), point_4=str(spline_points[3]), color=str(lineColor),
                                     thickness=lineThickness, tag=f"spline {tools.spline_count}")
                            tools.spline_count += 1

                            for count in range(tools.temp_count + 1):
                                delete_item(f"temp_point {count}")

                            tools.temp_count = 1
                            spline_points[0] = spline_points[3]
                            break

                    # 结束绘制
                    if isMouseButtonRightReleased() or is_key_down(mvKey_Escape):
                        init()
                        break
