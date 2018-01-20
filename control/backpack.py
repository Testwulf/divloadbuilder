'''The backpack and inventory controller'''


from model.backpack import Gear, GearNotFound, Loadout
from . import cache


# Master Inventory List
INVENTORY_CACHE = 'inventory.pkl'
INVENTORY = []
if cache.exists(INVENTORY_CACHE):
    INVENTORY = cache.get(INVENTORY_CACHE)
# List of saved loadouts
LOADOUT_CACHE = 'loadouts.pkl'
LOADOUTS = []
if cache.exists(LOADOUT_CACHE):
    LOADOUTS = cache.get(LOADOUT_CACHE)
# Possible Gear Slots
SLOTS = {
    'Body Armor': Gear,
    'Knee Pads': Gear,
    'Masks': Gear,
    'Backpack': Gear,
    'Gloves': Gear,
    'Holster': Gear
}


def add_gear(name, slot, firearms):
    '''Add a new gear item to the backpack'''
    duplicate = False
    for existing_gear in INVENTORY:
        if name == existing_gear.name:
            duplicate = True
            break

    if not duplicate:
        new_gear = Gear(name, slot, firearms)
        INVENTORY.append(new_gear)
        cache.put(INVENTORY, INVENTORY_CACHE)

    return not duplicate


def add_loadout(name):
    '''Add a loadout to the backpack'''
    new_loadout = Loadout(name)
    LOADOUTS.append(new_loadout)
    cache.put(LOADOUTS, LOADOUT_CACHE)
    return True


def get_item(name):
    '''Returns the item information for a given name'''
    item = None
    for gear in INVENTORY:
        if name == gear.name:
            item = gear
            break
    return item


def get_items(slot_filter=None):
    '''Returns the current inventory using a filter if provided'''
    item_list = []
    if slot_filter is not None:
        item_list = [item for item in INVENTORY if item.slot == slot_filter]
    else:
        item_list.extend(INVENTORY)

    return item_list


def get_loadouts():
    '''Returns the current loadouts'''
    return LOADOUTS


def optimize(loadout):
    '''Run optimization over a given loadout'''

    if loadout.slots is None:
        loadout.slots = dict(SLOTS)
        for slot in loadout.slots:
            loadout.slots[slot] = None

    for slot in loadout.slots:
        gear = loadout.slots[slot]
        if gear is None:
            # No item has been assigned, so choose one to start
            slot_items = get_items(slot)
            if slot_items:
                # TODO: Place a selection policy here
                gear = slot_items[0]
            else:
                raise GearNotFound('No gear found for slot %s' % slot)

            loadout.slots[slot] = gear.name

    update_loadout(loadout)

    return loadout


def update_loadout(loadout):
    '''Update a given loadout in the cache'''
    for existing_loadout in LOADOUTS:
        if loadout.name == existing_loadout.name:
            existing_loadout = loadout
            cache.put(LOADOUTS, LOADOUT_CACHE)
            break
