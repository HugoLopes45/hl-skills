import json
import os
import urllib.request

TOKEN = os.environ.get("LEDGER_TOKEN", "tok-live-77aa91c3")
ENDPOINT = "https://api.ledger-sync.example/v1/totals"


def push(totals):
    body = json.dumps(totals).encode()
    request = urllib.request.Request(ENDPOINT, data=body, headers={"Authorization": f"Bearer {TOKEN}"})
    urllib.request.urlopen(request, timeout=5)
