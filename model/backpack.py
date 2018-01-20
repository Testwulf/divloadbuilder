'''Models related to gear and backpack inventory'''


class Item:
    '''A model of a basic item'''

    def __init__(self, name, slot):
        '''Create a named item for a given slot'''
        self.name = name
        self.slot = slot


class Gear(Item):
    '''A model of a gear piece'''

    def __init__(self, name, slot, armor, firearms, stamina, electronics):
        '''Create a gear piece with the given attributes'''
        Item.__init__(self, name, slot)
        self.armor = armor
        self.firearms = firearms
        self.stamina = stamina
        self.electronics = electronics


class GearNotFound(Exception):
    '''A model of an error when gear is not found'''
    pass


class Loadout():
    '''A model of a gear loadout'''

    def __init__(self, name):
        '''Create a set of gear as a loadout'''
        self.name = name
        self.slots = None
        self.weights = {
            'armor': 1.0,
            'firearms': 1.0,
            'stamina': 2.0,
            'electronics': 1.0
        }
