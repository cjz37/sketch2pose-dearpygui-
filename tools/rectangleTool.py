from dearpygui.dearpygui import *
import time
from db_manage import *


def rectangleTool(pad_name, lineColor, lineThickness, edgeRounding, fillRectangle):
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
                # Checking quadrants because of imgui bug
                # Check if user wants to constraint rectangle to square
                if is_key_down(mvKey_Shift):
                    if get_drawing_mouse_pos()[0] < mouse_position[0]:
                        # Check if in second quadrant
                        if get_drawing_mouse_pos()[1] < mouse_position[1]:
                            first_point = [mouse_position[0] - (mouse_position[1] - get_drawing_mouse_pos()[1]), get_drawing_mouse_pos()[1]]
                            second_point = mouse_position
                            draw_rectangle(
                                pmin=first_point,
                                pmax=second_point,
                                color=lineColor,
                                thickness=lineThickness,
                                rounding=edgeRounding,
                                fill=fillRectangle,
                                tag=f"rectangle {tools.rectangle_count}",
                                parent=pad_name,
                            )
                        # Check if in third quadrant
                        else:
                            first_point = [mouse_position[0] - (get_drawing_mouse_pos()[1] - mouse_position[1]), mouse_position[1]]
                            second_point = [mouse_position[0], get_drawing_mouse_pos()[1]]
                            draw_rectangle(
                                pmin=first_point,
                                pmax=second_point,
                                color=lineColor,
                                thickness=lineThickness,
                                rounding=edgeRounding,
                                fill=fillRectangle,
                                tag=f"rectangle {tools.rectangle_count}",
                                parent=pad_name,
                            )
                    # Check if in first quadrant
                    elif get_drawing_mouse_pos()[1] < mouse_position[1]:
                        first_point = [mouse_position[0], get_drawing_mouse_pos()[1]]
                        second_point = [mouse_position[0] + (mouse_position[1] - get_drawing_mouse_pos()[1]), mouse_position[1]]
                        draw_rectangle(
                            pmin=first_point,
                            pmax=second_point,
                            color=lineColor,
                            thickness=lineThickness,
                            rounding=edgeRounding,
                            fill=fillRectangle,
                            tag=f"rectangle {tools.rectangle_count}",
                            parent=pad_name,
                        )
                    # Check if in fourth quadrant
                    else:
                        first_point = mouse_position
                        second_point = [mouse_position[0] + (get_drawing_mouse_pos()[1] - mouse_position[1]), get_drawing_mouse_pos()[1]]
                        draw_rectangle(
                            pmin=mouse_position,
                            pmax=second_point,
                            color=lineColor,
                            thickness=lineThickness,
                            rounding=edgeRounding,
                            fill=fillRectangle,
                            tag=f"rectangle {tools.rectangle_count}",
                            parent=pad_name,
                        )

                # For creating rectangles
                else:
                    if get_drawing_mouse_pos()[0] < mouse_position[0]:
                        # Check if in second quadrant
                        if get_drawing_mouse_pos()[1] < mouse_position[1]:
                            first_point = get_drawing_mouse_pos()
                            second_point = mouse_position
                            draw_rectangle(
                                pmin=first_point,
                                pmax=second_point,
                                color=lineColor,
                                thickness=lineThickness,
                                rounding=edgeRounding,
                                fill=fillRectangle,
                                tag=f"rectangle {tools.rectangle_count}",
                                parent=pad_name,
                            )
                        # Check if in third quadrant
                        else:
                            first_point = [get_drawing_mouse_pos()[0], mouse_position[1]]
                            second_point = [mouse_position[0], get_drawing_mouse_pos()[1]]
                            draw_rectangle(
                                pmin=first_point,
                                pmax=second_point,
                                color=lineColor,
                                thickness=lineThickness,
                                rounding=edgeRounding,
                                fill=fillRectangle,
                                tag=f"rectangle {tools.rectangle_count}",
                                parent=pad_name,
                            )
                    # Check if in first quadrant
                    elif get_drawing_mouse_pos()[1] < mouse_position[1]:
                        first_point = [mouse_position[0], get_drawing_mouse_pos()[1]]
                        second_point = [get_drawing_mouse_pos()[0], mouse_position[1]]
                        draw_rectangle(
                            pmin=first_point,
                            pmax=second_point,
                            color=lineColor,
                            thickness=lineThickness,
                            rounding=edgeRounding,
                            fill=fillRectangle,
                            tag=f"rectangle {tools.rectangle_count}",
                            parent=pad_name,
                        )
                    # Check if in fourth quadrant
                    else:
                        first_point = mouse_position
                        second_point = get_drawing_mouse_pos()
                        draw_rectangle(
                            pmin=first_point,
                            pmax=second_point,
                            color=lineColor,
                            thickness=lineThickness,
                            rounding=edgeRounding,
                            fill=fillRectangle,
                            tag=f"rectangle {tools.rectangle_count}",
                            parent=pad_name,
                        )
                time.sleep(0.01)

                # Check if user wants to select the second point of the line
                if isMouseButtonLeftReleased():
                    # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                    if get_active_window() != "Drawing Pad":
                        delete_item(f"rectangle {tools.rectangle_count}")
                        break

                    write_db(tool="rectangle tool", point_1=str(first_point), point_2=str(second_point),
                             color=str(lineColor), thickness=lineThickness, rounding=edgeRounding, fill=str(fillRectangle),
                             tag=f"rectangle {tools.rectangle_count}")

                    tools.rectangle_count += 1
                    time.sleep(0.01)
                    break

                # Check if user wants to exit the line tool
                if isMouseButtonRightReleased():
                    delete_item(f"rectangle {tools.rectangle_count}")
                    break

                # Check if user wants to exit the line tool
                if is_key_released(mvKey_Escape):
                    delete_item(f"rectangle {tools.rectangle_count}")
                    break

                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                delete_item(f"rectangle {tools.rectangle_count}")


def fillRectangleCheckbox():
    if get_value("Fill rectangle"):
        set_item_height("tool properties", height=255)
        add_spacer(height=2, parent="tool properties", tag="tempSpace1")
        add_checkbox(
            tag="Fill with same color",
            label="Fill with same color",
            default_value=False,
            parent="tool properties",
            callback=fillRectangleSameCheckbox
        )
        add_spacer(height=2, parent="tool properties", tag="tempSpace2")
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
        set_item_height("tool properties", height=175)


def fillRectangleSameCheckbox():
    if get_value("Fill with same color"):
        delete_item("tempSpace2")
        delete_item("Fill Color")
        set_item_height("tool properties", height=215)

    else:
        set_item_height("tool properties", height=255)
        add_spacer(height=2, parent="tool properties", tag="tempSpace2")
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
