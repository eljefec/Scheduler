from enum import Enum
from functools import total_ordering

class Time(Enum):
    EARLY = 1
    LATE = 2

@total_ordering
class Div(Enum):
    A = 1
    BPlus = 2
    B = 3
    C = 4
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class TimeRequest:
    def __init__(self, date, time):
        self.date = date
        self.time = time

class Team:
    def __init__(self, name, division, corecount = 0):
        self.name = name
        self.division = division
        self.corecount = corecount
        self.bye_requests = []
        self.time_requests = []
        self.time_pref = None
        self.gym_pref = None
        self.ref_count = 0

    def request_bye(self, date):
        self.bye_requests.append(date)

    def request_time(self, date, time):
        self.time_requests.append(TimeRequest(date, time))

    def prefer_time(self, time):
        self.time_preference = time

    def prefer_gym(self, gym):
        self.gym_pref = gym

    def __repr__(self):
        return self.name
