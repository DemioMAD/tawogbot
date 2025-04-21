# tawogbot
A Discord bot to fetch info from the [TAWOG wiki](https://theamazingworldofgumball.fandom.com/wiki)

# usage
install python

clone the repository using git
```
git clone https://github.com/DemioMAD/tawogbot.git
```

run these commands in your terminal if using uv:
```
uv sync
uv venv
```

install dependencies

uv:
```
uv pip install -r requirements.txt
```
pip:
```
pip install -r requirements.txt
```

rename .env.example to .env and add these contents:
```
DISCORD_TOKEN="your discord bot token goes here"
```

then run main.py

if not using uv:
```
python main.py
```
if using uv:
```
uv run main.py
```