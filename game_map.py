import numpy as np  # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  #tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  #tiles the player has seen before


    #makes an invisible wall so the player doesnt go out of bounds
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    #faster rendering then using console.print
    def render(self, console: Console) -> None:
        #if a tile is in the 'visible' array then it is drawn with 'light' colours
        #if a tile isn't in the 'visible' array but its in the 'explored' array, then it is drawn with the 'dark' colour.
        #otherwise it is then defaulted to MIST

        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.MIST
        )