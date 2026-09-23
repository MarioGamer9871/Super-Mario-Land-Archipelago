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
    Choose whether to add power up unlocks into the item pool:
    """
    display_name = "Randomize Power Ups?"

class VehicleSetting(Toggle):
    """
    Choose whether to add the vehicles in 2-3 and 4-3 into the item pool:
    """
    display_name = "Randomize Vehicles?"

@dataclass
class MarioLandOptions(PerGameCommonOptions):
    starting_lives: StartingLives
    power_up_setting: PowerUpSetting
    vehicle_setting: VehicleSetting
