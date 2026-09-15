#!/usr/bin/env python3
"""
Reverse of sheets_to_md.py: dump curated data-source markdown into CSVs that
paste into the canonical Google Sheet tabs.

Scope is deliberately limited to fields that already have a home in the two
existing tabs (the inventory tab and a per-track Fields tab). Richer markdown
content that the spreadsheet model doesn't yet represent — relationships,
use_cases, constraints, mcp tool lists, realms — is NOT dumped; it is reported
as "not represented in sheet" so the team can decide where it should live.

Usage:
    python3 md_to_sheet.py --track Support [-o out_dir]
Writes <out_dir>/<track>-inventory.csv and <out_dir>/<track>-fields.csv.
"""
import csv
import sys
import argparse
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent
DATA_SOURCES_DIR = SCRIPT_DIR / "data-sources"

# Markdown frontmatter content with no home in the current sheet tabs. Presence
# of any of these is reported per source so the team can decide where it goes.
UNREPRESENTED_KEYS = [
    "relationships", "use_cases", "constraints", "mcp_authenticated",
    "realms", "provides_data_for",
]

INVENTORY_HEADER = [
    "Track", "Data Source", "Description", "Category", "Canonical Sources",
    "Data Access mechanism(s)", "API", "MCP", "Storage Location",
    "Refresh Frequency", "Query Capacity", "Access Level", "User-Facing Priority",
    "Notes",
]


def mcp_cell(fm):
    """Serialize a source's mcp block into one cell: 'package | tool1, tool2'.

    Blank when no MCP server is available. Presence of a package implies
    available=true on the way back in (see sheets_to_md.parse_mcp). Per-tool
    method/description are NOT carried here — they remain richer md content; the
    cell preserves the MCP identity (package) and the tool inventory (names).
    """
    mcp = fm.get("mcp") or {}
    if not mcp.get("available"):
        return ""
    package = (mcp.get("url") or mcp.get("package") or "").strip().strip('"')
    tools = mcp.get("tools") or []
    names = [t.get("name", "") for t in tools if isinstance(t, dict) and t.get("name")]
    tools_str = ", ".join(names)
    if package and tools_str:
        return f"{package} | {tools_str}"
    return package or tools_str

FIELDS_HEADER = [
    "Data Source", "Name", "Type", "Authoritative Source", "Access",
    "Notes on Access", "Description", "Required", "Computed?", "Notes",
    "MCP Name", "Semantic Type", "Primary Key (DBs only)", "Reference (DBs Only)",
]


def load_sources():
    """Load every data-source markdown file's frontmatter."""
    sources = []
    for path in sorted(DATA_SOURCES_DIR.glob("*.md")):
        text = path.read_text()
        if not text.startswith("---"):
            continue
        fm = yaml.safe_load(text[3:text.index("---", 3)])
        if isinstance(fm, dict):
            sources.append(fm)
    return sources


def name_for_id(source_id, sources):
    """Resolve a slug id back to its source display name for the sheet."""
    for s in sources:
        if s.get("id") == source_id:
            return s.get("name", source_id)
    return source_id


def canonical_sources_cell(fm, sources):
    """The inventory's Canonical Sources cell: blank if canonical, else the
    display names of the upstream sources (inverse of parse_canonical_sources)."""
    if fm.get("is_canonical"):
        return ""
    cs = fm.get("canonical_source") or []
    if not isinstance(cs, list):
        cs = [cs]
    return ", ".join(name_for_id(c, sources) for c in cs)


def _yesno(value):
    return "TRUE" if value else "FALSE"


def inventory_row(fm, sources):
    return [
        fm.get("track", ""),
        fm.get("name", ""),
        fm.get("description", ""),   # Description column
        fm.get("category", ""),
        canonical_sources_cell(fm, sources),
        fm.get("data_access_mechanism", ""),
        fm.get("api_endpoint", ""),   # API column (after Data Access mechanism)
        mcp_cell(fm),                 # MCP column: 'package | tool1, tool2'
        fm.get("storage_location", ""),
        fm.get("refresh_frequency", ""),
        fm.get("query_capacity", ""),
        fm.get("access_level", ""),
        fm.get("priority", ""),
        fm.get("notes", ""),         # Notes column
    ]


def field_rows(fm):
    """One heading row (Data Source set, rest blank) then one row per field
    (Data Source blank). Round-trips with sheets_to_md.group_fields."""
    rows = [[fm.get("name", "")] + [""] * (len(FIELDS_HEADER) - 1)]
    for f in fm.get("fields", []):
        access = f.get("access", "")
        access_cell = ", ".join(access) if isinstance(access, list) else access
        rows.append([
            "",                                   # Data Source (blank = field of current source)
            f.get("name", ""),
            f.get("type", ""),
            f.get("authoritative_source", ""),
            access_cell,
            f.get("access_notes", ""),
            f.get("description", ""),
            _yesno(f.get("required")),
            _yesno(f.get("computed")),
            f.get("notes", ""),
            f.get("mcp_name", ""),
            f.get("semantic_type", ""),
            _yesno(f.get("primary_key")),
            f.get("references", ""),
        ])
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Dump curated data-source markdown into sheet-pasteable CSVs")
    parser.add_argument("--track", required=True, help="Track to dump (e.g. Support)")
    parser.add_argument("-o", "--out", default=".", help="Output directory")
    args = parser.parse_args()

    all_sources = load_sources()
    track_sources = [s for s in all_sources if s.get("track") == args.track]
    if not track_sources:
        parser.error(f"No data sources found for track {args.track!r}")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    inv_path = out_dir / f"{args.track}-inventory.csv"
    fields_path = out_dir / f"{args.track}-fields.csv"

    with open(inv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(INVENTORY_HEADER)
        for s in track_sources:
            w.writerow(inventory_row(s, all_sources))

    with open(fields_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(FIELDS_HEADER)
        for s in track_sources:
            for row in field_rows(s):
                w.writerow(row)

    # Report content that has no home in the sheet — the team's agenda.
    print(f"Wrote {inv_path}", file=sys.stderr)
    print(f"Wrote {fields_path}", file=sys.stderr)
    print(f"\n{len(track_sources)} {args.track} source(s) dumped.", file=sys.stderr)
    print("Markdown content NOT represented in the sheet (left in markdown):", file=sys.stderr)
    any_unrep = False
    for s in track_sources:
        present = [k for k in UNREPRESENTED_KEYS if s.get(k)]
        if present:
            any_unrep = True
            print(f"  {s.get('name')}: {', '.join(present)}", file=sys.stderr)
    if not any_unrep:
        print("  (none)", file=sys.stderr)


if __name__ == "__main__":
    main()
