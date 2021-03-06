from attribute.attribute import Attribute
from attribute.weapon import Shootable
from player import Player
from decoration import Decoration

class Person(Attribute):
    def __init__(self):
        Attribute.__init__(self)

class Stowaway(Person, Shootable):
    def __init__(self, args=None):
        Person.__init__(self)
        Shootable.__init__(self)

        self.commands['INTERROGATE'] = self.interrogate

    def interrogate(self, player, args):
        if len(args) == 0:
            player.send_msg('Who do you want to interrogate?')
        else:
            targets = list(filter(lambda c: isinstance(c, Decoration) and
                c.name.lower() == args.lower(), player.room.contents))
            if len(targets) == 1:
                player.send_msg('"Please don\'t hurt me," the hostage begged. "I want to help you," you say, still unsure if you want to HELP him or dispose of him. You were ordered to get ELIMINATE him as he is an evil man, but you also are wary of elimination life.')

def make_new_stowaway():
    return Decoration('Stowaway', 'an out of place person',
        "This person doesn't look like they belong here.",
        ['stowaway', 'person'], [Stowaway()])
