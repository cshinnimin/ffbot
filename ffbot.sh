##### Final Fantasy Bot Configuration #####

export RAMDISK_DIR=/mnt/ramdisk-ffbot/
export LUA_PACKAGE_DIR=/home/linuxbrew/.linuxbrew/Cellar/luarocks/3.12.2/share/lua/5.4/
export ROM_FILE=../../roms/FF1.nes

RAMDISK_SIZE=64M

###########################################

##### Final Fantasy Bot Loading Script ####
##### (do not modify below) ###############

export FFBOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# unmount a previous RAMdisk
sudo umount --quiet $RAMDISK_DIR

# mount new RAMdisk
sudo mount -t tmpfs -o size=$RAMDISK_SIZE tmpfs $RAMDISK_DIR

# set up RAMdisk initial state
touch $RAMDISK_DIR/execute.lua
touch $RAMDISK_DIR/ram_contents.json
cp data/ram_catalog.json $RAMDISK_DIR/ram_catalog.json
cp data/bestiary.json $RAMDISK_DIR/bestiary.json

# load python write_ram endpoint in background process
python scripts/python/write_ram.py &
PYTHON_PID=$!

# load python Flask LLM API in background process (on 5001)
LLM_API_PORT=5001 python -m api.llm.app &
LLM_API_PID=$!

# load npm server in background process
npm run dev --silent --prefix bot-app &
NPM_PID=$!

# wait a second for npm to load then open browser and load bot-app
sleep 1
xdg-open "http://localhost:5173" &

# load emulator
eval "${1:-fceux-gui --loadlua \"$FFBOT_DIR/scripts/lua/main_daemon.lua\" $ROM_FILE}"

# clean up background processes
kill $PYTHON_PID
kill $LLM_API_PID
kill $NPM_PID
