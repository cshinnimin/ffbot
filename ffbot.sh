##### Final Fantasy Bot Configuration #####

export RAMDISK_DIR=/mnt/ramdisk-ffbot/
export LUA_PACKAGE_DIR=/home/linuxbrew/.linuxbrew/Cellar/luarocks/3.12.2/share/lua/5.4/

RAMDISK_SIZE=64M

###########################################

##### Final Fantasy Bot Loading Script ####
##### (do not modify below) ###############

# unmount a previous RAMdisk
sudo umount --quiet $RAMDISK_DIR

# mount new RAMdisk
sudo mount -t tmpfs -o size=$RAMDISK_SIZE tmpfs $RAMDISK_DIR

# set up RAMdisk initial state
touch $RAMDISK_DIR/execute.lua
touch $RAMDISK_DIR/ram_contents.json

# load emulator
eval "${1:-fceux-gui}"
