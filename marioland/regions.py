from BaseClasses import Region


LEVELS = [
    "1-1",
    "1-2",
    "1-3",

    "2-1",
    "2-2",
    "2-3",

    "3-1",
    "3-2",
    "3-3",

    "4-1",
    "4-2",
    "4-3",
]

ITEMLEVELS = [
    "1-2",
    "1-3",

    "2-1",
    "2-2",
    "2-3",

    "3-1",
    "3-2",
    "3-3",

    "4-1",
    "4-2",
    "4-3",
]


def create_regions(world):
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for level in LEVELS:
        region = Region(level, world.player, world.multiworld)
        world.multiworld.regions.append(region)

        menu.connect(region)