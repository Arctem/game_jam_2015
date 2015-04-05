import pickle

from attribute.attribute import Attribute
from decoration import Decoration
from item import Item
from player import Player

class Room:
    def __init__(self, name, short_desc, desc, keywords, attributes=[], possible_start=False):
        self.name = name
        self.short_desc = short_desc
        self.desc = desc
        self.keywords = keywords
        self.attributes = attributes
        for attr in self.attributes:
            attr.parent = self
        self.possible_start = possible_start
        self.connections = []
        self.contents = []

    def place_player(self, player, leaving=None, arrival=None, to_others=None):
        self.contents.append(player)
        player.set_room(self, leaving, arrival, to_others)
        #player.send_room_description()

    def player_leave(self, player):
        self.contents.remove(player)

    def add_content(self, item):
        self.contents.append(item)
        item.room = self

    def remove_item(self, item):
        item.room = None
        self.contents.remove(item)

    def contains(self, obj):
        if issubclass(obj, Attribute):
            for a in self.attributes:
                if isinstance(self, obj):
                    return True

            for i in filter(lambda c: not isinstance(c, Player), self.contents):
                for j in i.attributes:
                    if isinstance(j, obj):
                        return True
        elif issubclass(obj, Decoration) or issubclass(obj, Item):
            for i in self.contents:
                if isinstance(i, obj):
                    return True
        else:
            return False

    def add_connection(self, connection):
        self.connections.append(connection)

    def short_description(self):
        return self.short_desc

    def description(self):
        return self.desc