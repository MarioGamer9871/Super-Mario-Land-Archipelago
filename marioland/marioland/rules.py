from worlds.generic.Rules import set_rule


def set_rules(world):
    menu = world.get_region("Menu")

    for level in [
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
    ]:
        entrance = next(
            entrance
            for entrance in menu.exits
            if entrance.connected_region.name == level
        )

        set_rule(
            entrance,
            lambda state, level=level:
                state.has(f"World {level}", world.player)
        )