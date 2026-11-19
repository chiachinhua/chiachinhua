#!/usr/bin/env python3
"""Remove empty rows from every CSV in data/raw/ and write the results to data/clean/.

A row is empty when every field is blank or whitespace-only (e.g. a blank line
or a line of bare commas). The header row and all non-empty rows are kept as-is.
"""
import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def is_empty(row):
    return all(not field.strip() for field in row)


def clean_file(src: Path, dst: Path) -> tuple[int, int]:
    """Copy src to dst without empty rows. Returns (rows_kept, rows_removed)."""
    with src.open(newline="", encoding="utf-8-sig") as f:
        sample = f.read(64 * 1024)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.reader(f, dialect))

    kept = [r for r in rows if not is_empty(r)]
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=dialect.delimiter, quotechar=dialect.quotechar or '"').writerows(kept)
    return len(kept), len(rows) - len(kept)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=REPO_ROOT / "data" / "raw")
    p.add_argument("--output", type=Path, default=REPO_ROOT / "data" / "clean")
    args = p.parse_args(argv)

    files = sorted(args.input.glob("*.csv"))
    if not files:
        print(f"No CSV files found in {args.input}", file=sys.stderr)
        return 1

    for src in files:
        kept, removed = clean_file(src, args.output / src.name)
        print(f"{src.name}: kept {kept} rows, removed {removed} empty rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
