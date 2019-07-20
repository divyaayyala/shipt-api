# restfull_swapico.py
import restfull_swapico
from assertpy import assert_that
from jsonschema import validate
import simplejson as json


def test_films_for_Obi_Wan():
    resp = restfull_swapico.get_films("")
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    i=0
    for film in resp.json()['results']:
        assert_that(resp.ok, 'HTTP Request OK').is_true()
        if film['title'] == 'A New Hope':
            for characterUrl in film['characters']:
                #print('characterurl', characterUrl)
                peopleResp = restfull_swapico.describe(characterUrl);
                assert_that(peopleResp.ok, 'HTTP Request OK').is_true()
                #print("characterName: ",peopleResp.json()["name"])
                if peopleResp.json()["name"] != 'Obi-Wan Kenobi':
                    continue
                characterName = peopleResp.json()["name"]
                assert_that(characterName =='Obi-Wan Kenobi',"Values are Equal")
                i=i+1
                break
    assert i>0, "Not Found Obi-Wan Kenobi"

def test_Enterprise_is_A_StarShip():
    resp = restfull_swapico.search_starship("Enterprise")
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    assert resp.json()['count']==0

def test_Chewbacca_is_Wookie():
    resp = restfull_swapico.search_people("Chewbacca")
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    assert resp.json()['count']==1
    i = 0
    for people in resp.json()['results']:
        species_associated = people['species']
        #print('species_associated', species_associated)
        for species_url in species_associated:
            species_resp = restfull_swapico.describe(species_url)
            assert_that(species_resp.ok, 'HTTP Request OK').is_true()
            if species_resp.json()["name"] != 'Wookiee':
                continue
            specie_name = species_resp.json()["name"]
            #print('specie_name', specie_name)
            assert specie_name=='Wookiee'
            i = i + 1
            break
        break
    #print('counter', i)
    assert i > 0, "Not Found Wookiee"

def test_Starships_pagination():
    resp = restfull_swapico.get_starships('')
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    #print('count',resp.json()['count'])
    count = resp.json()['count']
    paginationLink = resp.json()['next']
    #print('results_length', len(resp.json()['results']))
    assert_count = len(resp.json()['results'])
    while paginationLink is not None:
        paged_response = restfull_swapico.describe(paginationLink)
        assert_that(paged_response.ok, 'HTTP Request OK').is_true()
        paginationLink = paged_response.json()['next']
        #print('paginationLink', paginationLink)
        #print('results_length', len(paged_response.json()['results']))
        assert_count = assert_count + len(paged_response.json()['results'])

    assert count==assert_count, "Paginated Count is Not Same as actual"

def test_Starships_schema_validation():
    resp = restfull_swapico.get_starships('')
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    for start_ship in resp.json()['results']:
        #print('start_ship data: ',start_ship)
        assert 'name' in start_ship
        assert 'model' in start_ship
        assert 'crew' in start_ship
        assert 'hyperdrive_rating' in start_ship
        assert 'pilots' in start_ship
        assert 'films' in start_ship

def test_Starships_schema_validation2():
    resp = restfull_swapico.get_starships('')
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    with open('star_ships_schema.json', 'r') as f:
        schema_data = f.read()
    schema = json.loads(schema_data)
    print('parsed the schema')
    for start_ship in resp.json()['results']:
        validate(start_ship, schema)
