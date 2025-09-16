# The Final Fantasy Bot Project

The Final Fantasy Bot Project (FFBot) is currently documented for Fedora Linux (specifically Fedora 43) only.

## Setup

### Install the FCEUX Emulator

Install the FCEUX emulator using [snapd](https://snapcraft.io/install/fceux-gui/fedora). At the time of writing, the `fceux-gui` package was not available for Fedora 43 with the `dnf` package manager.

### Install **lunajson** Package via LUARocks

The main LUA daemon requires the ability to manipulate JSON which is not native to LUA. We need to install and configure **lunajson**.

* Install **luarocks** using homebrew:
```
brew install luarocks
```

* Use luarocks to install the **lunajson** package:
```
luarocks install lunajson
```

* Determine the location where **lunajson.lua** was installed. Open the **ffbot.sh** bash script and update the exported `LUA_PACKAGE_DIR` environment variable accordingly. On Fedora 43 the location was:
```
export LUA_PACKAGE_DIR=/home/linuxbrew/.linuxbrew/Cellar/luarocks/3.12.2/share/lua/5.4/
```

### Install Python and Flask

The React bot app needs the ability to write a file to the RAMdisk in order to write contents back to NES memory. This is accomplished by exposing a simple API endpoint using Python / Flask.

* Install Python and 'pip', Python's package manager:
```
sudo dnf update
sudo dnf install python3 python3-pip
```

* Install Flask and Flask-CORS (needed for React app to make cross origin request to python API from different port):
```
pip install Flask
pip install Flask-CORS
```

### Run the FFBot

* From the root project folder, run the **ffbot.sh** script in a terminal:
```
./ffbot.sh
```

* The script assumes the emulator command is `fceux-gui`. To run FFBot with a different emulator command if needed, provide the command as an argument (for example, if the needed emulator command is simply `fceux`):
```
./ffbot.sh fceux
```