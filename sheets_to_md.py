#!/usr/bin/env python3
"""
Convert Google-Sheets CSV exports of the ACCESS Data Inventory into the
data-sources/*.md markdown files that generate.py consumes.

Source of truth: the per-track field CSVs define which data sources and fields
exist. The inventory CSV (optional, via -d) only enriches catalog-level
metadata when a source name matches; an unmatched source is generated anyway
with a warning. Nothing crashes on mismatch.

Usage:
    python3 sheets_to_md.py -f path/to/fields-dir [-d inventory.csv] [-o data-sources] [--dry-run]
"""
import re
import csv
import sys
import argparse
from pathlib import Path

import yaml


def slugify(name: str) -> str:
    """Stable id from a source name: lowercase, non-alphanumerics -> single _."""
    slug = re.sub(r"[^a-z0-9]+", "_", name.strip().lower())
    return slug.strip("_")


def read_type(value: str):
    """Read the Type cell verbatim. Blank -> None (omit).

    No remapping: the sheet is the source of truth. An invalid type (e.g.
    "Video" or "decimal, text, int") flows through unchanged so validation
    flags it for fixing in the sheet, rather than being silently rewritten.
    """
    v = (value or "").strip()
    return v or None


def normalize_access(value: str):
    """Map a CSV Access cell to an access value. Blank -> None.

    A comma-separated value like "Public, Authenticated" becomes a list of the
    levels it names; a single value stays a scalar. Per-field access nuance
    (e.g. which JSON keys need auth) lives in the sheet's "Notes on Access"
    column, read separately in build_field — not synthesized here.
    """
    v = (value or "").strip()
    if not v:
        return None
    if "," in v:
        return [part.strip() for part in v.split(",") if part.strip()]
    return v


def _truthy(value: str) -> bool:
    """Sheet booleans arrive as TRUE/FALSE or as 1/0 depending on the export."""
    return (value or "").strip().upper() in ("TRUE", "1")


def is_placeholder_field(row: dict) -> bool:
    """A row that isn't a real field yet: blank name or a TODO marker."""
    name = (row.get("Name") or "").strip()
    if not name:
        return True
    return name.upper().startswith("TODO")


def build_field(row: dict) -> dict:
    """Build a markdown field dict from a fields-CSV row. Omits blank optionals."""
    field = {"name": (row.get("Name") or "").strip()}

    ftype = read_type(row.get("Type", ""))
    if ftype:
        field["type"] = ftype

    access = normalize_access(row.get("Access", ""))
    if access:
        field["access"] = access

    access_notes = (row.get("Notes on Access") or "").strip()
    if access_notes:
        field["access_notes"] = access_notes

    desc = (row.get("Description") or "").strip()
    if desc:
        field["description"] = desc

    if _truthy(row.get("Required", "")):
        field["required"] = True
    if _truthy(row.get("Computed?", "")):
        field["computed"] = True

    mcp_name = (row.get("MCP Name") or "").strip()
    if mcp_name:
        field["mcp_name"] = mcp_name

    semantic = (row.get("Semantic Type") or "").strip()
    if semantic:
        field["semantic_type"] = semantic

    if _truthy(row.get("Primary Key (DBs only)", "")):
        field["primary_key"] = True

    # Header casing varies between exports ("DBs only" vs "DBs Only").
    ref = (row.get("Reference (DBs Only)") or row.get("Reference (DBs only)") or "").strip()
    if ref:
        field["references"] = ref

    notes = (row.get("Notes") or "").strip()
    if notes:
        field["notes"] = notes

    # Field-level authoritative origin (distinct from the source-level
    # Canonical Sources): where this specific field's value comes from.
    authoritative = (row.get("Authoritative Source") or "").strip()
    if authoritative:
        field["authoritative_source"] = authoritative

    return field


