import smashgg
import smashdata
from tournament import Player, TournamentPlacing
from time import sleep


''' Main script that performs automatic seeding functionality. '''

def calculate_placing_score(tourney: TournamentPlacing, index: int) -> float:
    ''' Calculates a score for a single tournament placing. '''
    # Feel free to experiment with these constants to see how they affect
    # the seeds!
    prestige = 1.2  # Controls the rate at which a tournament's value increases
    online_constant = 0.75  # Reduces the value of online tournaments
    placing_constant = 0.94  # Controls the rate at which score goes down by placings
    recency = 0.97 # Controls the rate at which older scores "decay"

    tourney_value = tourney.num_entrants**prestige * (online_constant if tourney.online else 1)
    placing_score = tourney_value * placing_constant**(tourney.placement - 1) * recency**index
    return placing_score


def calculate_seed_score(tourneys: [TournamentPlacing]) -> float:
    ''' Calculates a seed score for a list of tournament placings. '''
    score = 0
    for index, tourney in enumerate(tourneys):
        score += calculate_placing_score(tourney, index)
        # only score 50 most recent
        if index == 50: break
    return score


def prompt_for_number(prompt: str) -> int:
    ''' Takes user input until a proper number is given. '''
    number = input(prompt)
    while not number.isnumeric():
        print(f"{number} must be a valid integer number.")
        number = input(prompt)
    return int(number)


def autoseeder(event_id: int, num_entrants: int, update: bool = True, phase_id: int = 0) -> [Player]:
    ''' Returns a sorted list of players seeded from highest to
    lowest. '''
    entrants = smashgg.get_event_entrants(event_id, num_entrants, update, phase_id)
    for entrant in entrants:
        placings = smashdata.get_player_placings(entrant)
        entrant.set_placings(placings)
        score = calculate_seed_score(placings)
        entrant.set_score(score)
        # To ensure politeness
        sleep(.3)
    seeds = sorted(entrants, key = lambda entrant: entrant.seed_score, reverse = True)
    if update:
        smashgg.update_smashgg_seeds(seeds, phase_id)
    return seeds

if __name__ == '__main__':
    event_id = prompt_for_number("Please enter the event's ID: ")
    num_entrants = prompt_for_number("Enter the number of entrants at this event: ")
    update = True if input("Would you like to automatically update the seeds on smash.gg? " +
                           "(Y or N, default = N): ") == 'Y' else False
    phase_id = 0
    if update:
        print("NOTE: Only players marked as seeded on the seeding page will get seeded by autoseeder.")
        input("Press enter to continue once you have verified all necessary players are marked seeded.")
        phase_id = prompt_for_number("Please enter the phase ID for the event: ")
    print("Running autoseeder... (will take a while because of server requests)")
    seeds = autoseeder(event_id, num_entrants, update, phase_id)
    for seed, player in enumerate(seeds, 1):
        print(f"{seed}.\t\t{player!s:30s}{player.seed_score}")
