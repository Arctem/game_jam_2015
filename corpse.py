class Corpse(Decoration):
    def __init__(self, player):
        long_desc = 'The inglorious remains of {}.'.format(player.name)
        if player.clothes:
            long_desc += ' It is wearing {}.'.format(player.clothes)
        Decoration.__init__(self, "{}'s Corpse".format(player.name),
            "{}'s corpse".format(player.name),
            long_desc, ['corpse', player.name, 'body'])

        self.clothes = player.clothes