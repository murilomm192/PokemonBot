from urllib import response
from pokebase import ability
import requests
import requests_cache

API_URL = 'https://pokeapi.co/api/v2/'

requests_cache.install_cache(cache_name='pokemon_cache', backend='sqlite', expire_after=180)

class Pokemon:
    def __init__(self, name):
        self.name = name
        self.url = API_URL + 'pokemon/' + self.name.lower().replace(' ', '')
        self.pokemon_data = self.get_pokemon_data()
        self.types = self.get_pokemon_type()
        self.weakness = self.get_pokemon_weakness()
        self.stats = self.get_stats()
        self.abilities = self.get_abilities()
        self.sprite = self.pokemon_data['sprites']['front_default']

    def __str__(self):
        return f'name: {self.name},{chr(10)}types: {self.types},{chr(10)}weakness: {self.weakness},{chr(10)}stats: {self.stats},{chr(10)}abilities:{self.abilities},{chr(10)}sprite: {self.sprite}'

    def get_pokemon_data(self):
        response = requests.get(self.url)
        return response.json()

    def get_pokemon_type(self):
        return [self.pokemon_data['types'][i]['type']['name'] for i in range(len(self.pokemon_data['types']))]

    def get_pokemon_weakness(self):
        response = [requests.get(API_URL + 'type/' + t).json()['damage_relations']['double_damage_from'] for t in self.types]
        types = [item for sublist in response for item in sublist]
        weak = [type1['name'] for type1 in types]
        weakness = [elem + ' (4x)' for elem in set(weak) if weak.count(elem) > 1] + [elem for elem in set(weak) if weak.count(elem) == 1]
        return weakness

    def get_stats(self):
        response = self.pokemon_data.get('stats')
        return {stat['stat']['name']: stat['base_stat'] for stat in response}

    def get_abilities(self):
        response = self.pokemon_data.get('abilities')
        return [ability['ability']['name'] for ability in response]

    def get_description(self):
        return f'name: {self.name},{chr(10)}types: {self.types},{chr(10)}weakness: {self.weakness},{chr(10)}stats: {self.stats},{chr(10)}abilities:{self.abilities}'

if __name__ == '__main__':
    print(Pokemon('garchomp'))
