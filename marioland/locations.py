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

class MarioLandLocation(Location):
    game = "Super Mario Land"