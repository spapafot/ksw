from ship import Ship
import pandas as pd
import datetime
import random

ermis = Ship(name="ΕΡΜΗΣ", start=[8, 45], total_departures=6, starting_port="K", duration=[1, 15])
eleni = Ship(name="ΕΛΕΝΗ", start=[3, 30], total_departures=4, starting_port="H", duration=[1, 45])
eirini = Ship(name="ΑΓΙΑ ΕΙΡΗΝΗ", start=[7, 30], total_departures=4, starting_port="K", duration=[1, 45])
nanti = Ship(name="ΝΑΝΤΗ", start=[10, 0], total_departures=4, starting_port="H", duration=[1, 45])
ionas = Ship(name="ΙΩΝΑΣ", start=[5, 30], total_departures=4, starting_port="H", duration=[1, 30])
spyridon = Ship(name="ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ", start=[13, 0], total_departures=4, starting_port="K", duration=[1, 30])

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
all_tables = []
time = datetime.timedelta(minutes=30)

while not all_tables:
    for _ in igo_:
        if num == len(igo_)-1:
            all_tables.append(all_)
            break
        else:
            try:
                if igo_[num] <= igo_[num+1] - time and cfu_[num] <= cfu_[num+1] - time:
                     num += 1
                else:
                    all_ = gen_new(ships)
                    igo_ = [x[0] for x in all_[0]]
                    cfu_ = [x[0] for x in all_[1]]
                    num = 0
            except IndexError:
                print("ΔΙΑΦΟΡΕΤΙΚΟΣ ΑΡΙΘΜΟΣ ΔΡΟΜΟΛΟΓΙΩΝ ΑΠΟ ΛΙΜΑΝΙ ΣΕ ΛΙΜΑΝΙ")
                exit()

for port in all_tables:
    igo_table = [[x.strftime("%H:%M"), y] for x, y in port[0]]
    cfu_table = [[x.strftime("%H:%M"), y] for x, y in port[1]]

igo_times = [x[0] for x in igo_table]
igo_ships = [x[1] for x in igo_table]
cfu_times = [x[0] for x in cfu_table]
cfu_ships = [x[1] for x in cfu_table]

with pd.ExcelWriter("empty.xlsx", engine="xlsxwriter") as writer:
    pd.DataFrame(list(map(list, zip(igo_times, igo_ships, cfu_times, cfu_ships))),
                 columns=['H', '', 'K', '']
                 ).to_excel(writer, sheet_name='1', startrow=1, startcol=1, index=False)

