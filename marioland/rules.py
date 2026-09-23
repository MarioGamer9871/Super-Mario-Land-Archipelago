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


    if world.options.power_up_setting:
        for location_name in [
            "1-3 Secret Area 2",
            "3-2 Secret Area 1",
        ]:
            location = world.get_location(location_name)
 
            set_rule(
                location,
                lambda state:
                    state.has("Progressive Power Up", world.player)
            )

    if world.options.vehicle_setting:
        for location_name in [
            "2-3 Clear",
        ]:
            location = world.get_location(location_name)
 
            set_rule(
                location,
                lambda state:
                    state.has("Marine Pop", world.player)
            )


    if world.options.vehicle_setting:
        for location_name in [
            "4-3 Clear",
        ]:
            location = world.get_location(location_name)
 
            set_rule(
                location,
                lambda state:
                    state.has("Sky Pop", world.player)
            )