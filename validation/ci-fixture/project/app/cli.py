"""Command-line entry point for monthly reports: python -m app.cli [--csv] < rows.json"""
import json
import sys

from app.reports.monthly import export_csv, monthly_summary


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    rows = json.load(sys.stdin)
    print(export_csv(rows) if "--csv" in argv else json.dumps(monthly_summary(rows)))


if __name__ == "__main__":
    main()
