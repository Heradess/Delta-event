class Action:
    pass


#detects when esc is pressed
class EscapeAction(Action):
    pass


#this detects movement
class MovementAction(Action):
    def __init__(self, dx: int, dy:int):
        super().__init__()

        #this detects the direction of the movement
        self.dx = dx
        self.dy = dy
