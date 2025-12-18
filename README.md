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

* Determine the location where **lunajson.lua** was installed. Remember this location for later when we set up the environment variables. It will be needed for the `LUA_PACKAGE_DIR` environment variable. On Fedora 43 the location was:
```
/home/linuxbrew/.linuxbrew/Cellar/luarocks/3.12.2/share/lua/5.4/
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

### Configure React App .env

Copy `.env-sample` to `.env` and update any configuration variables.

* `RAMDISK_SIZE`: The size of the RAMDisk we will use to read and write RAM values from the game. Default of 64M is likely much more than enough.
* `RAMDISK_DIR`: The path on the local machine to create the RAMDisk. 
* `ROM_FILE`: The location of the Final Fantasy ROM file on your local machine.
* `LUA_PACKAGE_DIR`: The location on the local machine where LUA packages reside. The LUA Daemon in scripts/lua will need this to load its dependencies.
* `LLM_PROVIDER`: The LLM service we want to use. This is important since different services have different APIs and our end of the API needs to know how to interface correctly. There is currently support for OpenAI (`openai`), OpenRouter.ai (`openrouter`) or local Ollama (`ollama`).
* `LLM PORT`: The port for the LLM service. Only required if using a local service.
* `LLM_API_KEY`: The API key for the LLM of your choice, if applicable. Local LLMs running on Ollama do not require an API key.
* `LLM_MODEL`: The model of your chosen LLM.
* `LLM_THROTTLE_DELAY`: In milliseconds, a forced delay between LLM chat completion requests. Use this to throttle the app if your chosen model is returning 429 "Too Many Request" responses. The FFBot app may require multiple chat completion requests under the hood for each response seen in the chat window, so actual response times in the app may be longer than this value.
* `LLM_TEMPERATURE`: The temparature setting for the LLM, from 0.0 to 2.0. Lower values tune the LLM to be more focused, higher values tune it to be more creative.
* `LLM_KEEP_ALIVE`: Amount of time in minutes (with format `[num_minutes]s`) that the specified LLM will remain in memory. Useful to set if running a local LLM.
* `VITE_DEBUG_MODE`: When debug mode is set to `TRUE`, debugging information will be logged to the console in the browser.
* `VITE_TRAINING_MAX ATTEMPTS`: The bot app attempts to re-issue training to the LLM if it responds in a format it is not expecting. Set the maximum number of attempts before giving up.
* `NES_API_PORT`: The port the Python service used by the React front end to write data to the RAMDisk should be run on. Deafult 5000.
* `LLM_API_PORT`: The port the Python service used by the React front end to interface with the LLM should be run on. Default 5001.
* `VITE_PORT`: The port the front end React Vite application should be run on. Default 5173.

### Install a Local LLM, if Desired

Local LLMs have limitations. The app was tested using a variety of Ollama LLMs with 3B parameters or less (so that they could run on a modest laptop with 8GB of RAM). Duriung testing it was found that only Llama 3.2 (3B) could reasonably ingest the instructions and understand it's role as the "FFBot". If you want to install and run Llama 3.2 locally:

```
sudo dnf install ollama
ollama serve
ollama run llama3.2:3b
```

Note that the `run` command downloads the model to your hard disk and will require several GB of space. Once you have downloaded the model once, you will not need to execute the run command again to use FFBot, only the serve command.

### Run the FFBot

* If you are running a local LLM with Ollama, serve it in a terminal window:

```
ollama serve
```

* In a separate terminal window, from the root project folder, run the **ffbot.sh** script:
```
bash ./ffbot.sh
```

* The script assumes the emulator command is `fceux-gui`. To run FFBot with a different emulator command if needed, provide the command as an argument (for example, if the needed emulator command is simply `fceux`):
```
bash ./ffbot.sh fceux
```