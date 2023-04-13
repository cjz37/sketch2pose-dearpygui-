import time

from dearpygui.dearpygui import *

import threading
import webbrowser
import os

from ToolSpecTemplate import *
from GenerateSpecTemplate import *
import tools
from db_manage import *


def global_resize():
    cur_viewport_width = get_viewport_width()
    cur_viewport_height = get_viewport_height()

    set_item_height(
        item="Tools",
        height=cur_viewport_height - 315
    )

    set_item_pos(
        item="miscTools",
        pos=[0, cur_viewport_height - 290]
    )

    set_item_height(
        item="Tool Specifications",
        height=cur_viewport_height - 304
    )

    set_item_pos(
        item="Mouse Pad Coordinates",
        pos=[360, cur_viewport_height - 70]
    )

    set_item_width(
        item="Mouse Pad Coordinates",
        width=cur_viewport_width - 375
    )

    set_item_pos(
        item="mouse info",
        pos=[get_viewport_width() - 620, 3]
    )

    set_item_pos(
        item="Sys info",
        pos=[100, cur_viewport_height - 70]
    )

    set_item_width(
        item="Draw list",
        width=cur_viewport_width - 375
    )

    set_item_height(
        item="Draw list",
        height=cur_viewport_height - 86 - 32
    )


def open_website(sender, data):
    webbrowser.open(data)


def pad_mouse_coordinates():
    set_value("mouse info",
              f"Mouse coordinates: {get_drawing_mouse_pos()}")

    # Display cross cursor on pad
    delete_item("cursor circle")
    delete_item("cursor node")

    mouse_x = get_drawing_mouse_pos()[0]
    mouse_y = get_drawing_mouse_pos()[1]

    draw_circle(
        center=[mouse_x, mouse_y],
        radius=8,
        tag="cursor circle", 
        parent="Pad",
        color=[100, 100, 100],
        thickness=2,
    )
    draw_circle(
        center=[mouse_x, mouse_y],
        radius=2,
        tag="cursor node", 
        parent="Pad",
        color=[100, 100, 100],
        fill=[100, 100, 100],
        thickness=0,
    )


def apply_settings(sender, data):
    if data == "cancel tool":
        delete_item("Tool Specifications", children_only=True)
        add_text(
            default_value="Please select one of the tools from\nthe column on the left to continue\ndrawing.",
            parent="Tool Specifications"
        )

    if data == "straight line tool":
        tools.straightLineTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "polyline tool":
        tools.polylineTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "eraser tool":
        tools.doodleTool("Pad", [255., 255., 255., 255.], get_value("Thickness"))

    if data == "doodle tool":
        tools.doodleTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "curve tool":
        tools.curveTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "rectangle tool":
        if get_value("Fill rectangle"):
            if get_value("Fill with same color"):
                tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), get_value("Color"))
            else:
                tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), get_value("Fill Color"))
        else:
            tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), [0, 0, 0, 0])

    if data == "circle tool":
        if get_value("Fill Circle"):
            if get_value("Fill with same color"):
                tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Color"))
            else:
                tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Fill Color"))
        else:
            tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), [0, 0, 0, 0])

    if data == "bezier tool":
        tools.bezierTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == 'image tool':
        if get_value("##imagePath") != "Please select an image.":
            tools.imageTool("Pad", get_value("##imagePath"))
        else:
            pass

    if data == 'bbw tool':
        tools.bbwTool("Pad")

    if data == 'skeleton tool':
        tools.skeletonTool("Pad")

    if data == 'generate tool':
        if "Canvas" == get_value(item="Generation method"):
            print("generating from canvas ... ...")
            disable_item(item="Generate")
            set_item_label(item="Generate", label="Generating")
            tools.generateTool("temp/temp_file.png")
            enable_item(item="Generate")
            set_item_label(item="Generate", label="Generate")
        elif "Image" == get_value(item="Generation method"):
            temp_image_path = get_value("##imagePath")
            if temp_image_path != "Please select an image.":
                print("generating from image ... ...")
                disable_item(item="Generate")
                set_item_label(item="Generate", label="Generating")
                tools.generateTool(temp_image_path)
                enable_item(item="Generate")
                set_item_label(item="Generate", label="Generate")
            else:
                pass


def apply_settings_dispatcher(sender, app_data, user_data):
    settings_thread = threading.Thread(
        name="toolSettingsCallbackThread",
        target=apply_settings,
        args=(sender, user_data,),
        daemon=True,
    )
    settings_thread.start()


