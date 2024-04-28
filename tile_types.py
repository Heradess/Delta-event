from typing import Tuple

import numpy as np  #type: ignore

#tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  #unicode codepoint.
        ("fg", "3B"),  #3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

#tile struct used for rigidly defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  #true if this tile can be walked over.
        ("transparent", np.bool_),  #true if this tile doesn't block FOV.
        ("dark", graphic_dt),  #graphics for when this tile is not in FOV.
        ("light", graphic_dt),  #graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  #enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

MIST = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

#setting the floor tile with a colour a representative character in this case blank, as well as the colour when its visible and when it isn't visible
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)

#this sets the wall tile with its colour its representative character and the colour it is when visible and invisible
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)

#changing any of the tile values will change what the tiles look like and how they function
#example. if you change the walkable argument to true for the wall, then you can go through the wall and have no clip, changing the dark or light arguments will change the rgb value and change what the tile looks like