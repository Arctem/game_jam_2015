from attribute.weapon import RangedWeapon, MeleeWeapon
from attribute.clonebay import CloneBay
from attribute.stowaway import Stowaway

attr_lookup = {
    'ranged_weapon': RangedWeapon,
    'melee_weapon': MeleeWeapon,
    'clone_bay': CloneBay,
    'stowaway' : Stowaway,
}

def create_attribute(attr):
    if len(attr) is 0:
        return []
    else:
        attr = attr.split(':')
        return list(map(parse_attribute, attr))

def parse_attribute(attr):
    attr = attr.split(',', 1)
    name = attr[0]
    args = attr[1] if len(attr) > 1 else None
    return attr_lookup[name](args)