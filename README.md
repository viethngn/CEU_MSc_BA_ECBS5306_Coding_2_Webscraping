# Pokemon Showdown - Coding2 Final Project

## Overview
**WARNING**: The Jupiter notebook will only work when cloning this Github repo to your local machine.

This is a project to collect and analyze Pokemon battle game data from PokemonShowdown.com for the most recent 250 games today.

We will do the following steps:
1. Collect battle data from Pokemon Showdown API
2. Clean the battle log with Python scripts
3. Build visualizations:
- Top used Pokemons in battle
- Top Pokemon types used in battle
- Pokemon total base stats
- Player elo ranking distribution
- Battle length distribution

## Technical Design
The notebook is powered by the source code found under the `src` directory.

### API calling functions
The API calling functions are defined in the [`ps_utils.py`](https://github.com/viethngn/CEU_MSc_BA_ECBS5306_Coding_2_Webscraping/blob/main/src/utils/ps_utils.py).

```python
# Generic API calling function used by other functions to get Pokemon static data like Pokedex, Movedex, etc.
def get_ps_url_response():
    ...

# Specialized API calling function for getting the latest 250 battles data
def get_ps_replays():
    ...

# Specialized API calling function for getting the battle log of the latest 250 battles data
def get_replay_details():
    ...

# Specialized API calling function for getting the player data
def get_player_details():
    ...
```

### Parsing & Cleaning battle log functions
After getting the data from APIs, the parsing and cleaning functionalities are handled by [`ps_game_state_utils.py`](https://github.com/viethngn/CEU_MSc_BA_ECBS5306_Coding_2_Webscraping/blob/main/src/utils/ps_game_state_utils.py), 
with the support of cleaning functions from other utils scripts.

The main functionality is to read in the raw log from the APIs data, transform it into the entities defined in the 
`entites` package and then output a csv file with every important turn in every game.

### Notebook helper functions
As stated above, the Jupiter notebook is powered by the Python scripts in this repo, mainly by [`notebook_helper.py`](https://github.com/viethngn/CEU_MSc_BA_ECBS5306_Coding_2_Webscraping/blob/main/src/utils/notebook_helper.py).

This Python script is responsible for building the necessary dataframe for each visualization in the notebook 
(since putting the code into the notebook will be extremely long and hard to read).
