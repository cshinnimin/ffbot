# Training Information

[
    {"prompt": "What is character 1's class?", "response": "Character 1's class is [0x006100]"},
    {"prompt": "What is character 1's strength (STR.)?", "response": "Character 1's strength is [0x006110]"},
    {"prompt": "What is character 1's agility (AGL.)?", "response": "Character 1's agility is [0x006111]"},
    {"prompt": "What is character 1's intelligence (INT.)?", "response": "Character 1's intelligence is [0x006112]"},
    {"prompt": "What is character 1's vitality (VIT.)?", "response": "Character 1's vitality is [0x006113]"},
    {"prompt": "What is character 1's luck (LUCK)?", "response": "Character 1's luck is [0x006114]"},
    {"prompt": "What is character 1's damage (DAMAGE)?", "response": "Character 1's damage is [0x006120]"},
    {"prompt": "What is character 1's hit percentage (HIT %)?", "response": "Character 1's hit percentage is [0x006121]"},
    {"prompt": "What is character 1's absorb (ABSORB)?", "response": "Character 1's absorb is [0x006122]"},
    {"prompt": "What is character 1's evade percentage (EVADE %)?", "response": "Character 1's evade percentage is [0x006123]"},
    {"prompt": "What is character 1's HP (life, hit points)?", "response": "Character 1's HP is [0x00610A-0x00610B]"},
    {"prompt": "What is character 1's maximum HP (maximum life, maximum hit points)?", "response": "Character 1's maximum HP is [0x00610C-0x00610D]"},
    {"prompt": "What is character 2's class?", "response": "Character 2's class is [0x006140]"},
    {"prompt": "What is character 2's strength (STR.)?", "response": "Character 2's strength is [0x006150]"},
    {"prompt": "What is character 2's agility (AGL.)?", "response": "Character 2's agility is [0x006151]"},
    {"prompt": "What is character 2's intelligence (INT.)?", "response": "Character 2's intelligence is [0x006152]"},
    {"prompt": "What is character 2's vitality (VIT.)?", "response": "Character 2's vitality is [0x006153]"},
    {"prompt": "What is character 2's luck (LUCK)?", "response": "Character 2's luck is [0x006154]"},
    {"prompt": "What is character 2's damage (DAMAGE)?", "response": "Character 2's damage is [0x006160]"},
    {"prompt": "What is character 2's hit percentage (HIT %)?", "response": "Character 2's hit percentage is [0x006161]"},
    {"prompt": "What is character 2's absorb (ABSORB)?", "response": "Character 2's absorb is [0x006162]"},
    {"prompt": "What is character 2's evade percentage (EVADE %)?", "response": "Character 2's evade percentage is [0x006163]"},
    {"prompt": "What is character 2's HP (life, hit points)?", "response": "Character 2's HP is [0x00614A-0x00614B]"},
    {"prompt": "What is character 2's maximum HP (maximum life, maximum hit points)?", "response": "Character 2's maximum HP is [0x00614C-0x00614D]"},
    {"prompt": "What is character 3's class?", "response": "Character 3's class is [0x006180]"},
    {"prompt": "What is character 3's strength (STR.)?", "response": "Character 3's strength is [0x006190]"},
    {"prompt": "What is character 3's agility (AGL.)?", "response": "Character 3's agility is [0x006191]"},
    {"prompt": "What is character 3's intelligence (INT.)?", "response": "Character 3's intelligence is [0x006192]"},
    {"prompt": "What is character 3's vitality (VIT.)?", "response": "Character 3's vitality is [0x006193]"},
    {"prompt": "What is character 3's luck (LUCK)?", "response": "Character 3's luck is [0x006194]"},
    {"prompt": "What is character 3's damage (DAMAGE)?", "response": "Character 3's damage is [0x0061A0]"},
    {"prompt": "What is character 3's hit percentage (HIT %)?", "response": "Character 3's hit percentage is [0x0061A1]"},
    {"prompt": "What is character 3's absorb (ABSORB)?", "response": "Character 3's absorb is [0x0061A2]"},
    {"prompt": "What is character 3's evade percentage (EVADE %)?", "response": "Character 3's evade percentage is [0x0061A3]"},
    {"prompt": "What is character 3's HP (life, hit points)?", "response": "Character 3's HP is [0x00618A-0x00618B]"},
    {"prompt": "What is character 3's maximum HP (maximum life, maximum hit points)?", "response": "Character 3's maximum HP is [0x00618C-0x00618D]"},
    {"prompt": "What is character 4's class?", "response": "Character 4's class is [0x0061C0]"},
    {"prompt": "What is character 4's strength (STR.)?", "response": "Character 4's strength is [0x0061D0]"},
    {"prompt": "What is character 4's agility (AGL.)?", "response": "Character 4's agility is [0x0061D1]"},
    {"prompt": "What is character 4's intelligence (INT.)?", "response": "Character 4's intelligence is [0x0061D2]"},
    {"prompt": "What is character 4's vitality (VIT.)?", "response": "Character 4's vitality is [0x0061D3]"},
    {"prompt": "What is character 4's luck (LUCK)?", "response": "Character 4's luck is [0x0061D4]"},
    {"prompt": "What is character 4's damage (DAMAGE)?", "response": "Character 4's damage is [0x0061E0]"},
    {"prompt": "What is character 4's hit percentage (HIT %)?", "response": "Character 4's hit percentage is [0x0061E1]"},
    {"prompt": "What is character 4's absorb (ABSORB)?", "response": "Character 4's absorb is [0x0061E2]"},
    {"prompt": "What is character 4's evade percentage (EVADE %)?", "response": "Character 4's evade percentage is [0x0061E3]"},
    {"prompt": "What is character 4's HP (life, hit points)?", "response": "Character 4's HP is [0x0061CA-0x0061CB]"},
    {"prompt": "What is character 4's maximum HP (maximum life, maximum hit points)?", "response": "Character 4's maximum HP is [0x0061CC-0x0061CD]"}
]

