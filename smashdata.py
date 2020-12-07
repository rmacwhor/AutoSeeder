import requests
from bs4 import BeautifulSoup
from tournament import Player, TournamentPlacing

''' Functions that handle scraping tournament data from smashdata.gg. '''

def make_soup(url: str) -> BeautifulSoup:
    ''' Helper function that constructs a BeautifulSoup object. '''
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "lxml")

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

def construct_tourney_placings(tourneys: list) -> [TournamentPlacing]:
    ''' Helper function to construct all the tourney placings from
    a list of HTML tags.'''
    results = []
    for tourney in tourneys:
        if is_valid(tourney):
            result = construct_tourney_placing(tourney)
            results.append(result)
    return results

def get_player_placings(player: Player) -> [TournamentPlacing]:
    ''' Given a player's tag and ID, retrieves the player's page
        on smashdata.gg and returns the player's tournament results
        as a list of TournamentPlacing objects. '''
    url = f"https://smashdata.gg/smash/ultimate/player/{player.tag}?id={player.id}"
    soup = make_soup(url)
    tourneys = soup.find_all(class_="tournament-listing")
    if tourneys:
        return construct_tourney_placings(tourneys)
    else:
        # check if on invalid players page
        invalid_players = soup.find(class_="invalid-players")
        # look for an ID match
        if invalid_players:
            for possible_player in invalid_players.find_all('a'):
                if possible_player['href'].endswith(str(player.id)):
                    print(f"Results for {player.tag} found under alias {possible_player.text}.")
                    url = "https://smashdata.gg" + possible_player['href']
                    soup = make_soup(url)
                    tourneys = soup.find_all(class_="tournament-listing")
                    return construct_tourney_placings(tourneys)
        print(f"No tournaments were found on record for {player.tag} (ID: {player.get_player_id()}).")
        return []

if __name__ == '__main__':
    player = Player("Vantage", 1508177)
    for result in get_player_placings(player):
        print(f"At {result.name}, {player.tag} placed #{result.placement} out of {result.num_entrants} attendees.")

