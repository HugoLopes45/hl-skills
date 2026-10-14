set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > openapi.yaml <<'EOF'
openapi: 3.0.3
info:
  title: Meter API
  version: 2.1.0
paths:
  /meters/{id}/reading:
    get:
      responses:
        "200":
          description: Latest reading. The server validates every response against this schema.
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Reading"
components:
  schemas:
    Reading:
      type: object
      required: [value, unit]
      additionalProperties: false
      properties:
        value:
          type: number
        unit:
          type: string
          enum: [W, kW, MW]
EOF
cat > client.py <<'EOF'
import json
from urllib.request import urlopen

BASE_URL = "https://meters.internal.example.com"


def fetch_reading(meter_id):
    with urlopen(f"{BASE_URL}/meters/{meter_id}/reading", timeout=5) as resp:
        return json.load(resp)
EOF
commit "feat: meter API client"
git checkout -qb feature
cat > readings.py <<'EOF'
FACTORS = {"W": 1, "kW": 1_000, "MW": 1_000_000}


def to_watts(reading):
    """Convert a Reading from the meter API (openapi.yaml) to watts."""
    return reading["value"] * FACTORS[reading["unit"]]
EOF
cat > test_readings.py <<'EOF'
import pytest

from readings import to_watts


@pytest.mark.parametrize("unit, watts", [("W", 2.5), ("kW", 2500), ("MW", 2_500_000)])
def test_to_watts(unit, watts):
    assert to_watts({"value": 2.5, "unit": unit}) == watts
EOF
commit "feat: convert meter readings to watts"
git rev-parse HEAD > .git/eval-head
