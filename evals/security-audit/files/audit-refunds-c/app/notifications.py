import os

import requests

MAILER = os.environ["MAILER_URL"]


def send_refund_receipt(customer_id: int, order_id: int, amount_cents: int) -> None:
    requests.post(
        f"{MAILER}/send",
        json={"template": "refund", "customer_id": customer_id, "order_id": order_id, "amount_cents": amount_cents},
        timeout=10,
    ).raise_for_status()
