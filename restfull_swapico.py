# restfull_swapico.py
import requests

def _url(path):
    return 'https://swapi.co/api' + path

def get_films(film_Id):
    if film_Id:
        return requests.get(_url('/films/{:d}/'.format(film_Id)))
    else:
        return requests.get(_url('/films/'))

def get_starships(starship_id):
    if starship_id:
        return requests.get(_url('/starships/{:d}/'.format(starship_id)))
    else:
        return requests.get(_url('/starships/'))

def describe(characterUrl):
    #print('characterRequest', characterUrl)
    return requests.get(characterUrl)

def search_starship(name=""):
    if name:
        return requests.get(_url('/starships/?search='+name))
    else:
        return requests.get(_url('/starships/'))

def search_people(name=""):
    if name:
        return requests.get(_url('/people/?search='+name))
    else:
        return requests.get(_url('/people/'))
