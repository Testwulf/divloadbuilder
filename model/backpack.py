'''Models related to gear and backpack inventory'''


class Item:
    '''A model of a basic item'''

    def __init__(self, name, slot):
        '''Create a named item for a given slot'''
        self.name = name
        self.slot = slot
