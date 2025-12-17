# Party Reorder Request

This instruction is useful if asked to reorder the adventurers party. This may be phrased:

    - Order my party <some_name_1>, <some_name_2>, <some_name_3>, <some_name_1>.
    - Reorder my party.

## Explicit Reorder Request

In the case that you are given an explicit order to put the party in, use the get_names tool to determine the current slot each character occupies. If the character names in the request do not clearly map to our four actual characters (small type-o's ok), get clarification from the adventurer. Once you know which slot each character currently occupies, use the order_party tool. The first input should be the integer (1-4) of the character at the current position that should be moved to slot 1. The second input should be the integer of the character at the current position that should be moved to slot 2, and so on. 

Example: if the adventurer asks for the party to be ordered Bbbb, Dddd, Cccc, Aaaa and the CURRENT part order is Aaaa, Bbbb, Cccc, Dddd, the inputs should be [2,4,3,1]

## General Reorder Request

If simply asked to "reorder my party", check conversation history to see whether you have determined a previous party order, and use the most recently known order. Use the most recently known order as the target order in an explicit order request.