from typing import Dict

from BaseClasses import Item, MultiWorld
from worlds.AutoWorld import World

from .items import (
    MarioLandItem,
    ITEM_NAME_TO_ID,
    create_item as create_mario_land_item,
)
from .locations import MarioLandLocation, LOCATION_NAME_TO_ID
from .regions import LEVELS, ITEMLEVELS, create_regions
from .rules import set_rules


class MarioLandWorld(World):
    """
    Archipelago implementation for Super Mario Land.
    """

    game = "Super Mario Land"

    topology_present = True

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    item_name_groups = {
        "Worlds": {
            "World 1-1",
            "World 1-2",
            "World 1-3",
            "World 2-1",
            "World 2-2",
            "World 2-3",
            "World 3-1",
            "World 3-2",
            "World 3-3",
            "World 4-1",
            "World 4-2",
            "World 4-3",
        }
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        create_regions(self)

        for level in LEVELS:
            region = self.multiworld.get_region(level, self.player)

            location_name = f"{level} Clear"
            location_id = LOCATION_NAME_TO_ID[location_name]

            region.locations.append(
                MarioLandLocation(
                    self.player,
                    location_name,
                    location_id,
                    region
                )
            )

    def create_items(self):
        for name in ITEM_NAME_TO_ID:
            if name.startswith("World "):
                self.multiworld.itempool.append(self.create_item(name))

        self.multiworld.itempool.append(self.create_item("Coin"))

    def create_item(self, name: str) -> Item:
        return create_mario_land_item(self, name)

    def item_classification(self, name: str):
        return self.item_name_to_id[name] and \
            __import__("BaseClasses")

    def set_rules(self) -> None:
        set_rules(self)

    def set_completion_rules(self) -> None:
        self.multiworld.completion_condition[
            self.player
        ] = lambda state: state.can_reach(
            "4-3 Clear",
            "Location",
            self.player
        )

    def fill_slot_data(self) -> Dict:
        return {}