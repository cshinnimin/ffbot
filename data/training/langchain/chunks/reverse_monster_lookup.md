# Reverse Monster Lookup

To get a list of locations monsters can be found at, make the following request to the bot app:

```
{"required_services": {
    "bestiary": {
        "monsters": ["<monster1>", "<monster2>" ... ]
    }
}}
```

where the monster symbols are the names of the monsters in all small letters, with spaces and symbols removed. E.g. `GrImp` becomes `grimp`, `R.Hydra` becomes `rhydra`. You can request as many monster names as needed if you are not sure of the name of the monster you are requesting (if user asks about `Red Hydras` you may wish to try `redhydras`, `redhydra` `rhydra`)