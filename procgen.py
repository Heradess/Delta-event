from __future__ import annotations

import random

from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types
import entity_factory

if TYPE_CHECKING:
    from entity import Entity

#the room type this sets the properties of the rooms and can be used as a template to make new rooms with potentially more rigid structure
class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    #this returns the center value for the console and returns it.
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    
    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
    
#this defines how the entities are placed within the map, specifically entities which are not the player as the player is spawned with the rooms
def place_entities(
    room: RectangularRoom, dungeon: GameMap, maximum_monsters: int,
) -> None:
    number_of_monsters = random.randint(0, maximum_monsters)

    #random number of monsters to be added to the room 
    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.9:
                entity_factory.orc.spawn(dungeon, x, y) #there is a 90% chance that the orc spawns 
            else:
                entity_factory.orc_lord.spawn(dungeon, x, y) #there is a 10% chance that the orc lord spawns


#this is the function that controls the tunnels that are between the rooms.
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points being 1 tile wide."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        #moves horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        #moves vertically, then horizontally.
        corner_x, corner_y = x1, y2

    #generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

#this function generates the dungeon with all the given arguments and attributes
def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
    max_monsters_per_room: int
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        #"RectangularRoom" class makes rectangles easier to work with and allows it to change the sizes freely
        new_room = RectangularRoom(x, y, room_width, room_height)

        #run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt until finding a valid room
        #if there are no intersections then the room is valid.
        #if a room is invalid then it just skips it and therefore creates randomness, the map will not always have the maximum number of rooms.

        #this carves out the inner area of the room 
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            #make the first room, where the player starts
            player.x, player.y = new_room.center
        else:  #all rooms after the first
            #dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        place_entities(new_room, dungeon, max_monsters_per_room)

        #now i append the new room to the list
        rooms.append(new_room)

    return dungeon