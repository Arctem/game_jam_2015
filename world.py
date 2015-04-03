import random

class World:
    def __init__(self):
        self.rooms = []
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        valid_rooms = list(filter(lambda r: r.possible_start, self.rooms))
        print(valid_rooms)
        starter = random.choice(valid_rooms)
        starter.place_player(player)

    def add_room(self, room):
        self.rooms.append(room)