def group_fields(rows):
    """Group field rows under their data source.

    A row with a non-blank 'Data Source' starts a new source. Subsequent rows
    with a blank 'Data Source' are that source's fields. Placeholder rows are
    collected into `skipped` rather than emitted.

    Returns (grouped: {source_name: [field_dict, ...]}, skipped: [(source, name), ...]).
    """
    grouped = {}
    skipped = []
    current = None

    for row in rows:
        ds = (row.get("Data Source") or "").strip()
        if ds:
            current = ds
            grouped.setdefault(current, [])
            continue
        if current is None:
            continue  # field row before any source heading; ignore
        if is_placeholder_field(row):
            skipped.append((current, (row.get("Name") or "").strip()))
            continue
        grouped[current].append(build_field(row))

    return grouped, skipped


def read_fields_dir(fields_dir: Path):
    """Read every *.csv in fields_dir. Returns (sources, skipped, warnings).

    sources: {source_name: {"track": str, "fields": [...]}}
    Track is parsed from the filename pattern '... - <Track> Fields.csv'.
    """
    sources = {}
    skipped = []
    warnings = []

    for csv_path in sorted(fields_dir.glob("*.csv")):
        track = parse_track_from_filename(csv_path.name)
        if track is None:
            warnings.append(f"Could not parse track from filename: {csv_path.name}; skipping file")
            continue
        with open(csv_path, newline="") as f:
            rows = list(csv.DictReader(f))
        grouped, file_skipped = group_fields(rows)
        skipped.extend((track, src, name) for src, name in file_skipped)
        for src_name, fields in grouped.items():
            if src_name in sources:
                warnings.append(
                    f"Duplicate data source '{src_name}' (track {track}); merging fields")
                sources[src_name]["fields"].extend(fields)
            else:
                sources[src_name] = {"track": track, "fields": fields}

    return sources, skipped, warnings


def parse_track_from_filename(filename: str):
    """Extract the track from a fields filename.

    Expected pattern: '<prefix> - <Track> Fields.csv', e.g.
    'ACCESS Data Source Inventory - Metrics Fields.csv' -> 'Metrics'.
    Returns None if the pattern doesn't match.
    """
    stem = filename[:-4] if filename.lower().endswith(".csv") else filename
    m = re.search(r"-\s*(.+?)\s+Fields$", stem)
    if m:
        return m.group(1).strip()
    return None


def read_inventory(inventory_path: Path):
    """Read the inventory CSV into {(track, data_source): row}."""
    inv = {}
    with open(inventory_path, newline="") as f:
        for row in csv.DictReader(f):
            key = ((row.get("Track") or "").strip(), (row.get("Data Source") or "").strip())
            inv[key] = row
    return inv


def parse_canonical_sources(value: str):
    """Derive (is_canonical, canonical_source) from the inventory's
    'Canonical Sources' cell.

    Blank (or the literal "none") means this source is itself canonical:
    -> (True, None). Otherwise the cell is a comma-separated list of the OTHER
    inventory data sources this one derives from, returned as slugified ids:
    -> (False, [ids]).
    """
    v = (value or "").strip()
    if not v or v.lower() == "none":
        return True, None
    ids = [slugify(part) for part in v.split(",") if part.strip()]
    return False, (ids or None)


