#importing necessary libraries
import copy

import tcod

#importing classes and subclasses created previously
from engine import Engine
import entity_factory
from input_handlers import EventHandler
from procgen import generate_dungeon




def main() -> None:
    #this is setting the variables for the screen size
    #changing these variables will change the size of the window
    screen_width = 80
    screen_height = 50

    #sets map size
    #changing these values will change the size of the area that the generator will use
    map_width = 80
    map_height = 45

    #sets the max and min sizes for the generator to use when making a room as well as the max number of rooms possible within 1 map
    #changing this would change the average sizes of the rooms as well as the limit on how many there can be in 1 map
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    #the number of monsters allowed per room
    max_monsters_per_room = 2

    #this is loading what font to use from the tileset file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    #creates instance of EventHandler class, used to receive and process events
    event_handler = EventHandler()

    #copies the player data from the entity factory and loads it 
    player = copy.deepcopy(entity_factory.player)


    #map generation arguments 
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player,
        max_monsters_per_room=max_monsters_per_room
    )

    #passing all the variables stated above through the engine and setting it as a variable
    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    #this part creates the tab along with giving the window a title
    #this part also enables and disables vsync
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset = tileset,
        title = "Bare Bones",
        vsync = True,
    ) as context:
        
        #this creates the console and is set to be the same size as the tab
        #numpy reads from y and x in order which is not good so we switch it with 'order = "F"'
        root_console = tcod.console.Console(screen_width, screen_height, order = "F")
        
        #this is the game loop
        while True:
            #this is the engine rendering and what makes the console render the game itself
            engine.render(console=root_console, context=context)

            #this line waits for the input of the player
            events = tcod.event.wait
            
            #handles the key presses to the right output
            engine.handle_events(events)


#this only allows the main fuction to run when 'python main.py' is explicitly executed in the terminal or through opening the file
if __name__ == "__main__":
    main()