import datetime
from datetime import date

def adjacent_time(start, other):
    small = min(start, other)
    big = max(start, other)

    duration = datetime.datetime.combine(date.min, big) - datetime.datetime.combine(date.min, small)
    TWO_HOURS_IN_SECS = 7200
    return (duration.days == 0
            and duration.seconds > 0
            and duration.seconds < TWO_HOURS_IN_SECS)

def get_adjacent_teams(slot, day_slots):
    adjacent = []
    for other in day_slots:
        if other.gym == slot.gym and adjacent_time(other.start, slot.start):
            adjacent.append(other.teamA)
            adjacent.append(other.teamB)
    return adjacent

class Schedule:
    def __init__(self, slots, teams):
        self.teams = teams

        self.day_slots = {}
        for slot in slots:
            if slot.date not in self.day_slots:
                self.day_slots[slot.date] = []
            self.day_slots[slot.date].append(slot)

    def assign_refs(self):
        team_ref_count = {}

        for t in self.teams.values():
            t.ref_count = 0

        for date, day_slots in self.day_slots.items():
            for slot in day_slots:
                adjacent_teams = get_adjacent_teams(slot, day_slots)
                adjacent_teams.sort(key=lambda t: t.ref_count)
                for t in adjacent_teams:
                    if t.division <= slot.teamA.division:
                        slot.ref = t
                        t.ref_count += 1
                        break

if __name__ == '__main__':
    print(adjacent_time(datetime.time(3, 15), datetime.time(1, 45)))
    print(adjacent_time(datetime.time(3, 15), datetime.time(3, 15)))
