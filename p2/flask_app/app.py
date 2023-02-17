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
    pokemons = poke_client.get_pokemon_list()

    return render_template('index.html', pokemons=pokemons)
    # pokemons= pokemon_names allows us to use the variable pokemon_names in the index.html file

@app.route('/pokemon/<pokemon_name>')
def pokemon_info(pokemon_name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """

    # pokemon = poke_client.get_pokemon_info(pokemon_name)


    # abilities = pokemon['abilities']
    # abilities = [each['ability']['name'] for each in abilities]
    # pokemon['abilities'] = abilities

    # return render_template('pokemon.html', pokemon=pokemon)
    return f'This is {pokemon_name}\'s user profile'


@app.route('/pokemon/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    pass
