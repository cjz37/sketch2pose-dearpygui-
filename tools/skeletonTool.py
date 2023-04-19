from dearpygui.dearpygui import *
import time
from db_manage import *
import math
import os
import cv2
import imutils


body_3_img = cv2.imread("./data/body/big-arm-left.png", cv2.IMREAD_UNCHANGED)
body_4_img = cv2.imread("./data/body/big-arm-right.png", cv2.IMREAD_UNCHANGED)
body_11_img = cv2.imread("./data/body/calf-left.png", cv2.IMREAD_UNCHANGED)
body_12_img = cv2.imread("./data/body/calf-right.png", cv2.IMREAD_UNCHANGED)
body_13_img = cv2.imread("./data/body/foot-left.png", cv2.IMREAD_UNCHANGED)
body_14_img = cv2.imread("./data/body/foot-right.png", cv2.IMREAD_UNCHANGED)
body_5_img = cv2.imread("./data/body/forearm-left.png", cv2.IMREAD_UNCHANGED)
body_6_img = cv2.imread("./data/body/forearm-right.png", cv2.IMREAD_UNCHANGED)
body_1_img = cv2.imread("./data/body/head.png", cv2.IMREAD_UNCHANGED)
body_2_img = cv2.imread("./data/body/hip.png", cv2.IMREAD_UNCHANGED)
body_7_img = cv2.imread("./data/body/palm-left.png", cv2.IMREAD_UNCHANGED)
body_8_img = cv2.imread("./data/body/palm-right.png", cv2.IMREAD_UNCHANGED)
body_9_img = cv2.imread("./data/body/thigh-left.png", cv2.IMREAD_UNCHANGED)
body_10_img = cv2.imread("./data/body/thigh-right.png", cv2.IMREAD_UNCHANGED)
body_0_img = cv2.imread("./data/body/upper-body.png", cv2.IMREAD_UNCHANGED)

body_imgs = [body_0_img, body_1_img, body_2_img, body_3_img, body_4_img, body_5_img, body_6_img, body_7_img, body_8_img, body_9_img, body_10_img, body_11_img, body_12_img, body_13_img, body_14_img]


def update_texture(i):
    data = load_image(f"./data/body/temp/body_{i}.png")
    set_value(f"body {i} texture", data[3])
    # delete_item(f"body {i} texture")
    # add_static_texture(width=data[0], height=data[1], default_value=data[3], tag=f"body {i} texture", parent="global texture")


def rotate(i, angle):
    global body_imgs
    rotated = imutils.rotate_bound(body_imgs[i], angle)
    cv2.imwrite(f"./data/body/temp/body_{i}.png", rotated)
    update_texture(i)


def check(p1, p2, k):
    return abs(p1[0] - p2[0]) < k and abs(p1[1] - p2[1]) < k


def vectorAdd(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]


def vectorSub(p1, p2):
    return [p1[0] - p2[0], p1[1] - p2[1]]


def vectorHalf(v):
    return [v[0] / 2, v[1] / 2]


def draw_body(i, center, point_radius, point_color, first_point, second_point, pad_name):
    draw_image(
        texture_tag=f"body {i} texture",
        pmin=first_point,
        pmax=second_point,
        parent=pad_name,
        tag=f"body {i}",
    )
    draw_circle(
        center=center,
        radius=point_radius,
        tag=f"control point {i}",
        color=point_color,
        fill=point_color,
        parent=pad_name,
    )
    draw_text(
        pos=vectorSub(center, [5, 10]),
        text=f"{i}",
        size=20,
        color=[20, 20, 20],
        tag=f"point label {i}",
        parent=pad_name
    )


def initPad(pad_name, control_points_sum, control_points, point_radius, point_color, body_width):
    tools.resetPad(pad_name)

    for i in range(control_points_sum):
        center = control_points[i]
        first_point = vectorSub(center, vectorHalf(body_width[i]))
        second_point = vectorAdd(center, vectorHalf(body_width[i]))

        draw_body(i, center, point_radius, point_color, first_point, second_point, pad_name)


def skeletonTool(pad_name):
    button_id = -1
    is_release = False
    angle = 0

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

    def _release_handler(sender, data):
        nonlocal button_id
        nonlocal is_release
        mouse_type = get_item_info(sender)["type"]
        if mouse_type == "mvAppItemType::mvMouseReleaseHandler":
            button_id = data
            is_release = True

    def _drag_handler(sender, data):
        nonlocal angle
        angle = data[1]

    for handler in get_item_children("mouse handler", 1):
        set_item_callback(handler, _release_handler)

    set_item_callback("mr_drag", _drag_handler)

    control_points_sum = 15
    point_radius = 10
    point_color = [255, 255, 255]
    body_width = [[174, 213], [109, 112], [132, 145], [152, 41], [152, 41], [138, 43], [138, 43], [67, 73], [67, 73], [62, 218], [62, 218], [58, 237], [58, 237], [52, 67], [52, 67]]
    control_points = [[618.0, 261.0], [618.0, 117.0], [618.0, 365.0], [485.0, 213.0], [751.0, 213.0], [377.0, 210.0], [866.0, 210.0], [302.0, 182.0], [943.0, 182.0], [581.0, 489.0], [654.0, 489.0], [574.0, 669.0], [661.0, 669.0], [579.0, 785.0], [656.0, 785.0]]
    initPad(pad_name, control_points_sum, control_points, point_radius, point_color, body_width)

    while True:
        current_mouse_pos = get_drawing_mouse_pos()

        if is_mouse_button_down(mvMouseButton_Right):

            print(angle)

            if get_active_window() != "Drawing Pad":
                break

            for i in range(control_points_sum):

                if check(control_points[i], current_mouse_pos, point_radius):

                    while not isMouseButtonLeftReleased():
                        time.sleep(0.02)

                        rotate(i, angle)

                        delete_item(f"body {i}")
                        delete_item(f"control point {i}")
                        delete_item(f"point label {i}")
                        #
                        current_mouse_pos = get_drawing_mouse_pos()
                        first_point = vectorSub(current_mouse_pos, vectorHalf(body_width[i]))
                        second_point = vectorAdd(current_mouse_pos, vectorHalf(body_width[i]))

                        draw_body(i, current_mouse_pos, point_radius, point_color, first_point, second_point, pad_name)

                    control_points[i] = current_mouse_pos

        if is_mouse_button_down(mvMouseButton_Left):
            # current_mouse_pos = get_drawing_mouse_pos()

            if get_active_window() != "Drawing Pad":
                break

            for i in range(control_points_sum):

                if check(control_points[i], current_mouse_pos, point_radius):

                    while not isMouseButtonLeftReleased():
                        time.sleep(0.02)

                        delete_item(f"body {i}")
                        delete_item(f"control point {i}")
                        delete_item(f"point label {i}")

                        current_mouse_pos = get_drawing_mouse_pos()
                        first_point = vectorSub(current_mouse_pos, vectorHalf(body_width[i]))
                        second_point = vectorAdd(current_mouse_pos, vectorHalf(body_width[i]))

                        draw_body(i, current_mouse_pos, point_radius, point_color, first_point, second_point, pad_name)

                    control_points[i] = current_mouse_pos

                    # print(control_points)

