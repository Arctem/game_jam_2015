class Room:
    def __init__(self, name, desc, possible_start=False):
        self.name = name
        self.desc = desc
        self.possible_start = possible_start
        self.connections = []
        self.contents = []

    def place_player(self, player):
        self.contents.append(player)
        player.room = self
        player.send_room_description()

    def description(self):
        return self.desc