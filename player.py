import pickle

class Player:
    def __init__(self, sock, name, clothes=None):
        self.name = name
        self.sock = sock
        self.room = None
        self.inventory = []
        self.clothes = clothes

    def description():
        msg = [name]
        if self.clothes:
            msg.append('They are completely naked.')
        else:
            msg.append('They are wearing a {} jumpsuit.'.format(clothes))
        return ' '.join(msg)

    def send_room_description(self):
        msg = []
        if self.room:
            room = self.room.description()
            msg.append('You are in {}'.format(room))
            for obj in self.room.contents:
                if obj is not self and obj.description():
                    msg.append('There is {}'.format(obj.description()))

        msg = '\n'.join(msg)
        self.sock.sendall(pickle.dumps(msg))