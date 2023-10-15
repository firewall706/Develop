pokemon_data = [
    {"id": 1, "name": "Bulbasaur", "product": 1676544, "attack": 118, "defense": 111, "hp": 128, "level_40": 1115, "level_50": 1260},
    {"id": 2, "name": "Ivysaur", "product": 3346915, "attack": 151, "defense": 143, "hp": 155, "level_40": 1699, "level_50": 1921},
    {"id": 3, "name": "Venusaur", "product": 7110180, "attack": 198, "defense": 189, "hp": 190, "level_40": 2720, "level_50": 3075},
    {"id": 4, "name": "Charmander", "product": 1272984, "attack": 116, "defense": 93, "hp": 118, "level_40": 980, "level_50": 1108},
    {"id": 5, "name": "Charmeleon", "product": 3006108, "attack": 158, "defense": 126, "hp": 151, "level_40": 1653, "level_50": 1868},
    {"id": 6, "name": "Charizard", "product": 7175694, "attack": 223, "defense": 173, "hp": 186, "level_40": 2889, "level_50": 3266},
]

def compare_pokemon(pokemon1, pokemon2):
    """Compare two Pokemon based on their stats."""
    stats = ["attack", "defense", "hp", "level_40", "level_50"]
    for stat in stats:
        if pokemon1[stat] > pokemon2[stat]:
            return pokemon1
        elif pokemon2[stat] > pokemon1[stat]:
            return pokemon2
    return None

# Compare Bulbasaur and Charmander
pokemon1 = pokemon_data[0]
pokemon2 = pokemon_data[3]
winner = compare_pokemon(pokemon1, pokemon2)

if winner is not None:
    print(f"The winner between {pokemon1['name']} and {pokemon2['name']} is {winner['name']}!")
else:
    print(f"{pokemon1['name']} and {pokemon2['name']} are equally strong!")
