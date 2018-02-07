from Gym import *
from Schedule import *
from Slot import *
from Team import *
from datetime import *
import itertools
import roundRobin

def make_slots(dates, gyms, times):
    slots = []

    for d in dates:
        for g in gyms:
            for c in g.courts:
                for t in times:
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

def make_divisions(gyms):
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

    bbgc = gyms['bbgc']
    tyee = gyms['tyee']

    teams['B+4'].corecount = 2
    teams['B+7'].corecount = 1
    teams['B5'].corecount = 1
    teams['B8'].corecount = 1

    better = teams['A1']
    better.request_time(date(2018, 2, 11), Time.EARLY)
    better.request_time(date(2018, 3, 18), Time.EARLY)
# TODO: Fill rest of requests

    diva = teams['A2']
    diva.prefer_time(Time.LATE)

    up = teams['A3']
    up.request_bye(date(2018, 3, 18))
    up.request_bye(date(2018, 3, 25))

    fambam = teams['A4']
    fambam.prefer_gym(bbgc)
    fambam.prefer_time(Time.LATE)

    return divisions, teams

def make_gyms():
    bbgc = Gym('BBGC', [1, 2, 3, 4])
    tyee = Gym('Tyee', [1, 2])

    return {'bbgc': bbgc, 'tyee': tyee}

def get_teams_with_byes(slots, all_teams):
    date_teams_dict = {}
    for slot in slots:
        if slot.date not in date_teams_dict:
            date_teams_dict[slot.date] = set()
        teams_set = date_teams_dict[slot.date]
        teams_set.add(slot.teamA)
        teams_set.add(slot.teamB)

    date_teams_with_byes = {}
    for date, teams_set in date_teams_dict.items():
        teams_with_byes = []
        for t in all_teams.values():
            if t not in teams_set:
                teams_with_byes.append(t)
        date_teams_with_byes[date] = teams_with_byes

    return date_teams_with_byes

def main():
    gyms = make_gyms()

    divisions, teams = make_divisions(gyms)

    rr_divs = []
    for d in divisions:
        print(d)
        rr_divs.append(roundrobin(d))

    dates = [date(2018, 2, 11),
             date(2018, 2, 18),
             date(2018, 3, 4)]

    times = [time(1, 30),
             time(3, 15)]

    slots = make_slots(dates, list(gyms.values()), times)

    cur_date = date(1867, 7, 1)

    fill_slots(slots, rr_divs)

    slots.sort(key=lambda slot: (slot.date, slot.gym, slot.start, slot.court))

    schedule = Schedule(slots, teams)
    schedule.assign_refs()

    for slot in slots:
        if cur_date != slot.date:
            print(slot.date)
            cur_date = slot.date
        print(slot)

    date_teams_with_byes = get_teams_with_byes(slots, teams)
    print(date_teams_with_byes)

if __name__ == '__main__':
    main()
