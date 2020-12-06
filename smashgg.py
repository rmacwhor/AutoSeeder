import requests
from requests.exceptions import HTTPError
from tournament import Player

''' Functions that handle interacting with the Smash.gg API
    to grab player information and modify seeding. '''

AUTH_TOKEN = "YOUR_AUTH_TOKEN"


def run_query(query: str, variables: {str: int or str}) -> dict:
    ''' Given the query and variables, sends a request to Smash.gg's API
    and returns the json response. Raises an exception if the status code
    indicates failure. '''
    try:
        request = requests.post('https://api.smash.gg/gql/alpha',
                                json = {'query': query, 'variables': variables},
                                headers = {'Authorization': f'Bearer {AUTH_TOKEN}'})
        request.raise_for_status()
        json = request.json()
        if not json:
            raise Warning("Response from smash.gg is empty.")
        return json
    except HTTPError as http_err:
        print(f"HTTPError occurred: {http_err}")
        print("You might have forgotten to paste your auth token into smashgg.py!")
        return dict()


def get_event_entrants(event_id: int, num_entrants: int, seeds: bool = False, phase_id: int = 0) -> [Player]:
    ''' Given an event ID for a tournament on Smash.gg and the number
    of entrants, returns a list of Player objects, representing players
    at the tournament. If the seeds flag is true, the Player objects will have
    both player IDs and seed IDs (all players must be marked as seeded on smash.gg
    for this to work). '''
    if seeds:
        with open('queries/queryphaseseeds.txt') as phaseseeds:
            query = phaseseeds.read()
        variables = { 'phaseId': phase_id, 'perPage': num_entrants }
    else:
        with open('queries/queryevententrants.txt') as evententrants:
            query = evententrants.read()
        variables = { 'eventId': event_id, 'perPage': num_entrants }
    response = run_query(query, variables)
    entrants = []
    event_key = "event" if not seeds else "phase"
    players_key = "entrants" if not seeds else "seeds"
    if response and response["data"][event_key]:
        event = response["data"][event_key]
        nodes = event[players_key]["nodes"]
        for node in nodes:
            seed_id = 0 if not seeds else node["id"]
            node = node if not seeds else node["entrant"]
            player = node["participants"][0]["player"]
            player = Player(player["gamerTag"], player["id"], seed_id)
            entrants.append(player)
    return entrants

# TODO: Write function that updates seeding on smash.gg's site
def update_smashgg_seeds(player_seeds: [Player], phase_id: int):
    ''' Given a list of seeded players and the phase ID, updates the seeding
    on the smash.gg page with the new seeds. '''
    seed_mapping = []
    for seed_num, player in enumerate(player_seeds, 1):
        seed_mapping.append({
            "seedId": player.get_seed_id(),
            "seedNum": seed_num
        })
    with open('queries/queryupdatephaseseeds.txt') as updatephaseseeds:
        query = updatephaseseeds.read()
    variables = { 'phaseId': phase_id, 'seedMapping': seed_mapping }
    response = run_query(query, variables)
    if 'errors' in response:
        print(f"An error occurred while updating seeds on smash.gg: {response['errors']}")
    else:
        print("Successfully updates smash.gg seeds.")

if __name__ == '__main__':
    for entrant in get_event_entrants(536923, 25, True, 886557):
        print(entrant.tag, entrant.get_player_id(), entrant.get_seed_id())

    
