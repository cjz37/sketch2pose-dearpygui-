from shlex import join

from dearpygui.dearpygui import *
import time

import tools
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


# 是否显示关节点
def showJoints():
    if get_value("Show joints"):
        tools.joint_color = [155, 224, 229, 255]
    else:
        tools.joint_color = [155, 224, 229, 0]


# 判断点击范围
def check(p1, p2, k):
    return abs(p1[0] - p2[0]) < k and abs(p1[1] - p2[1]) < k


# 点坐标加法
def vectorAdd(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]


# 点坐标减法
def vectorSub(p1, p2):
    return [p1[0] - p2[0], p1[1] - p2[1]]


# 1/2 点坐标
def vectorHalf(v):
    return [v[0] / 2, v[1] / 2]


# 取中点
def mid_point(p1, p2):
    return vectorHalf(vectorAdd(p1, p2))


# 绘制身体部位 i
def draw_body(i, center, first_point, second_point, pad_name):
    point_radius = 10
    point_color = [255, 255, 255]
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


# 初始化人体
def initPad(pad_name, control_points, body_width, joints):
    joint_radius = 12

    tools.resetPad(pad_name)

    num = len(control_points)
    for i in range(num):
        center = control_points[i]
        first_point = vectorSub(center, vectorHalf(body_width[i]))
        second_point = vectorAdd(center, vectorHalf(body_width[i]))

        draw_body(i, center, first_point, second_point, pad_name)

    num = len(joints)
    for i in range(num):
        draw_circle(
            center=joints[i]['pos'],
            radius=joint_radius,
            tag=f"joint {i}",
            color=tools.joint_color,
            fill=tools.joint_color,
            parent=pad_name,
        )

    # 更新手掌
    i = 7
    delete_old_item(i)
    i = 8
    delete_old_item(i)
    # 更新脚
    i = 13
    delete_old_item(i)
    i = 14
    delete_old_item(i)


# 更新纹理
def update_texture(i, angle):
    if i == 4 or i == 5 or i == 10 or i == 11:
        return
    if i != 1 or i != 3:
        angle = -angle

    global body_imgs

    i += 3
    rotated = imutils.rotate(body_imgs[i], angle)
    cv2.imwrite(f"./data/body/temp/body_{i}.png", rotated)

    data = load_image(f"./data/body/temp/body_{i}.png")
    set_value(f"body {i} texture", data[3])


# 删除旧的身体部位
def delete_old_item(i):
    delete_item(f"body {i}")
    delete_item(f"control point {i}")
    delete_item(f"point label {i}")


# 更新人体
def update_body(joints, body_width, pad_name):
    # 更新大臂左
    i = 3
    delete_old_item(i)
    center = mid_point(joints[0]['pos'], joints[2]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)
    # 更新大臂右
    i = 4
    delete_old_item(i)
    center = mid_point(joints[1]['pos'], joints[3]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)
    # 更新小臂左
    i = 5
    delete_old_item(i)
    center = mid_point(joints[2]['pos'], joints[4]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)
    # 更新小臂右
    i = 6
    delete_old_item(i)
    center = mid_point(joints[3]['pos'], joints[5]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)
    # 更新大腿左
    i = 9
    delete_old_item(i)
    center = mid_point(joints[6]['pos'], joints[8]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)
    # 更新大腿右
    i = 10
    delete_old_item(i)
    center = mid_point(joints[7]['pos'], joints[9]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)
    # 更新小腿左
    i = 11
    delete_old_item(i)
    center = mid_point(joints[8]['pos'], joints[10]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)
    # 更新小腿右
    i = 12
    delete_old_item(i)
    center = mid_point(joints[9]['pos'], joints[11]['pos'])
    first_point = vectorSub(center, vectorHalf(body_width[i]))
    second_point = vectorAdd(center, vectorHalf(body_width[i]))
    draw_body(i, center, first_point, second_point, pad_name)

    # 更新手掌
    i = 7
    delete_old_item(i)
    i = 8
    delete_old_item(i)
    # 更新脚
    i = 13
    delete_old_item(i)
    i = 14
    delete_old_item(i)


