from ship import Ship
import datetime
import random

ermis = Ship(name="ΕΡΜΗΣ", start=[9, 15], total_departures=6, starting_port="K", duration=[1, 15])
eleni = Ship(name="ΕΛΕΝΗ", start=[3, 0], total_departures=4, starting_port="H", duration=[1, 45])
eirini = Ship(name="ΑΓΙΑ ΕΙΡΗΝΗ", start=[7, 30], total_departures=4, starting_port="K", duration=[1, 45])
nanti = Ship(name="ΝΑΝΤΗ", start=[10, 30], total_departures=4, starting_port="K", duration=[1, 45])
ionas = Ship(name="ΙΩΝΑΣ", start=[6, 30], total_departures=4, starting_port="H", duration=[1, 30])
spyridon = Ship(name="ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ", start=[10, 45], total_departures=4, starting_port="H", duration=[1, 30])

ships = [ermis, ionas, spyridon, eleni, eirini, nanti]

for i in ships:
    random_ = i.create_random_schedules()
    i.clean_data(random_)

all_tables = []

for ship in ships:
    c = random.randint(0, (len(ship.timetables)-1))
    for dep in ship.timetables[c]:
        all_tables.append([dep,ship.starting_port])

igo = [x[0] for x in all_tables if x[1] == "H"]
cfu = [x[0] for x in all_tables if x[1] == "K"]

igo.sort()
cfu.sort()
print(igo,cfu)



