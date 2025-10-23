# Requesting Nearby Overworld Monsters

If we are outside on the overworld, not in a castle, town or dungeon, first consult the Overworld Monster Encounter Grid document to determine your current overworld grid cell. Then you will need to make a request to the bot app with the following format:

```
{"required_services": {
    "bestiary": {
        "location": "<location>"
    }
}}
```

## Determining <location>

* If we are on land, <location> is the overworld grid cell coordinate, like `(4,4)`
* If we are in the canoe, <location> is `(canoe,north)` if we are in the cell with a Y value of 2 or less, otherwise `(canoe,south)`
* If we are in the ship, <location> is `(ocean)`
* If we are in the airship, we are safe from enemy encounters and we do not need to make the request to the bot app