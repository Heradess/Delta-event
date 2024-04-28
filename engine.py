from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

#this class serves as a way of keeping entities unique because having two of the same entities wouldn't make sense
class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    #this processes events such as key presses or mouse movements
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events():
            action = self.event_handler.dispatch(event)

            if action is None:
                continue #if nothing is pressed then everything continues rather than crashing or just stopping.
            
            action.perform(self, self.player)

            self.update_fov()  #update the FOV before the players next action. 

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8, #the range of the fov in a square around the player. this allows the player to have the illusion of a vision line
        )
        #if a tile is or was "visible" it should be added to "explored"
        self.game_map.explored |= self.game_map.visible
    
    #this handles drawing the  screen
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)


        context.present(console)

        console.clear() #this clears the screen of any previous changes, this eliminates any trails left by moving. however on a larger scale this may cause lag as it is rendering all of the entities and map every single time that the action is pressed.