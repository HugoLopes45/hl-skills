def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def top(values: list[float], n: int) -> list[float]:
    ordered = sorted(values, reverse=True)
    return ordered[:n]


def report(values: list[float]) -> str:
    if not values:
        return "no data"
    return f"mean={mean(values):.2f} top={top(values, 3)}"
