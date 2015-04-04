import random

from special.clone import ClonePod

class World:
    def __init__(self):
        self.rooms = []
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        valid_rooms = list(filter(lambda r: r.possible_start, self.rooms))
        starter = random.choice(valid_rooms)
        starter.place_player(player)

    def add_room(self, room):
        self.rooms.append(room)

    def get_random_spawn(self):
        spawns = list(filter(lambda r: self.room.contains(ClonePod)
            ,self.rooms))