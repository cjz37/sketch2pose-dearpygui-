from dearpygui.dearpygui import *
import time
from db_manage import *


def doodleTool(pad_name, lineColor, lineThickness):

    time.sleep(0.1)

    while True:
        if is_mouse_button_down(mvMouseButton_Left):
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
                draw_polyline(
                    points=doodleCoordinates,
                    color=lineColor,
                    thickness=lineThickness,
                    tag=f"doodle {tools.doodle_count}",
                    parent=pad_name
                )

                time.sleep(0.01)

                # Check if user wants to exit the line tool
                if not is_mouse_button_down(mvMouseButton_Left):
                    write_db(
                        tool="doodle tool",
                        point_1=str(doodleCoordinates),
                        color=str(lineColor),
                        thickness=lineThickness,
                        tag=f"doodle {tools.doodle_count}"
                    )
                    tools.doodle_count += 1
                    time.sleep(0.01)
                    break

                delete_item(f"doodle {tools.doodle_count}")
