from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Payout:
    seller_id: str
    amount_cents: int
    paid_on: date


PAYOUTS: list[Payout] = []
