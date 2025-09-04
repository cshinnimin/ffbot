
local EXECUTION_CADENCE = 30 -- NES / FCEUX runs at about 60 frames per second
local frame_count = 0

while true do
    if (frame_count < EXECUTION_CADENCE) then
        frame_count = frame_count + 1
    else
        -- only execute primary functionality once every EXECUTION_CADENCE frames
        frame_count = 0 -- reset frame counter

        local RAMDISK_DIR = os.getenv("RAMDISK_DIR")
        local LUA_PACKAGE_DIR = os.getenv("LUA_PACKAGE_DIR")

        -- update LUAs `package.path` to include directory with lunajson
        package.path = package.path .. ";" .. LUA_PACKAGE_DIR .. "?.lua"
        local JSON = require("lunajson") -- load lunajson for JSON parsing

        local ram_catalog_file = io.open(RAMDISK_DIR .. "ram_catalog.json", "r")
        local RAM_CATALOG = JSON.decode(ram_catalog_file:read("*all"))
        -- note keys are NOT sorted in order by their hex values
        ram_catalog_file:close()

        local ram_contents = "{"
        for ram_address, info in pairs(RAM_CATALOG.ram_addresses) do
            local decimal_value = memory.readbyte(tonumber(ram_address))
            local hex_string = string.format("0x%02X", decimal_value)
            ram_contents = ram_contents .. '"' .. ram_address .. '": "' .. hex_string .. '",'
        end
         -- remove trailing comma and close JSON object
        ram_contents = ram_contents:sub(1, -2) .. "}"

        -- note that because LUA tables do not maintain order, the current solution
        -- will not sort the ram_contents.json file by its hex key values
        local ram_contents_file = io.open(RAMDISK_DIR .. "ram_contents.json", "w")
        ram_contents_file:write(ram_contents)
        ram_contents_file:close()

        -- execute any scripts the bot has dropped in execute.lua
        local result = dofile(RAMDISK_DIR .. "execute.lua")
        if (result) then
             -- clear contents of execute.lua
            io.open(RAMDISK_DIR .. "execute.lua","w"):close()
            print("Executed script from bot")
        end
    end

    emu.frameadvance() -- crucial for allowing the emulator to advance a frame
end
