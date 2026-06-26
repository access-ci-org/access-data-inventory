# ACCESS Data Inventory

Unified documentation for ACCESS data sources, APIs, and MCP tools.

## Goals

The ACCESS ecosystem spans dozens of data sources across multiple teams and tracks. This project exists to bring clarity and structure to that landscape so teams can work with data more effectively.

- **Catalog every ACCESS data source** in a single, version-controlled inventory
- **Document fields, relationships, and access levels** so consumers know what's available and how to use it
- **Enable discovery across tracks** by generating browsable docs and interactive diagrams
- **Power AI tools and automation** by providing machine-readable metadata that integrates with MCP servers, agents, and other workflows

## How It Works

The **canonical source of truth is the Google Sheet** ("ACCESS Data Source
Inventory"). Everything else is generated from it:

```
Google Sheet  →  CSV export  →  sheets_to_md.py  →  data-sources/*.md  →  generate.py  →  docs/ (Pages + dbdocs)
   (canonical)                  (converter)         (generated md)        (visualizations)
```

1. **Edit the Google Sheet** — add or update a row in the inventory tab and its
   fields in the matching `<Track> Fields` tab.
2. **Regenerate the markdown** — export the sheet tabs to CSV and run
   `python sheets_to_md.py -f <fields-dir> -d <inventory.csv> -o data-sources`.
   This rewrites `data-sources/*.md` from the sheet.
3. **Commit and push to `main`** — GitHub Actions then runs `generate.py` and
   publishes the docs.

> **Important:** `data-sources/*.md` are a **generated intermediate**. Do NOT
> hand-edit them — your changes will be overwritten the next time the sheet is
> exported. Edit the Google Sheet instead. (`md_to_sheet.py` is a helper for the
> reverse direction: dumping curated markdown back into sheet-pasteable CSVs.)

> **Coming soon:** the sheet export + regeneration is currently a manual local
> step. The plan is to automate pulling from the Google Sheet (via the Sheets
> API) so a sheet edit regenerates and publishes without the manual export.

The generated documentation is published to:
- **GitHub Pages** - browsable docs and interactive relationship diagram
- **dbdocs.io** - interactive ERD at https://dbdocs.io/access-ci/access-data-inventory

## Adding or Editing a Data Source

**Edit the Google Sheet, not the markdown.** Add a row to the inventory tab
(Track, Data Source, Description, Category, Canonical Sources, Data Access
mechanism(s), API, MCP, Access Level, etc.) and its field rows in the matching
`<Track> Fields` tab, then regenerate (step 2 above).

The reference below documents the markdown frontmatter that `sheets_to_md.py`
produces, so you can see how a sheet row maps to the generated structure. Treat
it as a schema reference, not an editing target.

### Minimal Example

```markdown
---
id: my_source
name: My Data Source
description: What this source contains
category: Community & Outreach
track: Support
responsible_team: Support
access_level: Public
is_canonical: false
canonical_source: null
api_endpoint: null
priority: Medium

mcp:
  available: false
  package: null
  tools: []

fields: []
relationships: []
---

## Overview

Description of this data source.
```

### Full Example with Fields

```markdown
---
id: my_source
name: My Data Source
description: What this source contains
category: Community & Outreach
track: Support
responsible_team: Support
access_level: Public
is_canonical: false
canonical_source: access-support-drupal
api_endpoint: https://example.com/api
dynamic: false
priority: Medium

mcp:
  available: true
  package: "@access-mcp/my-source"
  tools:
    - name: search_my_source
      method: GET
      description: Search with filters

use_cases:
  - What items are available for a given topic?
  - How many items were created this month?

constraints:
  - type: privacy
    description: Email fields contain PII and must not be exposed publicly.

fields:
  - name: id
    type: int
    access: Public
    primary_key: true
    description: Unique identifier
    semantic_type: entity_id

  - name: title
    type: varchar
    access: Public
    required: true
    mcp_name: title
    description: Display title
    semantic_type: entity_name

  - name: internal_notes
    type: text
    access: Internal Only
    description: Staff-only notes

relationships:
  - type: belongs_to
    target: other_source
    field: other_id
    description: Links to other source

  - type: has_many
    target: tags
    through: entity_tags
    description: Tagged for categorization
---

## Overview

Detailed description of this data source.

## Notes

- Additional context
- Known issues or limitations
```

### Field Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Field name |
| `type` | Yes | `int`, `varchar`, `text`, `boolean`, `date`, `timestamp`, `decimal` |
| `access` | Yes | `Public`, `Authenticated`, `Restricted`, `Internal Only`, `Sensitive` |
| `description` | Yes | What this field contains |
| `primary_key` | No | Set `true` for primary key |
| `required` | No | Set `true` if field is required |
| `mcp_name` | No | Field name in MCP if different |
| `computed` | No | Set `true` if calculated/derived |
| `references` | No | Foreign key reference (e.g., `users.user_id`) |
| `allowed_values` | No | List of valid values |
| `semantic_type` | No | Controlled vocabulary tag for cross-source field matching (see [Semantic Types](#semantic-types)) |

### Allowed Values

**category:** Community & Outreach, Events & Training, Users & Identity, Content Management, Allocations, Resources, Operations, Metrics & Reporting

**track:** Support, Operations, Allocations, ACO

**access_level:** Public, Authenticated, Public and Authenticated, Restricted, Internal Only, Sensitive, Varies, TBD

**priority:** High, Medium, Low

### Use Cases

The `use_cases` property is an optional list of plain-language questions that a data source can help answer. These appear in the field dictionary and help stakeholders understand the practical value of each data source.

```yaml
use_cases:
  - What training sessions are available for beginners this month?
  - Which events are associated with a specific affinity group?
```

### Constraints

The `constraints` property documents policy, privacy, or regulatory restrictions on a data source. Each constraint has a `type` (from the controlled vocabulary below) and a free-text `description`.

```yaml
constraints:
  - type: privacy
    description: Contains PII that must not be exposed through public APIs.
  - type: acceptable_use
    description: Data may only be used for event management and reporting.
```

**constraint_type:** privacy, acceptable_use, licensing, retention, regulatory

### Semantic Types

The `semantic_type` property is an optional tag on individual fields that links equivalent fields across different data sources. For example, `title` in events, `title` in announcements, and `title` in Drupal nodes all serve the same purpose — `entity_name` captures that relationship.

```yaml
fields:
  - name: title
    type: varchar
    access: Public
    description: Event title
    semantic_type: entity_name
```

Fields that are foreign key references (with a `references` property) should generally NOT have a `semantic_type` — the relationship is already captured by the reference.

**semantic_type vocabulary:**

| Type | Covers fields like | Purpose |
|------|-------------------|---------|
| `entity_id` | id, nid, user_id | Primary/business identifier |
| `uuid` | uuid | Universal unique identifier |
| `entity_name` | title, name (of a thing) | Human-readable name/title |
| `entity_description` | description, body | Full descriptive content |
| `entity_summary` | summary, goals | Short-form summary |
| `entity_type` | event_type, type, category | Classification |
| `entity_status` | status, attendance_status | Lifecycle state |
| `date_start` / `date_end` | start_date, end_date | Time bounds |
| `date_published` | published_date | Publication timestamp |
| `date_created` / `date_modified` | created, changed | Record timestamps |
| `duration` / `time_relative` | duration_hours, starts_in_hours | Time measurements |
| `person_name` / `person_email` | name (of a person), email | PII fields |
| `institution` | institution | Org affiliation |
| `location` | location | Physical location |
| `url_registration` / `url_meeting` / `url_external` | registration_url, virtual_meeting_link | URL types |
| `contact_info` | contact, mailing_list | Contact details |
| `skill_level` | skill_level | Target audience level |
| `affiliation` | affiliation | ACCESS vs community |
| `media_ref` | image_id | Media references |
| `tags` | tags | Taxonomy tags |

This vocabulary is provisional and will evolve as more data sources are added. Adding, renaming, or removing types only requires editing the list in `schema.yaml`.

## Local Development

```bash
# First time setup
npm install
cd docs && bundle install && cd ..

# Generate + preview (recommended)
npm run preview
# Then open http://localhost:8080

# Or, step by step:
python generate.py              # Generate docs
npm run serve                   # Start Jekyll dev server

# Validate without generating
python generate.py --validate
```

## Project Structure

```
data-inventory/
├── data-sources/           # GENERATED from the sheet via sheets_to_md.py - do not hand-edit
│   ├── announcements.md
│   ├── events.md
│   └── ...
├── docs/                   # Auto-generated (do not edit)
│   ├── index.md
│   ├── summary.md
│   ├── field-dictionary.md
│   ├── inventory.dbml
│   ├── inventory.json
│   └── heb-visualization.html
├── templates/              # HTML templates
│   └── heb-visualization.html
├── generate.py             # Generator script
├── schema.yaml             # Validation rules
└── package.json            # Node dependencies (dbdocs)
```

## Generated Outputs

| File | Description | Where to View |
|------|-------------|---------------|
| `index.md` | Landing page | GitHub Pages |
| `summary.md` | Stakeholder overview by track | GitHub Pages |
| `field-dictionary.md` | Detailed field documentation | GitHub Pages |
| `heb-visualization.html` | Interactive relationship diagram | GitHub Pages |
| `inventory.dbml` | Database schema | dbdocs.io |
| `inventory.json` | Machine-readable data | API/tools |

## Initial Setup (One-Time, Already Done)

These steps have already been completed for this repository. They're documented here for reference if setting up a new instance.

### GitHub Pages

1. Go to repo Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, folder: `/docs`

### dbdocs.io (CI Deployment)

1. Create account at https://dbdocs.io
2. Get API token from dbdocs dashboard
3. Add `DBDOCS_TOKEN` secret to GitHub repo (Settings → Secrets → Actions)

### dbdocs.io (Local Deployment - Optional)

Only needed if you want to manually deploy from your machine:

```bash
npm run dbdocs:login  # One-time authentication
npm run dbdocs:build  # Deploy
```
