'''The backpack and inventory controller'''


from model.backpack import Item


# Master Inventory List
INVENTORY = []


def add_item(name):
    '''Add a new item with the given name to the backpack'''
    new_item = Item(name)
    INVENTORY.append(new_item)
    return True
