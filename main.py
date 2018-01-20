'''
Main application entry point.
'''

from control import backpack
from model.backpack import Gear
from ui.prompt import Prompt


def add_item():
    '''Add an item to the inventory'''
    name = input('What is the item named? ')
    print('Which slot does it use?')
    key_list = []
    for index, possible_slot in enumerate(backpack.SLOTS):
        key_list.append(possible_slot)
        print(' %s] %s' % (index, possible_slot))
    slot = int(input('(Enter the slot number): '))
    slot = key_list[slot]
    slot_type = backpack.SLOTS[slot]
    if slot_type == Gear:
        firearms = int(input('What Firearms bonus does it have? '))
        if backpack.add_gear(name, slot, firearms):
            print('%s added to the backpack' % name)


def add_loadout():
    '''Add a loadout to the stash'''
    name = input('What should this loadout be named? ')
    if backpack.add_loadout(name):
        print('%s loadout added to backpack' % name)


def list_items():
    '''List all items in the inventory'''
    item_list = backpack.get_items()
    for item in item_list:
        print('Name: %s (%s)' % (item.name, item.slot))


def list_loadouts():
    '''List all current loadouts'''
    loadouts = backpack.get_loadouts()
    for loadout in loadouts:
        print('Name: %s' % loadout.name)


def optimize_loadout():
    '''Optimize a chosen loadout'''
    loadouts = backpack.get_loadouts()
    for index, loadout in enumerate(loadouts):
        print(' %s] %s' % (index, loadout.name))
    index = int(input('(Enter the loadout number): '))
    loadout = loadouts[index]


# Command Registry
COMMANDS = {
    'add': {
        #agent:
        'item': add_item,
        'loadout': add_loadout
    },
    #delete: {
        #agent:
        #item:
        #loadout:
    #}
    #edit: {
        #agent
        #item
        #loadout
    #}
    #inspect: {
        #agent
        #item
        #loadout
    #}
    'list': {
        #agents
        'items': list_items,
        'loadouts': list_loadouts
    },
    'optimize': {
        'loadout': optimize_loadout
    }
}


if __name__ == '__main__':
    PROMPT = Prompt(COMMANDS, 'The Division Loadout Builder')
    PROMPT.run()
