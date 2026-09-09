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

        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True

        # 1-1 is always unlocked.
        ctx.unlocked_levels = {"1-1"}

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            values = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0x33, 1, "HRAM"),  # FFB3 - Game State
                    (0x34, 1, "HRAM"),  # FFB4 - World/Level
                    (0x64, 1, "HRAM"),  # FFE4 - Level Index
                ],
            )

            game_state = values[0][0]
            world_level = values[1][0]
            level_index = values[2][0]


            current_level = get_level_from_values(
                world_level,
                level_index
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

            if game_state == 15:
                # Enable Level Select
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (0x1A, [2], "HRAM"),
                    ],
                )

 

            else:
                # We've left the title screen
                ctx.level_select_initialized = False

                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (0x1A, [0], "HRAM"),
                    ],
                )

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

            if item_name == "Coin":
                ctx.coins_to_add = getattr(ctx, "coins_to_add", 0) + 1

                print(
                    f"Received Coin! "
                    f"Coins waiting to add: {ctx.coins_to_add}"
                )

                continue