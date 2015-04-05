import random
import threading
from threading import Lock
import time

from attribute.clonebay import CloneBay
from mission import Mission
from player import Player

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

    def find_room(self, keyword):
        for r in self.rooms:
            if keyword in r.keywords:
                return r

        assert False, 'There is no room with keyword {}.'.format(keyword)

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
                self.give_missions()
                print('Server tick {} ending.'.format(self.tick_count))

    def handle_respawns(self):
        for p in self.players:
            if not p.room:
                self.get_random_spawn().place_player(p,
                    arrival='You schlop out of the cloning vat in the {}, fresh and new.',
                    to_others="{}'s new clone slides smoothly from the cloning vat.")

    def give_missions(self):
        briefing = self.find_room('briefing')
        for p in filter(lambda c: isinstance(c, Player), briefing.contents):
            if not p.mission:
                p.give_mission(Mission(p, self))
