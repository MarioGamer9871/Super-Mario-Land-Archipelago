from dataclasses import dataclass
 
from Options import (
    Toggle,
    DefaultOnToggle,
    Range,
    Choice,
    DeathLink,
    PerGameCommonOptions,
    OptionGroup,
)
 
class StartingLives(Range):
    """The number of lives you start with after selecting a level from the title screen."""
    display_name = "Starting Lives"
    range_start = 1
    range_end = 99
    default = 2


class PowerUpSetting(Toggle):
    """
    Adds power up unlocks into the item pool:
    """
    display_name = "Randomize Power Ups?"

class VehicleSetting(Toggle):
    """
    Adds the vehicles in 2-3 and 4-3 into the item pool
    """
    display_name = "Randomize Vehicles?"

class BonusGameChecks(Toggle):
    """
    Adds each end of level bonus game as a location
    """
    display_name = "Bonus Game Checks?"

class Heartsanity(Toggle):
    """
    Adds each 1UP Heart as a location, NOTE: THIS REQUIRES AN EXTRA LUA SCRIPT IN ORDER TO WORK. SEE README FOR MORE INFO
    """
    display_name = "Heartsanity"


@dataclass
class MarioLandOptions(PerGameCommonOptions):
    starting_lives: StartingLives
    power_up_setting: PowerUpSetting
    vehicle_setting: VehicleSetting
    bonus_game_checks: BonusGameChecks
    heartsanity: Heartsanity
