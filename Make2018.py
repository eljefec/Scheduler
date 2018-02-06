from Gym import *
from Slot import *
from Team import *
from datetime import *
import itertools
import roundRobin

def make_slots(dates, gyms, times):
    slots = []

    for d in dates:
        for g in gyms:
            for t in times:
                for c in g.courts:
                    slots.append(Slot(d, g, c, t))

    return slots

def generate_matches(rr_divs):
    group_index = 0
    while True:
        for rr_div in rr_divs:
            group = rr_div[group_index % len(rr_div)]
            for match in group:
                yield match
        group_index += 1

def fill_slots(slots, rr_divs):
    match_generator = generate_matches(rr_divs)

    slot_index = 0
    while slot_index < len(slots):
        match = next(match_generator)
        slots[slot_index].teamA = match[0]
        slots[slot_index].teamB = match[1]
        slot_index += 1

def roundrobin(a):
    s = roundRobin.create_schedule(a)
    filtered = []
    for round in s:
        new_round = []
        for match in round:
            if match[0] == 'BYE' or match[1] == 'BYE':
                pass
            else:
                new_round.append(match)
        filtered.append(new_round)
    return filtered

NAMES = {Div.A : 'A',
         Div.BPlus : 'B+',
         Div.B : 'B',
         Div.C : 'C'}

def get_division_name(division):
    return NAMES[division]

def make_division(division, count):
    teams = []
    for i in range(1, count+1):
        team_name = get_division_name(division) + str(i)
        teams.append(Team(team_name, division))
    return teams

def make_divisions():
    div_team_count = {Div.A : 7,
                      Div.BPlus : 7,
                      Div.B: 8,
                      Div.C: 4}

    divisions = []
    teams = {}

    for (div, count) in div_team_count.items():
        div_teams = make_division(div, count)
        divisions.append(div_teams)
        for t in div_teams:
            teams[t.name] = t

    teams['B+4'].corecount = 2
    teams['B+7'].corecount = 1
    teams['B5'].corecount = 1
    teams['B8'].corecount = 1

    return divisions

def main():
    bbgc = Gym('BBGC', [1, 2, 3, 4])
    tyee = Gym('Tyee', [1, 2])

    ateams = []

    better = Team('Better Lucky Than Good', Div.A)
    better.request_time(date(2018, 2, 11), Time.EARLY)
    better.request_time(date(2018, 3, 18), Time.EARLY)
# TODO: Fill rest of requests

    diva = Team('Diva Setters', Div.A)
    diva.prefer_time(Time.LATE)

    up = Team('On the Up and Up', Div.A)
    up.request_bye(date(2018, 3, 18))
    up.request_bye(date(2018, 3, 25))

    fambam = Team('FamBam', Div.A)
    fambam.prefer_gym(bbgc)
    fambam.prefer_time(Time.LATE)

    ateams.append(better)
    ateams.append(diva)
    ateams.append(up)
    ateams.append(fambam)

    divisions = make_divisions()

    rr_divs = []
    for d in divisions:
        print(d)
        rr_divs.append(roundrobin(d))

    dates = [date(2018, 2, 11),
             date(2018, 2, 18),
             date(2018, 3, 4)]

    times = [time(1, 30),
             time(3, 15)]

    gyms = [bbgc, tyee]

    slots = make_slots(dates, gyms, times)

    fill_slots(slots, rr_divs)
    for slot in slots:
        print(slot)

if __name__ == '__main__':
    main()
