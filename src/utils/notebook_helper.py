import pandas as pd

from src.cache.ps_static_data import PSStaticData


def get_battle_turns_df(df: pd.DataFrame):
    battle_turns_df = df.groupby(
        ['game_id', 'p1_pkm1_code', 'p1_pkm2_code', 'p1_pkm3_code', 'p1_pkm4_code', 'p1_pkm5_code', 'p1_pkm6_code',
         'p2_pkm1_code', 'p2_pkm2_code', 'p2_pkm3_code', 'p2_pkm4_code', 'p2_pkm5_code', 'p2_pkm6_code'])[
        ['game_id', 'p1_pkm1_code', 'p1_pkm2_code', 'p1_pkm3_code', 'p1_pkm4_code', 'p1_pkm5_code', 'p1_pkm6_code',
         'p2_pkm1_code', 'p2_pkm2_code', 'p2_pkm3_code', 'p2_pkm4_code', 'p2_pkm5_code',
         'p2_pkm6_code']].value_counts().reset_index()
    battle_turns_df.rename(columns={'count': 'turns'}, inplace=True)
    return battle_turns_df


def get_pkm_usage(df: pd.DataFrame, ps_static: PSStaticData):
    battle_turns_df = get_battle_turns_df(df)

    used_pokemons = []
    for index, row in battle_turns_df.iterrows():
        game_id = row['game_id']
        for s, item in row.items():
            if s == 'game_id' or s == 'turns':
                game_id = item
            else:
                used_pokemons.append({"game_id": game_id, 'pokemon': item})

    used_pokemon_df = pd.DataFrame(used_pokemons).groupby(['pokemon'])[
        'pokemon'].value_counts().reset_index().rename(columns={'count': 'usage_count'}).sort_values(by=['usage_count'],
                                                                                                     ascending=False)
    total_usage_count = used_pokemon_df['usage_count'].sum()
    used_pokemon_df['usage_%'] = (used_pokemon_df.usage_count / total_usage_count) * 100
    used_pokemon_df = used_pokemon_df.round(decimals=2)
    used_pokemon_df['pkm_name'] = used_pokemon_df.pokemon.apply(lambda x: ps_static.pokedex[x]['name'])
    used_pokemon_df['pkm_types'] = used_pokemon_df.pokemon.apply(lambda x: '-'.join(ps_static.pokedex[x]['types']))

    del battle_turns_df

    return used_pokemon_df


def get_type_usage_df(df: pd.DataFrame):
    type_turns_df = df.groupby(
        ['game_id', 'p1_pkm1_code', 'p1_pkm2_code', 'p1_pkm3_code', 'p1_pkm4_code', 'p1_pkm5_code', 'p1_pkm6_code',
         'p2_pkm1_code', 'p2_pkm2_code', 'p2_pkm3_code', 'p2_pkm4_code', 'p2_pkm5_code', 'p2_pkm6_code'])[
        ['game_id', 'p1_has_bug', 'p1_has_dark', 'p1_has_dragon', 'p1_has_electric', 'p1_has_fairy', 'p1_has_fighting',
         'p1_has_fire', 'p1_has_flying', 'p1_has_ghost', 'p1_has_grass', 'p1_has_ground', 'p1_has_ice', 'p1_has_normal',
         'p1_has_poison', 'p1_has_psychic', 'p1_has_rock', 'p1_has_steel', 'p1_has_water', 'p2_has_bug', 'p2_has_dark',
         'p2_has_dragon', 'p2_has_electric', 'p2_has_fairy', 'p2_has_fighting', 'p2_has_fire', 'p2_has_flying',
         'p2_has_ghost', 'p2_has_grass', 'p2_has_ground', 'p2_has_ice', 'p2_has_normal', 'p2_has_poison',
         'p2_has_psychic', 'p2_has_rock', 'p2_has_steel', 'p2_has_water']].value_counts().reset_index()
    type_turns_df.rename(columns={'count': 'turns'}, inplace=True)

    team_type_usage_series = type_turns_df[
        ['p1_has_bug', 'p1_has_dark', 'p1_has_dragon', 'p1_has_electric', 'p1_has_fairy', 'p1_has_fighting',
         'p1_has_fire', 'p1_has_flying', 'p1_has_ghost', 'p1_has_grass', 'p1_has_ground', 'p1_has_ice', 'p1_has_normal',
         'p1_has_poison', 'p1_has_psychic', 'p1_has_rock', 'p1_has_steel', 'p1_has_water', 'p2_has_bug', 'p2_has_dark',
         'p2_has_dragon', 'p2_has_electric', 'p2_has_fairy', 'p2_has_fighting', 'p2_has_fire', 'p2_has_flying',
         'p2_has_ghost', 'p2_has_grass', 'p2_has_ground', 'p2_has_ice', 'p2_has_normal', 'p2_has_poison',
         'p2_has_psychic', 'p2_has_rock', 'p2_has_steel', 'p2_has_water']].sum(numeric_only=True)

    type_usage_dict = {
        'Bug': 0,
        'Dark': 0,
        'Dragon': 0,
        'Electric': 0,
        'Fairy': 0,
        'Fighting': 0,
        'Fire': 0,
        'Flying': 0,
        'Ghost': 0,
        'Grass': 0,
        'Ground': 0,
        'Ice': 0,
        'Normal': 0,
        'Poison': 0,
        'Psychic': 0,
        'Rock': 0,
        'Steel': 0,
        'Water': 0
    }
    for index, item in team_type_usage_series.items():
        if 'bug' in index:
            type_usage_dict['Bug'] += item
        elif 'dark' in index:
            type_usage_dict['Dark'] += item
        elif 'dragon' in index:
            type_usage_dict['Dragon'] += item
        elif 'electric' in index:
            type_usage_dict['Electric'] += item
        elif 'fairy' in index:
            type_usage_dict['Fairy'] += item
        elif 'fighting' in index:
            type_usage_dict['Fighting'] += item
        elif 'fire' in index:
            type_usage_dict['Fire'] += item
        elif 'flying' in index:
            type_usage_dict['Flying'] += item
        elif 'ghost' in index:
            type_usage_dict['Ghost'] += item
        elif 'grass' in index:
            type_usage_dict['Grass'] += item
        elif 'ground' in index:
            type_usage_dict['Ground'] += item
        elif 'ice' in index:
            type_usage_dict['Ice'] += item
        elif 'normal' in index:
            type_usage_dict['Normal'] += item
        elif 'poison' in index:
            type_usage_dict['Poison'] += item
        elif 'psychic' in index:
            type_usage_dict['Psychic'] += item
        elif 'rock' in index:
            type_usage_dict['Rock'] += item
        elif 'steel' in index:
            type_usage_dict['Steel'] += item
        else:
            type_usage_dict['Water'] += item

    total_usage = sum(type_usage_dict.values())

    result_df = (pd.DataFrame.from_dict({'type': type_usage_dict.keys(),
                                        'usage_count': type_usage_dict.values(),
                                        'usage_%': [x / total_usage * 100 for x in type_usage_dict.values()]})
                 .round(decimals=2)
                 .sort_values(by=['usage_count'],ascending=False ))

    del type_turns_df

    return result_df
