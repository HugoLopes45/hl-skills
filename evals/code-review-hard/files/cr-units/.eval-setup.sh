set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
mkdir -p samples
cat > scale.py <<'EOF'
SCALES = [(1_000_000, "MW"), (1_000, "kW"), (1, "W")]


def scale_rows(rows):
    """Scale each series to the largest unit its peak reaches.

    rows: [{"time": str, "values": {series: watts}}]. A row may lack a series,
    for example solar production at night. Returns rows whose values are in the
    chosen unit, with a "units" map for the series present in that row.
    """
    peaks = {}
    for row in rows:
        for name, watts in row["values"].items():
            peaks[name] = max(peaks.get(name, 0), abs(watts))
    chosen = {}
    for name, peak in peaks.items():
        chosen[name] = next((f, u) for f, u in SCALES if peak >= f or f == 1)
    return [
        {
            "time": row["time"],
            "values": {n: w / chosen[n][0] for n, w in row["values"].items()},
            "units": {n: chosen[n][1] for n in row["values"]},
        }
        for row in rows
    ]
EOF
cat > chart.py <<'EOF'
DEFAULT_UNIT = "W"


def series_unit(rows, name):
    # The first rows can lack a series; take the unit from a row that has it.
    for row in rows:
        if name in row["units"]:
            return row["units"][name]
    return DEFAULT_UNIT


def chart_series(rows, name):
    return {
        "name": name,
        "unit": series_unit(rows, name),
        "points": [row["values"].get(name) for row in rows],
    }
EOF
cat > dashboard.py <<'EOF'
import json

from chart import chart_series
from scale import scale_rows


def site_chart(path):
    with open(path) as f:
        raw = json.load(f)
    rows = scale_rows(raw)
    return [chart_series(rows, name) for name in ("grid", "solar")]
EOF
cat > samples/site_a.json <<'EOF'
[
  {"time": "05:00", "values": {"grid": 850}},
  {"time": "06:00", "values": {"grid": 900, "solar": 120}},
  {"time": "12:00", "values": {"grid": 400, "solar": 2000}}
]
EOF
cat > test_chart.py <<'EOF'
from dashboard import site_chart


def test_grid_series():
    grid = site_chart("samples/site_a.json")[0]
    assert grid["unit"] == "W"
    assert grid["points"] == [850, 900, 400]
EOF
cat > README.md <<'EOF'
# Site dashboard

Charts power series per site. Values are scaled per series (W, kW, MW) by `scale.scale_rows`.
EOF
commit "feat: site power chart"
git checkout -qb feature
cat > chart.py <<'EOF'
DEFAULT_UNIT = "W"


def chart(rows):
    """Build every series of the chart in one pass."""
    if not rows:
        return []
    names = sorted({name for row in rows for name in row["values"]})
    units = rows[0]["units"]
    return [
        {
            "name": name,
            "unit": units.get(name, DEFAULT_UNIT),
            "points": [row["values"].get(name) for row in rows],
        }
        for name in names
    ]


def tooltip(raw_row, name):
    """Hover text for one point, from the unscaled row."""
    watts = raw_row["values"].get(name)
    return "no data" if watts is None else f"{watts:g} W"
EOF
cat > dashboard.py <<'EOF'
import json

from chart import chart
from scale import scale_rows


def site_chart(path):
    with open(path) as f:
        raw = json.load(f)
    return chart(scale_rows(raw))
EOF
cat > test_chart.py <<'EOF'
from chart import tooltip
from dashboard import site_chart


def test_grid_series():
    grid = site_chart("samples/site_a.json")[0]
    assert grid["unit"] == "W"
    assert grid["points"] == [850, 900, 400]


def test_tooltip():
    assert tooltip({"values": {"grid": 1500000}}, "grid") == "1.5e+06 W"
EOF
commit "refactor: build all chart series in one pass, add tooltips"
git rev-parse HEAD > .git/eval-head
