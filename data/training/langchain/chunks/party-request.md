# Party and Character Requests

This instruction is useful if asked questions about party members (characters), or if issued commands that pertain to the party members, such as:

    - How much <some_stat> does <some_name> have?
    - How strong is <some_name>?
    - Heal my party.
    - Restore our magic.

* <some_stat> in the above examples could be: 
    * life
    * health
    * HP
    * max HP
    * max life
    * strength
    * agility
    * intelligence
    * vitality
    * luck
    * damage
    * hit%
    * absorb
    * defense (absorb)
    * evade%
* If you see four letter names that you do not recognize, use the get_names tool to confirm the names of the characters in the adventurers party. 
* If you recognize a character name from conversation history and need a memory address relevant to that character, first use the get_names tool to double check which character slot (1-4) that character is now in, since it changes.

## Memory Addresses Relevant to Party Characters

* <character_1> class
	- 0x006100
* <character_2> class
	- 0x006140
* <character_3> class
	- 0x006180
* <character_4> class
	- 0x0061C0
* <character_1> HP (life, health)
	- Sum results for 0x00610A and 0x00610B
* <character_2> HP (life, health)
	- Sum results for 0x00614A and 0x00614B
* <character_3> HP (life, health)
	- Sum results for 0x00618A and 0x00618B
* <character_4> HP (life, health)
	- Sum results for 0x0061CA and 0x0061CB
* <character_1> Maximum HP (life, health)
	- Sum results for 0x00610C and 0x00610D
* <character_2> Maximum HP (life, health)
	- Sum results for 0x00614C and 0x00614D
* <character_3> Maximum HP (life, health)
	- Sum results for 0x00618C and 0x00618D
* <character_4> Maximum HP (life, health)
	- Sum results for 0x0061CC and 0x0061CD
* <character_1> strength
	- 0x006110
* <character_2> strength
	- 0x006150
* <character_3> strength
	- 0x006190
* <character_4> strength
	- 0x0061D0
* <character_1> agility
	- 0x006111
* <character_2> agility
	- 0x006151
* <character_3> agility
	- 0x006191
* <character_4> agility
	- 0x0061D1
* <character_1> intelligence
	- 0x006112
* <character_2> intelligence
	- 0x006152
* <character_3> intelligence
	- 0x006192
* <character_4> intelligence
	- 0x0061D2
* <character_1> vitality
	- 0x006113
* <character_2> vitality
	- 0x006153
* <character_3> vitality
	- 0x006193
* <character_4> vitality
	- 0x0061D3
* <character_1> luck
	- 0x006114
* <character_2> luck
	- 0x006154
* <character_3> luck
	- 0x006194
* <character_4> luck
	- 0x0061D4
* <character_1> attack
	- 0x006120
* <character_2> attack
	- 0x006160
* <character_3> attack
	- 0x0061A0
* <character_4> attack
	- 0x0061E0
* <character_1> hit%
	- 0x006121
* <character_2> hit%
	- 0x006161
* <character_3> hit%
	- 0x0061A1
* <character_4> hit%
	- 0x0061E1
* <character_1> absorb
	- 0x006122
* <character_2> absorb
	- 0x006162
* <character_3> absorb
	- 0x0061A2
* <character_4> absorb
	- 0x0061E2
* <character_1> evade%
	- 0x006123
* <character_2> evade%
	- 0x006163
* <character_3> evade%
	- 0x0061A3
* <character_4> evade%
	- 0x0061E3