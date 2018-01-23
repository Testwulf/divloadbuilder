'''The backpack and inventory controller'''


import copy
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


def delete_item(name):
    '''Delete a given item from inventory'''
    new_inventory = [item for item in INVENTORY if name != item.name]

    INVENTORY.clear()
    INVENTORY.extend(new_inventory)

    loadouts = get_loadouts()
    for loadout in loadouts:
        for slot in loadout.slots:
            gear_name = loadout.slots[slot]
            if name == gear_name:
                loadout.slots[slot] = None
                update_loadout(loadout)

    cache.put(INVENTORY, INVENTORY_CACHE)


def get_item(name):
    '''Returns the item information for a given name'''
    item = None
    for gear in INVENTORY:
        if name == gear.name:
            item = gear
            break

    if item is None:
        raise GearNotFound('No item found by name: %s' % name)

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

    run_limit = 20000
    runs = 0
    while runs < run_limit:

        test_loadout = copy.deepcopy(loadout)

        random_slot = random.choice(list(loadout.slots.keys()))

        slot_items = get_items(random_slot)
        if not slot_items:
            raise GearNotFound('No gear found for slot %s' % random_slot)

        gear = random.choice(slot_items)
        test_loadout.slots[random_slot] = gear.name

        new_score = score_loadout(test_loadout)
        if new_score > best_score:
            best_score = new_score
            update_loadout(test_loadout)
            loadout = test_loadout
        #TODO Place simulated annealing check here

        runs += 1
        #TODO: Place output feedback here

    update_loadout(loadout)

    return loadout


def score_item(loadout, item):
    '''Calculate a score for a given item using a given loadout weights'''
    score = 0

    armor_score = item.armor * loadout.weights['armor']
    score += armor_score

    target_firearms = item.firearms * loadout.weights['firearms']
    target_stamina = item.stamina * loadout.weights['stamina']
    target_electronics = item.electronics * loadout.weights['electronics']

    score += target_firearms + target_stamina + target_electronics

    return score

def score_loadout(loadout):
    '''Calculate a score for the given loadout'''
    score = 0

    for slot in loadout.slots:
        gear_name = loadout.slots[slot]

        if gear_name is not None:
            gear = get_item(gear_name)
            score += score_item(loadout, item)

    return score


def update_loadout(loadout):
    '''Update a given loadout in the cache'''
    remove_loadout = None
    for existing_loadout in LOADOUTS:
        if loadout.name == existing_loadout.name:
            remove_loadout = existing_loadout
            break

    if remove_loadout is not None:
        LOADOUTS.remove(remove_loadout)
    LOADOUTS.append(loadout)
    cache.put(LOADOUTS, LOADOUT_CACHE)
