##### Final Fantasy Bot Configuration #####

export RAMDISK_DIR=/mnt/ramdisk-ffbot/
export LUA_PACKAGE_DIR=/home/linuxbrew/.linuxbrew/Cellar/luarocks/3.12.2/share/lua/5.4/

RAMDISK_SIZE=64M

###########################################

##### Final Fantasy Bot Loading Script ####
##### (do not modify below) ###############

sudo umount --quiet $RAMDISK_DIR

sudo mount -t tmpfs -o size=$RAMDISK_SIZE tmpfs $RAMDISK_DIR

touch $RAMDISK_DIR/execute.lua
touch $RAMDISK_DIR/ram_contents.json
cp data/ram_catalog.json $RAMDISK_DIR/ram_catalog.json

eval "${1:-fceux-gui}"
