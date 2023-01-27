from dearpygui.dearpygui import *


class ToolSpec:
    # Class that will create all widgets inside the Tool Specifications Window
    def __init__(self, title: str, height: int):
        self.title = title
        self.height = height
        self.parent = "Tool Specifications"

        add_spacer(height=1, parent=self.parent)
        add_text(self.title, parent=self.parent)
        add_spacer(height=3, parent=self.parent)
        add_separator(parent=self.parent)
        add_spacer(height=1, parent=self.parent)

        with child_window(tag="tool properties", label="tool properties", height=self.height, parent=self.parent):
            self.add_space(height=4)

        with group(horizontal=True, parent=self.parent):
            add_button(tag="Cancel", label="Cancel", height=30, width=110)
            # add_spacer(parent=self.parent)
            # add_same_line(spacing=8.0, parent=self.parent)
            add_button(tag="Apply", label="Apply", height=30, width=110)
        add_spacer(parent=self.parent)
        # add_spacing(count=1, parent=self.parent)
        add_separator(parent=self.parent)

    def add_space(self, height: int):
        add_spacer(height=height, parent="tool properties")

    def add_separate(self):
        add_separator(parent="tool properties")

    def add_instructions(self, value: str):
        add_spacer(height=20, parent=self.parent)
        add_text(default_value="How to use: ", parent=self.parent)
        add_spacer(height=10, parent=self.parent)
        add_text(default_value=value, parent=self.parent)