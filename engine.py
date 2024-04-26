from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

#this class serves as a way of keeping entities unique because having two of the same entities wouldn't make sense
class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    #this processes events such as key presses or mouse movements
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events():
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)

            self.update_fov()  #update the FOV before the players next action.

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        #if a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible
    
    #this handles drawing the  screen
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            #only prints entities that are in the FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.colour)

        context.present(console)

        console.clear()