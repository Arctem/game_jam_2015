from attribute.attribute import Attribute
from player import Player

class Weapon(Attribute):
    def __init__(self):
        Attribute.__init__(self)

class RangedWeapon(Weapon):
    def __init__(self, args):
        Weapon.__init__(self)
        self.commands['SHOOT'] = self.shoot

    def shoot(self, player, args):
        if len(args) == 0:
            player.send_msg('What would you like to shoot?')
        else:
            targets = list(filter(lambda c: RangedWeapon.valid_target,
                player.room.contents))
            if len(targets) == 1:
                target = targets[0]
                if isinstance(target, Player):
                    targets[0].inform_others('{} shoots {}!'.format(player.name,
                        targets[0].name))
                    targets[0].send_msg('{} shoots you!'.format(player.name))
                    targets[0].kill('shot')
                else:
                    target.shoot(player, self)

    def valid_target(item):
        if isinstance(item, Player) and c.name.lower() == args.lower():
            return True
        elif isinstance(item, Decoration):
            for attr in item.attributes:
                if isinstance(attr, Shootable) and args.lower in item.keywords:
                    return True
        else:
            return False

class MeleeWeapon(Weapon):
    def __init__(self, args):
        Weapon.__init__(self)

class Shootable(Attribute):
    def __init__(self):
        Attribute.__init__(self)
        self.shot = False

    def shoot(self, shooter, weapon):
        self.shot = True
        shooter.inform_others('{} shot {}.'.format(shooter.name,
            self.parent.name))
