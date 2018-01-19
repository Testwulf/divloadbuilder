'''The backpack and inventory controller'''


from model.backpack import Item, Gear


# Master Inventory List
INVENTORY = []
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
    return True


def get_items():
    '''Returns the current inventory'''
    return INVENTORY