def tool_callbacks(caller_button):
    if "No##reset" == caller_button:
        configure_item("reset popup", show=False)

    elif "Yes##reset" == caller_button:
        configure_item("reset popup", show=False)
        delete_item("Tool Specifications", children_only=True)
        add_text(
            default_value="To get started, please select one of\nthe tools from the column on the\nleft.",
            parent="Tool Specifications",
        )
        tools.resetPad("Pad")

    elif "straight line tool" == caller_button:
        print("\nstraight line tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        straight_line_specifications = ToolSpec(
            title="        Straight Line Tool Properties", height=60)

        add_input_int(
            tag="Thickness",
            label="Thickness",
            default_value=2,
            min_value=1,
            width=145,
            parent="tool properties"
        )
        straight_line_specifications.add_space(height=2)
        straight_line_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                            "the first point. Then left click, right\n"
                                                            "click or hit escape key to end the line\n"
                                                            "tool.")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="straight line tool"))
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"))

        # Straight line main function call
        tools.straightLineTool("Pad", get_value(
            "Color"), get_value("Thickness"))

    elif "polyline tool" == caller_button:
        print("\npolyline tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        polyline_specifications = ToolSpec(
            title="            Polyline Tool Properties", height=100)

        add_input_int(
            tag="Thickness",
            label="Thickness",
            default_value=2,
            min_value=1,
            width=145,
            parent="tool properties"
        )
        polyline_specifications.add_space(height=2)
        polyline_specifications.add_separate()
        polyline_specifications.add_space(height=2)
        add_checkbox(
            tag="Close polyline",
            label="Close polyline",
            default_value=False,
            parent="tool properties"
        )

        polyline_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                       "the first point. Then left click to add\n"
                                                       "more points. Right click or hit the\n"
                                                       "escape key on the keyboard to end\n"
                                                       "the line tool.\n"
                                                       "\n"
                                                       "If you have selected \"Close polyline\",\n"
                                                       "then the polyline will close when the\n"
                                                       "tool is terminated")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="polyline tool"))
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"))

        # Polyline main function call
        tools.polylineTool("Pad", get_value("Color"), get_value("Thickness"))

    elif "curve tool" == caller_button:
        print("\ncurve tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        curve_specifications = ToolSpec(
            title="           Curve Tool Properties",
            height=60,
        )

        add_input_int(
            tag="Thickness",
            label="Thickness",
            default_value=2,
            min_value=1,
            min_clamped=True,
            max_value=20,
            max_clamped=True,
            width=145,
            parent="tool properties",
        )

        curve_specifications.add_space(height=2)

        curve_specifications.add_instructions(
            value="Left click on the drawing pad.\n")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="curve tool"),
        )
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )

        # Curve main function call
        tools.curveTool(
            pad_name="Pad",
            lineColor=get_value("Color"),
            lineThickness=get_value("Thickness")
        )

    elif "eraser tool" == caller_button:
        print("\neraser tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        eraser_specifications = ToolSpec(
            title="           Eraser Tool Properties",
            height=60,
        )

        add_input_int(
            tag="Thickness",
            label="Thickness",
            default_value=20,
            min_value=20,
            min_clamped=True,
            max_value=60,
            max_clamped=True,
            width=145,
            step=5,
            parent="tool properties",
        )

        eraser_specifications.add_space(height=2)

        eraser_specifications.add_instructions(
            value="Left click on the drawing pad to set\n"
                  "the first point. Then left click, to end\n"
                  "the tool. Right click or hit escape key\n"
                  "to undo the drawn line"
        )

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="eraser tool"),
        )

        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="eraser tool"),
        )

        tools.doodleTool(
            pad_name="Pad",
            lineColor=[255., 255., 255., 255.],
            lineThickness=get_value("Thickness"),
        )
        
    elif "doodle tool" == caller_button:
        print("\ndoodle tool\n-------")
        delete_item("Tool Specifications", children_only=True)
        
        doodle_specifications = ToolSpec(
            title="           Doodle Tool Properties",
            height=60,
        )

        add_input_int(
            tag="Thickness",
            label="Thickness",
            default_value=2,
            min_value=1,
            min_clamped=True,
            max_value=20,
            max_clamped=True,
            width=145,
            parent="tool properties",
        )

        doodle_specifications.add_space(height=2)

        doodle_specifications.add_instructions(
            value="Left click on the drawing pad to set\n"
                  "the first point. Then left click, to end\n"
                  "the tool. Right click or hit escape key\n"
                  "to undo the drawn line"
        )

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="doodle tool"),
        )
        
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )

        tools.doodleTool(
            pad_name="Pad",
            lineColor=get_value("Color"),
            lineThickness=get_value("Thickness"),
        )

    elif "skeleton tool" == caller_button:
        print("\nskeleton tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        skeleton_specifications = ToolSpec(
            title="            Skeleton Tool Properties",
            height=60,
        )

        skeleton_specifications.add_instructions(value="skeleton test")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="skeleton tool"),
        )
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )

        tools.skeletonTool(pad_name="Pad")

    elif "rectangle tool" == caller_button:
        print("\nrectangle tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        rectangle_specifications = ToolSpec(
            title="            Rectangle Tool Properties",
            height=175
        )

        add_input_float(
            tag="Thickness",
            label="Thickness",
            default_value=2,
            step=1,
            min_value=1,
            width=145,
            parent="tool properties"
        )
        rectangle_specifications.add_space(height=2)
        add_input_float(
            tag="Rounding",
            label="Rounding",
            default_value=0,
            step=1,
            min_value=0,
            width=145,
            parent="tool properties"
        )
        rectangle_specifications.add_space(height=2)
        rectangle_specifications.add_separate()
        rectangle_specifications.add_space(height=2)
        add_checkbox(
            tag="Fill rectangle",
            label="Fill rectangle",
            default_value=False,
            parent="tool properties",
            callback=tools.fillRectangleCheckbox
        )

        rectangle_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                        "the first point. Then left click to set\n"
                                                        "the second point. Right click or hit\n"
                                                        "escape key to end the tool")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="rectangle tool"))
        set_item_callback(
            "Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"))

        # Doodle main function call
        tools.rectangleTool("Pad", get_value("Color"), get_value(
            "Thickness"), get_value("Rounding"), [0, 0, 0, 0])

    elif "circle tool" == caller_button:
        print("\ncircle tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        circle_specifications = ToolSpec(
            title="            Circle Tool Properties", height=135)

        add_input_float(
            tag="Thickness",
            label="Thickness",
            default_value=2,
            step=1,
            min_value=1,
            width=145,
            parent="tool properties"
        )
        circle_specifications.add_space(height=2)
        circle_specifications.add_separate()
        circle_specifications.add_space(height=1)
        add_checkbox(
            tag="Fill Circle",
            label="Fill Circle",
            default_value=False,
            parent="tool properties",
            callback=tools.fillCircleCheckbox
        )

        circle_specifications.add_instructions(value="Left click on the drawing pad to set\n"
                                                     "the centre point. Then left click to set\n"
                                                     "the radius. Right click or hit\n"
                                                     "escape key to end the tool")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="circle tool"))
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"))

        # Circle main function call
        tools.circleTool("Pad", get_value("Color"),
                         get_value("Thickness"), [0, 0, 0, 0])

    elif "bezier tool" == caller_button:
        print("\nbezier tool\n-------")
        delete_item("Tool Specifications", children_only=True)
        bezier_specifications = ToolSpec(
            title="           Bezier Tool Properties",
            height=100,
        )
        add_input_int(
            tag="Thickness", 
            label="Thickness", 
            default_value=2, 
            min_value=1,
            min_clamped=True,
            max_value=20,
            max_clamped=True,
            width=145, 
            parent="tool properties",
        )
        bezier_specifications.add_space(height=2)
        bezier_specifications.add_separate()
        bezier_specifications.add_space(height=2)
        add_checkbox(
            tag="Close bezier curve",
            label="Close bezier curve",
            default_value=False,
            parent="tool properties",
        )
        bezier_specifications.add_instructions(
            value="Left click on the drawing pad to set\n"
                  "the first point. Then left click to\n"
                  "add three more points. Right click \n"
                  "or hit the escape key on the key-\n"
                  "board to end the tool.\n\n"
                  "If you have selected the \"Close \n"
                  "bezier curve\" then the bezier \n"
                  "curve will close when the third \n"
                  "point is selected")
        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="bezier tool"),
        )
        set_item_callback(
            item="Cancel", 
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )
        # Bezier main function call
        tools.bezierTool(
            pad_name="Pad", 
            lineColor=get_value("Color"), 
            lineThickness=get_value("Thickness")
        )

    elif "image tool" == caller_button:
        print("\nimage tool\n-------")
        delete_item("Tool Specifications", children_only=True)
        
        image_specifications = ToolSpec(
            title="           Image Tool Properties",
            height=115
        )

        add_button(
            tag="Search image",
            label="Search image",
            width=225,
            height=30,
            parent="tool properties",
            callback=tools.searchImage,
        )
        image_specifications.add_space(height=2)
        
        add_input_text(
            tag="##imagePath",
            label="##imagePath",
            multiline=True,
            readonly=True,
            parent="tool properties",
            width=225,
            height=42,
        )

        set_value("##imagePath", "Please select an image.")

        image_specifications.add_instructions(value="Select an image by clicking on the\n"
                                                    "\"Search image\" button and then \n"
                                                    "click apply. Left click on the \n"
                                                    "drawing pad to select the first \n"
                                                    "point and then left click again \n"
                                                    "to place the image.\n"
                                                    ""
                                                    "Hold down shift while placing the\n"
                                                    "image to fix the aspect ratio of \n"
                                                    "the image.")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="image tool"),
        )
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )

    elif "bbw tool" == caller_button:
        print("\nbbw tool\n-------")

        delete_item("Tool Specifications", children_only=True)
        bbw_specifications = ToolSpec(
            title="           BBW Tool Properties",
            height=60
        )

        bbw_specifications.add_instructions(value="bbw test")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="bbw tool"),
        )
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )

        tools.bbwTool(pad_name="Pad")
    
    elif "generate tool" == caller_button:
        print("\ngenerate tool\n-------")

        delete_item("Tool Specifications", children_only=True)
        generate_specifications = GenerateSpec(
            title="         Generate Tool Properties",
            height=64,
        )
        
        with group(horizontal=True, parent="tool properties"):
            add_spacer(width=10)

            add_radio_button(
                items=["Image", "Canvas"],
                tag="Generation method",
                label="Generation method",
                horizontal=True,
                default_value="Canvas",
                callback=generate_method,
            )

        generate_specifications.add_space(height=2)

        add_button(
            tag="Search image",
            label="Search image",
            width=225,
            height=30,
            parent="tool properties",
            callback=tools.searchImage,
            show=False,
        )

        generate_specifications.add_space(height=2)
        
        add_input_text(
            tag="##imagePath",
            label="##imagePath",
            multiline=True,
            readonly=True,
            parent="tool properties",
            width=225,
            height=40,
            show=False,
        )

        set_value("##imagePath", "Please select an image.")

        generate_specifications.add_instructions(value="\tSelect a way to generate.")

        set_item_callback(
            item="Generate",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="generate tool"),
        )
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )

    elif "open model editor tool" == caller_button:
        print("\nopen model editor\n-------")
        os.system('runModelEditor.bat')


