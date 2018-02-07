class Gym:
    def __init__(self, name, courts):
        self.name = name
        self.courts = courts

    def __lt__(self, other):
        return self.name < other.name
