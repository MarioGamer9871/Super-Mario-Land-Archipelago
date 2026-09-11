from typing import Dict

from BaseClasses import Item, MultiWorld
from worlds.AutoWorld import World

from .items import (
    MarioLandItem,
    ITEM_NAME_TO_ID,
    FILLER_ITEMS,
    create_item as create_mario_land_item,
)
from .locations import MarioLandLocation, LOCATION_NAME_TO_ID
from .regions import LEVELS, ITEMLEVELS, create_regions
from .rules import set_rules
from rule_builder.rules import CanReachLocation


#Reigon Logic
LEVEL_LOCATIONS = {
    "1-1": [
        "1-1 Clear",
        "1-1 Secret Area 1",
        "1-1 Secret Area 2",
    ],
    "1-2": [
        "1-2 Clear",
    ],
    "1-3": [
        "1-3 Clear",
        "1-3 Secret Area 1",
        "1-3 Secret Area 2",
    ],
    "2-1": [
        "2-1 Clear",
        "2-1 Secret Area 1",
        "2-1 Secret Area 2",
    ],
    "2-2": [
        "2-2 Clear",
        "2-2 Secret Area 1",
        "2-2 Secret Area 2",
    ],
    "2-3": [
        "2-3 Clear",
    ],
    "3-1": [
        "3-1 Clear",
        "3-1 Secret Area 1",
        "3-1 Secret Area 2",
    ],
    "3-2": [
        "3-2 Clear",
        "3-2 Secret Area 1",
        "3-2 Secret Area 2",
    ],
    "3-3": [
        "3-3 Clear",
        "3-3 Secret Area 1",
        "3-3 Secret Area 2",
    ],
    "4-1": [
        "4-1 Clear",
        "4-1 Secret Area 1",
        "4-1 Secret Area 2",
    ],
    "4-2": [
        "4-2 Clear",
        "4-2 Secret Area 1",
        "4-2 Secret Area 2",
    ],
    "4-3": [
        "4-3 Clear",
    ],
}



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


    #Compile Logic and create Reigons
    def create_regions(self) -> None:
        create_regions(self)

        for level in LEVELS:
            region = self.multiworld.get_region(level, self.player)

            for location_name in LEVEL_LOCATIONS[level]:
                location_id = LOCATION_NAME_TO_ID[location_name]

                region.locations.append(
                    MarioLandLocation(
                        self.player,
                        location_name,
                        location_id,
                        region
                    )
                )


    #Compile and Create Items
    def create_items(self):
        # Progression items
        for name in ITEM_NAME_TO_ID:
            if name.startswith("World "):
                self.multiworld.itempool.append(
                    self.create_item(name)
                )

        # Fill remaining locations with filler items
        remaining = len(LOCATION_NAME_TO_ID) - len(self.multiworld.itempool)

        for i in range(remaining):
            filler_name = FILLER_ITEMS[i % len(FILLER_ITEMS)]

            self.multiworld.itempool.append(
                self.create_item(filler_name)
            )



    def create_item(self, name: str) -> Item:
        return create_mario_land_item(self, name)

    def item_classification(self, name: str):
        return self.item_name_to_id[name] and \
            __import__("BaseClasses")

    def set_rules(self) -> None:
        set_rules(self)
        self.set_completion_rule(
            lambda state: state.can_reach(
                "4-3 Clear",
                "Location",
                self.player,
            )
        )

    def fill_slot_data(self) -> Dict:
        return {}