def tool_callback_dispatcher(sender):
    tool_thread = threading.Thread(
        name="toolCallbackThread",
        target=tool_callbacks,
        args=(sender,),
        daemon=True,
    )
    tool_thread.start()


def theme_switcher(sender, app_data, user_data):
    if "light" == user_data:
        set_item_label(sender, label="Dark")
        set_item_user_data(sender, user_data="dark")
    else:
        set_item_label(sender, label="Light")
        set_item_user_data(sender, user_data="light")


def generate_method(sender, app_data):
    if "Image" == app_data:
        show_item(item="Search image")
        show_item(item="##imagePath")
        set_item_height(item="tool properties", height=155)
    elif "Canvas" == app_data:
        hide_item(item="Search image")
        hide_item(item="##imagePath")
        set_item_height(item="tool properties", height=64)


create_db()
create_context()

# 字体设置
with font_registry():
    default_font = add_font("fonts/OpenSans-Regular.ttf", 19)
    bigger_font = add_font("fonts/OpenSans-Regular.ttf", 19)

bind_font(default_font)

# 主题设置
with theme(tag="global theme"):
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_ItemSpacing, 10.00, 5.00, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_WindowTitleAlign, 0.50, 0.50, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_FrameBorderSize, 1.0)
        add_theme_style(mvStyleVar_WindowPadding, 20, 5, category=mvThemeCat_Core)

        add_theme_color(mvThemeCol_MenuBarBg, [36, 36, 36], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_WindowBg, [36, 36, 36], category=mvThemeCat_Core)
    
