# Overworld Monster Encounter Grid

Use these instructions if to determine your overworld grid cell. Your current grid cell determines which monsters it is possible to encounter. This is only relevant if we are outside. If we are in a town, castle or dungeon, a different system is used to determine which monsters may be encountered.

## Coordinate System: How Cells Work

The overworld is divided into a grid of **8 columns (X: 0–7)** and **8 rows (Y: 0–7)**. Each cell is a square section of the map.

- **(x, y)** format is used, where **x = horizontal (left to right)** and **y = vertical (top to bottom)**
- **(0,0)** is the top-left; **(7,7)** is the bottom-right.

## Finding Your Cell

1. The world map is 256x256 tiles.
2. Each grid region is 32x32 tiles.
3. If you know your in-game tile position:
    - **Grid X = floor(tile_x / 32)**
    - **Grid Y = floor(tile_y / 32)**
    - Example: Tile (50, 110) → (1, 3)
