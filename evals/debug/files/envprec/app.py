import argparse
import sys

import config
import service
from client import call_with_retries


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--retries", type=int)
    parser.add_argument("--timeout", type=int)
    settings = config.resolve(parser.parse_args(argv))
    try:
        print(call_with_retries(lambda: service.fetch(settings["timeout"]), settings["retries"], log))
    except ConnectionError:
        print(f"giving up after {settings['retries'] + 1} attempts", file=sys.stderr)
        return 1
    return 0


def log(message):
    print(message, file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
