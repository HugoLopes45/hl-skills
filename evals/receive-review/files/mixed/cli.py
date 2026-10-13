import sys

from stats import mean


def load(path: str) -> list[float]:
    with open(path) as f:
        return [float(line) for line in f if line.strip()]


def main(path: str) -> None:
    print(f"{mean(load(path)):.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
