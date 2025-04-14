"""
File in charge of containing the esoteric types used by tkinter so that they can be referenced in the code.
"""

from typing import TypeAlias, Union, Literal

TK_ANCHOR_TYPE: TypeAlias = Union[
    str,
    Literal[
        "nw", "n", "ne", "w", "center",
        "e", "sw", "s", "se"
    ]
]

TK_RELIEF_TYPE: TypeAlias = Union[
    str,
    Literal[
        "flat", "raised", "sunken", "groove", "ridge"
    ]
]

TK_SIDE_TYPE: TypeAlias = Union[
    str,
    Literal["left", "right", "top", "bottom"]
]


TK_SCROLL_ORIENTATION_TYPE: TypeAlias = Union[
    str,
    Literal["horizontal", "vertical"]
]
