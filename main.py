#importing necessary libraries
import tcod

#importing classes and subclasses created previously
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler




def main() -> None:
    #this is setting the variables for the screen size
    screen_width = 80
    screen_height = 50

    #this keeps track of the current position of the player
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    #this is loading what font to use from the tileset file
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    #creates instance of EventHandler class, used to receive and process events
    event_handler = EventHandler()

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
        root_console = tcod.Console(screen_width, screen_height, order = "F")
        
        #this is the game loop
        while True:
            #this is what tells the computer where to put the character @ where we want it 
            root_console.print(x=player_x, y=player_y, string="@")

            #this line is basically just a print function, it displays changes on the screen
            context.present(root_console)
            
            #clears the trail so it moves every frame
            root_console.clear()

            #these lines of code allows the program to close instead of crashing
            #this is also taking inputs from the user
            for event in tcod.event.wait():
                #this sends events to the correct places
                action = event_handler.dispatch(event)
                #this allows the code to jump if there is no valid key presses
                if action is None:
                    continue

                #this allows the movement to happen
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                
                #closes the game when escape is pressed
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


#this only allows the main fuction to run when 'python main.py' is explicitly executed in the terminal
if __name__ == "__main__":
    main()