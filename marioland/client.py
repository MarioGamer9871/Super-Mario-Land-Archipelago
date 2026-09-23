from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


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


LEVEL_VALUES = {
    "1-1": (0x11, 0),
    "1-2": (0x12, 1),
    "1-3": (0x13, 2),
    "2-1": (0x21, 3),
    "2-2": (0x22, 4),
    "2-3": (0x23, 5),
    "3-1": (0x31, 6),
    "3-2": (0x32, 7),
    "3-3": (0x33, 8),
    "4-1": (0x41, 9),
    "4-2": (0x42, 10),
    "4-3": (0x43, 11),
}


#Secret Area Values W1-W3 (0x74)
SECRET_AREAS = {
    "1-1": {
        1: ("1-1 Secret Area 1", 111),
        2: ("1-1 Secret Area 2", 112),
    },

    "1-3": {
        2: ("1-3 Secret Area 1", 131),
        1: ("1-3 Secret Area 2", 132),
    },

    "2-1": {
        1: ("2-1 Secret Area 1", 211),
        2: ("2-1 Secret Area 2", 212),
    },

    "2-2": {
        1: ("2-2 Secret Area 1", 221),
        2: ("2-2 Secret Area 2", 222),
    },

    "3-1": {
        2: ("3-1 Secret Area 1", 311),
        1: ("3-1 Secret Area 2", 312),
    },

    "3-2": {
        1: ("3-2 Secret Area 1", 321),
        2: ("3-2 Secret Area 2", 322),
    },

    "3-3": {
        1: ("3-3 Secret Area 1", 331),
        2: ("3-3 Secret Area 2", 332),
    },
}

#Secret Area Values W4 (0x75)
WORLD_4_SECRET_AREAS = {
    "4-1": {
        3: ("4-1 Secret Area 1", 411),
        22: ("4-1 Secret Area 2", 412),
    },

    "4-2": {
        6: ("4-2 Secret Area 1", 421),
        18: ("4-2 Secret Area 2", 422),
    },
}

#Find unlocked levels
def get_next_unlocked_level(ctx, current_level):
    if current_level not in LEVEL_VALUES:
        return None

    current_index = LEVEL_VALUES[current_level][1]

    for level, (_, index) in LEVEL_VALUES.items():
        if index > current_index and level in ctx.unlocked_levels:
            return level

    for level, (_, index) in LEVEL_VALUES.items():
        if index < current_index and level in ctx.unlocked_levels:
            return level

    return None



def get_previous_level(level: str):
    """Return the level immediately before the given level."""
    index = LEVEL_VALUES[level][1]

    if index == 0:
        return None

    for name, (_, level_index) in LEVEL_VALUES.items():
        if level_index == index - 1:
            return name

    return None


def get_level_from_values(world_level: int, level_index: int):
    """Convert FFB4/FFE4 values into a level name."""
    for level, (world_value, index_value) in LEVEL_VALUES.items():
        if world_level == world_value and level_index == index_value:
            return level

    return None


