import csv


def count_users(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    return sum(1 for row in rows if row.get("email"))


if __name__ == "__main__":
    print(f"{count_users('users.csv')} users")
