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
        armor = int(input('How much armor does it have? '))
        firearms = int(input('What Firearms bonus does it have? '))
        stamina = int(input('What Stamina bonus does it have? '))
        electronics = int(input('What Electronics bonus does it have? '))
        if backpack.add_gear(name, slot, armor, firearms, stamina, electronics):
            print('%s added to the backpack' % name)
        else:
            print('An item by that name already exists. Use a new name.')


def add_loadout():
    '''Add a loadout to the stash'''
    name = input('What should this loadout be named? ')
    if backpack.add_loadout(name):
        print('%s loadout added to backpack' % name)


def delete_item():
    '''Delete an item from the inventory'''
    print('Which slot?')
    key_list = []
    for index, possible_slot in enumerate(backpack.SLOTS):
        key_list.append(possible_slot)
        print(' %s] %s' % (index, possible_slot))
    slot = int(input('(Enter the slot number): '))
    slot = key_list[slot]

    item_list = backpack.get_items(slot_filter=slot)
    if item_list:
        print('Which item?')
        for index, item in enumerate(item_list):
            print(' %s] %s' % (index, item.name))
        index = int(input('(Enter the item number): '))
        item = item_list[index]

        backpack.delete_item(item.name)
        print(item.name, ' removed from inventory')
    else:
        print('No items found in that slot category.')


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

    total_armor = 0
    total_firearms = 0
    total_stamina = 0
    total_electronics = 0

    print('Name: %s' % loadout.name)
    if loadout.slots is not None:
        print('Gear:')
        for slot in loadout.slots:
            gear_name = loadout.slots[slot]
            gear = backpack.get_item(gear_name)

            total_armor += gear.armor
            total_firearms += gear.firearms
            total_stamina += gear.stamina
            total_electronics += gear.electronics

            print('  %s] %s' % (slot, gear.name))
            print('    Armor: %s' % gear.armor)
            print('    Firearms: %s' % gear.firearms)
            print('    Stamina: %s' % gear.stamina)
            print('    Electronics: %s' % gear.electronics)

        print('Total:')
        print('  Armor: %s' % total_armor)
        print('  Firearms: %s' % total_firearms)
        print('  Stamina: %s' % total_stamina)
        print('  Electronics: %s' % total_electronics)

        print('Score: %s' % round(backpack.score_loadout(loadout), 2))
    else:
        print('No gear assigned to this loadout. Run "optimize loadout" to determine gear.')



def list_items():
    '''List all items in the inventory'''

    item_list = None

    print('Which slot?')
    key_list = []
    for index, possible_slot in enumerate(backpack.SLOTS):
        key_list.append(possible_slot)
        print(' %s] %s' % (index, possible_slot))
    slot = input('(Enter the slot number, Blank = All items): ')
    if slot:
        slot = key_list[int(slot)]
        item_list = backpack.get_items(slot_filter=slot)
    else:
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
    'delete': {
        #agent:
        'item': delete_item
        #loadout:
    },
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
