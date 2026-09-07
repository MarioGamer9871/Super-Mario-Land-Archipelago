from worlds.generic.Rules import set_rule


def set_rules(world):
    # 1-1 is available from the beginning.

    set_rule(
        world.get_region("1-2"),
        lambda state: state.has("World 1-2", world.player)
    )

    set_rule(
        world.get_region("1-3"),
        lambda state: state.has("World 1-3", world.player)
    )

    set_rule(
        world.get_region("2-1"),
        lambda state: state.has("World 2-1", world.player)
    )

    set_rule(
        world.get_region("2-2"),
        lambda state: state.has("World 2-2", world.player)
    )

    set_rule(
        world.get_region("2-3"),
        lambda state: state.has("World 2-3", world.player)
    )

    set_rule(
        world.get_region("3-1"),
        lambda state: state.has("World 3-1", world.player)
    )

    set_rule(
        world.get_region("3-2"),
        lambda state: state.has("World 3-2", world.player)
    )

    set_rule(
        world.get_region("3-3"),
        lambda state: state.has("World 3-3", world.player)
    )

    set_rule(
        world.get_region("4-1"),
        lambda state: state.has("World 4-1", world.player)
    )

    set_rule(
        world.get_region("4-2"),
        lambda state: state.has("World 4-2", world.player)
    )

    set_rule(
        world.get_region("4-3"),
        lambda state: state.has("World 4-3", world.player)
    )