bind_theme("global theme")

with theme(tag="tools theme"):
    with theme_component(mvAll):
        add_theme_color(mvThemeCol_WindowBg, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBg, [50, 50, 50], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBgActive, [50, 50, 50], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_Button, [65, 65, 65], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonHovered, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonActive, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ScrollbarBg, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ScrollbarGrab, [100, 100, 100], category=mvThemeCat_Core)

with theme(tag="miscTools theme"):
    with theme_component(mvAll):
        add_theme_color(mvThemeCol_WindowBg, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBg, [50, 50, 50], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBgActive, [50, 50, 50], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_Button, [65, 65, 65], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonHovered, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonActive, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ScrollbarBg, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ScrollbarGrab, [100, 100, 100], category=mvThemeCat_Core)

with theme(tag="foot bar theme"):
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_WindowPadding, 20, 3, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_WindowBorderSize, 0, category=mvThemeCat_Core)

        add_theme_color(mvThemeCol_WindowBg, [36, 36, 36], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_Text, [160, 160, 160], category=mvThemeCat_Core)

with theme(tag="drawingPad theme"):
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_WindowPadding, 0, 0, category=mvThemeCat_Core)

        add_theme_color(mvThemeCol_WindowBg, [255, 255, 255], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBg, [95, 95, 95], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBgActive, [95, 95, 95], category=mvThemeCat_Core)

