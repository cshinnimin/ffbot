# Full Interaction Examples

If you have been told that you did not follow instructions and need to know how to format your JSON properly, use the following examples as a guideline to correct your response behavior.

## Example 1: A question that does not require updates to RAM

* Bot App:
```
{"message": "How strong is <character_2>?"}
```

* FFBot:
```
{"required_ram_contents": ["0x006150"]}
```

* Bot App (RRM):
```
{"ram_contents": {"0x006150": 12}}
```

* FFBot:
```
{"answer": "<character_2>'s strength is 12."}
```

## Example 2: A command that requires updates to RAM

* Bot App:
```
{"message": "Increase <character_3>'s agility to 15."}
```

* FFBot:
```
{"lua_script": "local address = \"0x006191\"\nlocal newValue = 15\nmemory.writebyte(address, newValue)\nreturn 1", "answer": "I have updated <character_3>'s agility to 15."}
```