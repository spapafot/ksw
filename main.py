from ship import Ship
import datetime
import random

ermis = Ship(name="ΕΡΜΗΣ", start=[9, 15], total_departures=6, starting_port="K", duration=[1, 15])
eleni = Ship(name="ΕΛΕΝΗ", start=[3, 0], total_departures=4, starting_port="H", duration=[1, 45])
eirini = Ship(name="ΑΓΙΑ ΕΙΡΗΝΗ", start=[7, 30], total_departures=3, starting_port="K", duration=[1, 45])
nanti = Ship(name="ΝΑΝΤΗ", start=[13, 0], total_departures=3, starting_port="H", duration=[1, 45])
ionas = Ship(name="ΙΩΝΑΣ", start=[5, 30], total_departures=4, starting_port="H", duration=[1, 30])
spyridon = Ship(name="ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ", start=[7, 0], total_departures=4, starting_port="H", duration=[1, 30])

ships = [ermis, ionas, spyridon, eleni, eirini, nanti]

for i in ships:
    random_ = i.create_random_schedules()
    i.clean_data(random_)


def gen_new(ships):
    igo_ = []
    cfu_ = []
    for ship in ships:
        port = ship.starting_port
        num = random.randint(0, len(ship.timetables)-1)
        for departure in ship.timetables[num]:
            if port == "H":
                igo_.append([departure, ship.name])
                port = "K"
            else:
                cfu_.append([departure, ship.name])
                port = "H"
    igo_.sort()
    cfu_.sort()
    return [igo_, cfu_]

all_ = gen_new(ships)

igo_ = [x[0] for x in all_[0]]
cfu_ = [x[0] for x in all_[1]]


num = 0
valid = []
all = []
time = datetime.timedelta(minutes=45)

while len(valid) <= 3:
    for _ in igo_:
        if num == len(igo_)-1:
            valid.append([igo_, cfu_])
            all.append(all_)
        else:
            if igo_[num] <= igo_[num+1] - time and cfu_[num] <= cfu_[num+1] - time:
                num += 1
            else:
                all_ = gen_new(ships)
                igo_ = [x[0] for x in all_[0]]
                cfu_ = [x[0] for x in all_[1]]
                num = 0


print(valid)
print(all)
