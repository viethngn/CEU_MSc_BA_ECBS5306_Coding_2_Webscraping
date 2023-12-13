import json
import re
from random import uniform
from time import sleep

import requests

from src.cache.ps_static_data import PSStaticData
from src.utils.ps_parser import remove_special_pkm_forms_from_battle_log
from src.utils.udf_utils import fix_response_text


def load_static_data():
    return PSStaticData(get_type_chart(), get_abilities(), get_movedex(), get_items(), get_pokedex(), get_learn_sets())


def read_config(filename):
    print(f"Reading config file at {filename}")

    with open(filename, 'r') as file:
        configs = json.load(file)
    return configs


def get_ps_replays(pages=5):
    replays = []

    # set page limit to call 5 pages in the paginated API
    for page in range(1, pages + 1):
        print(f"Calling get replay API for page {page}")

        try:
            response = requests.get(
                f'https://replay.pokemonshowdown.com/api/replays/search?username=&format=gen9doublesou&page={page}')
        except requests.exceptions.RequestException as e:
            print(f"""There is an error calling the get_ps_replays api at page {page}
            Error message: {e}""")
            break

        if response.status_code == 200:
            data = json.loads(response.text[1:])
            replays.extend(data)
        else:
            print(f"""There is an error calling the get_ps_replays api at page {page}
            No response received. Status code {response.status_code}""")
            break

        # ps has a limitation of 51 per page in the response
        # if there is less than 51 items then this is the last page
        if len(data) < 51:
            break

        # sleep randomly for at most 0.5 seconds
        sleep(uniform(0, 0.5))

    return replays


def get_replay_details(replays):
    replay_details = []

    for r in replays:
        print(f"Calling get replay detail API [Game-id: {r['id']}]")

        try:
            response = requests.get(f"https://replay.pokemonshowdown.com/{r['id']}.json")
        except requests.exceptions.RequestException as e:
            print(f"""There is s an error calling the get_replay_details api
            Error message: {e}""")
            break

        if response.status_code == 200:
            data = json.loads(response.text)
            replay_details.append(data)
        else:
            print(f"""There is an error calling the get_replay_details api: https://replay.pokemonshowdown.com/{r['id']}.json
            No response received.""")
            break

        sleep(uniform(0, 0.3))

    return replay_details


def get_pokedex():
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/pokedex.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
        if 'forme' in v.keys():
            v['num'] = f"{v['num']}-{v['forme']}"
    return response


def get_learn_sets():
    """
    In the learn sets, the code letters for how to learn a move are as following:
    L = Level up
    T = Move tutor
    M = TM/HM
    S = Event only
    V = Virtual console from Gen 1
    E = Egg move

    Code format: 8L25 -> Gen 8, learn at level 25

    :return:
    """
    return get_ps_url_response(f"https://play.pokemonshowdown.com/data/learnsets.js")


def get_type_chart():
    """
    Type chart explained:
    - Each key is the typing at defensive position
    - Values are types at attacking position

    Code explained:
    0 = x1 effective
    1 = x2 effective
    2 = x1/2 effective
    3 = Immune (x0 effective)

    :return:
    """
    return get_ps_url_response(f"https://play.pokemonshowdown.com/data/typechart.js")


def get_movedex():
    """
    Move category:
    0 = status
    1 = physical
    2 = special

    :return:
    """
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/moves.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
        # correct names containing comma
        v['name'] = v['name'].replace(',', '_')
        # correct accuracy to all int (True -> 999)
        if v['accuracy'] is True:
            v['accuracy'] = 999
    return response


def get_items():
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/items.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
    return response


def get_abilities():
    response = get_ps_url_response(f"https://play.pokemonshowdown.com/data/abilities.js")
    for k, v in response.items():
        # correct < 1 num (id)
        if v['num'] < 1:
            v['num'] += 10000
        # correct a duplicate key
        if v['num'] == 284:
            v['num'] = f"{v['num']}-{v['name'].split()[0].lower()}"
    return response


def get_ps_url_response(url):
    print(f"Calling get API: [{url}]")

    response = None

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"""There is s an error calling the url {url}
                    Error message: {e}""")

    if response is not None:
        # need to fix the json here since the response is not JSON corrected
        corrected_json = fix_response_text(response.text)

        response_json = json.loads(corrected_json)
        return response_json
    else:
        print(f"""There is an error calling the url {url}
                    No response received.""")
        return None


def get_player_details(player_ids):
    player_details = {}
    for p_id in player_ids:
        response = get_ps_url_response(f"https://pokemonshowdown.com/users/{p_id}.json")
        player_details[p_id] = response
        # sleep randomly for at most 0.5 seconds
        sleep(uniform(0, 0.5))

    return player_details


def save_to_files(filepath, data):
    """
    Save json data to file (json/csv)
    :param filepath: (str) filepath
    :param data: (dict/list) json object/sql string list
    :return: None
    """
    print(f"Writing data to file {filepath}")

    json_formatted_data = json.dumps(data, indent=4)

    with open(filepath, 'w') as replay_file:
        replay_file.write(json_formatted_data)


def get_cleaned_battle_log(log: str) -> tuple:
    raw_data = remove_special_pkm_forms_from_battle_log(log).split('|start')
    battle_log = raw_data[1]

    battle_log = (re.sub(r'|inactive|.*?left.\n', '', battle_log)
                  .replace('|upkeep\n', '')
                  .replace('|\n', ''))

    battle_log_list = battle_log.strip().split('\n')

    # remove unnecessary rows
    poke_player_list = [x for x in raw_data[0].split('\n') if '|poke|' in x or '|player|' in x]

    battle_log_cleaned = poke_player_list + ['|turn|0']
    for row in battle_log_list:
        if ('|n|' in row or '|t:|' in row or '|j|' in row or '|l|' in row
                or '|b|' in row or '|raw|' in row or '|c|' in row):
            continue
        battle_log_cleaned.append(row)

    pkm_list = re.findall("(?:switch\||drag\||replace\|).*?\n", battle_log)
    battling_pkm = {}
    for item in pkm_list:
        player = item.split(':')[0].split('|')[1].replace('p1a', 'p1').replace('p1b', 'p1').replace('p2a', 'p2').replace('p2b', 'p2')
        item_ref = item.replace('p1a', 'p').replace('p1b', 'p').replace('p2a', 'p').replace('p2b', 'p')
        pkm_text = item_ref.replace(' ', '').lower().split('|')[1:3]
        pkm_text = '|'.join(pkm_text).split('p:')[1].split(',')[0]
        p_key = f"{player}_{re.sub(r'[^A-Za-z0-9 ]+', '', pkm_text.split('|')[0])}"
        p_val = re.sub(r'[^A-Za-z0-9 ]+', '', pkm_text.split('|')[1])
        if p_key in battling_pkm.keys():
            continue
        battling_pkm[p_key] = p_val

    return battling_pkm, battle_log_cleaned


def clean_pkm_name_text(pkm_name: str) -> str:
    return re.sub(r'\W+', '', pkm_name.lower())
