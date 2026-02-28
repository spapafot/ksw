# Ferry Schedule Creator

Creates ferry schedule combinations that are compliant with Greek legislation for the **Igoumenitsa–Corfu** route.

## Rules

- **Shift**: Up to 13 hours; loading/unloading and trip duration define feasible departure slots.
- **Break**: Mandatory 1-hour break between the 3h–6h mark of the shift.
- **Spacing**: Departures from the same port must be at least a minimum number of minutes apart (configurable, default 30).

Suitable for creating timetables where many ships operate with different specifications.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Optional arguments:

| Option                   | Description                                   | Default           |
| ------------------------ | --------------------------------------------- | ----------------- |
| `-o`, `--output`         | Output Excel file                             | `timetables.xlsx` |
| `-g`, `--min-gap`        | Min minutes between departures from same port | 30                |
| `-n`, `--max-iterations` | Max attempts to find a valid timetable        | 50000             |
| `-c`, `--config`         | Path to ships JSON config                     | `ships.json`      |

If no valid timetable is found (e.g. with default 30 min gap), try a lower `--min-gap` (e.g. `15`) or higher `--max-iterations`.

Examples:

```bash
python main.py -o summer.xlsx -g 45
python main.py -c my_ships.json -n 100000
```

## Configuration

Ship definitions live in `ships.json`. Each entry has:

- `name`: Ship name
- `start`: First departure time as `[hour, minute]`
- `total_departures`: Number of departures per day
- `starting_port`: `"H"` (Igoumenitsa) or `"K"` (Corfu)
- `duration`: Trip duration as `[hours, minutes]`

Edit this file to add or change ships without touching the code.

## Output

- Prints the combined timetable (IGO–CFU and CFU–IGO columns) to the console.
- Writes an Excel file with the same table plus per-ship schedule blocks; row layout is dynamic so ships with more departures get more rows.
