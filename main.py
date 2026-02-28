"""
Ferry timetable generator for Igoumenitsa–Corfu routes.

Generates compliant schedule combinations and exports to Excel.
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import random
from dataclasses import dataclass, field
from itertools import cycle, zip_longest
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd

from ship import PORT_CFU, PORT_IGO, Ship

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_MIN_GAP_MINUTES = 30
DEFAULT_MAX_ITERATIONS = 50_000
DEFAULT_OUTPUT_FILE = "timetables.xlsx"
DEFAULT_SHIPS_CONFIG = "ships.json"


@dataclass
class TimetableEntry:
    """A single departure: port code and time string (HH:MM)."""

    port: str
    time: str
    ship_name: str


@dataclass
class ShipTimetable:
    """One ship's chosen schedule as port–time pairs."""

    name: str
    entries: List[TimetableEntry] = field(default_factory=list)


def load_ships(config_path: Path) -> List[Ship]:
    """Load ship definitions from JSON and return validated Ship instances."""
    with open(config_path, encoding="utf-8") as f:
        raw = json.load(f)
    ships = []
    for item in raw:
        ship = Ship(
            name=item["name"],
            start=tuple(item["start"]),
            total_departures=item["total_departures"],
            starting_port=item["starting_port"],
            duration=tuple(item["duration"]),
        )
        if not ship.schedules:
            raise ValueError(
                f"Ship '{ship.name}' has no valid schedules (break/turnaround constraints)."
            )
        ships.append(ship)
    return ships


def generate_random_timetables(ships: List[Ship]) -> List[ShipTimetable]:
    """Pick a random valid schedule for each ship and return as timetables."""
    timetables: List[ShipTimetable] = []
    for ship in ships:
        schedule = random.choice(ship.schedules)
        ports = cycle((PORT_CFU, PORT_IGO)) if ship.starting_port == PORT_CFU else cycle((PORT_IGO, PORT_CFU))
        entries = [
            TimetableEntry(port=next(ports), time=dt.strftime("%H:%M"), ship_name=ship.name)
            for dt in schedule
        ]
        timetables.append(ShipTimetable(name=ship.name, entries=entries))
    return timetables


def create_dataframe(timetables: List[ShipTimetable]) -> pd.DataFrame:
    """Build a DataFrame with IGO–CFU and CFU–IGO columns per departure."""
    igo_to_cfu: List[str] = []
    cfu_to_igo: List[str] = []

    for st in timetables:
        for e in st.entries:
            line = f"{e.time} {st.name}"
            if e.port == PORT_IGO:
                igo_to_cfu.append(line)
            else:
                cfu_to_igo.append(line)

    df = pd.DataFrame(data=(sorted(igo_to_cfu), sorted(cfu_to_igo))).transpose()
    df[["IGO-CFU", "IGO_SHIP"]] = df[0].str.split(" ", n=1, expand=True)
    df[["CFU-IGO", "CFU_SHIP"]] = df[1].str.split(" ", n=1, expand=True)
    df = df.drop([0, 1], axis=1)
    return df


def check_minimum_gap(
    timetables: List[ShipTimetable],
    min_gap_minutes: int = DEFAULT_MIN_GAP_MINUTES,
) -> bool:
    """Return True if departures from each port are at least min_gap_minutes apart."""
    gap = datetime.timedelta(minutes=min_gap_minutes)
    igoumenitsa_times: List[datetime.datetime] = []
    corfu_times: List[datetime.datetime] = []

    for st in timetables:
        for e in st.entries:
            t = datetime.datetime.strptime(e.time, "%H:%M")
            if e.port == PORT_IGO:
                igoumenitsa_times.append(t)
            else:
                corfu_times.append(t)

    igoumenitsa_times.sort()
    corfu_times.sort()

    def gaps_ok(times: List[datetime.datetime]) -> bool:
        return all(
            (y - x) >= gap for x, y in zip(times, times[1:])
        )

    return gaps_ok(igoumenitsa_times) and gaps_ok(corfu_times)


def find_valid_timetables(
    ships: List[Ship],
    min_gap_minutes: int,
    max_iterations: int,
) -> Optional[List[ShipTimetable]]:
    """Try up to max_iterations random draws; return a valid timetable or None."""
    for attempt in range(max_iterations):
        timetables = generate_random_timetables(ships)
        if check_minimum_gap(timetables, min_gap_minutes):
            logger.info("Valid timetable found after %d attempt(s).", attempt + 1)
            return timetables
    logger.warning("No valid timetable found after %d attempts.", max_iterations)
    return None


def write_excel(
    df: pd.DataFrame,
    ships: List[Ship],
    timetables: List[ShipTimetable],
    output_path: Path,
    sheet_name: str = "1",
) -> None:
    """Write combined table and per-ship sheets; row layout is dynamic by ship."""
    # Build lookup ship_name -> (igo times, cfu times) for ordered ships
    ship_to_igo = df.set_index("IGO_SHIP").groupby(level=0)["IGO-CFU"].apply(list).to_dict()
    ship_to_cfu = df.set_index("CFU_SHIP").groupby(level=0)["CFU-IGO"].apply(list).to_dict()

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name=sheet_name, startrow=1, startcol=1, index=False)

        start_row = 1
        for ship in ships:
            igo_times = ship_to_igo.get(ship.name, [])
            cfu_times = ship_to_cfu.get(ship.name, [])
            rows = list(zip_longest(igo_times, cfu_times))
            block_height = max(len(rows), 1)

            if rows:
                pd.DataFrame(
                    rows,
                    columns=["K", "H"],
                ).to_excel(
                    writer,
                    sheet_name=sheet_name,
                    startrow=start_row,
                    startcol=6,
                    index=False,
                )
            start_row += block_height + 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Greek legislation–compliant ferry timetables (Igoumenitsa–Corfu)."
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT_FILE),
        help=f"Output Excel file (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "-g", "--min-gap",
        type=int,
        default=DEFAULT_MIN_GAP_MINUTES,
        help=f"Minimum minutes between departures from the same port (default: {DEFAULT_MIN_GAP_MINUTES})",
    )
    parser.add_argument(
        "-n", "--max-iterations",
        type=int,
        default=DEFAULT_MAX_ITERATIONS,
        help=f"Max random attempts to find a valid timetable (default: {DEFAULT_MAX_ITERATIONS})",
    )
    parser.add_argument(
        "-c", "--config",
        type=Path,
        default=Path(DEFAULT_SHIPS_CONFIG),
        help=f"Ships JSON config (default: {DEFAULT_SHIPS_CONFIG})",
    )
    args = parser.parse_args()

    ships = load_ships(args.config)
    timetables = find_valid_timetables(ships, args.min_gap, args.max_iterations)
    if timetables is None:
        raise SystemExit(1)

    df = create_dataframe(timetables)
    try:
        print(df)
    except UnicodeEncodeError:
        print("(Timetable generated; console encoding cannot display ship names.)")
    write_excel(df, ships, timetables, args.output)
    logger.info("Wrote %s", args.output)


if __name__ == "__main__":
    main()
