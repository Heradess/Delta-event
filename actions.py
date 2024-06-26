from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity




class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


#detects when esc is pressed
class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


#this detects movement through the arrow keys
class MovementAction(Action):
    def __init__(self, dx: int, dy:int):
        super().__init__()

        #this detects the direction of the movement
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  #destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  #destination is blocked by a tile.
        #this just stops movement from happening if it is an invalid direction or destination for the movement

        entity.move(self.dx, self.dy)
