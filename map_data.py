"""
map_data.py

Stores tile-based map data for the game.
We define a small 10x8 (width x height) grid with tile types:
 - 0 = normal grass
 - 1 = research station
 - 2 = production site
"""

TILE_MAP = [
    [0,0,0,0,0,0,2,0,0,0],
    [0,1,0,0,0,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,2],
    [0,0,0,0,2,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,2,0,0,0,0,0,0,1,0],
    [0,0,0,0,1,0,0,2,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]

# 10 columns wide x 8 rows tall
MAP_WIDTH = 10
MAP_HEIGHT = 8
TILE_SIZE = 64   # each tile is 64x64 pixels
