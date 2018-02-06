from Gym import *
from Slot import *
from Team import *
from datetime import *
import itertools
import roundRobin

def overlap(c1, c2):
    return c1[0] == c2[0] or c1[0] == c2[1] or c1[1] == c2[0] or c1[1] == c2[1]

def group_overlap(group, c):
    for g in group:
        if overlap(g, c):
            return True
    return False

def roundrobin(a):
    combos = []
    for c in itertools.combinations(a, 2):
        combos.append(c)

    print(len(combos))

    desired_group_size = int(len(a) / 2)
    groups = []
    while combos:
        print(len(combos))
        print(combos)
        new_group = [combos.pop(0)]
        while len(new_group) < desired_group_size:
            for i in range(len(combos), 0, -1):
                c = combos[i - 1]
                if not group_overlap(new_group, c):
                    new_group.append(combos.pop(i - 1))
        groups.append(new_group)

        print(groups)

    return groups

def make_slots(dates, gyms, times):
    slots = []

    for d in dates:
        for g in gyms:
            for t in times:
                for c in g.courts:
                    slots.append(Slot(d, g, c, t))

    return slots

def fill_slots(slots, rr_divs):
    slot_index = 0

    while rr_divs:
        for rr_div in rr_divs:
            if slot_index >= len(slots):
                return
            if rr_div:
                group = rr_div.pop(0)
                for match in group:
                    slots[slot_index].teamA = match[0]
                    slots[slot_index].teamB = match[1]
                    slot_index += 1
                    if slot_index >= len(slots):
                        return

bbgc = Gym('Bellevue Boys and Girls\' Club', [1, 2, 3, 4])
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

bplus = []
for i in range(1, 8):
    bplus.append(Team('B+' + str(i), Div.BPlus))

bteams = []
for i in range(1, 9):
    bteams.append(Team('B' + str(i), Div.B))

cteams = []
for i in range(1, 5):
    cteams.append(Team('C' + str(i), Div.C))

divisions = [ateams, bplus, bteams, cteams]

rr_divs = []
for d in divisions:
    print(d)
    rr_divs.append(roundRobin.create_schedule(d))

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
