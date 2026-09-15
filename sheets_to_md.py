#!/usr/bin/env python3
"""
Convert Google-Sheets CSV exports of the ACCESS Data Inventory into the
data-sources/*.md markdown files that generate.py consumes.

Source of truth: the per-track field CSVs define which data sources and fields
exist. The inventory CSV (optional, via -d) only enriches catalog-level
metadata when a source name matches; an unmatched source is generated anyway
with a warning. Nothing crashes on mismatch.

Existing files in the output directory are updated in place, matched by id or
by name: every sheet-owned key (see SHEET_OWNED_KEYS) is replaced from the
sheet, while keys the sheet has no column for (use_cases, constraints,
relationships, realms, mcp_authenticated, ...) and the markdown body are
preserved. Every inventory row is written, including ones with no field rows
yet (their file says so; pass --skip-empty to leave those out). An existing
file whose sheet source has no field rows keeps its curated fields.

Data problems are not fixed here and do not stop generation: they are written
to sync-report.json, which generate.py folds into docs/data-quality.md so the
team can see what to clean up in the sheet.

Usage:
    python3 xlsx_to_csv.py "ACCESS Data Source Inventory.xlsx" -o export
    python3 sheets_to_md.py -f export/fields -d export/inventory.csv [-o data-sources] [--dry-run]
"""
import re
import csv
import sys
import json
import argparse
from datetime import datetime
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


SPREADSHEET_ERRORS = ("#NUM!", "#REF!", "#N/A", "#VALUE!", "#DIV/0!", "#NAME?", "#ERROR!", "#NULL!")


def is_error_cell(value: str) -> bool:
    """A spreadsheet formula error (#NUM!, #REF!, ...) exported as text."""
    return (value or "").strip().upper() in SPREADSHEET_ERRORS


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
    with a blank 'Data Source' are that source's fields. TODO placeholder rows
    are collected into `skipped` rather than emitted; fully blank rows (the
    empty grid below the data) are ignored silently. A heading that is a
    spreadsheet error value (a broken lookup formula) is collected into
    `bad_headings` and its rows are dropped.

    Returns (grouped: {source_name: [field_dict, ...]},
             skipped: [(source, name), ...],
             bad_headings: [str, ...]).
    """
    grouped = {}
    skipped = []
    bad_headings = []
    current = None

    for row in rows:
        ds = (row.get("Data Source") or "").strip()
        if ds:
            if is_error_cell(ds):
                bad_headings.append(ds)
                current = None
                continue
            current = ds
            grouped.setdefault(current, [])
            continue
        if current is None:
            continue  # field row before any source heading; ignore
        if is_placeholder_field(row):
            name = (row.get("Name") or "").strip()
            if name:
                skipped.append((current, name))
            continue
        grouped[current].append(build_field(row))

    return grouped, skipped, bad_headings


def read_fields_dir(fields_dir: Path):
    """Read every *.csv in fields_dir. Returns (sources, skipped, warnings).

    sources: {(track, source_name): {"track": str, "name": str, "fields": [...]}}
    Keyed by track as well as name because two tracks can list a source of the
    same name (e.g. "Publications" under both Allocations and Metrics); the
    inventory tab is keyed the same way.
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
        grouped, file_skipped, bad_headings = group_fields(rows)
        skipped.extend((track, src, name) for src, name in file_skipped)
        warnings.extend(
            f"Skipped spreadsheet error heading {h!r} in {csv_path.name}" for h in bad_headings)
        for src_name, fields in grouped.items():
            key = (track, src_name)
            if key in sources:
                warnings.append(
                    f"Duplicate data source '{src_name}' (track {track}); merging fields")
                sources[key]["fields"].extend(fields)
            else:
                sources[key] = {"track": track, "name": src_name, "fields": fields}

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


def add_inventory_only_sources(sources: dict, inventory: dict):
    """Add inventory rows that appear in no Fields tab as field-less sources.

    The catalog value of a row (description, access level, sensitivity) does
    not depend on anyone having typed its fields yet. Returns the (track, name)
    keys added, for reporting.
    """
    added = []
    for (track, name) in inventory:
        if not track or not name or is_error_cell(name):
            continue
        if (track, name) not in sources:
            sources[(track, name)] = {"track": track, "name": name, "fields": []}
            added.append((track, name))
    return added


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


