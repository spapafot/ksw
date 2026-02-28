"""
Ship model and valid schedule generation under Greek maritime labor rules.

Rules: max 13h shift, mandatory 1h break between 3h–6h into shift,
minimum turnaround = trip + unloading + loading between departures.
"""

from __future__ import annotations

import datetime
import itertools
from typing import List, Tuple

# Port codes: Igoumenitsa (IGO) and Corfu/Kerkyra (CFU)
PORT_IGO = "H"
PORT_CFU = "K"


class Ship:
    """
    A ferry with fixed shift and trip parameters that can generate
    all valid daily schedules (departure times) under Greek legislation.
    """

    def __init__(
        self,
        name: str,
        start: Tuple[int, int],
        total_departures: int,
        starting_port: str,
        duration: Tuple[int, int],
    ) -> None:
        self.name = name
        self.start = start  # (hour, minute) first departure
        self.total_departures = total_departures
        self.starting_port = starting_port
        self.duration = duration  # (hours, minutes) trip time

        self.loading = datetime.timedelta(minutes=30)
        self.unloading = datetime.timedelta(minutes=15)
        self.full_shift = datetime.timedelta(hours=13)
        self.break_duration = datetime.timedelta(hours=1)
        self.step = datetime.timedelta(minutes=15)

        self.first_departure = datetime.datetime(
            year=2021, month=1, day=1, hour=start[0], minute=start[1]
        )
        self.trip_time = datetime.timedelta(hours=duration[0], minutes=duration[1])
        self.shift_start = self.first_departure - datetime.timedelta(minutes=30)
        self.shift_end = self.shift_start + self.full_shift

        self.schedules = self._compute_valid_schedules()

    def _compute_valid_schedules(self) -> List[List[datetime.datetime]]:
        """All valid departure sequences satisfying turnaround and break rules."""
        candidates = self._create_candidate_schedules()
        return self._filter_valid_break(candidates)

    def _create_candidate_schedules(self) -> List[List[datetime.datetime]]:
        """All schedules with correct first departure and minimum turnaround."""
        possible_departures = [self.first_departure]
        slot = self.first_departure
        min_turnaround = self.trip_time + self.unloading + self.loading

        while slot <= self.shift_end - self.trip_time - self.loading:
            slot += self.step
            possible_departures.append(slot)

        valid = []
        for combo in itertools.combinations(possible_departures, self.total_departures):
            combo_list = list(combo)
            if combo_list[0] != self.first_departure:
                continue
            if all(
                combo_list[i] + min_turnaround <= combo_list[i + 1]
                for i in range(len(combo_list) - 1)
            ):
                valid.append(combo_list)
        return valid

    def _filter_valid_break(
        self, schedules: List[List[datetime.datetime]]
    ) -> List[List[datetime.datetime]]:
        """
        Keep only schedules where the mandatory 1h break fits in the 3h–6h
        window. Checks every consecutive pair of departures for a gap that
        can contain the break.
        """
        arrival_duration = self.trip_time + self.unloading
        three_hour_mark = self.shift_start + datetime.timedelta(hours=3)
        six_hour_mark = self.shift_start + datetime.timedelta(hours=6)

        valid_schedules = []
        for schedule in schedules:
            for t in range(len(schedule) - 1):
                arrival = schedule[t] + arrival_duration
                next_departure = schedule[t + 1]
                # Break must start at or after 3h and end by 6h
                break_start = max(arrival, three_hour_mark)
                break_end = break_start + self.break_duration
                if break_end > six_hour_mark:
                    continue
                if break_end + self.loading <= next_departure:
                    valid_schedules.append(schedule)
                    break
        return valid_schedules