with theme(tag="popup theme"):
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_FrameBorderSize, 1.0, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_WindowRounding, 8, category=mvThemeCat_Core)

with theme(tag="toolSpecifications theme"):
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_ItemInnerSpacing, 5, 0, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_FrameRounding, 2.0, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_ChildBorderSize, 1, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_ChildRounding, 5, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_WindowPadding, 8, 8, category=mvThemeCat_Core)

        add_theme_color(mvThemeCol_WindowBg, [70, 70, 70], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBg, [70, 70, 70], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBgActive, [70, 70, 70], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_Button, [80, 80, 80], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonHovered, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonActive, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_FrameBg, [60, 60, 60], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_FrameBgHovered, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_FrameBgActive, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ChildBg, [80, 80, 80], category=mvThemeCat_Core)

with theme(tag="colorSelector theme"):
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_FramePadding, 4, 2, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_ItemInnerSpacing, 2, 4, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_ScrollbarSize, 10, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_WindowPadding, 10, 5, category=mvThemeCat_Core)

        add_theme_color(mvThemeCol_WindowBg, [70, 70, 70], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBg, [70, 70, 70], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_TitleBgActive, [70, 70, 70], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_Button, [80, 80, 80], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonHovered, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ButtonActive, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_FrameBg, [60, 60, 60], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_FrameBgHovered, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_FrameBgActive, [40, 40, 40], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_ChildBg, [80, 80, 80], category=mvThemeCat_Core)

# 纹理加载
data = list()
# light icons
data.append(load_image("icons/dark-straight-line-tool.png"))  # 0
data.append(load_image("icons/dark-dashed-line-tool.png"))
data.append(load_image("icons/dark-polyline-tool.png"))
data.append(load_image("icons/dark-doodle-tool.png"))
data.append(load_image("icons/dark-rectangle-tool.png"))  # 4
data.append(load_image("icons/dark-circle-tool.png"))
data.append(load_image("icons/dark-arrow-tool.png"))
data.append(load_image("icons/dark-bezier-tool.png"))
data.append(load_image("icons/dark-text-tool.png"))  # 8
data.append(load_image("icons/dark-image-tool.png"))
data.append(load_image("icons/canvas-color-tool.png"))
data.append(load_image("icons/dark-generate-tool.png"))
data.append(load_image("icons/dark-reset-tool.png"))  # 12
data.append(load_image("icons/open-model-editor-tool.png"))
data.append(load_image("icons/dark-curve-tool.png"))
data.append(load_image("icons/colorPickup-tool.png"))
data.append(load_image("icons/bbw-tool.png"))  # 16
data.append(load_image("data/images/smpl.png"))
data.append(load_image("icons/eraser-tool.png"))
data.append(load_image("icons/skeleton-tool.png"))
data.append(load_image("data/body/big-arm-left.png"))   # 20
data.append(load_image("data/body/big-arm-right.png"))
data.append(load_image("data/body/calf-left.png"))
data.append(load_image("data/body/calf-right.png"))
data.append(load_image("data/body/foot-left.png"))   # 24
data.append(load_image("data/body/foot-right.png"))
data.append(load_image("data/body/forearm-left.png"))
data.append(load_image("data/body/forearm-right.png"))
data.append(load_image("data/body/head.png"))   # 28
data.append(load_image("data/body/hip.png"))
data.append(load_image("data/body/palm-left.png"))
data.append(load_image("data/body/palm-right.png"))
data.append(load_image("data/body/thigh-left.png"))   # 32
data.append(load_image("data/body/thigh-right.png"))
data.append(load_image("data/body/upper-body.png"))

