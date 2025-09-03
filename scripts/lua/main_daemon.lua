local RAMDISK_DIR = os.getenv("RAMDISK_DIR")
local LUA_PACKAGE_DIR = os.getenv("LUA_PACKAGE_DIR")
local EXECUTION_CADENCE = 30 -- NES / FCEUX runs at about 60 frames per second

local frame_count = 0

package.path = package.path .. ";" .. LUA_PACKAGE_DIR .. "?.lua"
local json = require("lunajson")

local jsonString = '{"name": "Example", "value": 123}'
local luaTable = json.decode(jsonString)
print(luaTable.name) -- Outputs: Example

while true do
    if (frame_count < EXECUTION_CADENCE) then
        frame_count = frame_count + 1
    else
        frame_count = 0

        local result = dofile(RAMDISK_DIR .. "execute.lua")

        if (result) then
            print("Executed a script")
            io.open(RAMDISK_DIR .. "execute.lua","w"):close() -- clear contents of execute.lua
        end
    end

    emu.frameadvance() -- crucial for allowing the emulator to advance a frame
end
