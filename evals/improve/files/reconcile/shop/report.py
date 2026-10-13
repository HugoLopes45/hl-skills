import sys

from shop.pagination import page


def render(rows):
    lines = []
    for row in rows:
        try:
            lines.append(f"{row['name']}: {row['total']:.2f}")
        except Exception:
            pass
    return "\n".join(lines)


def main(argv):
    rows = [{"name": "a", "total": 1.0}, {"name": "b", "total": 2.5}]
    print(render(page(rows, 0, 10)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
