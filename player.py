import pickle

class Player:
    def __init__(self, sock, name, clothes=None):
        self.name = name
        self.sock = sock
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
        self.room = room
        self.sock.sendall(pickle.dumps('You find yourself in {}.'
            .format(room.short_description())))

    def send_room_description(self):
        msg = []
        if self.room:
            room = self.room.description()
            msg.append('You are in {}'.format(room))
            for obj in self.room.contents:
                if obj is not self and obj.short_description():
                    msg.append('There is {}.'.format(obj.short_description()))
            for obj in self.room.connections:
                if obj.short_description():
                    msg.append('There is {}.'.format(obj.short_description()))

        msg = '\n'.join(msg)
        self.sock.sendall(pickle.dumps(msg))