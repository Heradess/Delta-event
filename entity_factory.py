from entity import Entity

player = Entity(char="@", colour=(128, 0, 255), name="Player", blocks_movement=True)

orc = Entity(char="o", colour=(63, 127, 63), name="Orc", blocks_movement=True)
orc_lord = Entity(char="O", colour=(0, 127, 0), name="Orc Lord", blocks_movement=True)