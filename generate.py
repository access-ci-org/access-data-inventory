#!/usr/bin/env python3
"""
Generate various output formats from markdown+frontmatter data source files.

Outputs (in docs/ for GitHub Pages):
- docs/index.md - Landing page
- docs/summary.md - High-level stakeholder summary
- docs/field-dictionary.md - Detailed field reference
- docs/inventory.dbml - For dbdiagram.io
- docs/inventory.json - Machine-readable data

Note: docs/heb-visualization.md uses Jekyll layout (docs/_layouts/heb.html)

Usage:
    python generate.py
    python generate.py --validate  # Just validate, don't generate
"""

import re
import sys
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime

# Directory setup
SCRIPT_DIR = Path(__file__).parent
DATA_SOURCES_DIR = SCRIPT_DIR / "data-sources"
DOCS_DIR = SCRIPT_DIR / "docs"
SCHEMA_FILE = SCRIPT_DIR / "schema.yaml"


def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Parse a markdown file with YAML frontmatter."""
    content = filepath.read_text()

    if not content.startswith('---'):
        raise ValueError(f"{filepath}: Missing YAML frontmatter")

    end_index = content.index('---', 3)
    frontmatter_str = content[3:end_index].strip()
    body = content[end_index + 3:].strip()

    frontmatter = yaml.safe_load(frontmatter_str)
    return frontmatter, body


def load_schema() -> dict:
    """Load the schema file."""
    if SCHEMA_FILE.exists():
        return yaml.safe_load(SCHEMA_FILE.read_text())
    return {}


def cell(value) -> str:
    """Make a value safe inside a one-line markdown table cell: sheet cells can
    contain line breaks (which end the row) and pipes (which add a column)."""
    text = "" if value is None else str(value)
    text = " ".join(line.strip() for line in text.splitlines() if line.strip())
    return text.replace("|", "\\|")


def canonical_source_ids(source: dict) -> list[str]:
    """Return a source's canonical_source list of source ids ([] if canonical).

    canonical_source is always a list of slugified source ids — emitted by the
    converter from the inventory's 'Canonical Sources' column, and authored the
    same way in the data-source files.
    """
    return list(source.get('canonical_source') or [])


SYNC_REPORT_FILE = SCRIPT_DIR / "sync-report.json"


def structural_errors(source: dict) -> list[str]:
    """Problems that make a source impossible to publish (unlike vocabulary or
    blank-cell findings, which are reported on the data quality page)."""
    errors = []
    label = source.get('id') or source.get('_filepath', 'unknown')
    if not source.get('id'):
        errors.append(f"{label}: missing id")
    if not source.get('name'):
        errors.append(f"{label}: missing name")
    return errors


def validate_source(source: dict, schema: dict) -> list[str]:
    """Validate a data source against the schema. Returns list of errors."""
    errors = []
    source_id = source.get('id', 'unknown')

    for field in schema.get('required_fields', []):
        if field not in source:
            errors.append(f"{source_id}: Missing required field '{field}'")

    allowed = schema.get('allowed_values', {})

    if 'category' in source and source['category'] not in allowed.get('category', []):
        errors.append(f"{source_id}: Invalid category '{source['category']}'")

    if 'track' in source and source['track'] not in allowed.get('track', []):
        errors.append(f"{source_id}: Invalid track '{source['track']}'")

    if 'access_level' in source and source['access_level'] not in allowed.get('access_level', []):
        errors.append(f"{source_id}: Invalid access_level '{source['access_level']}'")

    if 'priority' in source and source['priority'] not in allowed.get('priority', []):
        errors.append(f"{source_id}: Invalid priority '{source['priority']}'")

    for constraint in source.get('constraints', []):
        ctype = constraint.get('type', '')
        if ctype not in allowed.get('constraint_type', []):
            errors.append(f"{source_id}: Invalid constraint type '{ctype}'")

    for field in source.get('fields', []):
        field_name = field.get('name', 'unknown')

        if 'access' in field:
            # access may be a single level or a list of levels (a field whose
            # access varies, e.g. public in aggregate, authenticated in detail).
            access_values = field['access'] if isinstance(field['access'], list) else [field['access']]
            for av in access_values:
                if av not in allowed.get('field_access', []):
                    errors.append(f"{source_id}.{field_name}: Invalid access '{av}'")

        # Type vocabulary is matched case-insensitively: the sheet says JSON,
        # the schema says json, and neither is wrong.
        if 'type' in field and str(field['type']).lower() not in allowed.get('field_type', []):
            errors.append(f"{source_id}.{field_name}: Invalid type '{field['type']}'")

        if 'semantic_type' in field and field['semantic_type'] not in allowed.get('semantic_type', []):
            errors.append(f"{source_id}.{field_name}: Invalid semantic_type '{field['semantic_type']}'")

    return errors


def load_all_sources() -> list[dict]:
    """Load all data source files."""
    sources = []

    for filepath in sorted(DATA_SOURCES_DIR.glob("*.md")):
        try:
            frontmatter, body = parse_frontmatter(filepath)
            frontmatter['_body'] = body
            frontmatter['_filepath'] = str(filepath)
            sources.append(frontmatter)
        except Exception as e:
            print(f"Error loading {filepath}: {e}", file=sys.stderr)

    return sources




def generate_index(sources: list[dict]) -> str:
    """Generate the landing page following ACCESS brand guidelines."""
    mcp_count = sum(1 for s in sources if s.get('mcp', {}).get('available'))

    # Group sources by track
    by_track = {}
    for source in sources:
        track = source.get('track', 'Unknown')
        by_track.setdefault(track, []).append(source)

    lines = [
        "---",
        "layout: default",
        "title: Data Inventory",
        "---",
        "",
        "# Data Inventory",
        "",
        "{: .intro}",
        "Unified documentation for ACCESS data sources, APIs, and MCP tools.",
        "",
        "## Goals",
        "",
        "The ACCESS ecosystem spans dozens of data sources across multiple teams and tracks. This project exists to bring clarity and structure to that landscape so teams can work with data more effectively.",
        "",
        "- **Catalog every ACCESS data source** in a single, version-controlled inventory",
        "- **Document fields, relationships, and access levels** so consumers know what's available and how to use it",
        "- **Enable discovery across tracks** by generating browsable docs and interactive diagrams",
        "- **Power AI tools and automation** by providing machine-readable metadata that integrates with MCP servers, agents, and other workflows",
        "",
        "## Documentation Hubs",
        "",
        "Front doors to the APIs and MCP servers catalogued below. Individual sources link to their own endpoint and MCP server in the table; these are the catalogs that list them all:",
        "",
        "- **[ACCESS Support API docs](https://support.access-ci.org/api-docs)** — interactive Swagger documentation for the Support-track REST APIs (events, announcements, affinity groups, resource documentation, content, and more).",
        "- **[ACCESS MCP servers](https://mcp.access-ci.org/docs/)** — the catalog of MCP servers that expose ACCESS data to AI tools and agents.",
        "",
        "_Other teams' API-docs hubs can be added here as they come online._",
        "",
    ]

    # Data Sources by Track
    lines.append("## Data Sources")
    lines.append("")

    for track in sorted(by_track.keys()):
        track_sources = by_track[track]
        lines.append(f"### {track}")
        lines.append("")
        lines.append("| Source | Description | Access | |")
        lines.append("|--------|-------------|--------|---|")

        for source in sorted(track_sources, key=lambda x: x.get('name', '')):
            name = source.get('name', '')
            source_id = source.get('id', '')
            desc = cell(source.get('description', ''))
            access = cell(source.get('access_level', ''))
            mcp = source.get('mcp', {})

            # Links column
            links = []
            if mcp.get('available'):
                package = mcp.get('package', '')
                if mcp.get('url'):
                    links.append(f"[MCP]({mcp['url']})")
                elif package:
                    package_name = package.replace('@access-mcp/', '')
                    links.append(f"[MCP](https://mcp.access-ci.org/docs/servers/{package_name})")
            if source.get('api_endpoint'):
                links.append(f"[API]({source.get('api_endpoint')})")
            if source.get('docs_url'):
                links.append(f"[Docs]({source.get('docs_url')})")
            links_str = " · ".join(links)

            # Add canonical source indicator
            canonical_note = ""
            canon_ids = canonical_source_ids(source)
            if not source.get('is_canonical') and canon_ids:
                links = []
                for canon_id in canon_ids:
                    canon = next((s for s in sources if s.get('id') == canon_id), None)
                    if canon:
                        links.append(f"[{canon.get('name', canon_id)}](field-dictionary#{canon_id})")
                    else:
                        links.append(canon_id.replace('_', ' '))  # not an inventory row; see data-quality
                canonical_note = f" *(sourced from {', '.join(links)})*"

            lines.append(f"| [{name}](field-dictionary#{source_id}) | {desc}{canonical_note} | {access} | {links_str} |")

        lines.append("")

    # Resources section
    lines.append("## Resources")
    lines.append("")
    lines.append("- [Fields](field-dictionary) — Field-level documentation")
    lines.append("- [Data quality](data-quality) — Sheet cells that need attention, by track")
    lines.append("- [Connections](heb-visualization) — Interactive relationship visualization")
    lines.append("- [Schema](erd) — Entity-relationship diagram")
    lines.append("- [DBML](inventory.dbml) — Raw schema for dbdiagram.io")
    lines.append("- [JSON](inventory.json) — Machine-readable export")
    lines.append("- [Repository](https://github.com/Sweet-and-Fizzy/access-data-inventory) — Source files and contribution guide")
    lines.append("")

    return "\n".join(lines)


def generate_field_dictionary(sources: list[dict]) -> str:
    """Generate a detailed field dictionary."""
    lines = [
        "---",
        "layout: default",
        "title: Fields",
        "---",
        "",
        "# Fields",
        "",
        "Field-level documentation for all ACCESS data sources.",
        "",
        "## Table of Contents",
        "",
    ]

    for source in sorted(sources, key=lambda x: x.get('name', '')):
        source_id = source.get('id', '')
        source_name = source.get('name', 'Unknown')
        lines.append(f"- [{source_name}](#{source_id})")

    lines.append("")

    for source in sorted(sources, key=lambda x: x.get('name', '')):
        source_id = source.get('id', '')
        lines.append(f"<h2 id=\"{source_id}\">{source.get('name', 'Unknown')}</h2>")
        lines.append("")
        lines.append(f"*{source.get('description', '')}*")
        lines.append("")

        # Add canonical source cross-link for non-authoritative sources
        canon_ids = canonical_source_ids(source)
        if not source.get('is_canonical') and canon_ids:
            links = []
            for canon_id in canon_ids:
                canon = next((s for s in sources if s.get('id') == canon_id), None)
                if canon:
                    links.append(f"[{canon.get('name', canon_id)}](#{canon_id})")
                else:
                    links.append(canon_id.replace('_', ' '))  # not an inventory row; see data-quality
            lines.append(f"> **Canonical source:** {', '.join(links)} — this data is derived from the authoritative source(s) above.")
            lines.append("")
        elif source.get('is_canonical') and source.get('provides_data_for'):
            derived = source['provides_data_for']
            derived_links = []
            for d in derived:
                d_name = next((s.get('name', d) for s in sources if s.get('id') == d), d)
                derived_links.append(f"[{d_name}](#{d})")
            lines.append(f"> **Authoritative source** for: {', '.join(derived_links)}")
            lines.append("")

        # Source-level provenance / operational metadata
        for key, label in (
            ('storage_location', 'Storage'),
            ('data_access_mechanism', 'Access mechanism'),
            ('refresh_frequency', 'Refresh frequency'),
            ('query_capacity', 'Query capacity'),
            ('sensitivity', 'Sensitivity'),
            ('how_to_request_access', 'How to request access'),
        ):
            if source.get(key):
                lines.append(f"**{label}:** {cell(source[key])}")
                lines.append("")
        if source.get('docs_url'):
            lines.append(f"**Docs:** <{source['docs_url']}>")
            lines.append("")

        # Render use_cases
        use_cases = source.get('use_cases', [])
        if use_cases:
            lines.append("**Example questions this data can answer:**")
            lines.append("")
            for uc in use_cases:
                lines.append(f"- {uc}")
            lines.append("")

        # Render constraints
        constraints = source.get('constraints', [])
        if constraints:
            lines.append("**Constraints:**")
            lines.append("")
            for c in constraints:
                ctype = c.get('type', '').replace('_', ' ').title()
                lines.append(f"- **{ctype}:** {c.get('description', '')}")
            lines.append("")

        realms = source.get('realms', [])
        if realms:
            lines.append("### Realms")
            lines.append("")
            lines.append(f"XDMoD organizes data into **{len(realms)} realms**, each with its own dimensions and statistics.")
            lines.append("")
            for realm in realms:
                realm_name = realm.get('name', '')
                lines.append(f"#### {realm_name}")
                lines.append("")
                lines.append(f"*{realm.get('description', '')}*")
                lines.append("")
                # Access level
                access = realm.get('access_level', '')
                if access:
                    lines.append(f"**Access:** {access}")
                    lines.append("")
                # Dimensions
                dims = realm.get('dimensions', [])
                if dims:
                    dim_str = ", ".join(f"`{d}`" for d in dims if d != "none")
                    if dim_str:
                        lines.append(f"**Dimensions:** {dim_str}")
                        lines.append("")
                # Statistics table
                stats = realm.get('statistics', [])
                if stats:
                    lines.append("| Statistic | Description |")
                    lines.append("|-----------|-------------|")
                    for stat in stats:
                        lines.append(f"| `{stat.get('name', '')}` | {stat.get('description', '')} |")
                    lines.append("")

        fields = source.get('fields', [])
        if not fields and not realms:
            lines.append("*No fields documented.*")
            lines.append("")
            continue

        if not fields:
            continue

        lines.append("| Field | Type | Access | MCP Name | Description |")
        lines.append("|-------|------|--------|----------|-------------|")

        for field in fields:
            pk = " (PK)" if field.get('primary_key') else ""
            req = " *" if field.get('required') else ""
            computed = " (computed)" if field.get('computed') else ""
            mcp_name = field.get('mcp_name', '')
            sem = f" [{field['semantic_type']}]" if field.get('semantic_type') else ""
            auth = f" (source: {field['authoritative_source']})" if field.get('authoritative_source') else ""
            access = field.get('access', '')
            access_str = ", ".join(access) if isinstance(access, list) else access
            if field.get('access_notes'):
                access_str = f"{access_str} ({cell(field['access_notes'])})"
            notes = f" — {cell(field['notes'])}" if field.get('notes') else ""

            lines.append(
                f"| `{cell(field.get('name', ''))}`{pk}{req} | "
                f"{cell(field.get('type', ''))} | "
                f"{cell(access_str)} | "
                f"{cell(mcp_name)} | "
                f"{cell(field.get('description', ''))}{computed}{sem}{auth}{notes} |"
            )

        lines.append("")
        lines.append("*PK = Primary Key, * = Required, [type] = Semantic Type*")
        lines.append("")

        relationships = source.get('relationships', [])
        if relationships:
            lines.append("### Relationships")
            lines.append("")
            for rel in relationships:
                rel_type = rel.get('type', '').replace('_', ' ').title()
                target = rel.get('target', '')
                desc = rel.get('description', '')
                lines.append(f"- **{rel_type}** `{target}`: {desc}")
            lines.append("")

    return "\n".join(lines)


DBML_IDENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def dbml_ident(value, default: str = 'varchar') -> str:
    """A DBML column name or type. Sheet field names can be anything
    ("Endpoint Name", "storage.<multiple_attributes>"); DBML wants a bare
    identifier or a double-quoted one."""
    text = str(value).strip() if value not in (None, '') else default
    if DBML_IDENT.match(text):
        return text
    return '"' + text.replace('"', '\\"') + '"'


def dbml_note(text) -> str:
    """Single-quoted DBML string content: one line, apostrophes escaped."""
    flat = " ".join(str(text).split())
    return flat.replace("'", "\\'")


def generate_dbml(sources: list[dict]) -> str:
    """Generate DBML for dbdiagram.io."""
    lines = [
        "// ACCESS Data Inventory",
        f"// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "// Source: data-sources/*.md",
        "",
        "// =============================================================================",
        "// DATA SOURCES",
        "// =============================================================================",
        "",
        "Enum data_source {",
    ]

    for source in sources:
        note_lines = [
            f"name: {source.get('name', '')}",
            f"description: {source.get('description', '')}",
            f"category: {source.get('category', '')}",
            f"track: {source.get('track', '')}",
            f"access_level: {source.get('access_level', '')}",
            f"is_canonical: {str(source.get('is_canonical', False)).lower()}",
            f"canonical_source: {', '.join(canonical_source_ids(source)) or 'null'}",
            f"mcp_available: {str(source.get('mcp', {}).get('available', False)).lower()}",
            f"mcp_package: {source.get('mcp', {}).get('package') or 'null'}",
            f"api_endpoint: {source.get('api_endpoint') or 'null'}",
            f"storage_location: {source.get('storage_location') or 'null'}",
            f"priority: {source.get('priority', '')}",
        ]

        # Optional operational metadata — only emitted when present.
        for key in ('data_access_mechanism', 'refresh_frequency', 'query_capacity',
                    'docs_url', 'sensitivity', 'how_to_request_access'):
            if source.get(key):
                note_lines.append(f"{key}: {source[key]}")

        realms = source.get('realms', [])
        if realms:
            realm_summaries = []
            for r in realms:
                stats_count = len(r.get('statistics', []))
                dims_count = len([d for d in r.get('dimensions', []) if d != 'none'])
                realm_summaries.append(f"{r['name']} ({stats_count} stats, {dims_count} dims)")
            note_lines.append(f"realms: {', '.join(realm_summaries)}")

        lines.append(f"  {source.get('id', '')} [note: '''")
        for note_line in note_lines:
            lines.append(f"    {note_line}")
        lines.append("  ''']")
        lines.append("")

    lines.append("}")
    lines.append("")

    lines.append("// =============================================================================")
    lines.append("// ENTITIES")
    lines.append("// =============================================================================")
    lines.append("")

    for source in sources:
        fields = source.get('fields', [])
        if not fields:
            continue

        table_name = source.get('id', 'unknown')
        lines.append(f"Table {table_name} {{")

        seen_names = {}
        for field in fields:
            # A field name repeated in the sheet would be a DBML syntax error;
            # keep both (the data-quality page reports the duplicate).
            name = str(field.get('name', '') or 'unnamed')
            seen_names[name] = seen_names.get(name, 0) + 1
            if seen_names[name] > 1:
                name = f"{name}_{seen_names[name]}"
            field_line = f"  {dbml_ident(name, 'unnamed')} {dbml_ident(field.get('type'))}"

            attrs = []
            if field.get('primary_key'):
                attrs.append('pk')
            if field.get('required'):
                attrs.append('not null')

            field_access = field.get('access', 'Public')
            if isinstance(field_access, list):
                field_access = ", ".join(field_access)
            note_parts = [f"access: {field_access}"]
            if field.get('mcp_name'):
                note_parts.append(f"mcp: {field.get('mcp_name')}")
            if field.get('computed'):
                note_parts.append("computed: true")
            if field.get('semantic_type'):
                note_parts.append(f"semantic: {field.get('semantic_type')}")
            if field.get('description'):
                note_parts.append(field.get('description'))

            attrs.append(f"note: '{dbml_note(' | '.join(str(x) for x in note_parts))}'")

            if attrs:
                field_line += f" [{', '.join(attrs)}]"

            lines.append(field_line)

        lines.append("")
        lines.append(f"  Note: '''")
        lines.append(f"    source: {source.get('id', '')}")
        lines.append(f"    description: {source.get('description', '')}")
        lines.append(f"    access_level: {source.get('access_level', '')}")

        use_cases = source.get('use_cases', [])
        if use_cases:
            lines.append(f"    use_cases:")
            for uc in use_cases:
                # Escape apostrophes for DBML
                uc_escaped = uc.replace("'", "\\'")
                lines.append(f"      - {uc_escaped}")

        constraints = source.get('constraints', [])
        if constraints:
            lines.append(f"    constraints:")
            for c in constraints:
                desc_escaped = c.get('description', '').replace("'", "\\'")
                lines.append(f"      - {c.get('type', '')}: {desc_escaped}")

        lines.append(f"  '''")
        lines.append("}")
        lines.append("")

    # Generate tables for realm-based sources (e.g., XDMoD)
    for source in sources:
        realms = source.get('realms', [])
        if not realms:
            continue
        source_id = source.get('id', 'unknown')
        for realm in realms:
            realm_id = realm.get('name', '').lower().replace(' ', '_')
            table_name = f"{source_id}_{realm_id}"
            lines.append(f"Table {table_name} {{")

            # Dimensions
            for dim in realm.get('dimensions', []):
                if dim == 'none':
                    continue
                lines.append(f"  {dim} dimension [note: 'filter dimension']")

            # Statistics
            for stat in realm.get('statistics', []):
                desc = stat.get('description', '').replace("'", "\\'")
                lines.append(f"  {stat.get('name', '')} metric [note: '{desc}']")

            lines.append("")
            lines.append(f"  Note: '''")
            lines.append(f"    source: {source_id}")
            lines.append(f"    realm: {realm.get('name', '')}")
            lines.append(f"    description: {realm.get('description', '')}")
            lines.append(f"    access_level: {realm.get('access_level', '')}")
            lines.append(f"    type: XDMoD realm (dimensions are query filters, statistics are computed metrics)")
            lines.append(f"  '''")
            lines.append("}")
            lines.append("")

    lines.append("// =============================================================================")
    lines.append("// RELATIONSHIPS")
    lines.append("// =============================================================================")
    lines.append("")

    # Build a map of table -> primary key field (only for tables we have)
    pk_map = {}
    table_ids = set()
    for source in sources:
        table_id = source.get('id', '')
        table_ids.add(table_id)
        for field in source.get('fields', []):
            if field.get('primary_key'):
                pk_map[table_id] = field.get('name')
                break

    # Register realm table IDs
    for source in sources:
        for realm in source.get('realms', []):
            realm_id = realm.get('name', '').lower().replace(' ', '_')
            table_ids.add(f"{source.get('id', 'unknown')}_{realm_id}")

    for source in sources:
        for rel in source.get('relationships', []):
            if rel.get('type') == 'belongs_to' and rel.get('field'):
                source_table = source.get('id', '')
                target_table = rel.get('target', '')
                field = rel.get('field', '')

                # Only create ref if target table exists in our sources
                if target_table not in table_ids:
                    continue

                # Look up the target's primary key, default to 'id'
                target_pk = pk_map.get(target_table, 'id')
                lines.append(f"Ref: {source_table}.{dbml_ident(field)} > {target_table}.{dbml_ident(target_pk)}")

    lines.append("")

    return "\n".join(lines)


def collect_quality_findings(sources: list[dict], schema: dict) -> list[dict]:
    """Everything worth fixing in the sheet, as {track, source, name, message}.

    Nothing here blocks generation; the docs publish with the data as it is
    and this list becomes docs/data-quality.md.
    """
    findings = []
    ids = {s.get('id') for s in sources}

    def add(source, message):
        findings.append({
            'track': source.get('track') or 'Unknown',
            'source': source.get('id', ''),
            'name': source.get('name', source.get('id', '')),
            'message': message,
        })

    for source in sources:
        prefix = f"{source.get('id', 'unknown')}"
        for err in validate_source(source, schema):
            # validate_source prefixes "<id>: " or "<id>.<field>: "; keep the rest.
            msg = err[len(prefix) + 1:].strip() if err.startswith(prefix) else err
            if err.startswith(prefix + "."):
                field = err[len(prefix) + 1:].split(":", 1)[0]
                msg = f"field `{field}`: {err.split(':', 1)[1].strip()}"
            msg = (msg.replace("Missing required field", "blank cell:")
                      .replace("Invalid category", "category not in the vocabulary:")
                      .replace("Invalid track", "track not in the vocabulary:")
                      .replace("Invalid access_level", "access level not in the vocabulary:")
                      .replace("Invalid priority", "priority not in the vocabulary:")
                      .replace("Invalid type", "type not in the vocabulary:")
                      .replace("Invalid access", "access not in the vocabulary:")
                      .replace("Invalid semantic_type", "semantic type not in the vocabulary:"))
            add(source, msg)
        for canon_id in canonical_source_ids(source):
            if canon_id not in ids:
                add(source, f"Canonical Sources names '{canon_id.replace('_', ' ')}', "
                            f"which is not an inventory row")
        names = [str(f.get('name', '')) for f in source.get('fields') or []]
        for dup in sorted({n for n in names if names.count(n) > 1}):
            add(source, f"field `{dup}` appears {names.count(dup)} times")
        if not source.get('fields') and not source.get('realms'):
            add(source, "no fields documented yet")
    return findings


def generate_data_quality(sources: list[dict], findings: list[dict], sync_report: dict | None) -> str:
    """The cleanup agenda: findings grouped by track and source, plus what the
    last sheet sync noticed (broken formula headings, rows in one tab but not
    the other, curated content the sheet does not hold yet)."""
    lines = [
        "---",
        "layout: default",
        "title: Data quality",
        "---",
        "",
        "# Data quality",
        "",
        "The inventory is generated from the Google Sheet as-is. Nothing on this page "
        "stops the docs from publishing; it is the list of sheet cells that would make "
        "them better. Each item names the track (the `<Track> Fields` tab, or the "
        "inventory tab for source-level items) and the source row.",
        "",
    ]

    EMPTY = 'no fields documented yet'
    real = [f for f in findings if f['message'] != EMPTY]
    by_track: dict[str, dict[str, list[dict]]] = {}
    for f in findings:
        by_track.setdefault(f['track'], {}).setdefault(f['source'], []).append(f)

    lines.append("## Summary")
    lines.append("")
    lines.append("| Track | Sources | Items to fix | Sources with no fields yet |")
    lines.append("|-------|---------|--------------|----------------------------|")
    for track in sorted(by_track):
        n_sources = sum(1 for s in sources if (s.get('track') or 'Unknown') == track)
        n_real = sum(1 for f in real if f['track'] == track)
        n_empty = sum(1 for s in sources if (s.get('track') or 'Unknown') == track
                      and not s.get('fields') and not s.get('realms'))
        lines.append(f"| {track} | {n_sources} | {n_real} | {n_empty} |")
    lines.append("")

    for track in sorted(by_track):
        lines.append(f"## {track}")
        lines.append("")
        for source_id, items in sorted(by_track[track].items(), key=lambda kv: kv[1][0]['name'].lower()):
            msgs = [i['message'] for i in items if i['message'] != EMPTY]
            if not msgs:
                continue  # only "no fields yet"; listed together below
            lines.append(f"**[{items[0]['name']}](field-dictionary#{source_id})**")
            lines.append("")
            for m in msgs:
                lines.append(f"- {m}")
            lines.append("")
        empties = sorted(i[0]['name'] for i in by_track[track].values()
                         if any(x['message'] == EMPTY for x in i))
        if empties:
            lines.append(f"*No fields documented yet ({len(empties)}):* " + ", ".join(empties))
            lines.append("")

    if sync_report:
        lines.append("## Noticed during the last sheet sync")
        lines.append("")
        lines.append(f"_Sync run {sync_report.get('generated', '')}._")
        lines.append("")
        sections = (
            ("warnings", "Converter warnings", lambda w: w),
            ("not_in_fields_tab", "In the inventory tab but missing from the Fields tab",
             lambda r: f"{r['track']}: {r['source']}"),
            ("not_in_inventory", "In a Fields tab but missing from the inventory tab",
             lambda r: f"{r['track']}: {r['source']}"),
            ("placeholder_rows", "TODO placeholder field rows",
             lambda r: f"{r['track']}: {r['source']} — {r['name']}"),
            ("files_without_sheet_source", "Repository files with no sheet row (kept as-is)",
             lambda f: f"`{f}`"),
        )
        for key, title, fmt in sections:
            items = sync_report.get(key) or []
            if not items:
                continue
            lines.append(f"**{title}**")
            lines.append("")
            for item in items:
                lines.append(f"- {fmt(item)}")
            lines.append("")

    return "\n".join(lines)


def generate_json(sources: list[dict]) -> str:
    """Generate JSON for visualization and tools."""
    clean_sources = []
    for source in sources:
        clean = {k: v for k, v in source.items() if not k.startswith('_')}
        clean_sources.append(clean)

    output = {
        "generated": datetime.now().isoformat(),
        "source_count": len(sources),
        "sources": clean_sources,
        "by_track": {},
        "by_category": {},
        "by_access_level": {},
    }

    for source in clean_sources:
        track = source.get('track', 'Unknown')
        output["by_track"].setdefault(track, []).append(source.get('id'))

        category = source.get('category', 'Unknown')
        output["by_category"].setdefault(category, []).append(source.get('id'))

        access = source.get('access_level', 'Unknown')
        output["by_access_level"].setdefault(access, []).append(source.get('id'))

    return json.dumps(output, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate outputs from data source files")
    parser.add_argument('--validate', action='store_true',
                        help="Only check; exit 1 on structural problems, print data-quality items")
    args = parser.parse_args()

    schema = load_schema()
    sources = load_all_sources()

    if not sources:
        print("No data source files found in data-sources/", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(sources)} data source(s)")

    fatal = [e for source in sources for e in structural_errors(source)]
    if fatal:
        print("\nCannot generate:", file=sys.stderr)
        for error in fatal:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    findings = collect_quality_findings(sources, schema)
    to_fix = [f for f in findings if f['message'] != 'no fields documented yet']
    if to_fix:
        print(f"\nData quality: {len(to_fix)} item(s) to fix in the sheet "
              f"(see docs/data-quality.md):", file=sys.stderr)
        for f in to_fix:
            print(f"  - {f['track']}/{f['name']}: {f['message']}", file=sys.stderr)
    else:
        print("Data quality: nothing to fix")

    if args.validate:
        return

    sync_report = None
    if SYNC_REPORT_FILE.exists():
        sync_report = json.loads(SYNC_REPORT_FILE.read_text())

    DOCS_DIR.mkdir(exist_ok=True)

    outputs = [
        ("index.md", generate_index(sources)),
        ("field-dictionary.md", generate_field_dictionary(sources)),
        ("data-quality.md", generate_data_quality(sources, findings, sync_report)),
        ("inventory.dbml", generate_dbml(sources)),
        ("inventory.json", generate_json(sources)),
    ]

    for filename, content in outputs:
        filepath = DOCS_DIR / filename
        filepath.write_text(content)
        print(f"Generated: {filepath}")

    print("\nDone! Output is in docs/ - ready for GitHub Pages")


if __name__ == "__main__":
    main()
