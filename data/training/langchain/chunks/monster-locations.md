# Monster Locations

This instruction is useful if you are asked questions about locations of monsters. For example, if asked:

    - Which enemies are nearby?
    - Which monsters are close?
    - Are any <monster_type>s around here?
    - Where can I find <monster_type>s?

## Bestiary Request

Use these instructions for determining which monsters are present in a known location. To know the adventurers location for the purpose of determining nearby monsters, you need to know whether you are outdoors, or in a town/dungeon. Check address 0x0000F8 to know this.

    * If in a town/dungeon:
        
        1. Check 0x000048 to know which floor we are on.
        2. Call the get_monsters_by_location tool with the town/dungeon name translated to lowercase snake, followed by a comma, followed by the floor code, all surrounded in brackets as the input. Eg: 
            "Castle of Ordeal" on floor "2F" should have input `{"location": "(castle_of_ordeal,2f)"}`
            "Ice Cave" on floor "3B" should have input `{"location": "(ice_cave,3b)"}`

    * If not in a town/dungeon:  
        1. Check 0x000042 to determine if we are on land, in the ship, in the canoe or in the airship. If we are in the airship, just tell the adventurer we are safe from enemy encounters in the airship.
        2. If we are not in the airship, check 0x000027 for our overworld X position and 0x000028 for our overworld Y position. 
        3. Translate our X,Y coordinates to a "cell". The world map is 256x256 tiles. Each cell is 32x32 tiles, forming an 8x8 grid of cells.
            Cell X = floor(tile_x / 32)
            Cell Y = floor(tile_y / 32)
            Example: Tile (50, 110) → Cell (1, 3)
        4. Call the get_monsters_by_location tool with the cell as the input, eg: `{"location": "(1,3)"}`.

## Reverse Bestiary Request

Use these instructions for determining which location(s) a given monster can be found at.

    1. Call the get_locations_by_monster tool using an array of monster names as the input, eg: `{"monsters": ["Cerebus", "WzOgre"]}`.

Do not include references to overworld cells in your final answer. Instead, use adjacent overworld landmarks to describe locations of the enemies being asked about. For example, if the tool tells you an Imp can be found at "(4,4)", do not respond with "Imps are found near (4,4)", respond with "Imps are found near Cornelia" (since Cornelia is in cell 4,4). Note: if a landmark is not IN a cell OR IMMEDIATELY ADJACENT, it is not considered "close". The whole grid is only 8x8, so two cells of distance is NOT close.

