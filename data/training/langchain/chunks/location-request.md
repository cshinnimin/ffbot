# Finding Your Overworld Location (Tile Coordinates)

This instruction is useful for any question about the current location of the party. For example, if asked:

    - Am I near <some_location>?
    - Where am I?
    - What is nearby/close?
    - I'm lost.

To know the adventurers location (tile coordinates) on the overworld map, you need to know the RAM contents of addresses 0x000027 (X position) and 0x000028 (Y position). Ask the read_addresses tool. For a more accurate location description, also check address 0x0000F8 to determine if the adventurer is on the overworld map (outside) or in a town or dungeon. If in a town or dungeon, check 0x000048 to know in which town or dungeon as well as on which floor.