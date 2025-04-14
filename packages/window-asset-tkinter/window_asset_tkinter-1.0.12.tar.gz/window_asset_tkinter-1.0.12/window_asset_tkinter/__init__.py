##
# EPITECH PROJECT, 2022
# Desktop_pet (Workspace)
# File description:
# __init__.py
##

"""
The file containing the code to ease the import of python files
contained in the current folder to any other python code that is
not contained in the same directory.
"""

# library dedicated to displaying input windows

# files of the lib
if __name__ == "__main__":
    from capsule import WindowAsset, WindowTools,  ErrMessages, ActionAssets, CalculateWindowPosition
else:
    from .capsule import WindowAsset, WindowTools, ErrMessages, ActionAssets, CalculateWindowPosition

__all__ = [
    "WindowAsset",
    "WindowTools",
    "ErrMessages",
    "ActionAssets",
    "CalculateWindowPosition",
]
