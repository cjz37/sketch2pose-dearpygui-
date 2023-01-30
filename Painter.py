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
        pos=[cur_viewport_width - 590, 3]
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
    # delete_item("cursorX")
    # delete_item("cursorY")
    delete_item("cursor circle")
    delete_item("cursor node")

    mouse_x = get_drawing_mouse_pos()[0]
    mouse_y = get_drawing_mouse_pos()[1]

    # draw_line(
    #     p1=(mouse_x - 10, mouse_y),
    #     p2=(mouse_x + 10, mouse_y),
    #     tag="cursorX", 
    #     parent="pad", 
    #     color=[100, 100, 100], 
    #     thickness=2,
    # )
    # draw_line(
    #     p1=(mouse_x, mouse_y - 10),
    #     p2=(mouse_x, mouse_y + 10),
    #     tag="cursorY", 
    #     parent="pad",
    #     color=[100, 100, 100],
    #     thickness=2,
    # )
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

    if data == "doodle tool":
        tools.doodleTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == "rectangle tool":
        if get_value("Fill rectangle"):
            if get_value("Fill with same color"):
                tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), get_value("Color"))
            else:
                tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), get_value("Fill color"))
        else:
            tools.rectangleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Rounding"), [0, 0, 0, 0])

    if data == "circle tool":
        if get_value("Fill circle"):
            if get_value("Fill with same color"):
                tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Color"))
            else:
                tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), get_value("Fill color"))
        else:
            tools.circleTool("Pad", get_value("Color"), get_value("Thickness"), [0, 0, 0, 0])

    if data == "bezier tool":
        tools.bezierTool("Pad", get_value("Color"), get_value("Thickness"))

    if data == 'image tool':
        if get_value("##imagePath") != "Please select an image.":
            tools.imageTool("Pad", get_value("##imagePath"))
        else:
            pass
        
    if data == 'generate tool':
        if "Canvas" == get_value(item="Generation method"):
            print("generating from canvas ... ...")
            disable_item(item="Generate")
            set_item_label(item="Generate", label="Generating")
            tools.autoSaveTool()
            tools.generateTool("temp/temp_file.png")
            enable_item(item="Generate")
            set_item_label(item="Generate", label="Generate")
        elif "Image" == get_value(item="Generation method"):
            temp_image_path = get_value("##imagePath")
            if get_value("##imagePath") != "Please select an image.":
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
            default_value="\t  To get started, please select one of\n\t  the tools from the column on the\n\t  left.",
            parent="Tool Specifications",
        )
        tools.resetPad("Pad")

    elif "straight line tool" == caller_button:
        print("\nstraight line tool\n-------")
        delete_item("Tool Specifications", children_only=True)

    elif "polyline tool" == caller_button:
        print("\npolyline tool\n-------")
        delete_item("Tool Specifications", children_only=True)
        
    elif "doodle tool" == caller_button:
        print("\ndoodle tool\n-------")
        delete_item("Tool Specifications", children_only=True)
        
        doodle_specifications = ToolSpec(
            title="             \tDoodle Tool Properties",
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
            value="\tLeft click on the drawing pad to set\n"
                  "\tthe first point. Then left click, to end\n"
                  "\tthe tool. Right click or hit escape key\n"
                  "\tto undo the drawn line"
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

    elif "rectangle tool" == caller_button:
        print("\nrectangle tool\n-------")
        delete_item("Tool Specifications", children_only=True)

    elif "circle tool" == caller_button:
        print("\ncircle tool\n-------")
        delete_item("Tool Specifications", children_only=True)

    elif "bezier tool" == caller_button:
        print("\nbezier tool\n-------")
        delete_item("Tool Specifications", children_only=True)

        bezier_specifications = ToolSpec(
            title="            \tBezier Tool Properties",
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
            value="\tLeft click on the drawing pad to set\n"
                  "\tthe first point. Then left click to add\n"
                  "\tthree more points. Right click or hit\n"
                  "\tthe escape key on the keyboard to\n"
                  "\tend the tool.\n\n"
                  "\tIf you have selected the \"Close bezier\n"
                  "\tcurve\" then the bezier curve will close\n"
                  "\twhen the third point is selected")

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
            title="               \tImage Tool Properties",
            height=115
        )

        add_button(
            tag="Search image",
            label="Search image",
            width=210,
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
            width=210,
            height=40,
        )

        set_value("##imagePath", "Please select an image.")

        image_specifications.add_instructions(value="\tSelect an image by clicking on the\n"
                                                    "\t\"Search image\" button and then click\n"
                                                    "\tapply. Left click on the drawing pad\n"
                                                    "\tto select the first point and then left\n"
                                                    "\tclick again to place the image.\n"
                                                    "\n"
                                                    "\tHold down shift while placing the\n"
                                                    "\timage to fix the aspect ratio of the\n"
                                                    "\timage.")

        set_item_callback(
            item="Apply",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="image tool"),
        )
        set_item_callback(
            item="Cancel",
            callback=lambda: apply_settings_dispatcher(sender=None, app_data=None, user_data="cancel tool"),
        )
    
    elif "generate tool" == caller_button:
        print("\ngenerate tool\n-------")

        delete_item("Tool Specifications", children_only=True)
        generate_specifications = GenerateSpec(
            title="               Generate Tool Properties",
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
    default_font = add_font("fonts/OpenSans-Regular.ttf", 18)

bind_font(default_font)

# 主题设置
with theme(tag="global theme"):
    with theme_component(mvAll):
        add_theme_style(mvStyleVar_ItemSpacing, 20.00, 5.00, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_WindowTitleAlign, 0.50, 0.50, category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_FrameBorderSize, 1.0)
        add_theme_style(mvStyleVar_WindowPadding, 20, 5, category=mvThemeCat_Core)

        add_theme_color(mvThemeCol_MenuBarBg, [55, 55, 55], category=mvThemeCat_Core)
        add_theme_color(mvThemeCol_WindowBg, [55, 55, 55], category=mvThemeCat_Core)
    
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

        add_theme_color(mvThemeCol_WindowBg, [55, 55, 55], category=mvThemeCat_Core)
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


with handler_registry(show=True, tag="global handler"):
    add_mouse_move_handler(callback=pad_mouse_coordinates)
    add_key_down_handler(callback=tools.hotkeyCommands)
    
with handler_registry(show=True, tag="mouse handler"):
    add_mouse_release_handler(button=mvMouseButton_Left, tag="ml_release")
    add_mouse_release_handler(button=mvMouseButton_Right, tag="mr_release")


create_viewport(
    title="Sketch2Pose",
    width=1400,
    height=740,
    min_width=1000,
    min_height=600,
    small_icon="icons/sp.ico",
    large_icon="icons/sp.ico",
)

set_viewport_resize_callback(callback=global_resize)

# Main window menu
with viewport_menu_bar():
    with menu(label="File"):
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

        # add_separator()

        # with menu(label="Settings"):
        #     add_menu_item(
        #         label="Setting 1",
        #         callback=print_me,
        #         check=True
        #     )
        #     add_menu_item(
        #         label="Setting 2",
        #         callback=print_me,
        #     )

    with menu(label="Edit"):
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

    with menu(label="Tools"):
        add_menu_item(
            label="Straight line tool", 
            callback=lambda: tool_callback_dispatcher(sender="straight line tool")
        )
        add_menu_item(
            label="Polyline tool", 
            callback=lambda: tool_callback_dispatcher(sender="polyline tool")
        )
        add_menu_item(
            label="Doodle tool", 
            callback=lambda: tool_callback_dispatcher(sender="doodle tool")
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
    
    with menu(label="Theme"):
        add_menu_item(
            label="Dark",
            user_data="dark",
            callback=theme_switcher,
        )

    with menu(label="Help"):
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
        tag="doodle tool",
        texture_tag="doodle tool texture",
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

bind_item_theme("miscTools", "miscTools theme")

with popup(
    tag="reset popup",
    parent="reset tool",
    modal=True,
    mousebutton=mvMouseButton_Left,
):
    add_text("Are you sure you want to erase the drawing pad?", indent=15)
    add_spacer()
    with group(horizontal=True):
        add_button(
            tag="Yes##reset",
            label="Yes##reset", 
            width=150, 
            height=25, 
            callback=tool_callback_dispatcher,
        )
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
    no_move=True,
    no_close=True,
    width=260,
    height=get_viewport_height() - 304,
    pos=[100, 235],
):
    add_text(default_value="\t  To get started, please select one of\n\t  the tools from the column on the\n\t  left.")

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
    add_text(tag="mouse info", default_value="Mouse coordinates:", pos=[get_viewport_width() - 590, 3])
    
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
# while is_dearpygui_running():
#     render_dearpygui_frame()
destroy_context()
 