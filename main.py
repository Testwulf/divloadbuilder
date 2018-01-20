'''
Main application entry point.
'''

from control import backpack
from model.backpack import Gear, GearNotFound
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
        else:
            print('An item by that name already exists. Use a new name.')


def add_loadout():
    '''Add a loadout to the stash'''
    name = input('What should this loadout be named? ')
    if backpack.add_loadout(name):
        print('%s loadout added to backpack' % name)


def inspect_loadout(loadout=None):
    '''Display information for a loadout'''
    if loadout is None:
        # Choose a loadout
        loadouts = backpack.get_loadouts()
        print('Inspect which loadout?')
        for index, loadout in enumerate(loadouts):
            print(' %s] %s' % (index, loadout.name))
        index = int(input('(Enter the loadout number): '))
        loadout = loadouts[index]

    total_firearms = 0

    print('Name: %s' % loadout.name)
    if loadout.slots is not None:
        print('Gear:')
        for slot in loadout.slots:
            gear_name = loadout.slots[slot]
            gear = backpack.get_item(gear_name)

            total_firearms += gear.firearms

            print('  %s] %s' % (slot, gear.name))
            print('    Firearms: %s' % gear.firearms)

        print('Total:')
        print('  Firearms: %s' % total_firearms)
    else:
        print('No gear assigned to this loadout. Run "optimize loadout" to determine gear.')



def list_items():
    '''List all items in the inventory'''
    item_list = backpack.get_items()
    if item_list:
        for item in item_list:
            print('Name: %s (%s)' % (item.name, item.slot))
    else:
        print('No items found. Use "add item" to initialize your inventory.')


def list_loadouts():
    '''List all current loadouts'''
    loadouts = backpack.get_loadouts()
    if loadouts:
        for loadout in loadouts:
            print('Name: %s' % loadout.name)
    else:
        print('No loadouts found. Use "add loadout" to initialize the list.')


def optimize_loadout():
    '''Optimize a chosen loadout'''
    loadouts = backpack.get_loadouts()
    for index, loadout in enumerate(loadouts):
        print('  %s] %s' % (index, loadout.name))
    index = int(input('(Enter the loadout number): '))
    loadout = loadouts[index]

    try:
        loadout = backpack.optimize(loadout)
        inspect_loadout(loadout=loadout)
    except GearNotFound as error:
        print(error)


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
    'inspect': {
        #agent
        #item
        'loadout': inspect_loadout
    },
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
