'''Models related to gear and backpack inventory'''


class Item:
    '''A model of a basic item'''

    def __init__(self, name, slot):
        '''Create a named item for a given slot'''
        self.name = name
        self.slot = slot


class Gear(Item):
    '''A model of a gear piece'''

    def __init__(self, name, slot, firearms):
        '''Create a gear piece with the given attributes'''
        Item.__init__(self, name, slot)
        self.firearms = firearms


class Loadout():
    '''A model of a gear loadout'''

    def __init__(self, name):
        '''Create a set of gear as a loadout'''
        self.name = name
