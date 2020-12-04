import requests
from bs4 import BeautifulSoup
from tournament import Player, TournamentPlacing

''' Functions that handle scraping tournament data from smashdata.gg. '''


def construct_tourney_placing(tourney) -> TournamentPlacing:
    ''' Helper function that constructs a TournamentPlacing object
    from a Tag object as part of a BeautifulSoup. '''
    name = tourney.find(class_="name-rank").span.text
    num_entrants = int(tourney["data-entrants"])
    placement = int(tourney["data-placing"])
    online = bool(int(tourney["data-online"]))
    return TournamentPlacing(name, num_entrants, placement, online)

def is_valid(tourney) -> bool:
    ''' Returns true if the tournament is valid (nothing wonky with the input). '''
    return tourney and tourney["data-placing"] != "None"

def get_player_placings(player: Player) -> [TournamentPlacing]:
    ''' Given a player's tag and ID, retrieves the player's page
        on smashdata.gg and returns the player's tournament results
        as a list of TournamentPlacing objects. '''
    url = f"https://smashdata.gg/smash/ultimate/player/{player.tag}"
    response = requests.get(url, params={'id': player.id})
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "lxml")
    results = []
    tourneys = soup.find_all(class_="tournament-listing")
    if tourneys:
        for tourney in tourneys:
            if is_valid(tourney):
                result = construct_tourney_placing(tourney)
                results.append(result)
    else:
        print(f"No tournaments were found on record for {player.tag}.")
    return results

if __name__ == '__main__':
    player = Player("Tempo", 28044)
    for result in get_player_placings(player):
        print(f"At {result.name}, {player.tag} placed #{result.placement} out of {result.num_entrants} attendees.")

