# Querying the Ram Read Request Module

* If you query the RRM, the message must have the format:
```
{"required_ram_contents": ["<ram_address_1>", "<ram_address_2>" ...]}
```

* If you query the RRM, it sends a response back in the format:
```
{"ram_contents": {"<ram_address_1>": "value1", "<ram_address_2>": "value2" ...}}
```