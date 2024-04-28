from entity import Entity

#the player entity, changing the char value will change what is displayed as the player character, changing the colour numbers will affect the rgb value and change the colour.
player = Entity(char="@", colour=(128, 0, 255), name="Player", blocks_movement=True)

#the enemies
#the changes on these are the same, the blocks movement argument states that if the player wanted to advance onto the tile that the enemy is on then they would be prevented from doing so similarly to how a wall does it.
orc = Entity(char="o", colour=(63, 127, 63), name="Orc", blocks_movement=True) 
orc_lord = Entity(char="O", colour=(0, 127, 0), name="Orc Lord", blocks_movement=True)