def parse_mcp(inv_row: dict):
    """Parse the inventory 'MCP' cell into an mcp block.

    Cell format: 'package | tool1, tool2, ...' (see md_to_sheet.mcp_cell). The
    first segment is either an npm package ("@access-mcp/events") or, as the
    sheet now records it, the server's URL ("https://mcp.access-ci.org/events/mcp");
    a URL lands in `url`, anything else in `package`.
    Presence of any content => available: true; a package and/or a tool list are
    extracted. Per-tool method/description are not carried in the sheet, so tools
    round-trip as name-only entries. Falls back to a legacy 'MCP Available'
    yes/no column if an older sheet has one and no 'MCP' cell.
    """
    cell = (inv_row.get("MCP") or "").strip()
    if not cell:
        legacy = (inv_row.get("MCP Available") or "").strip().lower()
        return {"available": legacy in ("yes", "true", "partial")}

    package, _, tools_part = cell.partition("|")
    package = package.strip().strip('"')
    tool_names = [t.strip() for t in tools_part.split(",") if t.strip()]

    mcp = {"available": True}
    if package.startswith(("http://", "https://")):
        mcp["url"] = package
    elif package:
        mcp["package"] = package
    if tool_names:
        mcp["tools"] = [{"name": n} for n in tool_names]
    return mcp


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
            ("API", "api_endpoint"),                      # endpoint URL (drives the [API] link)
            ("Docs", "docs_url"),                         # human-readable API/service docs
            ("Refresh Frequency", "refresh_frequency"),   # how often it updates
            ("Query Capacity", "query_capacity"),         # query load it supports
            ("Sensitivity", "sensitivity"),               # data sensitivity rating
            ("How to request access", "how_to_request_access"),
        ):
            val = (inv_row.get(col) or "").strip()
            if val:
                fm[key] = val
        # Canonical Sources: blank -> canonical; else list of upstream sources.
        is_canon, canon = parse_canonical_sources(inv_row.get("Canonical Sources", ""))
        fm["is_canonical"] = is_canon
        if canon:
            fm["canonical_source"] = canon
        fm["mcp"] = parse_mcp(inv_row)

    return fm, (inv_row is not None)


def render_markdown(frontmatter: dict, body: str = "") -> str:
    """Serialize frontmatter dict + markdown body into a markdown file string."""
    yaml_str = yaml.dump(frontmatter, sort_keys=False, default_flow_style=False,
                         allow_unicode=True, width=1000)
    out = f"---\n{yaml_str}---\n"
    if body.strip():
        out += "\n" + body.strip("\n") + "\n"
    return out


# Frontmatter keys the sheet owns. On regeneration each is replaced from the
# sheet, or dropped when the sheet cell is blank. Every other key found in an
# existing file (use_cases, constraints, relationships, realms,
# mcp_authenticated, dynamic, provides_data_for, ...) and the markdown body
# are hand-curated, because the sheet has no column for them, and survive.
SHEET_OWNED_KEYS = (
    "name", "track", "fields", "category", "access_level", "priority",
    "description", "notes", "storage_location", "data_access_mechanism",
    "api_endpoint", "docs_url", "refresh_frequency", "query_capacity",
    "sensitivity", "how_to_request_access", "is_canonical", "canonical_source",
    "mcp",
)


def split_frontmatter(text: str):
    """Split a markdown file into (frontmatter dict or None, body)."""
    if not text.startswith("---"):
        return None, text
    end = text.index("---", 3)
    fm = yaml.safe_load(text[3:end]) or {}
    return fm, text[end + 3:].strip("\n")


def load_existing(out_dir: Path):
    """Index existing *.md in out_dir: by_id -> entry, by_name -> [entries].
    An entry is (path, frontmatter, body). Names can repeat across tracks."""
    by_id, by_name = {}, {}
    for path in sorted(out_dir.glob("*.md")):
        fm, body = split_frontmatter(path.read_text())
        if not fm:
            continue
        entry = (path, fm, body)
        if fm.get("id"):
            by_id[str(fm["id"])] = entry
        if fm.get("name"):
            by_name.setdefault(str(fm["name"]).strip(), []).append(entry)
    return by_id, by_name


def find_existing(by_id: dict, by_name: dict, source_id: str, name: str, track: str):
    """Locate the existing file for a sheet source: by id (plain or
    track-suffixed), else by name, and only within the same track (two tracks
    may both list "Publications")."""
    candidates = [by_id.get(source_id), by_id.get(f"{source_id}_{slugify(track)}")]
    candidates += by_name.get(name, [])
    for entry in candidates:
        if entry and str(entry[1].get("track", "")).strip() == track:
            return entry
    return None


def merge_mcp_tools(sheet_mcp: dict, existing_mcp) -> dict:
    """The sheet decides which tools exist; an existing tool's method and
    description (not carried by the sheet) ride along when the name matches."""
    prior = {t.get("name"): t for t in (existing_mcp or {}).get("tools") or []
             if isinstance(t, dict)}
    if sheet_mcp.get("tools"):
        sheet_mcp["tools"] = [{**prior.get(t["name"], {}), **t} for t in sheet_mcp["tools"]]
    if (existing_mcp or {}).get("notes"):
        sheet_mcp["notes"] = existing_mcp["notes"]  # curated; no sheet column
    return sheet_mcp