# 更新关节点坐标及对应纹理
def update_joints_pos(joints, rotate_joint, angle):
    big_arm_length = 125
    forearm_length = 110
    thigh_length = 165
    calf_length = 195

    angle = (angle + joints[rotate_joint]['angle']) / 180 * math.pi

    if rotate_joint == 0:
        offset = [big_arm_length * math.cos(angle), big_arm_length * math.sin(angle)]
        joints[2]['pos'] = vectorSub(joints[0]['pos'], offset)

        joint_angle = joints[2]['angle'] / 180 * math.pi
        offset = [forearm_length * math.cos(joint_angle), forearm_length * math.sin(joint_angle)]
        joints[4]['pos'] = vectorSub(joints[2]['pos'], offset)
    elif rotate_joint == 1:
        offset = [big_arm_length * math.cos(angle), big_arm_length * math.sin(angle)]
        joints[3]['pos'] = vectorAdd(joints[1]['pos'], offset)

        joint_angle = joints[3]['angle'] / 180 * math.pi
        offset = [forearm_length * math.cos(joint_angle), forearm_length * math.sin(joint_angle)]
        joints[5]['pos'] = vectorAdd(joints[3]['pos'], offset)
    elif rotate_joint == 2:
        offset = [forearm_length * math.cos(angle), forearm_length * math.sin(angle)]
        joints[4]['pos'] = vectorSub(joints[2]['pos'], offset)
    elif rotate_joint == 3:
        offset = [forearm_length * math.cos(angle), forearm_length * math.sin(angle)]
        joints[5]['pos'] = vectorAdd(joints[3]['pos'], offset)
    elif rotate_joint == 4:
        pass
    elif rotate_joint == 5:
        pass
    elif rotate_joint == 6:
        angle += math.pi / 2
        offset = [thigh_length * math.cos(angle), thigh_length * math.sin(angle)]
        joints[8]['pos'] = vectorAdd(joints[6]['pos'], offset)

        joint_angle = joints[8]['angle'] / 180 * math.pi + math.pi / 2
        offset = [calf_length * math.cos(joint_angle), calf_length * math.sin(joint_angle)]
        joints[10]['pos'] = vectorAdd(joints[8]['pos'], offset)
    elif rotate_joint == 7:
        angle += math.pi / 2
        offset = [thigh_length * math.cos(angle), thigh_length * math.sin(angle)]
        joints[9]['pos'] = vectorAdd(joints[7]['pos'], offset)

        joint_angle = joints[9]['angle'] / 180 * math.pi + math.pi / 2
        offset = [calf_length * math.cos(joint_angle), calf_length * math.sin(joint_angle)]
        joints[11]['pos'] = vectorAdd(joints[9]['pos'], offset)
    elif rotate_joint == 8:
        angle += math.pi / 2
        offset = [calf_length * math.cos(angle), calf_length * math.sin(angle)]
        joints[10]['pos'] = vectorAdd(joints[8]['pos'], offset)
    elif rotate_joint == 9:
        angle += math.pi / 2
        offset = [calf_length * math.cos(angle), calf_length * math.sin(angle)]
        joints[11]['pos'] = vectorAdd(joints[9]['pos'], offset)
    elif rotate_joint == 10:
        pass
    elif rotate_joint == 11:
        pass

    return joints


# 更新关节点的旋转角度
def update_joints_angle(joints, rotate_joint, angle):
    joints[rotate_joint]['angle'] += angle
    return joints


# 重绘关节点
def redraw_joints(joints, pad_name):
    joint_radius = 12

    num = len(joints)
    for i in range(num):
        delete_item(f"joint {i}")
        draw_circle(
            center=joints[i]['pos'],
            radius=joint_radius,
            tag=f"joint {i}",
            color=tools.joint_color,
            fill=tools.joint_color,
            parent=pad_name,
        )


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

    set_item_callback("ml_drag", _drag_handler)

    # 纹理尺寸
    body_width = [[213, 213],
                  [112, 112],
                  [190, 190],
                  [152, 152],
                  [152, 152],
                  [138, 138],
                  [138, 138],
                  [95, 95],
                  [95, 95],
                  [218, 218],
                  [218, 218],
                  [237, 237],
                  [237, 237],
                  [67, 67],
                  [67, 67]]
    # 控制点信息（纹理的中心）
    control_points = [[618.0, 261.0],
                      [618.0, 117.0],
                      [618.0, 365.0],
                      [483.5, 210.0],
                      [750.5, 210.0],
                      [366.0, 210.0],
                      [867.0, 210.0],
                      [293.0, 182.0],
                      [943.0, 182.0],
                      [580.0, 487.5],
                      [654.0, 487.5],
                      [580.0, 667.5],
                      [654.0, 667.5],
                      [579.0, 785.0],
                      [656.0, 785.0]]
    # 关节点信息
    joints = [{'pos': [546, 210], 'angle': 0},  # 0
              {'pos': [688, 210], 'angle': 0},  # 1
              {'pos': [421, 210], 'angle': 0},  # 2
              {'pos': [813, 210], 'angle': 0},  # 3
              {'pos': [313, 210], 'angle': 0},  # 4
              {'pos': [921, 210], 'angle': 0},  # 5
              {'pos': [580, 405], 'angle': 0},  # 6
              {'pos': [654, 405], 'angle': 0},  # 7
              {'pos': [580, 570], 'angle': 0},  # 8
              {'pos': [654, 570], 'angle': 0},  # 9
              {'pos': [580, 765], 'angle': 0},  # 10
              {'pos': [654, 765], 'angle': 0}]  # 11
    # 关节点大小
    joint_radius = 12

    initPad(pad_name, control_points, body_width, joints)

    while True:

        current_mouse_pos = get_drawing_mouse_pos()

        if is_mouse_button_down(mvMouseButton_Left):
            if get_active_window() != "Drawing Pad":
                break
            for i in range(len(joints)):
                if check(joints[i]['pos'], current_mouse_pos, joint_radius):
                    while not isMouseButtonLeftReleased():
                        time.sleep(0.01)
                        # 更新旋转后各个关节点的位置
                        joints = update_joints_pos(joints, i, angle)
                        # 更新纹理
                        update_texture(i, angle + joints[i]['angle'])
                        # 更新人体
                        update_body(joints, body_width, pad_name)
                        # 重绘关节点
                        redraw_joints(joints, pad_name)
                    # 保存旋转后的角度
                    joints = update_joints_angle(joints, i, angle)
                    angle = 0
