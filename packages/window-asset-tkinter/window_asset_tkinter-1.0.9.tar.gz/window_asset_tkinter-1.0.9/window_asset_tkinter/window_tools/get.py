"""
File in charge of containing the funcitons that gather info from GUI elements
"""

import tkinter as tk
import tkinter.filedialog as TKF


class Get:
    """ The  class in charge of gathering the info of a GUI element """

    @staticmethod
    def get_entry_content(entry: tk.Entry) -> str:
        """ get the content and update the entry field """
        return entry.get()

    @staticmethod
    def get_window_width(window: tk.Tk) -> int:
        """ Get the width of the physical display """
        return window.winfo_screenwidth()

    @staticmethod
    def get_window_height(window: tk.Tk) -> int:
        """ Get the height of the physical display """
        return window.winfo_screenheight()

    @staticmethod
    def get_window_position_x(window: tk.Tk) -> int:
        """ Get the x position of the window """
        return window.winfo_x()

    @staticmethod
    def get_window_position_y(window: tk.Tk) -> int:
        """ Get the y position of the window """
        return window.winfo_y()

    @staticmethod
    def get_window_position(window: tk.Tk) -> tuple:
        """ Get the position of a tkinter window """
        return (window.winfo_x(), window.winfo_y())

    @staticmethod
    def get_window_geometry(window: tk.Tk) -> str:
        """ Get the geometry of the window """
        return window.winfo_geometry()

    @staticmethod
    def get_window_size(window: tk.Tk) -> tuple:
        """ Get the size of the window """
        return (window.winfo_width(), window.winfo_height())

    @staticmethod
    def get_window_title(window: tk.Tk) -> str:
        """ Get the title of the window """
        return window.title()

    @staticmethod
    def get_filepath(window_title: str, filetypes: list[tuple, tuple] = [('txt files', '.txt'), ('all files', '.*')]) -> str:
        """ Get a filepath from the user's computer """
        filename = TKF.askopenfilename(title=window_title, filetypes=filetypes)
        return filename

    @staticmethod
    def get_folderpath(window_title: str, initial_directory: str) -> str:
        """ Get the folderpath from the user's computer """
        folderpath = TKF.askdirectory(
            initialdir=initial_directory,
            mustexist=True,
            title=window_title
        )
        return folderpath

    @staticmethod
    def get_current_host_screen_dimensions(window: tk.Tk) -> dict:
        """
        Get the size of the screen on which the program is running
        Workaround to get the size of the current screen in a multi-screen setup.

        Returns:
            geometry (dict): The standard Tk geometry string.
                {"width":width, "height":height, "left":left, "top":top}
        """

        root = tk.Toplevel(window)
        root.update_idletasks()
        root.attributes('-fullscreen', True)
        root.withdraw()
        geometry = root.winfo_geometry()
        root.destroy()
        result = dict()
        result["width"] = int(geometry.split("+")[0].split("x")[0])
        result["height"] = int(geometry.split("+")[0].split("x")[1])
        result["left"] = int(geometry.split("+")[1])
        result["top"] = int(geometry.split("+")[2])
        return result

    @staticmethod
    def get_image_dimensions(image: tk.Image) -> dict[str, int]:
        """ Get the dimensions of a given image """
        result = dict()
        result["width"] = image.width()
        result["height"] = image.height()
        return result
