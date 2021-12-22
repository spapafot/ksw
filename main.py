from ship import Ship
from itertools import cycle, zip_longest
import pandas as pd
import datetime
import random

ermis = Ship(name="ΕΡΜΗΣ", start=[9, 0], total_departures=4, starting_port="K", duration=[1, 15])
spyridon = Ship(name="ΑΓΙΟΣ ΣΠΥΡΙΔΩΝ", start=[12, 45], total_departures=4, starting_port="K", duration=[1, 30])
eirini = Ship(name="ΑΓΙΑ ΕΙΡΗΝΗ", start=[6, 0], total_departures=3, starting_port="K", duration=[1, 45])

eleni = Ship(name="ΕΛΕΝΗ", start=[2, 30], total_departures=3, starting_port="H", duration=[1, 45])
nanti = Ship(name="ΝΑΝΤΗ", start=[10, 0], total_departures=4, starting_port="H", duration=[1, 45])
ionas = Ship(name="ΙΩΝΑΣ", start=[5, 15], total_departures=4, starting_port="H", duration=[1, 30])

theodora = Ship(name="ΑΓΙΑ ΘΕΟΔΩΡΑ", start=[9, 30], total_departures=4, starting_port="K", duration=[1, 30])
express = Ship(name="ΚΕΡΚΥΡΑ ΕΞΠΡΕΣ", start=[10, 00], total_departures=4, starting_port="K", duration=[1, 15])
kerkira = Ship(name="ΚΕΡΚΥΡΑ", start=[11, 45], total_departures=3, starting_port="K", duration=[1, 45])

alkinoos = Ship(name="ΑΛΚΙΝΟΟΣ", start=[8, 30], total_departures=3, starting_port="H", duration=[1, 45])
menekratis = Ship(name="ΜΕΝΕΚΡΑΤΗΣ", start=[7, 15], total_departures=4, starting_port="H", duration=[1, 45])
hora = Ship(name="ΑΝΩ ΧΩΡΑ ΙΙ", start=[4, 00], total_departures=4, starting_port="H", duration=[1, 30])

ships = [ermis, eleni, eirini, nanti, ionas, spyridon, hora, theodora, express, alkinoos, menekratis, kerkira]
N = 30

def generate_random_timetables():
    timetables = []

    for i in ships:
        if i.starting_port == "H":
            ports = cycle(("H", "K"))
        else:
            ports = cycle(("K", "H"))
        schedule = i.schedules[random.randint(0, len(i.schedules)-1)]
        timetables.append({
            "name": i.name,
            "schedule": [{next(ports): x.strftime("%H:%M")} for x in schedule]
        })
    return timetables


def create_dataframe(timetables):
    igo_cfu = []
    cfu_igo = []

    for d in timetables:
        for i in d['schedule']:
            for key, value in i.items():
                if key == "H":
                    igo_cfu.append(f"{value} {d['name']}")
                else:
                    cfu_igo.append(f"{value} {d['name']}")

    df = pd.DataFrame(data=(sorted(igo_cfu), sorted(cfu_igo))).transpose()
    df[['IGO-CFU', 'IGO_SHIP']] = df[0].str.split(' ', 1, expand=True)
    df[['CFU-IGO', 'CFU_SHIP']] = df[1].str.split(' ', 1, expand=True)
    df = df.drop([0, 1], axis=1)

    return df


def check(timetables, n=N):
    n = datetime.timedelta(minutes=n)
    ig = []
    cf = []
    for d in timetables:
        for i in d['schedule']:
            for key, value in i.items():
                if key == "H":
                    ig.append(datetime.datetime.strptime(value, "%H:%M"))
                else:
                    cf.append(datetime.datetime.strptime(value, "%H:%M"))
    ig = sorted(ig)
    cf = sorted(cf)

    if (all(y - x >= n for x, y in zip(ig, ig[1:]))) and all(y - x >= n for x, y in zip(cf, cf[1:])):
        return True
    else:
        return False

timetables = generate_random_timetables()

while not check(timetables):
    timetables = generate_random_timetables()

df = create_dataframe(timetables)
print(df)
counter = 1
sheet_name = "1"
writer = pd.ExcelWriter("timetables.xlsx", engine="xlsxwriter")

for i in ships:
    igo_data = df.loc[df["IGO_SHIP"] == i.name, "IGO-CFU"]
    cfu_data = df.loc[df["CFU_SHIP"] == i.name, "CFU-IGO"]
    pd.DataFrame(map(list, zip_longest(igo_data, cfu_data)),
                 columns=['K', 'H']).to_excel(excel_writer=writer,
                                              sheet_name=sheet_name,
                                              startrow=counter,
                                              startcol=6,
                                              index=False)
    counter += 5

df.to_excel(writer, sheet_name=sheet_name, startrow=1, startcol=1, index=False)
writer.save()
