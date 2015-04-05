import pickle

from item import Item
import kill_strings


class Player:
    def __init__(self, sock, name, world, clothes=None):
        self.name = name
        self.sock = sock
        self.world = world
        self.room = None
        self.inventory = []
        self.clothes = clothes

    def short_description(self):
        return self.name

    def description(self):
        msg = ['This is {}.'.format(self.name)]
        if self.clothes:
            msg.append('They are wearing a {} jumpsuit.'.format(self.clothes))
        else:
            msg.append('They are completely naked.')
        return ' '.join(msg)

    def set_room(self, room):
        if self.room:
            self.inform_others('{} has left the room.'.format(self.name))
        self.room = room
        self.send_msg('You find yourself in {}.'
            .format(room.short_description()))
        self.inform_others('{} has entered the room.'.format(self.name))

    def inform_others(self, msg):
        for person in filter(lambda c: isinstance(c, Player) and c is not self,
                self.room.contents):
            person.send_msg(msg)

    def send_room_description(self):
        msg = []
        if self.room:
            room = self.room.name
            desc = self.room.description()
            msg.append('You are in {}.'.format(room))
            msg.append('{}'.format(desc))
            for obj in self.room.contents:
                if obj is not self:
                    msg.append('There is {}.'.format(obj.short_description()))
            for obj in self.room.connections:
                if obj.short_description():
                    msg.append('There is {}.'.format(obj.short_description()))

        msg = '\n'.join(msg)
        self.send_msg(msg)

    def move_through(self, connection):
        self.room.player_leave(self)
        self.send_msg(connection.pass_desc)
        connection.destination.place_player(self)

    def gather_actions(self):
        actions = {}
        for item in self.inventory:
            print(item)
            print(item.attributes)
            for attr in item.attributes:
                actions.update(attr.commands)

        return actions

    def take_item(self, args):
        for item in filter(lambda c: not isinstance(c, Player), self.room.contents):
            if args in item.keywords:
                if isinstance(item, Item):
                    self.send_msg('You pick up {}.'.format(item.name))
                    self.inform_others('{} picks up {}.'.format(self.name,
                        item.name))
                    self.room.remove_item(item)
                    self.inventory.append(item)
                    item.player = self
                else:
                    self.send_msg("You can't take {}.".format(item.name))
                    self.inform_others('{} looks at {}, then shakes their head sadly.'
                        .format(self.name, item.name))

    def drop_item(self, args):
        possibles = list(filter(lambda i: args in i.keywords, self.inventory))
        if len(possibles) == 1:
            item = possibles[0]
            self.send_msg('You drop {}.'.format(item.name))
            self.inform_others('{} drops {}.'.format(self.name, item.name))
            item.player = None
            self.inventory.remove(item)
            self.room.add_content(item)
        elif len(possibles) == 0:
            self.send_msg("You don't have a {} to drop.".format(args))
            self.inform_others("{} searches their pockets, then looks dejected."
                .format(self.name))
        else:
            self.send_msg("You have multiple items by that name! Try a " +
                "different keyword.")


    def kill(self, method):
        self.inform_others(kill_strings.other_msg[method].format(name=self.name))
        for item in self.inventory:
            self.inform_others('{} drops {}.'.format(self.name, item.short_desc))
            self.room.add_content(item)
            item.player = None
        self.inventory = []

        self.send_msg(kill_strings.self_msg[method])

        self.set_room(self.world.get_random_spawn())

    def send_msg(self, msg):
        self.sock.sendall(pickle.dumps(msg))