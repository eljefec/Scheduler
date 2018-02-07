class Slot:
    def __init__(self, date, gym, court, start):
        self.date = date
        self.gym = gym
        self.court = court
        self.start = start

        self.teamA = None
        self.teamB = None
        self.ref = None

    def __repr__(self):
        return self.gym.name + ' ' + str(self.court) + ' ' + str(self.start) + ' ' + str(self.teamA) + ' vs. ' + str(self.teamB) + ' ref: ' + str(self.ref)
