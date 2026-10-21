from BaseClasses import Location

LOCATION_NAME_TO_ID = {
    #Levels
    "1-1 Clear": 11,
    "1-2 Clear": 12,
    "1-3 Clear": 13,

    "2-1 Clear": 21,
    "2-2 Clear": 22,
    "2-3 Clear": 23,

    "3-1 Clear": 31,
    "3-2 Clear": 32,
    "3-3 Clear": 33,

    "4-1 Clear": 41,
    "4-2 Clear": 42,
    "4-3 Clear": 43,

    #Secret Areas
    "1-1 Secret Area 1": 111,
    "1-1 Secret Area 2": 112,
    "1-3 Secret Area 1": 131,
    "1-3 Secret Area 2": 132,

    "2-1 Secret Area 1": 211,
    "2-1 Secret Area 2": 212,
    "2-2 Secret Area 1": 221,
    "2-2 Secret Area 2": 222,

    "3-1 Secret Area 1": 311,
    "3-1 Secret Area 2": 312,
    "3-2 Secret Area 1": 321,
    "3-2 Secret Area 2": 322,
    "3-3 Secret Area 1": 331,
    "3-3 Secret Area 2": 332,

    "4-1 Secret Area 1": 411,
    "4-1 Secret Area 2": 412,
    "4-2 Secret Area 1": 421,
    "4-2 Secret Area 2": 422,
}

BONUS_LOCATION_TO_ID = {
    #Bonus Games
    "1-1 Bonus Game": 101,
    "1-2 Bonus Game": 102,
    "1-3 Bonus Game": 103,

    "2-1 Bonus Game": 201,
    "2-2 Bonus Game": 202,
    "2-3 Bonus Game": 203,

    "3-1 Bonus Game": 301,
    "3-2 Bonus Game": 302,
    "3-3 Bonus Game": 303,

    "4-1 Bonus Game": 401,
    "4-2 Bonus Game": 402,
}

HEART_LOCATION_ID = {
    #Heartsanity Locations
    "1-1 1UP Heart": 2111,
    "1-2 1UP Heart 1": 2121,
    "1-2 1UP Heart 2": 2122,
    "1-3 1UP Heart": 2131,

    "2-1 1UP Heart": 2211,
    "2-3 1UP Heart": 2231,

    "3-1 1UP Heart": 2311,
    "3-3 1UP Heart": 2331,

    "4-1 1UP Heart": 2411,
    "4-3 1UP Heart": 2431,
}

class MarioLandLocation(Location):
    game = "Super Mario Land"