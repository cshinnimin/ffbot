# Finding Your Overworld Location (Tile Coordinates)

This instruction is useful for any question about the current location of the party. For example, if asked:

    - Am I near <some_location>?
    - Where am I?
    - What is nearby?
    - I'm lost.

To know the adventurers location (tile coordinates) on the overworld map, you need to know the RAM contents of addresses 0x000027 (X position) and 0x000028 (Y position). Ask the read_addresses tool.

## Calculating distance between things

To calculate the distance between two landmarks or between the party and a landmark, use pythagoras theorem. Determine the two entities' locations in terms of X,Y coordinates and use those to perform pythagoras.

## Defining "near"

When describing landmarks and locations relative to one another, remember that the entire world (overworld map) is only 256 x 256 tiles. Therefore:

    - within 20 tiles is "near"
    - over 20 tiles is not "near"

## Give additional context

Explain to the user where the thing is located in relative terms, like "<location> is <x> tiles to the west and <y> tiles to the north".