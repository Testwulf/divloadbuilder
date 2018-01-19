'''
Main application entry point.
'''

from control import backpack
from ui.prompt import Prompt


def add_item():
    '''Add an item to the inventory'''
    name = input('What is the item named? ')
    if backpack.add_item(name):
        print('%s added to the backpack' % name)


# Command Registry
COMMANDS = {
    'add': {
        'item': add_item
    }
}


if __name__ == '__main__':
    PROMPT = Prompt(COMMANDS, 'The Division Loadout Builder')
    PROMPT.run()
