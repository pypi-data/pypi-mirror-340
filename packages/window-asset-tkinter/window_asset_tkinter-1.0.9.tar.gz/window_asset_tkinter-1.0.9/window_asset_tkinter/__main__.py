"""
    File in charge of testing the window_asset_tkinter module
"""

from typing import Dict, Any

import os

import tkinter as tk

print(f"__name__ = {__name__}")

try:
    from window_tools import WindowTools
    from err_messages import ErrMessages
    from action_assets import ActionAssets
    from calculate_window_position import CalculateWindowPosition
except ModuleNotFoundError:
    from .window_tools import WindowTools
    from .err_messages import ErrMessages
    from .action_assets import ActionAssets
    from .calculate_window_position import CalculateWindowPosition
except ImportError:
    from .window_tools import WindowTools
    from .err_messages import ErrMessages
    from .action_assets import ActionAssets
    from .calculate_window_position import CalculateWindowPosition

__all__ = [
    "WindowTools",
    "ErrMessages",
    "ActionAssets",
    "CalculateWindowPosition"
]

if __name__ == "__main__":
    file_info: Dict[str, Dict[str, Any]] = {
        "err_message": {
            "width": 300,
            "height": 110,
            "min_width": 300,
            "min_height": 110,
            "max_width": 1000,
            "max_height": 1000,
            "window_position_x": 0,
            "window_position_y": 0,
            "resizable": True,
            "dark_mode_enabled": False,
            "full_screen": False,
            "dark_mode": {
                "background": "#000000",
                "foreground": "#FFFFFF"
            },
            "light_mode": {
                "background": "#FFFFFF",
                "foreground": "#000000"
            },
            "background": "#000000",
            "foreground": "#FFFFFF",
            "font_size": 12,
            "font_family": "Times New Roman",
            "debug_mode_enabled": False,
            "icon_path": f"{os.path.dirname(os.path.abspath(__file__))}/assets/favicon.ico",
            "button_width": 10,
            "button_height": 1,
            "error_icon_path": f"{os.path.dirname(os.path.abspath(__file__))}/assets/error_64x64.png",
            "warning_icon_path": f"{os.path.dirname(os.path.abspath(__file__))}/assets/warning_64x64.png",
            "information_icon_path": f"{os.path.dirname(os.path.abspath(__file__))}/assets/information_64x64.png",
            "image_width": 64,
            "image_height": 64
        }
    }

    def test_the_error_message_class() -> None:
        """_summary_
        This is a function in charge of testing the error message class
        """
        lore = False
        print("Please launch the main program")

        print_debug = False
        if lore is True:
            file_info["err_message"]["debug_mode_enabled"] = True
            print_debug = True

        base_window = tk.Tk()
        cwd: str = os.getcwd()
        emi = ErrMessages(
            base_window,
            file_info,
            print_debug=print_debug,
            cwd=cwd
        )
        win = emi.init_plain_window(base_window)
        win.update()
        emi.simple_err_message(
            my_window=win,
            title="Test message error",
            message="This is a test message for the error message box",
            button=emi.button_options["ok"],
            always_on_top=True,
            command=[win.destroy]
        )
        win = emi.init_plain_window(base_window)
        emi.simple_warning_message(
            my_window=win,
            title="Test message warning",
            message="This is a test message for the warning message box",
            button=emi.button_options["ok"],
            always_on_top=True,
            command=[win.destroy]
        )
        emi.window = emi.init_plain_window(base_window)
        emi.simple_information_message(
            my_window=emi.window,
            title="Test message information",
            message="This is a test message for the inform message box",
            button=emi.button_options["o/c"],  # button_options["c/a"],
            always_on_top=True,
            command=[emi.window.destroy, emi.window.destroy]
        )
        emi.advanced_warning_message(
            parent_window=base_window,
            title="You have found a corps",
            message="You have found a rotting corps",
            button=emi.button_options["ok"],
            always_on_top=True
        )
        response = emi.advanced_information_message(
            parent_window=base_window,
            title="Save corps?",
            message="Do you wish to save the rotting corpse to your inventory?",
            button=emi.button_options["s/d/c"],
            always_on_top=True
        )
        emi.err_message_print_debug(f"response = {response}")
        response_sentence = {
            0: "undefined",
            1: "save",
            2: "not save",
            3: "ignore"
        }
        if response == 0:
            if lore is True:
                emi.init_plain_window()
            emi.advanced_err_message(
                parent_window=base_window,
                title="Error",
                message="You have not chosen a response!\nThus, the corpse will be added to your inventory.\nTough luck bud!",
                button=emi.button_options["ok"],
                always_on_top=True
            )
        else:
            emi.advanced_information_message(
                parent_window=base_window,
                title="Your corpsy response",
                message=f"You have chosen to {response_sentence[response]} the corpse.",
                button=emi.button_options["ok"],
                always_on_top=True
            )
        emi.goodbye_message(parent_window=base_window)
        base_window.update()
        base_window.destroy()

    def test_window_position() -> None:
        """_summary_
        This is a function in charge of testing the window position
        """
        cwpi = CalculateWindowPosition(10, 10, 1, 1)
        test_input = {
            cwpi.top_left: (0, 0),
            cwpi.top_center: (4, 0),
            cwpi.top_right: (9, 0),
            cwpi.bottom_left: (0, 9),
            cwpi.bottom_center: (4, 9),
            cwpi.bottom_right: (9, 9),
            cwpi.left_center: (0, 4),
            cwpi.center: (4, 4),
            cwpi.right_center: (9, 4),
            "gobbledygook": (0, 0)
        }
        for key, value in test_input.items():
            print(f"Testing: CPI.re_router({key}):", end="")
            response = cwpi.re_router(key)
            if response == value:
                print("[OK]")
            else:
                print(f"[KO]: Got {response} but expected {value}")

    def test_assets() -> None:
        """ Test the assets """
        window = tk.Tk()
        ai = WindowTools()
        # basic elements
        sample_frame = ai.add_frame(
            window, 0, tk.GROOVE, "orange",
            width=50,
            height=1,
            fill=tk.NONE,
            anchor=tk.N,
            side=tk.TOP
        )
        ai.add_label(
            sample_frame, "Sample label", "black",
            "white", width=10, height=1,
            side=tk.TOP
        )
        ai.add_spinbox(
            window=sample_frame,
            minimum=0,
            maximum=100,
            bkg="white",
            fg="black",
            width=10,
            height=1
        )
        ai.add_entry(
            window=sample_frame,
            text_variable="Sample entry",
            width=20,
            bkg="white",
            fg="black",
            side=tk.TOP,
            position_x=10,
            position_y=2
        )
        sample_labelframe = ai.add_labelframe(
            sample_frame, "Sample labelframe", 10, 10,
            fill=tk.NONE, expand=tk.NO, side=tk.LEFT
        )
        ai.add_button(
            sample_labelframe, "Sample button", "black", "white", tk.LEFT,
            width=10,
            height=1,
            command=lambda: print("Button pressed")
        )
        sample_paned_window = ai.add_paned_window(
            window=window,
            orientation=tk.HORIZONTAL,
            side=tk.TOP,
            expand=tk.YES,
            fill=tk.BOTH,
            vertical_padding=10,
            horizontal_padding=10,
            width=10,
            height=100,
        )
        sample_label_frame_node = ai.add_labelframe(
            window=sample_paned_window,
            title="Paned window",
            padding_x=10,
            padding_y=10,
            fill=tk.NONE,
            expand=tk.YES,
            bkg="white",
            side=tk.TOP
        )
        ai.add_panned_window_node(
            sample_paned_window, sample_label_frame_node
        )
        ai.add_date_field(sample_label_frame_node)
        ai.add_dropdown(
            sample_label_frame_node, ["Option 1", "Option 2", "Option 3"],
            width=10, bkg="white", fg="black"
        )
        sample_text_field = ai.add_text_field(sample_label_frame_node)
        sample_text_field.insert(tk.END, "Sample text for the text field")
        sample_grid_labelframe = ai.add_labelframe(
            window=window,
            title="Sample grid",
            padding_x=10,
            padding_y=10,
            fill=tk.NONE,
            width=10,
            height=10,
            expand=tk.NO,
            side=tk.TOP
        )
        sample_grid = ai.add_grid(
            window=sample_grid_labelframe,
            borderwidth=2,
            relief=tk.GROOVE,
            bkg="white"
        )
        counter = 0
        for i in range(10):
            ai.add_label(
                sample_grid, f"Label {i+1}", "black",
                "white", width=10, height=1,
                position_x=0,
                position_y=0,
                side=tk.TOP,
                grid_column=i - i % 2,
                grid_row=counter
            )
            if i % 2 == 0:
                counter = 1
            else:
                counter = 0
        sample_scrolling = ai.add_labelframe(
            window=window,
            title="Sample scrolling",
            padding_x=10,
            padding_y=10,
            fill=tk.NONE,
            expand=tk.YES,
            bkg="white",
            side=tk.TOP
        )
        sample_scrollbox = ai.add_scrollbox(
            sample_scrolling, 0, tk.FLAT, "white",
            paragraph_height=5, paragraph_width=40,
        )
        sample_scrollbox["paragraph"].insert(
            tk.END, "Sample text for the scroll box.\n\n\n\n\n\nSample text for the scroll box."
        )
        sample_media_title_frame = ai.add_labelframe(
            window=window,
            title="Sample media",
            padding_x=10,
            padding_y=0,
            fill=tk.NONE,
            expand=tk.YES,
            bkg="white",
            side=tk.TOP
        )
        file_path = file_info["err_message"]["information_icon_path"]
        print(f"file_path = {file_path}")
        ai.add_image(
            sample_media_title_frame, file_path,
            width=64, height=64,
            padx=0, pady=0,
            side=tk.LEFT,
        )
        ai.add_emoji(
            sample_media_title_frame, "😀", "black", "white", width=2, height=2,
            position_x=0, position_y=0, side=tk.LEFT
        )
        ai.add_watermark(window)
        window.mainloop()

    print("Testing the calculate window position class")
    test_window_position()
    print("Testing the message boxes")
    test_the_error_message_class()
    print("Testing the window tools")
    print("Testing the assets")
    test_assets()
