'''
Main application entry point.
'''

from control import backpack
from ui.prompt import Prompt


def add_item():
    '''Add an item to the inventory'''
    name = input('What is the item named? ')
    print('Which slot does it use?')
    for index, possible_slot in enumerate(backpack.SLOTS):
        print(' %s] %s' % (index, possible_slot))
    slot = int(input('(Enter the slot number): '))
    slot = backpack.SLOTS[slot]
    if backpack.add_item(name, slot):
        print('%s added to the backpack' % name)


def list_items():
    '''List all items in the inventory'''
    item_list = backpack.get_items()
    for item in item_list:
        print('Name: %s (%s)' % (item.name, item.slot))


# Command Registry
COMMANDS = {
    'add': {
        'item': add_item
    },
    'list': {
        'items': list_items
    }
}


if __name__ == '__main__':
    PROMPT = Prompt(COMMANDS, 'The Division Loadout Builder')
    PROMPT.run()
