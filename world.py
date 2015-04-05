import random
import threading
from threading import Lock
import time

from attribute.clonebay import CloneBay

class World:
    def __init__(self):
        self.rooms = []
        self.players = []
        self.lock = Lock()
        self.tick_count = 0

    def add_player(self, player):
        self.players.append(player)
        valid_rooms = list(filter(lambda r: r.possible_start, self.rooms))
        starter = random.choice(valid_rooms)
        starter.place_player(player)

    def add_room(self, room):
        self.rooms.append(room)

    def get_random_spawn(self):
        spawns = list(filter(lambda r: r.contains(CloneBay),
            self.rooms))
        return random.choice(spawns)

    def ready(self):
        t = threading.Thread(target=self.repeating_tasks, args=tuple())
        t.start()

    def repeating_tasks(self):
        while True:
            time.sleep(5)

            with self.lock:
                self.tick_count += 1
                print('Server tick {}.'.format(self.tick_count))
                self.handle_respawns()
                print('Server tick {} ending.'.format(self.tick_count))

    def handle_respawns(self):
        for p in self.players:
            if not p.room:
                self.get_random_spawn().place_player(p)