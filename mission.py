import random

from attribute.stowaway import Stowaway, make_new_stowaway

class Mission:
    def __init__(self, player, world):
        self.player = player
        self.world = world
        self.target = None

    def start(self):
        self.target = make_new_stowaway()
        room = random.choice(list(filter(lambda r: not r.contains(Stowaway),
            self.world.rooms)))
        room.add_content(self.target)
        self.player.send_msg(open('dialog.txt', 'r').read().strip().format(room.name))

    def check_done(self):
        return self.target.shot
