# What Should I Do Next?

This instruction is useful when you are asked what to do next. Some examples of such questions might be:

    - What should I do next?
    - Where should I go now?
    - What should I do?
    - What now?
    - Help!
    - I'm not sure what to do next.

First check the RAM contents of address 0x00001C to see if we are in battle. If we are in battle, give advice on how to win the battle by checking the following memory addresses to see which enemies we are fighting, and give advice from the Battle Hints document, making sure to communicate the strengths, weaknesses, spells and special abilities of the enemies:

    - 0x006BE4: monster 1 type
    - 0x006BF8: monster 2 type
    - 0x006C0C: monster 3 type
    - 0x006C20: monster 4 type
    - 0x006C34: monster 5 type
    - 0x006C48: monster 6 type
    - 0x006C5C: monster 7 type
    - 0x006C70: monster 8 type
    - 0x006C84: monster 9 type

If we are not in battle, check the contents of the following memory addresses to see which items we have in our inventory. This is an ordered list (the order the items are acquired in the game). By paying attention to the LAST item in the list that we have, we know which item the adventurer needs to find next. Give advice from Final Fantasy (NES version) walkthroughs on the one to find next.

    - 0x006021: lute
    - 0x006022: crown
    - 0x006023: crystal
    - 0x006024: herb
    - 0x006025: mystic key
    - 0x006026: TNT
    - 0x006029: ruby
    - 0x00602A: rod
    - 0x006035: earth orb
    - 0x006031: canoe
    - 0x00602B: floater
    - 0x006032: fire orb
    - 0x00602D: tail
    - 0x00602F: bottle
    - 0x006030: oxyale
    - 0x006033: water orb
    - 0x006028: slab
    - 0x00602C: chime
    - 0x00602E: cube
    - 0x006027: adamant
    - 0x006034: wind orb