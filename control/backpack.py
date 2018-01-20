'''The backpack and inventory controller'''


from model.backpack import Gear, Loadout
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
    'Masks': Gear
}


def add_gear(name, slot, firearms):
    '''Add a new gear item to the backpack'''
    new_gear = Gear(name, slot, firearms)
    INVENTORY.append(new_gear)
    cache.put(INVENTORY, INVENTORY_CACHE)
    return True


def add_loadout(name):
    '''Add a loadout to the backpack'''
    new_loadout = Loadout(name)
    LOADOUTS.append(new_loadout)
    cache.put(LOADOUTS, LOADOUT_CACHE)
    return True


def get_items():
    '''Returns the current inventory'''
    return INVENTORY


def get_loadouts():
    '''Returns the current loadouts'''
    return LOADOUTS
