from attribute.attribute import Attribute
from player import Player
from decoration import Decoration

class Person(Attribute):
    def __init__(self):
        Attribute.__init__(self)
        
class Stowaway(Person):
    def __init__(self, args):
        Person.__init__(self)
        self.commands['INTERROGATE'] = self.interrogate
        
    def interrogate(self, player, args):
        if len(args) == 0:
            player.send_msg('Who do you want to interrogate?')
        else:
            targets = list(filter(lambda c: isinstance(c, Decoration) and 
                c.name.lower() == args.lower(), player.room.contents))
            if len(targets) == 1:
                player.send_msg('The stowaway spits in your face')