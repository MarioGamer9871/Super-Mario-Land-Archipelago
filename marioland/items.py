from BaseClasses import Item, ItemClassification

ITEM_NAME_TO_ID = {
    "Coin" : 1,

    "World 1-2": 12,
    "World 1-3": 13,

    "World 2-1": 21,
    "World 2-2": 22,
    "World 2-3": 23,

    "World 3-1": 31,
    "World 3-2": 32,
    "World 3-3": 33,

    "World 4-1": 41,
    "World 4-2": 42,
    "World 4-3": 43,
}


#List of ALL Filler Items
FILLER_ITEMS = [
    "Coin",
]


class MarioLandItem(Item) :
    game = "Super Mario Land"

ITEM_CLASSIFICATIONS = {
    "Coin": ItemClassification.filler,

    "World 1-2": ItemClassification.progression,
    "World 1-3": ItemClassification.progression,

    "World 2-1": ItemClassification.progression,
    "World 2-2": ItemClassification.progression,
    "World 2-3": ItemClassification.progression,

    "World 3-1": ItemClassification.progression,
    "World 3-2": ItemClassification.progression,
    "World 3-3": ItemClassification.progression,

    "World 4-1": ItemClassification.progression,
    "World 4-2": ItemClassification.progression,
    "World 4-3": ItemClassification.progression
}

def create_item(world, name: str):
    return MarioLandItem(
        name,
        ITEM_CLASSIFICATIONS[name],
        world.item_name_to_id[name],
        world.player
    )

def create_items(world) -> None:
    world.multiworld.itempool += [
        world.create.item("Coin"),

        world.create.item("World 1-2"),
        world.create.item("World 1-3"),

        world.create.item("World 2-1"),
        world.create.item("World 2-2"),
        world.create.item("World 2-3"),

        world.create.item("World 3-1"),
        world.create.item("World 3-2"),
        world.create.item("World 3-3"),

        world.create.item("World 4-1"),
        world.create.item("World 4-2"),
        world.create.item("World 4-3")
    ]