-- Define the address and the new value
local address = 0x006100 -- Example address, in hexadecimal
local newValue = 0x01   -- Example value to write, in hexadecimal

-- Write the new value to the specified address
memory.writebyte(address, newValue)

return 1 -- so that main daemon knows a script was executed and to clean up