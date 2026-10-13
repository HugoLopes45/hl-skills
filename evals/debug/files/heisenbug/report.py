import argparse
import sys

from loader import read_events
from stats import unique_users


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)
    events = read_events(args.path)
    if args.verbose:
        events = list(events)
        print(f"loaded {len(events)} events from {args.path}", file=sys.stderr)
    print(f"unique users: {unique_users(events)}")


if __name__ == "__main__":
    main()
