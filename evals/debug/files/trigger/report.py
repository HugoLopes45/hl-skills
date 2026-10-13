def count_with_email(path):
    n = 0
    with open(path) as f:
        next(f)
        for line in f:
            name, email = line.strip().split(",")
            if "@" in email:
                n += 1
    return n


if __name__ == "__main__":
    print(f"{count_with_email('users.csv')} users")
