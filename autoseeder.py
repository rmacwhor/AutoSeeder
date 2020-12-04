import smashgg
import smashdata
from tournament import Player, TournamentPlacing
from time import sleep


''' Main script that performs automatic seeding functionality. '''


def calculate_score(tourney: TournamentPlacing) -> float:
    ''' Calculates a score for a tournament placing.
    I'd like to develop a more advanced formula for seed calculations
    in the future! :) '''
    return tourney.num_entrants / tourney.placement


def prompt_for_number(prompt: str) -> int:
    ''' Takes user input until a proper number is given. '''
    number = input(prompt)
    while not number.isnumeric():
        print(f"{number} must be a valid integer number.")
        number = input(prompt)
    return int(number)


def autoseeder(event_id: int, num_entrants: int) -> [Player]:
    ''' Returns a sorted list of players seeded from highest to
    lowest. '''
    # TODO: Make this function automatically update the seeding on smash.gg as well!
    entrants = smashgg.get_event_entrants(event_id, num_entrants)
    for entrant in entrants:
        placings = smashdata.get_player_placings(entrant)
        entrant.set_placings(placings)
        score = 0
        for placing in entrant.placings:
            score += calculate_score(placing)
        entrant.set_score(score)
        # To ensure politeness
        sleep(.3)
    return sorted(entrants, key = lambda entrant: entrant.seed_score, reverse = True)

if __name__ == '__main__':
    event_id = prompt_for_number("Please enter the event's ID: ")
    num_entrants = prompt_for_number("Enter the number of entrants at this event: ")
    print("Running autoseeder... (will take a while because of server requests)")
    seeds = autoseeder(event_id, num_entrants)
    for seed, player in enumerate(seeds, 1):
        print(f"{seed}.\t\t{player!s:30s}{player.seed_score}")
