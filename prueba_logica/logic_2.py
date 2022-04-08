
pokemons = [
	'audino', 'bagon', 'baltoy', 'banette', 'bidoof', 'braviary', 'bronzor',
	'carracosta', 'charmeleon', 'cresselia', 'croagunk', 'darmanitan', 'deino', 
	'emboar', 'emolga', 'exeggcute', 'gabite', 'girafarig', 'gulpin', 
	'haxorus', 'heatmor', 'heatran', 'ivysaur', 'jellicent', 'jumpluff',
	'kangaskhan', 'kricketune', 'landorus', 'ledyba', 'loudred',
	'lumineon', 'lunatone', 'machamp', 'magnezone', 'mamoswine', 'nosepass',
	'petilil', 'pidgeotto', 'pikachu', 'pinsir', 'poliwrath', 'poochyena',
	'porygon2', 'porygonz', 'registeel', 'relicanth', 'remoraid', 'ruﬄet',
	'sableye', 'scolipede', 'scrafty', 'seaking', 'sealeo', 'silcoon',
	'simisear', 'snivy', 'snorlax', 'spoink', 'starly', 'tirtouga', 'trapinch',
	'treecko', 'tyrogue', 'vigoroth', 'vulpix', 'wailord', 'wartortle', 'whismur',
	'wingull', 'yamask',
]


def get_next_pokemon(current_pokemon, current_list):
	""" funcion para encontrar el siguiente pokemon en una lista dada
        
        :author: Luis Merizalde - luis.merizalde@outlook.com

        :param current_pokemon(str): nombre del pokemon que va a ser evaluado
        :param current_list(list): lista de pokemones disponibles

        :return: siguiente pokemon si existe
        :rtype: str        
    """
	last_letter = current_pokemon[-1]
	filtered_pokemons = list(filter(lambda x: x.startswith(last_letter), current_list))
	print(filtered_pokemons)
	return filtered_pokemons[0] if filtered_pokemons else ''

def get_list_by_pokemon(pokemon):
	""" funcion para encontrar el siguiente pokemon en una lista dada
        
        :author: Luis Merizalde - luis.merizalde@outlook.com

        :param pokemon(str): pokemon que va a ser evaluado

        :return: lista de la cadena de pokemons que se puede formar
        :rtype: list        
    """
	original_pokemon = pokemon
	pokemons_copy = pokemons.copy()
	pokemons_copy.remove(pokemon)

	current_list = []
	current_list.append(pokemon)	

	flg = True
	while flg == True:
		# print(f'Evaluando pokemon {pokemon}')
		next_pokemon = get_next_pokemon(pokemon, pokemons_copy)
		if next_pokemon:
			# remover pokemon de la lista
			pokemons_copy.remove(next_pokemon)
			current_list.append(next_pokemon)
			pokemon = next_pokemon
		else:
			# Terminar ciclo si no hay pokemon
			flg = False

	# print(f'El pokemon {original_pokemon} genero lista de  {len(current_list)} elementos', current_list)

	return current_list

# get_list_by_pokemon('machap')
	
major_pokemons = 0
major_pokemon = {}
for x, pokemon in enumerate(pokemons):
	list_pokemons = get_list_by_pokemon(pokemon)
	if len(list_pokemons) > major_pokemons:
		major_pokemon['name'] = pokemon
		major_pokemon['pokemons'] = list_pokemons
		major_pokemon['count'] = len(list_pokemons)
		major_pokemons = len(list_pokemons)

print(major_pokemon)
	

