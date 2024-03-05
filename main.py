#importing necessary libraries
import tcod

#importing classes and subclasses created previously
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon




def main() -> None:
    #this is setting the variables for the screen size
    screen_width = 80
    screen_height = 50

    #sets map size
    map_width = 80
    map_height = 45

    #this is loading what font to use from the tileset file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    #creates instance of EventHandler class, used to receive and process events
    event_handler = EventHandler()

    #importing the entities and store them in a set
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

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
            #this is what tells the computer to run the code in entity.py
            engine.render(console=root_console, context=context)

            #this line waits for the input of the player
            events = tcod.event.wait
            
            #handles the key presses to the right output
            engine.handle_events(events)


#this only allows the main fuction to run when 'python main.py' is explicitly executed in the terminal
if __name__ == "__main__":
    main()