# dark icons
# data.append(load_image("icons/dark-arrow-tool.png")[3])
# data.append(load_image("icons/dark-bezier-tool.png")[3])
# data.append(load_image("icons/dark-circle-tool.png")[3])
# data.append(load_image("icons/dark-dashed-line-tool.png")[3])
# data.append(load_image("icons/dark-doodle-tool.png")[3])
# data.append(load_image("icons/dark-mode.png")[3])
# data.append(load_image("icons/dark-polyline-tool.png")[3])
# data.append(load_image("icons/dark-rectangle-tool.png")[3])
# data.append(load_image("icons/dark-reset-tool.png")[3])
# data.append(load_image("icons/dark-straight-line-tool.png")[3])
# data.append(load_image("icons/dark-text-tool.png")[3])
# data.append(load_image("icons/light-mode.png")[3])
# data.append(load_image("icons/reset-tool.png")[3])
with texture_registry(show=False, tag="global texture"):
    add_static_texture(width=data[0][0], height=data[0][1], default_value=data[0][3], tag="straight line tool texture")
    add_static_texture(width=data[1][0], height=data[1][1], default_value=data[1][3], tag="dashed line tool texture")
    add_static_texture(width=data[2][0], height=data[2][1], default_value=data[2][3], tag="polyline tool texture")
    add_static_texture(width=data[3][0], height=data[3][1], default_value=data[3][3], tag="doodle tool texture")
    add_static_texture(width=data[4][0], height=data[4][1], default_value=data[4][3], tag="rectangle tool texture")
    add_static_texture(width=data[5][0], height=data[5][1], default_value=data[5][3], tag="circle tool texture")
    add_static_texture(width=data[6][0], height=data[6][1], default_value=data[6][3], tag="arrow tool texture")
    add_static_texture(width=data[7][0], height=data[7][1], default_value=data[7][3], tag="bezier tool texture")
    add_static_texture(width=data[8][0], height=data[8][1], default_value=data[8][3], tag="text tool texture")
    add_static_texture(width=data[9][0], height=data[9][1], default_value=data[9][3], tag="image tool texture")
    add_static_texture(width=data[10][0], height=data[10][1], default_value=data[10][3], tag="canvas color tool texture")
    add_static_texture(width=data[11][0], height=data[11][1], default_value=data[11][3], tag="generate tool texture")
    add_static_texture(width=data[12][0], height=data[12][1], default_value=data[12][3], tag="reset tool texture")
    add_static_texture(width=data[13][0], height=data[13][1], default_value=data[13][3], tag="open model editor tool texture")
    add_static_texture(width=data[14][0], height=data[14][1], default_value=data[14][3], tag="curve tool texture")
    add_static_texture(width=data[15][0], height=data[15][1], default_value=data[15][3], tag="color pickup tool texture")
    add_static_texture(width=data[16][0], height=data[16][1], default_value=data[16][3], tag="bbw tool texture")
    add_static_texture(width=data[17][0], height=data[17][1], default_value=data[17][3], tag="bbw template texture")
    add_static_texture(width=data[18][0], height=data[18][1], default_value=data[18][3], tag="eraser tool texture")
    add_static_texture(width=data[19][0], height=data[19][1], default_value=data[19][3], tag="skeleton tool texture")
    add_static_texture(width=data[20][0], height=data[20][1], default_value=data[20][3], tag="big arm left")
    add_static_texture(width=data[21][0], height=data[21][1], default_value=data[21][3], tag="big arm right")
    add_static_texture(width=data[22][0], height=data[22][1], default_value=data[22][3], tag="calf left")
    add_static_texture(width=data[23][0], height=data[23][1], default_value=data[23][3], tag="calf right")
    add_static_texture(width=data[24][0], height=data[24][1], default_value=data[24][3], tag="foot left")
    add_static_texture(width=data[25][0], height=data[25][1], default_value=data[25][3], tag="foot right")
    add_static_texture(width=data[26][0], height=data[26][1], default_value=data[26][3], tag="forearm left")
    add_static_texture(width=data[27][0], height=data[27][1], default_value=data[27][3], tag="forearm right")
    add_static_texture(width=data[28][0], height=data[28][1], default_value=data[28][3], tag="head")
    add_static_texture(width=data[29][0], height=data[29][1], default_value=data[29][3], tag="hip")
    add_static_texture(width=data[30][0], height=data[30][1], default_value=data[30][3], tag="palm left")
    add_static_texture(width=data[31][0], height=data[31][1], default_value=data[31][3], tag="palm right")
    add_static_texture(width=data[32][0], height=data[32][1], default_value=data[32][3], tag="thigh left")
    add_static_texture(width=data[33][0], height=data[33][1], default_value=data[33][3], tag="thigh right")
    add_static_texture(width=data[34][0], height=data[34][1], default_value=data[34][3], tag="upper bofy")


