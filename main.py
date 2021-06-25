from ship import Ship

ermis = Ship(name="ΕΡΜΗΣ", start=[9, 0], total_departures=6, starting_port="K", duration=[1, 15])
eleni = Ship(name="ΕΛΕΝΗ", start=[3, 0], total_departures=4, starting_port="H", duration=[1, 45])
eirini = Ship(name="ΑΓΙΑ ΕΙΡΗΝΗ", start=[12, 0], total_departures=4, starting_port="K", duration=[1, 45])
nanti = Ship(name="ΝΑΝΤΗ", start=[13, 0], total_departures=4, starting_port="K", duration=[1, 45])
ionas = Ship(name="ΙΩΝΑΣ", start=[4, 30], total_departures=4, starting_port="H", duration=[1, 30])
spyridon = Ship(name="ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ", start=[8, 30], total_departures=4, starting_port="H", duration=[1, 30])

ships = [ermis, ionas, spyridon, eleni, eirini, nanti]
timetables_ = []

for i in ships:
    random_ = i.create_random_schedules()
    final_ = i.clean_data(random_)
    timetables_.append(i.convert_to_dict(final_))

print(timetables_)





