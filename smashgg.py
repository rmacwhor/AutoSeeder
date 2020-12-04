import requests
from requests.exceptions import HTTPError
from tournament import Player

''' Functions that handle interacting with the Smash.gg API
    to grab player information and modify seeding. '''

AUTH_TOKEN = "YOUR_TOKEN_HERE"


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
        return dict()


def get_event_entrants(event_id: int, num_entrants: int) -> [Player]:
    ''' Given an event ID for a tournament on Smash.gg and the number
    of entrants, returns a list of Player objects, representing players
    at the tournament. '''
    # TODO: Use GetPhaseSeeds query to get seed IDs as well as player IDs
    query = '''
    query EventEntrants($eventId: ID!, $page: Int!, $perPage: Int!) {
        event(id: $eventId) {
        id
        name
        entrants(query: {
          page: $page
          perPage: $perPage
        }) {
          pageInfo {
            total
            totalPages
          }
          nodes {
            id
            participants {
              player {
                id
                gamerTag
              }
              gamerTag
            }
          }
        }
      }
    }
    '''
    variables = { 'eventId': event_id, 'page': 1, 'perPage': num_entrants }
    response = run_query(query, variables)
    entrants = []
    if response and response["data"]["event"]:
        event = response["data"]["event"]
        for node in event["entrants"]["nodes"]:
            player = node["participants"][0]["player"]
            player = Player(player["gamerTag"], player["id"])
            entrants.append(player)
    return entrants

# TODO: Write function that updates seeding on smash.gg's site

if __name__ == '__main__':
    for entrant in get_event_entrants(536923, 25):
        print(entrant.tag, entrant.id)

    
