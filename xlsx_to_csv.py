#!/usr/bin/env python3
"""
Export the ACCESS Data Source Inventory workbook (File > Download > .xlsx from
the Google Sheet) into the CSV layout sheets_to_md.py reads:

    <out>/inventory.csv                                   the inventory tab
    <out>/fields/ACCESS Data Source Inventory - <Track> Fields.csv   one per "* Fields" tab

Other tabs (Questions, Sorted by Priority, ...) are ignored. Cells are written
as text; booleans become TRUE/FALSE like a Google Sheets CSV export; formula
cells use their last computed value.

Usage:
    python3 xlsx_to_csv.py "ACCESS Data Source Inventory.xlsx" [-o export]
    python3 sheets_to_md.py -f export/fields -d export/inventory.csv
"""
import argparse
import csv
import sys
from pathlib import Path

try:
    import openpyxl
except ImportError:  # pragma: no cover
    sys.exit("openpyxl is required: pip install openpyxl")

INVENTORY_TAB = "ACCESS Data Source Inventory"
FIELDS_SUFFIX = " Fields"


def cell_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    return str(value)


def sheet_rows(ws):
    """Rows as lists of text, trailing blank rows and columns trimmed."""
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    while rows and all(cell_text(c) == "" for c in rows[-1]):
        rows.pop()
    width = 0
    for r in rows:
        for i in range(len(r) - 1, -1, -1):
            if cell_text(r[i]) != "":
                width = max(width, i + 1)
                break
    return [[cell_text(c) for c in (r + [None] * width)[:width]] for r in rows]


def write_csv(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)


def export(xlsx: Path, out: Path):
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    for ws in wb.worksheets:
        if ws.title == INVENTORY_TAB:
            target = out / "inventory.csv"
        elif ws.title.endswith(FIELDS_SUFFIX):
            target = out / "fields" / f"{INVENTORY_TAB} - {ws.title}.csv"
        else:
            print(f"skip tab: {ws.title}", file=sys.stderr)
            continue
        rows = sheet_rows(ws)
        write_csv(rows, target)
        print(f"{ws.title}: {len(rows)} rows -> {target}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("xlsx", type=Path, help="Downloaded .xlsx of the Google Sheet")
    parser.add_argument("-o", "--out", type=Path, default=Path("export"),
                        help="Output directory (default: export)")
    args = parser.parse_args()
    if not args.xlsx.is_file():
        parser.error(f"not a file: {args.xlsx}")
    export(args.xlsx, args.out)


if __name__ == "__main__":
    main()