def merge_frontmatter(existing: dict, sheet: dict, warnings: list, label: str) -> dict:
    """Overlay sheet-owned keys onto an existing file's frontmatter.

    Existing key order is kept so regeneration diffs stay small. The existing
    id wins (files may carry a shorter id than the name slug). If the sheet has
    no field rows for this source yet, curated fields are kept and reported.
    """
    sheet = dict(sheet)
    if not sheet.get("fields"):
        sheet.pop("fields", None)
        if existing.get("fields"):
            warnings.append(f"{label}: sheet has no field rows; kept {len(existing['fields'])} "
                            f"curated field(s) — paste them into the sheet")
    if "mcp" in sheet:
        sheet["mcp"] = merge_mcp_tools(dict(sheet["mcp"]), existing.get("mcp"))

    merged = {}
    for key, value in existing.items():
        if key not in SHEET_OWNED_KEYS or key == "id":
            merged[key] = value
        elif key in sheet:
            merged[key] = sheet[key]
        elif key == "fields":
            merged[key] = value
        elif value not in (None, "", [], {}):
            warnings.append(f"{label}: dropped '{key}' (blank in sheet; was {value!r})")
    for key, value in sheet.items():
        if key not in merged and key != "id":
            merged[key] = value
    return merged


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
    parser.add_argument("--skip-empty", action="store_true",
                        help="Do not write sources that have no field rows yet "
                             "(default: write them; an existing file is always updated)")
    parser.add_argument("--report", type=str, default="sync-report.json",
                        help="Where to write the JSON sync report generate.py reads "
                             "for docs/data-quality.md (default: sync-report.json)")
    args = parser.parse_args()

    fields_dir = Path(args.fields)
    if not fields_dir.is_dir():
        parser.error(f"--fields is not a directory: {fields_dir}")

    inventory = read_inventory(Path(args.data_sources)) if args.data_sources else None
    sources, skipped, warnings = read_fields_dir(fields_dir)
    inventory_only = add_inventory_only_sources(sources, inventory) if inventory else []

    out_dir = Path(args.out)
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    by_id, by_name = load_existing(out_dir) if out_dir.is_dir() else ({}, {})
    touched = set()
    written = 0
    unmatched = []
    skipped_empty = []
    seen_ids = {}
    for (track, source_name), data in sorted(sources.items()):
        fm, matched = build_frontmatter(source_name, track, data["fields"], inventory)
        if inventory is not None and not matched:
            unmatched.append((track, source_name))

        existing = find_existing(by_id, by_name, fm["id"], source_name, track)
        body = ""
        if existing:
            out_path, old_fm, body = existing
            touched.add(out_path)
            fm = merge_frontmatter(old_fm, fm, warnings, f"{track}/{source_name}")
        elif not data["fields"] and args.skip_empty:
            skipped_empty.append((track, source_name))
            continue
        else:
            if fm["id"] in seen_ids or (out_dir / f"{fm['id']}.md").exists():
                # Same name in another track: keep both, disambiguate by track.
                fm["id"] = f"{fm['id']}_{slugify(track)}"
                warnings.append(f"{track}/{source_name}: id collides with another track; using {fm['id']}")
            out_path = out_dir / f"{fm['id']}.md"

        sid = fm["id"]
        if sid in seen_ids and seen_ids[sid] != (track, source_name):
            warnings.append(f"id collision: {track}/{source_name} and "
                            f"{'/'.join(seen_ids[sid])} both -> {sid}")
        seen_ids[sid] = (track, source_name)
        action = "update" if existing else "create"
        if args.dry_run:
            print(f"[dry-run] would {action} {out_path} ({len(fm.get('fields') or [])} fields)")
        else:
            out_path.write_text(render_markdown(fm, body))
        written += 1

    stale = sorted({entry[0] for entry in by_id.values()} - touched)

    # Warnings to stderr so stdout stays clean.
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for track, src, name in skipped:
        print(f"SKIPPED placeholder field in {track}/{src}: {name!r}", file=sys.stderr)
    for track, src in unmatched:
        print(f"WARNING: source '{src}' (track {track}) not found in inventory; "
              f"generated from fields only", file=sys.stderr)
    if skipped_empty:
        print(f"Skipped {len(skipped_empty)} source(s) with no field rows (--skip-empty): "
              + ", ".join(f"{t}/{s}" for t, s in skipped_empty), file=sys.stderr)
    for track, src in inventory_only:
        print(f"NOTE: {track}/{src} is in the inventory tab but not in the {track} Fields tab",
              file=sys.stderr)
    for p in stale:
        print(f"NOTE: {p} has no matching source in the sheet (left untouched)", file=sys.stderr)

    if not args.dry_run and args.report:
        report = {
            "generated": datetime.now().isoformat(timespec="seconds"),
            "fields_dir": str(fields_dir),
            "inventory": args.data_sources,
            "warnings": warnings,
            "placeholder_rows": [{"track": t, "source": s, "name": n} for t, s, n in skipped],
            "not_in_inventory": [{"track": t, "source": s} for t, s in unmatched],
            "not_in_fields_tab": [{"track": t, "source": s} for t, s in inventory_only],
            "files_without_sheet_source": [str(p) for p in stale],
        }
        Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
        print(f"Sync report written to {args.report}", file=sys.stderr)

    print(f"Wrote {written} data source file(s) to {out_dir}"
          f"{' (dry run)' if args.dry_run else ''}", file=sys.stderr)


if __name__ == "__main__":
    main()
