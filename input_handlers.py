from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

#if program is X'ed then it will close instead of crashing
class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    #this method will receive key presses and either return an action subclass or none
    def ev_keydown(self, event:tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        #contains the raw input
        key = event.sym

        #movement controls, they tell the computer in what direction to move and how far 
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)
        
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()
        
        #no valid key was pressed
        return action