def build_frontmatter(source_name, track, fields, inventory):
    """Assemble the frontmatter dict for one source, enriching from inventory if matched."""
    inv_row = inventory.get((track, source_name)) if inventory else None

    # Id is derived from the name by default. The sheet has no id column today;
    # an optional "id" column, if ever added, overrides the derived value (e.g.
    # to pin a shorter id). Kept as a harmless fallback so adding it later is
    # zero-friction.
    explicit_id = (inv_row.get("id") or "").strip() if inv_row else ""
    fm = {
        "id": explicit_id or slugify(source_name),
        "name": source_name,
        "track": track,
        "fields": fields,
    }

    if inv_row:
        if inv_row.get("Category"):
            fm["category"] = inv_row["Category"].strip()
        if inv_row.get("Access Level"):
            fm["access_level"] = inv_row["Access Level"].strip()
        # The inventory tab column is "User-Facing Priority"; accept "Priority" too.
        priority = (inv_row.get("User-Facing Priority") or inv_row.get("Priority") or "").strip()
        if priority:
            fm["priority"] = priority
        if inv_row.get("Description"):
            fm["description"] = inv_row["Description"].strip()
        if inv_row.get("Notes"):
            fm["notes"] = inv_row["Notes"].strip()
        # Simple source-level metadata: sheet column -> frontmatter key.
        for col, key in (
            ("Storage Location", "storage_location"),     # where the data physically lives
            ("Data Access mechanism(s)", "data_access_mechanism"),  # how to get it
            ("Refresh Frequency", "refresh_frequency"),   # how often it updates
            ("Query Capacity", "query_capacity"),         # query load it supports
        ):
            val = (inv_row.get(col) or "").strip()
            if val:
                fm[key] = val
        # Canonical Sources: blank -> canonical; else list of upstream sources.
        is_canon, canon = parse_canonical_sources(inv_row.get("Canonical Sources", ""))
        fm["is_canonical"] = is_canon
        if canon:
            fm["canonical_source"] = canon
        mcp_avail = (inv_row.get("MCP Available") or "").strip().lower()
        fm["mcp"] = {"available": mcp_avail in ("yes", "true", "partial")}

    return fm, (inv_row is not None)


def render_markdown(frontmatter: dict) -> str:
    """Serialize frontmatter dict + empty body into a markdown file string."""
    yaml_str = yaml.dump(frontmatter, sort_keys=False, default_flow_style=False,
                         allow_unicode=True, width=1000)
    return f"---\n{yaml_str}---\n"


def main():
    parser = argparse.ArgumentParser(
        description="Convert ACCESS data inventory sheet CSVs to data-sources/*.md")
    parser.add_argument("-f", "--fields", type=str, required=True,
                        help="Directory containing per-track field CSV exports")
    parser.add_argument("-d", "--data-sources", type=str,
                        help="Optional inventory CSV for catalog metadata enrichment")
    parser.add_argument("-o", "--out", type=str, default="data-sources",
                        help="Output directory for markdown files (default: data-sources)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would be written without writing files")
    args = parser.parse_args()

    fields_dir = Path(args.fields)
    if not fields_dir.is_dir():
        parser.error(f"--fields is not a directory: {fields_dir}")

    inventory = read_inventory(Path(args.data_sources)) if args.data_sources else None
    sources, skipped, warnings = read_fields_dir(fields_dir)

    out_dir = Path(args.out)
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    unmatched = []
    seen_ids = {}
    for source_name, data in sorted(sources.items()):
        fm, matched = build_frontmatter(source_name, data["track"], data["fields"], inventory)
        if inventory is not None and not matched:
            unmatched.append((data["track"], source_name))
        sid = fm["id"]
        if sid in seen_ids and seen_ids[sid] != source_name:
            warnings.append(f"id collision: '{source_name}' and '{seen_ids[sid]}' both -> {sid}")
        seen_ids[sid] = source_name
        out_path = out_dir / f"{sid}.md"
        if args.dry_run:
            print(f"[dry-run] would write {out_path} ({len(data['fields'])} fields)")
        else:
            out_path.write_text(render_markdown(fm))
        written += 1

    # Warnings to stderr so stdout stays clean.
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for track, src, name in skipped:
        print(f"SKIPPED placeholder field in {track}/{src}: {name!r}", file=sys.stderr)
    for track, src in unmatched:
        print(f"WARNING: source '{src}' (track {track}) not found in inventory; "
              f"generated from fields only", file=sys.stderr)

    print(f"Wrote {written} data source file(s) to {out_dir}"
          f"{' (dry run)' if args.dry_run else ''}", file=sys.stderr)


if __name__ == "__main__":
    main()
