from attribute.weapon import RangedWeapon, MeleeWeapon
from attribute.clonebay import CloneBay

attr_lookup = {
    'ranged_weapon': RangedWeapon,
    'melee_weapon': MeleeWeapon,
    'clone_bay': CloneBay,
}

def create_attribute(attr):
    attr = attr.split(',', 1)
    name = attr[0]
    args = attr[1] if len(attr) > 1 else None
    return attr_lookup[name](args)