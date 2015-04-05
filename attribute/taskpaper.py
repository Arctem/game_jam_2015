class Note():
    def __init__(self, args):
        self.commands['READ'] = self.read
    def read(self, player, args):
        if len(args) == 0:
            player.send_msg('What do you want to read?')
        else:
            player.send_msg('Your task is to find and exterminate the stowaway threat.')