with handler_registry(show=True, tag="global handler"):
    add_mouse_move_handler(callback=pad_mouse_coordinates)
    add_key_down_handler(callback=tools.hotkeyCommands)
    
with handler_registry(show=True, tag="mouse handler"):
    add_mouse_release_handler(button=mvMouseButton_Left, tag="ml_release")
    add_mouse_release_handler(button=mvMouseButton_Right, tag="mr_release")


create_viewport(
    title="Sketch2Pose",
    width=1600,
    height=870,
    min_width=1000,
    min_height=600,
    small_icon="icons/sp.ico",
    large_icon="icons/sp.ico",
    resizable=True,
)

set_viewport_resize_callback(callback=global_resize)

# Main window menu
with viewport_menu_bar(tag="menu bar"):
    with menu(label="File", tag="menu file"):
        add_menu_item(
            label="Open drawing", 
            callback=tools.openTool,
            shortcut='Ctrl + O',
        )
        add_menu_item(
            label="Save drawing", 
            callback=tools.saveTool,
            shortcut='Ctrl + S',
        )
        add_menu_item(
            label="Exit", 
            callback=lambda: stop_dearpygui()
        )

    with menu(label="Edit", tag="menu edit"):
        add_menu_item(
            label="Undo",
            callback=lambda: read_db(action="undo"),
            shortcut='Ctrl + Z',
        )
        add_menu_item(
            label="Redo",
            callback=lambda: read_db(action="redo"),
            shortcut='Ctrl + Shift + Z',
        )

    with menu(label="Tools", tag="menu tools"):
        add_menu_item(
            label="Doodle tool",
            callback=lambda: tool_callback_dispatcher(sender="doodle tool")
        )
        add_menu_item(
            label="Straight line tool", 
            callback=lambda: tool_callback_dispatcher(sender="straight line tool")
        )
        add_menu_item(
            label="Polyline tool", 
            callback=lambda: tool_callback_dispatcher(sender="polyline tool")
        )
        add_menu_item(
            label="Curve tool",
            callback=lambda: tool_callback_dispatcher(sender="curve tool")
        )
        add_menu_item(
            label="Rectangle tool", 
            callback=lambda: tool_callback_dispatcher(sender="rectangle tool")
        )
        add_menu_item(
            label="Circle tool", 
            callback=lambda: tool_callback_dispatcher(sender="circle tool")
        )
        add_menu_item(
            label="Bezier tool", 
            callback=lambda: tool_callback_dispatcher(sender="bezier tool")
        )
        add_menu_item(
            label="Image tool", 
            callback=lambda: tool_callback_dispatcher(sender="image tool")
        )
    
    with menu(label="Theme", tag="menu theme"):
        add_menu_item(
            label="Dark",
            user_data="dark",
            callback=theme_switcher,
        )

    with menu(label="Help", tag="menu help"):
        add_menu_item(
            label="Github",
            callback=lambda: open_website(sender=None, data="https://github.com/cjz37/sketch2pose-dearpygui"),
        )

