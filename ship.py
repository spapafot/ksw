import datetime
import itertools


class Ship:
    def __init__(self, total_departures, duration, name, starting_port, start):
        self.start = start
        self.starting_port = starting_port
        self.name = name
        self.duration = duration
        self.total_departures = total_departures
        self.loading = datetime.timedelta(minutes=30)
        self.unloading = datetime.timedelta(minutes=15)
        self.full_shift = datetime.timedelta(hours=13)
        self.break_ = datetime.timedelta(hours=1)
        self.step = datetime.timedelta(minutes=15)
        self.first_departure = datetime.datetime(year=2021, month=1, day=1, hour=self.start[0], minute=self.start[1])
        self.trip_time = datetime.timedelta(hours=self.duration[0], minutes=self.duration[1])
        self.shift_start = self.first_departure - datetime.timedelta(minutes=30)
        self.shift_end = self.shift_start + self.full_shift
        self.schedules = self.call()

    def create_random_schedules(self):
        possible_departures = [self.first_departure]
        p = self.first_departure

        while p <= self.shift_end - self.trip_time - self.loading:
            p += self.step
            possible_departures.append(p)

        combinations = itertools.combinations(possible_departures, self.total_departures)
        valid = [list(i) for i in combinations if all(x + self.trip_time + self.unloading + self.loading <= y for x, y in zip(i, i[1:])) and i[0] == self.first_departure]

        return valid

    def check_valid_break(self, schedules):
        valid_schedules = []
        arrival = self.trip_time + self.unloading
        three_hour_mark = self.shift_start + datetime.timedelta(hours=3)
        six_hour_mark = self.shift_start + datetime.timedelta(hours=6)

        for schedule in schedules:
            for t in range(2):
                if schedule[t] + arrival >= three_hour_mark or three_hour_mark + self.break_ + self.loading <= schedule[t+1]:
                    try:
                        if schedule[t] + arrival + self.break_ + self.loading <= schedule[t+1]:
                            if schedule[t] + arrival + self.break_ <= six_hour_mark:
                                valid_schedules.append(schedule)
                    except IndexError:
                        continue
        return valid_schedules

    def call(self):
        combinations = self.create_random_schedules()
        valid_schedules = self.check_valid_break(combinations)
        return valid_schedules
