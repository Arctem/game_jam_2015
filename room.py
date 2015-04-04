import pickle

class Room:
    def __init__(self, name, short_desc, desc, keywords, attributes=[], possible_start=False):
        self.name = name
        self.short_desc = short_desc
        self.desc = desc
        self.keywords = keywords
        self.attributes = attributes
        self.possible_start = possible_start
        self.connections = []
        self.contents = []

    def place_player(self, player):
        self.contents.append(player)
        player.set_room(self)
        #player.send_room_description()

    def player_leave(self, player):
        self.contents.remove(player)

    def add_content(self, item):
        self.contents.append(item)
        item.room = self

    def add_connection(self, connection):
        self.connections.append(connection)

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc