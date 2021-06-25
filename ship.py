import datetime


class Ship:
    def __init__(self, total_departures, duration, name, starting_port, start, schedule=[]):
        self.start = start
        self.starting_port = starting_port
        self.name = name
        self.duration = duration
        self.total_departures = total_departures
        self.schedule = schedule
        self.set_default_values()
        self.create_schedule()

    def set_default_values(self):
        self.loading = datetime.timedelta(minutes=30)
        self.unloading = datetime.timedelta(minutes=15)
        self.full_shift = datetime.timedelta(hours=13)
        self.break_ = datetime.timedelta(hours=1)
        self.step = datetime.timedelta(minutes=15)
        self.first_departure = datetime.datetime(year=2021, month=1, day=1, hour=self.start[0], minute=self.start[1])
        self.trip_time = datetime.timedelta(hours=self.duration[0], minutes=self.duration[1])
        self.shift_start = self.first_departure - datetime.timedelta(minutes=30)
        self.shift_end = self.shift_start + self.full_shift

    def create_schedule(self):
        dep = self.first_departure
        schedule = [dep]
        br = self.break_
        arrival = dep + self.trip_time + self.unloading

        for i in range(self.total_departures - 1):
            if arrival >= self.shift_start + datetime.timedelta(
                    hours=3) and arrival + self.break_ <= self.shift_start + datetime.timedelta(hours=6):
                n = dep + self.loading + self.trip_time + self.unloading + br
                arrival = n + self.trip_time + self.unloading
                br = datetime.timedelta(hours=0)
                # print(f"ΔΙΑΚΟΠΗ {(n - self.break_ - self.loading).time()} ΜΕ {(n - self.loading).time()}")
            else:
                n = dep + self.trip_time + self.unloading + self.loading
                arrival = n + self.trip_time + self.unloading
            if (n + self.trip_time + self.unloading) > self.shift_end:
                break
            else:
                schedule.append(n)
                dep = n
        if br == self.break_:
            self.schedule = schedule
        else:
            self.schedule = schedule

    def create_random_schedules(self):

        sch_ = self.schedule
        all = []
        all += sch_
        t = self.total_departures - 1
        time_needed = self.trip_time + self.loading + self.unloading

        while sch_[t] + self.trip_time + self.unloading <= self.shift_end - self.step:
            sch_[t] = sch_[t] + self.step
            all += sch_
            for i in range(t, 1, -1):
                while sch_[i] - time_needed >= sch_[i - 1]:
                    sch_[i - 1] = sch_[i - 1] + self.step
                    all += sch_

        t = 1
        while t < self.total_departures:
            while sch_[t] > sch_[t - 1] + time_needed:
                sch_[t] = sch_[t] - self.step
                all += sch_
                if sch_[3] - sch_[2] >= time_needed + 3 * self.break_:
                    t += 1
            t += 1
        return all

    def check_valid_break(self, schedule):
        x = False
        t = self.total_departures - 1
        for _ in schedule[::-1]:
            time_between = schedule[t] - schedule[t - 1]
            t -= 1
            if time_between >= self.loading + self.trip_time + self.unloading + self.break_:
                s = schedule[t] + self.trip_time + self.unloading
                f = s + self.break_
                if f <= self.shift_start + datetime.timedelta(
                        hours=6) and s >= self.shift_start + datetime.timedelta(hours=3):
                    #print(f"ΔΙΑΚΟΠΗ {(f - self.break_).time()} ΜΕ {f.time()}")
                    x = True
                    return x
                else:
                    s = self.shift_start + datetime.timedelta(hours=3)
                    if s + self.break_ + self.loading <= schedule[1]:
                        #print(f"ΔΙΑΚΟΠΗ {s.time()} ΜΕ {(s + self.break_).time()}")
                        x = True
                        return x
        return x

    def clean_data(self, final_):
        valid_ = []
        timetables = [final_[x:x + self.total_departures] for x in range(0, len(final_), self.total_departures)]
        for i in timetables:
            b = self.check_valid_break(i)
            if b:
                if i not in valid_:
                    valid_.append(i)
        return valid_

    def convert_to_dict(self, valid_timetables):
        dict_ = {
            "ship": self.name,
            "timetables": []
        }

        for i in valid_timetables:
            for x in range(len(i)):
                time = i[x].strftime("%H:%M")
                if self.starting_port == "H":
                    if x % 2 == 0:
                        starting_port = self.starting_port
                    else:
                        starting_port = "K"
                else:
                    if x % 2 == 0:
                        starting_port = self.starting_port
                    else:
                        starting_port = "H"
                dict_["timetables"].append({time: starting_port})

        print(dict_)





