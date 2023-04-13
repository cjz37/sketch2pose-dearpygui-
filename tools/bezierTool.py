from dearpygui.dearpygui import *
import time

from db_manage import *


def bezierTool(pad_name, lineColor, lineThickness):
    
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

    while True:
        temp_polyline_count = 0
        bezier_points = []
        flag = 0

        time.sleep(0.1)

        while True:

            if flag == 1:
                break

            if isMouseButtonLeftReleased():

                # If mouse is clicked outside the Drawing Pad, exit the tool.
                if get_active_window() != "Drawing Pad":
                    return

                # Continue of clicked on the drawing pad
                bezier_points.append(get_drawing_mouse_pos())
                mouse_position = get_drawing_mouse_pos()
                time.sleep(0.01)

                while True:

                    if flag == 1:
                        break

                    # Draw line
                    point2 = get_drawing_mouse_pos()
                    draw_line(
                        p1=mouse_position,
                        p2=point2,
                        color=lineColor,
                        thickness=1,
                        tag=f"temp_polyline {temp_polyline_count}",
                        parent=pad_name
                    )

                    time.sleep(0.01)

                    # Check if user wants to select more points for the polyline
                    if isMouseButtonLeftReleased():
                        # If the user clicks outside the drawing pad, it is assumed that they want to terminate the tool
                        if get_active_window() != "Drawing Pad":
                            for count in range(temp_polyline_count+1):
                                delete_item(f"temp_polyline {count}")
                            flag = 1
                            break

                        temp_polyline_count += 1
                        mouse_position = point2
                        bezier_points.append(point2)

                        if temp_polyline_count == 2:

                            flag = 1

                            if get_value("Close bezier curve") == True:
                                draw_bezier_cubic(
                                    p1=bezier_points[0], 
                                    p2=bezier_points[1], 
                                    p3=bezier_points[2],
                                    p4=bezier_points[0], 
                                    color=lineColor, 
                                    thickness=lineThickness,
                                    tag=f"bezier {tools.bezier_count}",
                                    parent=pad_name,
                                )

                                # Deleting reference poly-lines
                                delete_item(f"temp_polyline {temp_polyline_count}")
                                for count in range(temp_polyline_count):
                                    delete_item(f"temp_polyline {count}")

                                write_db(tool="bezier tool", point_1=str(bezier_points[0]), point_2=str(bezier_points[1]),
                                         point_3=str(bezier_points[2]), point_4=str(bezier_points[0]),
                                         color=str(lineColor), thickness=lineThickness,
                                         tag=f"bezier {tools.bezier_count}")

                                tools.bezier_count += 1

                                break

                            while True:
                                point4 = get_drawing_mouse_pos()

                                draw_line(
                                    p1=bezier_points[2],
                                    p2=get_drawing_mouse_pos(),
                                    color=lineColor,
                                    thickness=1,
                                    tag=f"temp_polyline {temp_polyline_count}",
                                    parent=pad_name
                                )
                                draw_bezier_cubic(
                                    p1=bezier_points[0],
                                    p2=bezier_points[1],
                                    p3=bezier_points[2],
                                    p4=point4,
                                    color=lineColor,
                                    thickness=lineThickness,
                                    tag=f"bezier {tools.bezier_count}",
                                    parent=pad_name,
                                )

                                time.sleep(0.02)

                                if isMouseButtonLeftReleased():
                                    # Deleting reference poly-lines
                                    delete_item(f"temp_polyline {temp_polyline_count}")
                                    for count in range(temp_polyline_count):
                                        delete_item(f"temp_polyline {count}")

                                    if get_active_window() != "Drawing Pad":
                                        delete_item(f"bezier {tools.bezier_count}")
                                        break

                                    write_db(tool="bezier tool", point_1=str(bezier_points[0]),
                                             point_2=str(bezier_points[1]),
                                             point_3=str(bezier_points[2]), point_4=str(point4),
                                             color=str(lineColor), thickness=lineThickness,
                                             tag=f"bezier {tools.bezier_count}")

                                    tools.bezier_count += 1
                                    time.sleep(0.01)
                                    break

                                # Check if user wants to exit the line tool
                                if isMouseButtonRightReleased():
                                    # Deleting reference poly-lines
                                    delete_item(f"temp_polyline {temp_polyline_count}")
                                    for count in range(temp_polyline_count):
                                        delete_item(f"temp_polyline {count}")

                                    delete_item(f"bezier {tools.bezier_count}")
                                    break

                                # Check if user wants to exit the line tool
                                if is_key_down(mvKey_Escape):
                                    # Deleting reference poly-lines
                                    delete_item(f"temp_polyline {temp_polyline_count}")
                                    for count in range(temp_polyline_count):
                                        delete_item(f"temp_polyline {count}")

                                    delete_item(f"bezier {tools.bezier_count}")
                                    break

                                # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                                delete_item(f"temp_polyline {temp_polyline_count}")
                                delete_item(f"bezier {tools.bezier_count}")

                        time.sleep(0.01)

                    # Check if user wants to exit the tool
                    if isMouseButtonRightReleased():
                        # Deleting reference poly-lines
                        for count in range(temp_polyline_count+1):
                            delete_item(f"temp_polyline {count}")

                        break

                    # Check if user wants to exit the line tool
                    if is_key_down(mvKey_Escape):
                        # Deleting reference poly-lines
                        for count in range(temp_polyline_count+1):
                            delete_item(f"temp_polyline {count}")

                        break

                    # Delete the line drawn and begin the process again till user clicks the second point or exits the tool
                    delete_item(f"temp_polyline {temp_polyline_count}")