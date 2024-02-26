from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

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

    #this processes events such as key presses or mouse movements
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events():
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)
    
    #this handles drawing the  screen
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.colour)

        context.present(console)

        console.clear()