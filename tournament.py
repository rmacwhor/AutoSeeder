

''' Classes that are abstractions of competitive concepts such as players and tournament placings. '''


class TournamentPlacing:
    def __init__(self, name: str, num_entrants: int, placement: int, online: bool):
        self.name = name
        self.num_entrants = num_entrants
        self.placement = placement
        self.online = online

    def __str__(self):
        return f"#{self.placement} out of {self.num_entrants} at {self.name}"


class Player:
    def __init__(self, tag: str, id: int):
        self.tag = tag
        self.id = id
        self.placings = []
        self.seed_score = 0

    def set_placings(self, placings: [TournamentPlacing]):
        self.placings = placings

    def set_score(self, score: float):
        self.seed_score = score

    def __str__(self):
        return self.tag