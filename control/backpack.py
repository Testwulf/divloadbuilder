'''The backpack and inventory controller'''


import random

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
    'Masks': Gear,
    'Knee Pads': Gear,
    'Backpack': Gear,
    'Gloves': Gear,
    'Holster': Gear
}


def add_gear(name, slot, armor, firearms, stamina, electronics):
    '''Add a new gear item to the backpack'''
    duplicate = False
    for existing_gear in INVENTORY:
        if name == existing_gear.name:
            duplicate = True
            break

    if not duplicate:
        new_gear = Gear(name, slot, armor, firearms, stamina, electronics)
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

    best_score = score_loadout(loadout)

    run_limit = 20
    runs = 0
    while runs < run_limit:

        test_loadout = Loadout(loadout.name)
        test_loadout.slots = dict(loadout.slots)

        for slot in loadout.slots:
            gear = test_loadout.slots[slot]

            slot_items = get_items(slot)
            if not slot_items:
                raise GearNotFound('No gear found for slot %s' % slot)

            if gear is None:
                # No item has been assigned, so choose one to start
                # TODO: Place a selection policy here
                gear = slot_items[0]
                test_loadout.slots[slot] = gear.name
            else:
                # Found an item, replace with a random selection
                random_gear = random.choice(slot_items)
                test_loadout.slots[slot] = random_gear.name

        new_score = score_loadout(test_loadout)
        if new_score > best_score:
            best_score = new_score
            update_loadout(test_loadout)
            loadout = test_loadout

        runs += 1
        #TODO: Place output feedback here

    return loadout


def score_loadout(loadout):
    '''Calculate a score for the given loadout'''
    score = 0

    for slot in loadout.slots:
        gear_name = loadout.slots[slot]

        if gear_name is not None:
            gear = get_item(gear_name)

            score += gear.armor / loadout.weights['armor']

            score += gear.firearms / loadout.weights['firearms']
            score += gear.firearms / loadout.weights['stamina']
            score += gear.electronics / loadout.weights['electronics']

    return score


def update_loadout(loadout):
    '''Update a given loadout in the cache'''
    for existing_loadout in LOADOUTS:
        if loadout.name == existing_loadout.name:
            existing_loadout = loadout
            cache.put(LOADOUTS, LOADOUT_CACHE)
            break
