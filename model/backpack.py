'''Models related to gear and backpack inventory'''


class Item:
    '''A model of a basic item'''

    def __init__(self, name):
        '''Create a named item'''
        self.name = name
