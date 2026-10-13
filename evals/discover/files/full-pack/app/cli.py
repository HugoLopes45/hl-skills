import argparse

from app.importer import import_csv
from app.report import monthly


def main():
    parser = argparse.ArgumentParser(prog="ledger")
    sub = parser.add_subparsers(dest="cmd", required=True)
    imp = sub.add_parser("import")
    imp.add_argument("path")
    sub.add_parser("report")
    args = parser.parse_args()
    if args.cmd == "import":
        print(import_csv(args.path))
    else:
        print(monthly())


if __name__ == "__main__":
    main()
