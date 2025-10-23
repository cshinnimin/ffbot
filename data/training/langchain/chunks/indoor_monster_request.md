# Requesting Nearby Indoor or Underworld Monsters

If we are in a castle, town or dungeon, you will need to make a request to the bot app with the following format:

```
{"required_services": {
    "bestiary": {
        "location": "<location>"
    }
}}
```

## Determining <location>

* <location> is a lowercase snake of the location name with symbols removed, comma, floor, all wrapped in brackets (example `(temple_of_fiends_present,1F)`)