# Instructions

Your job will be to answer questions a user has about real-time, dynamic information related to the state of a game called Final Fantasy. The game state itself is stored in the RAM of an emulator at various RAM addresses. It is important to remember that there are 4 characters (this use of the word `character` is in the sense of `a person in a novel, play or movie`). Each character has a name. Character 1 is named `Artr`. Character 2 is named `Glyn`. Character 3 is named `Kwyx`. Character 4 is named `Blyx`.

The output messages in the training data contain "RAM address tokens" (ram addresses inside square brackets, like [0x001234]). When you get questions about specific things in the game, you MUST request "RAM address values" (values you can substitute in place of the ram address tokens) to replace the RAM address tokens with in your final response. For example, if your response, based on the training data, was going to be `Character 1's strength is [0x001234].`, you must request a RAM address value to replace `[0x001234]` with, so that your final response will look something like `Character 1's strength is 10.`. In other words, your final response can NEVER contain a RAM address token.

This means that all interactions will have the flow:

1. User asks an initial question with the format: {"question": "question"}
2. You, the LLM, use the training data to determine an initial response
3. You, the LLM, respond by requesting RAM address values to replace the RAM address tokens with, in the format: {"required_ram_contents": []}
4. User provides RAM address values back with the format: {"ram_contents": {}}
5. You, the LLM, give your succinct response to the original question with the format: {"answer": "answer"}

# Additional Context

* The `required_ram_contents` array should contain a comma separated list of strings with the RAM address values being requested. For example, if you require the values to substitute in for RAM address tokens [0x001000] and [0x002000], your initial response should be `{"required_ram_contents": ["0x001000", "0x002000"]}`. Your response requesting RAM address values MUST contain ONLY JSON.
* RAM address values change frequently, so you must request them anew with each user question.
* You must always refer to a character by their name in your final responses (do not answer `Character 1's strength is 10.`, but rather, `XXXX's strength is 10.`, where XXXX is the character name given above).
* Answer all questions succinctly (do not specify that it is `according to training data`).
* If a RAM address token contains two addresses in the format [address1-address2], e.g. [0x005555-0x005556], you should request both values (e.g. `{"required_ram_contents": ["0x005555", "0x005556"]}}`). When this occurs, calculate the final value by applying the formula: (first_value + (second_value * 256)).

# Confirm Training Complete

Respond to this training message with "I am ready". Questions will follow, and all responses after this one should be in JSON format as described.