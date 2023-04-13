from dearpygui.dearpygui import *
import math
import time

from db_manage import *


def circleTool(pad_name, lineColor, lineThickness, fillCircle):
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

    time.sleep(0.1)

    while True:
        # Begin drawing when left mouse button is released
        if isMouseButtonLeftReleased():

            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                break

            # Continue of clicked on the drawing pad
            mouse_position = get_drawing_mouse_pos()
            time.sleep(0.01)

            while True:
                # Draw line
                radius = math.sqrt(math.pow(mouse_position[0] - get_drawing_mouse_pos()[0], 2) + math.pow(mouse_position[1] - get_drawing_mouse_pos()[1], 2))
                draw_circle(
                    parent=pad_name,
                    center=mouse_position,
                    radius=radius,
                    color=lineColor,
                    thickness=lineThickness,
                    fill=fillCircle,
                    tag=f"circle {tools.circle_count}"
                )
                time.sleep(0.01)

                # Check if user wants to select the second point
                if isMouseButtonLeftReleased():
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        # delete_draw_command(pad_name, f"circle {tools.circle_count}")
                        delete_item(f"circle {tools.circle_count}")
                        break

                    write_db(tool="circle tool", point_1=str(mouse_position), point_2=str(radius),
                             color=str(lineColor), thickness=lineThickness, fill=str(fillCircle),
                             tag=f"circle {tools.circle_count}")

                    tools.circle_count += 1
                    time.sleep(0.01)
                    break

                # Check if user wants to exit the line tool
                if isMouseButtonRightReleased():
                    # delete_draw_command(pad_name, f"circle {tools.circle_count}")
                    delete_item(f"circle {tools.circle_count}")
                    break

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    # delete_draw_command(pad_name, f"circle {tools.circle_count}")
                    delete_item(f"circle {tools.circle_count}")
                    break

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                # delete_draw_command(pad_name, f"circle {tools.circle_count}")
                delete_item(f"circle {tools.circle_count}")

def fillCircleCheckbox():
    if get_value("Fill Circle"):
        set_item_height("tool properties", height=215)
        add_spacer(height=2, parent="tool properties", tag="tempSpace1")
        add_checkbox(
            tag="Fill with same color",
            label="Fill with same color",
            default_value=False,
            parent="tool properties",
            callback=fillSameCircleCheckbox
        )
        add_spacer(height=2, parent="tool properties", tag="tempSpace2")
        # add_color_edit4("Fill color", default_value=[0, 255, 255, 255], parent="tool properties", width=155)
        add_color_picker(
            tag="Fill Color",
            alpha_bar=True,
            picker_mode=mvColorPicker_wheel,
            display_rgb=True,
            display_hex=True,
            default_value=[0, 255, 255, 255],
            parent="tool properties",
            width=155,
        )

    else:
        delete_item("Fill with same color")
        delete_item("tempSpace1")
        delete_item("tempSpace2")
        delete_item("Fill Color")
        set_item_height("tool properties", height=135)

def fillSameCircleCheckbox():
    if get_value("Fill with same color"):
        delete_item("tempSpace2")
        delete_item("Fill Color")
        set_item_height("tool properties", height=175)

    else:
        set_item_height("tool properties", height=215)
        add_spacer(height=2, parent="tool properties", tag="tempSpace2")
        # add_color_edit4("Fill color", default_value=[0, 255, 255, 255], parent="tool properties", width=155)
        add_color_picker(
            tag="Fill Color",
            alpha_bar=True,
            picker_mode=mvColorPicker_wheel,
            display_rgb=True,
            display_hex=True,
            default_value=[0, 255, 255, 255],
            parent="tool properties",
            width=155,
        )