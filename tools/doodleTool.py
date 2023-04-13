from dearpygui.dearpygui import *
import time
from db_manage import *


def doodleTool(pad_name, lineColor, lineThickness):

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
        if is_mouse_button_down(mvMouseButton_Left):
        # if isMouseButtonLeftReleased():
            # If mouse is clicked outside the Drawing Pad, exit the tool.
            if get_active_window() != "Drawing Pad":
                break

            # Continue of clicked on the pad_name
            mouse_position = get_drawing_mouse_pos()
            
            time.sleep(0.01)

            doodleCoordinates = [mouse_position]

            while True:
                # Draw line
                doodleCoordinates.append(get_drawing_mouse_pos())
                draw_polyline(points=doodleCoordinates, color=lineColor, thickness=lineThickness, tag=f"doodle {tools.doodle_count}", parent=pad_name)

                time.sleep(0.01)

                # Check if user wants to exit the line tool
                if not is_mouse_button_down(mvMouseButton_Left):
                # if isMouseButtonLeftReleased():
                    write_db(tool="doodle tool", point_1=str(doodleCoordinates), color=str(lineColor), thickness=lineThickness, tag=f"doodle {tools.doodle_count}")
                    tools.doodle_count += 1
                    time.sleep(0.01)
                    break

                # # Check if user wants to exit the line tool
                # if isMouseButtonRightReleased():
                #     delete_item(f"doodle {tools.doodle_count}")
                #     break

                # # Check if user wants to exit the line tool
                # if is_key_down(mvKey_Escape):
                #     delete_item(f"doodle {tools.doodle_count}")
                #     break

                delete_item(f"doodle {tools.doodle_count}")
