# creating tiles
from typing import Tuple
import numpy as np # type: ignore

# creates data type that numpy can use
graphic_dt = np.dtype(
    [
        ('ch', np.int32), # character in integer format
        ('fg', '3B'), # foreground color
        ('bg', '3B') # background color
    ]
)

# Tile structure used for statically defined tile data
tile_dt = np.dtype(
    [
        ('walkable', bool), # True if tile can be walked over
        ('transparent', bool), # True if tile doesn't block FOV
        ('dark', graphic_dt), # graphics for when tile isnt in FOV
        ('light', graphic_dt) # graphics for when tile is in FOV
    ]
)

def new_tile(
    *, # Enforces use of keywords
    walkable:int,
    transparent:int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int,int,int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int,int,int]],
) -> np.ndarray:
    # helper function for defining indiviual tile types
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)



# SHROUD represents unseen and unexplored tiles
SHROUD = np.array((ord(' '), (255,255,255),(0,0,0)), dtype=graphic_dt)

floor = new_tile(
    walkable = True, 
    transparent=True, 
    dark=(ord(" "), (255,255,255), (150,50,50)), 
    light=(ord(' '), (255,255,255),(230,180,50))
    )
wall = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord('+'), (255,255,255), (100,0,0)),
    light=(ord('+'), (255,255,255), (160,110,50))
    )