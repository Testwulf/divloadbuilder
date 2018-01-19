'''The backpack and inventory controller'''


from model.backpack import Item


# Master Inventory List
INVENTORY = []
# Possible Gear Slots
SLOTS = [
    'Body Armor',
    'Knee Pads',
    'Masks'
]


def add_item(name, slot):
    '''Add a new item with the given name to the backpack'''
    new_item = Item(name, slot)
    INVENTORY.append(new_item)
    return True


def get_items():
    '''Returns the current inventory'''
    return INVENTORY
