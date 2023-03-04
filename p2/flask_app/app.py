from flask import Flask, render_template
from model import PokeClient
app = Flask(__name__)

poke_client = PokeClient()

@app.route('/')
def index():
    """
    Must show all of the pokemon names as clickable links

    Check the README for more detail.
    """
    # get the list of pokemons
    pokemon_names = poke_client.get_pokemon_list()

    return render_template('index.html', pokemons=pokemon_names)
    # pokemons=pokemon_names allows us to use the variable pokemon_names in the index.html file

@app.route('/pokemon/<pokemon_name>')
def pokemon_info(pokemon_name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """

    pokemon_dic_info = poke_client.get_pokemon_info(pokemon_name)

    message = f'This is {pokemon_name}\'s stats'
    
    return render_template('pokeinfo.html', poke_info=pokemon_dic_info, message=message)


@app.route('/pokemon/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    pokemon_with_ability = poke_client.get_pokemon_with_ability(ability_name)

    message1 = f'Pokemons with the ability {ability_name}'
    message2 = f'Go back to the home page'

    return render_template('abilityinfo.html', pokemons = pokemon_with_ability, message1=message1, message2=message2)