class MarioLandClient(BizHawkClient):
    game = "Super Mario Land"
    system = "GB"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            system = await bizhawk.get_system(ctx.bizhawk_ctx)

            if system != "GB":
                return False


            rom_hash = await bizhawk.get_hash(ctx.bizhawk_ctx)

            valid_hashes = {
                "3a4ddb39b234a67ffb361ee7abc3d23e0a8b1c89", #1.0 Rom
                "418203621b887caa090215d97e3f509b79affd3e", #1.1 Rom
            }

            if rom_hash.lower() not in valid_hashes:
                return False


        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True

        # 1-1 is always unlocked.
        ctx.unlocked_levels = {"1-1"}

        ctx.starting_lives_set = False

        ctx.power_up_level = 0
        ctx.star_unlocked = False 

        ctx.has_marine_pop = False
        ctx.has_sky_pop = False

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:

            values = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x33, 1, "HRAM"),  # FFB3 - Game State
                    (0x34, 1, "HRAM"),  # FFB4 - World/Level
                    (0x64, 1, "HRAM"),  # FFE4 - Level Index
                    (0x74, 1, "HRAM"),  # Secret area value
                    (0x75, 1, "HRAM"),  # World 4 secret area value
                ],
            )

            game_state = values[0][0]
            world_level = values[1][0]
            level_index = values[2][0]
            secret_area_value = values[3][0]
            world_4_secret_value = values[4][0]

            #Assign power up values
            powerup_values = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x19, 1, "HRAM"),  # FF99 - Powerup Status
                    (0x35, 1, "HRAM"),  # FFB5 - Has Superball
                ],
            )
 
            powerup_status = powerup_values[0][0]
            has_superball = powerup_values[1][0]


            current_level = get_level_from_values(
                world_level,
                level_index
            )

            # ---------------------------------------------------------
            # Vehicle enforcement
            # ---------------------------------------------------------
            if ctx.slot_data and ctx.slot_data.get("vehicle_setting"):
                if game_state == 13:
                    blocked = False

                    if current_level == "2-3" and not getattr(
                        ctx, "has_marine_pop", False
                    ):
                        blocked = True
                        print("Blocked Marine Pop entry (not unlocked)")

                    elif current_level == "4-3" and not getattr(
                        ctx, "has_sky_pop", False
                    ):
                        blocked = True
                        print("Blocked Sky Pop entry (not unlocked)")

                    if blocked:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (0x33, [0], "HRAM"),  # FFB3 - Game State
                                (0x1A15, [0], "WRAM"), # Lives to 0
                            ],
                        )


            # ---------------------------------------------------------
            # Power-up enforcement
            # ---------------------------------------------------------
            if ctx.slot_data and ctx.slot_data.get("power_up_setting"):
                power_up_level = getattr(ctx, "power_up_level", 0)
                star_unlocked = getattr(ctx, "star_unlocked", False)
 
                power_up_writes = []
 
                # Block growing into "big" entirely until the first
                # Progressive PowerUp has been received.
                if power_up_level < 1 and powerup_status in (0x01, 0x02):
                    power_up_writes.append((0x19, [0x03], "HRAM"))
 
                # "Big" is allowed once unlocked, but strip the
                # Superball flag until the second Progressive
                # PowerUp has been received.
                if power_up_level < 2 and has_superball != 0x00:
                    power_up_writes.append((0x35, [0x00], "HRAM"))
 
                if power_up_writes:
                    await bizhawk.write(ctx.bizhawk_ctx, power_up_writes)
 
                # Cancel Star invincibility if it hasn't been
                # unlocked yet.
                if not star_unlocked:
                    starman_values = await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [
                            (0xD3, 1, "WRAM"),  # C0D3 - Starman Timer
                        ],
                    )
 
                    if starman_values[0][0] != 0x00:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [
                                (0xD3, [0x01], "WRAM"),
                            ],
                        )



            # ---------------------------------------------------------
            # Secret Area Checks
            # ---------------------------------------------------------

            secret_location = None
            secret_location_id = None

            if current_level in SECRET_AREAS:
                # Worlds 1-3 use HRAM 0x74
                area = SECRET_AREAS[current_level].get(secret_area_value)

                if area is not None:
                    secret_location, secret_location_id = area

            elif current_level in WORLD_4_SECRET_AREAS:
                # World 4 uses HRAM 0x75
                area = WORLD_4_SECRET_AREAS[current_level].get(
                    world_4_secret_value
                )

                if area is not None:
                    secret_location, secret_location_id = area


            if secret_location_id is not None:
                if secret_location_id not in ctx.locations_checked:
                    print(
                        f"Entered secret area: {secret_location}"
                    )

                    ctx.locations_checked.add(secret_location_id)

                    await ctx.send_msgs([
                        {
                            "cmd": "LocationChecks",
                            "locations": [secret_location_id],
                        }
                    ])

                    print(
                        f"Sent secret area location check: "
                        f"{secret_location_id}"
                    )




            # ---------------------------------------------------------
            # Level completion
            # ---------------------------------------------------------
            if game_state == 7 and current_level is not None:

                if not getattr(ctx, "completion_handled", False):
                    ctx.completion_handled = True

                    print(f"Completed level: {current_level}")

                    # Location IDs are 11, 12, 13, 21, 22, etc.
                    location_id = int(current_level.replace("-", ""))

                    if location_id not in ctx.locations_checked:
                        ctx.locations_checked.add(location_id)
                        await ctx.send_msgs([
                            {
                                "cmd": "LocationChecks",
                                "locations": [location_id],
                            }
                        ])

                    print(f"Sent location check: {location_id}")

            elif game_state != 6:
                ctx.completion_handled = False



            # ---------------------------------------------------------
            # Game completion
            # ---------------------------------------------------------
            if game_state == 44:

                if not getattr(ctx, "goal_sent", False):
                    ctx.goal_sent = True

                    print("SUPER MARIO LAND COMPLETED!")

                    await ctx.send_msgs([
                        {
                            "cmd": "StatusUpdate",
                            "status": 30,
                        }
                    ])

            elif game_state != 44:
                ctx.goal_sent = False




            ctx.level_select_initialized = False

            # ---------------------------------------------------------
            # Level Select
            # ---------------------------------------------------------
            if game_state == 15:

                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (0x35, [0], "HRAM"),
                        (0x00D7, [5], "WRAM"),
                    ],
                )

                # Freeze the game while we check/fix the selected level.
                await bizhawk.lock(ctx.bizhawk_ctx)

                try:
                    # Enable level select
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [
                            (0x1A, [2], "HRAM"),
                        ],
                    )

                    #Reset starting lives
                    ctx.starting_lives_set = False
 

                    # Read the selection again while the game is frozen
                    select_values = await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [
                            (0x34, 1, "HRAM"),  # FFB4
                            (0x64, 1, "HRAM"),  # FFE4
                        ],
                    )

                    selected_world = select_values[0][0]
                    selected_index = select_values[1][0]

                    selected_level = get_level_from_values(
                        selected_world,
                        selected_index
                    )

                    # If the selected level is locked, immediately replace it
                    if (
                        selected_level is not None
                        and selected_level not in ctx.unlocked_levels
                    ):
                        next_level = get_next_unlocked_level(
                            ctx,
                            selected_level
                        )

                        if next_level is not None:
                            next_world, next_index = LEVEL_VALUES[next_level]

                            print(
                                f"Skipping locked level "
                                f"{selected_level} -> {next_level}"
                            )

                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [
                                    (0x34, [next_world], "HRAM"),
                                    (0x64, [next_index], "HRAM"),
                                ],
                            )

                finally:
                    # Let the game continue.
                    await bizhawk.unlock(ctx.bizhawk_ctx)

            else:
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (0x1A, [0], "HRAM"),
                    ],
                )

                # ---------------------------------------------------------
                # Starting lives
                # ---------------------------------------------------------
                if not getattr(ctx, "starting_lives_set", False):
                    starting_lives = 2
    
                    if ctx.slot_data is not None:
                        starting_lives = ctx.slot_data.get(
                            "starting_lives",
                            starting_lives
                        )
                        
                    # On-screen two-digit lives counter (tens/ones tiles),
                    # same layout as the coin counter.
                    lives_tens = starting_lives // 10
                    lives_ones = starting_lives % 10
                    lives_bcd = (lives_tens << 4) | lives_ones
    
                    # Underlying lives value used by the game's logic.
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [
                            (0x1A15, [lives_bcd], "WRAM"),
                        ],
                    )
    
    
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [
                            (0x1806, [lives_tens], "VRAM"),  # Tens
                            (0x1807, [lives_ones], "VRAM"),  # Ones
                        ],
                    )
    
                    ctx.starting_lives_set = True
    
                    print(f"Set starting lives to {starting_lives}")


            # ---------------------------------------------------------
            # Find current level
            # ---------------------------------------------------------
            current_level = None

            for level, (world_value, index_value) in LEVEL_VALUES.items():
                if world_level == world_value and level_index == index_value:
                    current_level = level
                    break



            # ---------------------------------------------------------
            # Locked level failsafe
            # ---------------------------------------------------------
            if game_state == 0 or game_state == 13 and current_level is not None:
                if current_level not in ctx.unlocked_levels:
                    print(f"LOCKED LEVEL DETECTED: {current_level}")
                    print("Game over!")

                    # Put the game into the death state.
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [
                            (0x1A15, [0], "WRAM"),  # Set Lives to 0
                            (0x33, [1], "HRAM"),  # FFB3 = Game State 1 (dead)
                        ],
                    )


        except bizhawk.RequestFailedError:
            return




        # ---------------------------------------------------------
        # Add received coins
        # ---------------------------------------------------------
        coins_to_add = getattr(ctx, "coins_to_add", 0)

        if coins_to_add > 0:

            values = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x7A, 1, "HRAM"),  # FFFA - Coins
                ],
            )

            coins_bcd = values[0][0]

            # BCD -> decimal
            coins = ((coins_bcd >> 4) * 10) + (coins_bcd & 0x0F)

            # Add received coins
            coins += coins_to_add

            # Maximum coin count
            if coins > 99:
                coins = 99

            # Decimal -> BCD
            new_coins_bcd = ((coins // 10) << 4) | (coins % 10)

            # Update actual coin count
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [
                    (0x7A, [new_coins_bcd], "HRAM"),
                ],
            )

            # Update visual coin count
            tens = coins // 10
            ones = coins % 10

            await bizhawk.write(
                ctx.bizhawk_ctx,
                [
                    (0x1829, [tens], "VRAM"),  # Tens
                    (0x182A, [ones], "VRAM"),  # Ones
                ],
            )

            print(
                f"Added {coins_to_add} coin(s)! "
                f"Total: {coins}"
            )

            ctx.coins_to_add = 0


        

    def on_package(

   
        self,
        ctx: "BizHawkClientContext",
        cmd: str,
        args: dict
    ) -> None:

        #REMOVE
        print(
            f"PACKET: {cmd} | "
            f"INDEX: {args.get('index', 'N/A')} | "
            f"ITEMS: {len(args.get('items', []))}"
        )
        #REMOVE


        if cmd != "ReceivedItems":
            return

        for item in args["items"]:
            item_name = ctx.item_names.lookup_in_game(
                item.item,
                "Super Mario Land"
            )

            print(f"Received item: {item_name}")

            if item_name.startswith("World "):
                level = item_name.replace("World ", "")

                if level in LEVEL_VALUES:
                    ctx.unlocked_levels.add(level)

                    print(f"Unlocked level: {level}")
                    print(
                        f"Unlocked levels: "
                        f"{sorted(ctx.unlocked_levels)}"
                    )

            if item_name == "Progressive Power Up":
                ctx.power_up_level = getattr(ctx, "power_up_level", 0) + 1
 
                print(
                    f"Power-up level increased to {ctx.power_up_level}"
                )
 
                continue
 
            if item_name == "Star":
                ctx.star_unlocked = True
 
                print("Star unlocked")
 
                continue

            if item_name == "Marine Pop":
                ctx.has_marine_pop = True

                print("Marine Pop unlocked")

                continue



            if item_name == "Sky Pop":
                ctx.has_sky_pop = True

                print("Sky Pop unlocked")

                continue


            if item_name == "Coin":
                ctx.coins_to_add = getattr(ctx, "coins_to_add", 0) + 1

                print(
                    f"Received Coin! "
                    f"Coins waiting to add: {ctx.coins_to_add}"
                )

                continue