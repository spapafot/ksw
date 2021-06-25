from ship import Ship

ermis = Ship(name="ΕΡΜΗΣ", start=[9, 30], total_departures=6, starting_port="K", duration=[1, 15])
eleni = Ship(name="ΕΛΕΝΗ", start=[3, 0], total_departures=4, starting_port="H", duration=[1, 45])
eirini = Ship(name="ΑΓΙΑ ΕΙΡΗΝΗ", start=[8, 0], total_departures=4, starting_port="K", duration=[1, 45])
nanti = Ship(name="ΝΑΝΤΗ", start=[13, 0], total_departures=4, starting_port="K", duration=[1, 45])
ionas = Ship(name="ΙΩΝΑΣ", start=[4, 30], total_departures=4, starting_port="H", duration=[1, 30])
spyridon = Ship(name="ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ", start=[7, 0], total_departures=4, starting_port="H", duration=[1, 30])

ships = [ermis, ionas, spyridon, eleni, eirini, nanti]
timetables_ = []
sch_=[]

for i in ships:
    random_ = i.create_random_schedules()
    final_ = i.clean_data(random_)
    dict_ = i.convert_to_dict(final_)
    timetables_.append(dict_)

ALL_=[]
IG_=[]
CF_=[]

for x in timetables_:
    for ship in ships:
        if ship.name == x["ship"]:
            for c in range(ship.total_departures):
                ALL_.append(x["timetables"][c])

print(ALL_)


for b in ALL_:
    for key,value in b.items():
        if value == "H":
            IG_.append(key)
        else:
            CF_.append(key)


IG_.sort()
CF_.sort()
print(IG_)
print(CF_)

