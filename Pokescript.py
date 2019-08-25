#!/usr/bin/env python
'''
Small script to find most optimal Pokemon team for original 150 Pokemon.
'''
import requests

POKEAPI_URL = 'https://pokeapi.co/api/v2'

def getPokemon():
    '''
    Generates list of tuples of pokemon names and their types
    '''
    pokemon = []
    for index in range(1, 251):
        pokeData = requests.get(f'{POKEAPI_URL}/pokemon/{index}').json()
        types = set()
        name = pokeData["name"]
        for elem in pokeData["types"]:
            types.add(elem["type"]["name"])
        pokemon.append((name, types))
    return pokemon

def getTypeRelations():
    '''
    Generates dict of each type to the type it counters.
    '''
    relations = {}
    for index in range(1, 19): # Get type #1-#18
        typeData = requests.get(f'{POKEAPI_URL}/type/{index}').json()
        thisType = typeData['name']
        thisEffectiveAgainst = []
        for typeObj in typeData['damage_relations']['double_damage_to']:
            thisEffectiveAgainst.append(typeObj['name'])
        relations[thisType] = thisEffectiveAgainst
    return relations

def main():
    '''
    Main func
    '''
    mostOptimalRem = float('inf')
    mostOptimalTeam = None
    def recurse(remaining, team, pokeList):
        nonlocal mostOptimalRem, mostOptimalTeam
        if not pokeList or len(team) >= 6:
            if len(remaining) < mostOptimalRem:
                print(
                    f'Team: {team}\nRemaining Types:{remaining}\nNum:{len(remaining)}\n'
                )
                mostOptimalRem = len(remaining)
                mostOptimalTeam = team
            return
        for (pokemon, types) in pokeList:
            if pokemon in team:
                continue
            recurse(remaining, team, pokeList[1:])
            if len(team) <= 5:
                effectiveAgainst = [typeRelations[t] for t in types]
                # Need to flatten list
                effectiveAgainst = [val for sublist in effectiveAgainst for val in sublist]
                for eType in effectiveAgainst:
                    remaining.discard(eType)
                team.add(pokemon)
                recurse(remaining, team, pokeList[1:])

    allPokemon = getPokemon()
    typeRelations = getTypeRelations()
    remainingTypes = {type for type in typeRelations}
    currentTeam = set()
    recurse(remainingTypes, currentTeam, allPokemon)
    print('Optimal team: \n', mostOptimalTeam)

if __name__ == '__main__':
    main()
