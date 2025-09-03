# The Final Fantasy Bot Project

The Final Fantasy Bot Project (FFBot) is currently documented for Fedora Linux (specifically Fedora 43) only.

## Setup

### Install the FCEUX Emulator

Install the FCEUX emulator using [snapd](https://snapcraft.io/install/fceux-gui/fedora). At the time of writing, the `fceux-gui` package was not available for Fedora 43 with the `dnf` package manager. 

### Create a RAMDisk

We will create a RAMdisk in memory since the FCEUX emulator will need to rapidly read and write data to a disk for the FFBot to read and write to the NES memory via LUA scripts. This will happen much faster on a RAMdisk than a physical folder. The FFBot LUA scripts will dump memory information from the NES emulator for the bot to read, and the bot will dump LUA scripts for the emulator to read and execute.

* Create a mount point:
```
sudo mkdir /mnt/ramdisk-ffbot
```

* Mount the tmpfs filesystem (change the `size` attribute depending on your available system resources since the LLM will also take a large portion of physical memory):
```
sudo mount -t tmpfs -o size=512M tmpfs /mnt/ramdisk-ffbot
```

* Create a placeholder execution script. The FFBot LUA daemon requires it to be present, even if empty.
```
touch /mnt/ramdisk-ffbot/execute.lua
```