# Tools bar
img_size = 45
img_padding = 5
with window(
    tag="Tools",
    label="Tools",
    no_collapse=True,
    no_resize=True,
    no_move=True,
    no_close=True,
    pos=[0, 25],
    width=80,
    height=get_viewport_height() - 315,
    no_title_bar=True,
):
    add_image_button(
        tag="doodle tool",
        texture_tag="doodle tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher,
    )
    add_spacer()
    add_image_button(
        tag="eraser tool",
        texture_tag="eraser tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher,
    )
    add_spacer()
    add_image_button(
        tag="skeleton tool",
        texture_tag="skeleton tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher,
    )
    add_spacer()
    add_image_button(
        tag="straight line tool",
        texture_tag="straight line tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher,
    )
    add_spacer()
    add_image_button(
        tag="polyline tool",
        texture_tag="polyline tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )
    add_spacer()
    add_image_button(
        tag="curve tool",
        texture_tag="curve tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher,
    )
    add_spacer()
    add_image_button(
        tag="rectangle tool",
        texture_tag="rectangle tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )
    add_spacer()
    add_image_button(
        tag="circle tool",
        texture_tag="circle tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )
    add_spacer()
    add_image_button(
        tag="bezier tool",
        texture_tag="bezier tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )
    add_spacer()
    add_image_button(
        tag="image tool",
        texture_tag="image tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )
    add_spacer()
    add_image_button(
        tag="bbw tool",
        texture_tag="bbw tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )
    add_spacer()
    add_image_button(
        tag="color pickup tool",
        texture_tag="color pickup tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )

bind_item_theme("Tools", "tools theme")

# misc tools bar
with window(
    tag="miscTools",
    label="miscTools",
    no_collapse=True,
    no_resize=True,
    no_move=True,
    no_close=True,
    pos=[0, get_viewport_height() - 290],
    width=80,
    height=260,
    no_title_bar=True,
):
    add_image_button(
        tag="generate tool",
        texture_tag="generate tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )
    add_spacer()
    add_image_button(
        tag="reset tool",
        texture_tag="reset tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
    )
    add_spacer()
    add_image_button(
        tag="open model editor tool",
        texture_tag="open model editor tool texture",
        width=img_size,
        height=img_size,
        frame_padding=img_padding,
        callback=tool_callback_dispatcher
    )

bind_item_theme("miscTools", "miscTools theme")

with popup(
    tag="reset popup",
    parent="reset tool",
    modal=True,
    mousebutton=mvMouseButton_Left,
):
    add_text("Are you sure you want to erase the drawing pad?", indent=0)
    add_spacer()
    with group(horizontal=True):
        add_button(
            tag="Yes##reset",
            label="Yes##reset", 
            width=150, 
            height=25, 
            callback=tool_callback_dispatcher,
        )
        add_spacer(width=8)
        add_button(
            tag="No##reset",
            label="No##reset",
            width=150,
            height=25,
            callback=tool_callback_dispatcher,
        )

bind_item_theme("reset popup", "popup theme")

# Color Selector
with window(
    tag="Color Selector",
    label="Color Selector",
    no_collapse=True,
    no_resize=True,
    no_move=True,
    no_close=True,
    width=260,
    height=210,
    pos=[100, 25],
):
    add_color_picker(
        tag="Color",
        alpha_bar=True,
        picker_mode=mvColorPicker_wheel,
        display_rgb=True,
        display_hex=True,
        default_value=[30, 30, 30, 255],
    )

bind_item_theme("Color Selector", "colorSelector theme")

# Tool Specifications
with window(
    tag="Tool Specifications",
    label="Tool Specifications",
    no_collapse=True,
    no_resize=True,
    no_scrollbar=True,
    no_move=True,
    no_close=True,
    width=260,
    height=get_viewport_height() - 304,
    pos=[100, 235],
):
    add_text(default_value="To get started, please select one of\nthe tools from the column on the\nleft.")

bind_item_theme("Tool Specifications", "toolSpecifications theme")

# Drawing Pad
with window(
    tag="Drawing Pad",
    label="Drawing Pad",
    autosize=True,
    no_collapse=True,
    no_move=True,
    no_close=True,
    pos=[360, 25],
):
    add_drawlist(tag="Draw list", width=get_viewport_width() - 375, height=get_viewport_height() - 118)
    add_draw_layer(tag="Pad", parent="Draw list")

bind_item_theme("Drawing Pad", "drawingPad theme")

with window(
    tag="Mouse Pad Coordinates",
    label="Mouse Pad Coordinates",
    no_collapse=True,
    no_move=True,
    no_close=True,
    no_resize=True,
    no_title_bar=True,
    width=get_viewport_width() - 375,
    height=40,
    pos=[360, get_viewport_height() - 70],
):
    add_text(tag="mouse info", default_value="Mouse coordinates:", pos=[get_viewport_width() - 620, 3])
    
bind_item_theme("Mouse Pad Coordinates", "foot bar theme")

with window(
    tag="Sys info",
    label="Sys info",
    no_collapse=True,
    no_move=True,
    no_close=True,
    no_resize=True,
    no_title_bar=True,
    width=260,
    height=40,
    pos=[100, get_viewport_height() - 70],
):
    add_text(tag="development info", default_value="Power by Dearpygui", pos=[70, 3])

bind_item_theme("Sys info", "foot bar theme")

setup_dearpygui()
show_viewport()
start_dearpygui()
destroy_context()
 