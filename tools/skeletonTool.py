from dearpygui.dearpygui import *
import time
from db_manage import *
import math
import os


def check(p1, p2, k):
    return abs(p1[0] - p2[0]) < k and abs(p1[1] - p2[1]) < k


def initPad(pad_name, num_control_points, point_radius, point_color):
    tools.resetPad(pad_name)

    first_point = [253, 0]
    second_point = [972, 752]
    draw_image(
        texture_tag="bbw template texture",
        pmin=first_point,
        pmax=second_point,
        parent=pad_name,
        tag="bbw template",
    )

    control_points = [[614.0, 56.0], [615.0, 119.0], [615.0, 199.0], [614.0, 288.0], [570.0, 387.0], [659.0, 387.0],
                      [575.0, 544.0], [653.0, 543.0], [569.0, 701.0], [657.0, 702.0], [529.0, 156.0], [694.0, 156.0],
                      [446.0, 168.0], [795.0, 168.0], [326.0, 168.0], [896.0, 168.0], [280.0, 184.0], [941.0, 181.0]]


    for i in range(num_control_points):
        draw_circle(
            center=control_points[i],
            radius=point_radius,
            tag=f"control point {i}",
            color=point_color,
            fill=point_color,
            parent=pad_name,
        )
        draw_text(
            pos=[control_points[i][0] - 5, control_points[i][1] - 10],
            text=f"{i + 1}",
            size=20,
            color=[255, 0, 0],
            tag=f"point label {i}",
            parent=pad_name)

    return control_points


def skeletonTool(pad_name):
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

    num_control_points = 18
    point_radius = 10
    point_color = [50, 50, 100]
    control_points = initPad(pad_name, num_control_points, point_radius, point_color)
    while True:

        if is_mouse_button_down(mvMouseButton_Left):
            current_mouse_pos = get_mouse_pos()

            if get_active_window() != "Drawing Pad":
                break

            for i in range(num_control_points):

                if check(control_points[i], current_mouse_pos, point_radius):

                    while not isMouseButtonLeftReleased():
                        time.sleep(0.02)
                        delete_item(f"control point {i}")
                        delete_item(f"point label {i}")
                        current_mouse_pos = get_mouse_pos()
                        draw_circle(
                            center=current_mouse_pos,
                            radius=point_radius,
                            tag=f"control point {i}",
                            color=point_color,
                            fill=point_color,
                            parent=pad_name)
                        draw_text(
                            pos=[current_mouse_pos[0] - 5, current_mouse_pos[1] - 10],
                            text=f"{i + 1}",
                            size=20,
                            color=[255, 0, 0],
                            tag=f"point label {i}",
                            parent=pad_name)
                    control_points[i] = current_mouse_pos

        if isMouseButtonRightReleased():

            current_mouse_pos = get_mouse_pos()

            draw_circle(
                center=current_mouse_pos,
                radius=point_radius,
                tag=f"control point {num_control_points}",
                color=point_color,
                fill=point_color,
                parent=pad_name)
            draw_text(
                pos=[current_mouse_pos[0] - 5, current_mouse_pos[1] - 10],
                text=f"{num_control_points + 1}",
                size=20,
                color=[255, 0, 0],
                tag=f"point label {num_control_points}",
                parent=pad_name)

            num_control_points += 1
            control_points.append(current_mouse_pos)

            if get_active_window() != "Drawing Pad":
                break

        if is_key_released(mvKey_S):
            print(control_points)
            break
