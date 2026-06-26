---
layout: default
title: Data Inventory
---

# Data Inventory

{: .intro}
Unified documentation for ACCESS data sources, APIs, and MCP tools.

## Goals

The ACCESS ecosystem spans dozens of data sources across multiple teams and tracks. This project exists to bring clarity and structure to that landscape so teams can work with data more effectively.

- **Catalog every ACCESS data source** in a single, version-controlled inventory
- **Document fields, relationships, and access levels** so consumers know what's available and how to use it
- **Enable discovery across tracks** by generating browsable docs and interactive diagrams
- **Power AI tools and automation** by providing machine-readable metadata that integrates with MCP servers, agents, and other workflows

## Documentation Hubs

Front doors to the APIs and MCP servers catalogued below. Individual sources link to their own endpoint and MCP server in the table; these are the catalogs that list them all:

- **[ACCESS Support API docs](https://support.access-ci.org/api-docs)** — interactive Swagger documentation for the Support-track REST APIs (events, announcements, affinity groups, resource documentation, content, and more).
- **[ACCESS MCP servers](https://mcp.access-ci.org)** — the catalog of MCP servers that expose ACCESS data to AI tools and agents.

_Other teams' API-docs hubs can be added here as they come online._

## Data Sources

### Metrics

| Source | Description | Access | |
|--------|-------------|--------|---|
| [XDMoD Metrics](field-dictionary#xdmod) | HPC metrics, usage analytics, and resource specifications from the ACCESS XDMoD instance | Varies | [MCP](https://mcp.access-ci.org/servers/xdmod) · [API](https://xdmod.access-ci.org/controllers/user_interface.php) |

### Operations

| Source | Description | Access | |
|--------|-------------|--------|---|
| [COManage/ACCESS Identity](field-dictionary#comanage) | User identity information | Sensitive |  |
| [Resource Information (CIDeR)](field-dictionary#resource_information_cider) | Organizations, resource descriptions, and integration information for ACCESS resource providers. | Public | [API](https://operations-api.access-ci.org/wh2/cider/v1/) |

### Support

| Source | Description | Access | |
|--------|-------------|--------|---|
| [ACCESS Support Drupal](field-dictionary#access_support_drupal) | ACCESS Support website CMS - canonical storage for support content | Varies | [API](https://support.access-ci.org) |
| [Affinity Groups](field-dictionary#affinity_groups) | Community groups organized by interest or domain *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [MCP](https://mcp.access-ci.org/servers/affinity-groups) · [API](https://support.access-ci.org/api/1.1/affinity_groups) |
| [Announcements](field-dictionary#announcements) | Resource provider and community announcements *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [MCP](https://mcp.access-ci.org/servers/announcements) · [API](https://support.access-ci.org/api/2.2/announcements) |
| [Content API](field-dictionary#content_api) | Plain-text page content and a discovery index for ACCESS Support pages, for RAG ingestion and search syndication. *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [API](https://support.access-ci.org/.well-known/content-index.json) |
| [Event Registrations](field-dictionary#event_registrations) | Registration and attendance data for events | Restricted |  |
| [Events and Training](field-dictionary#events) | Workshops, webinars, training sessions, and office hours *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [MCP](https://mcp.access-ci.org/servers/events) · [API](https://support.access-ci.org/api/2.2/events) |
| [Resource Documentation API](field-dictionary#resource_documentation_api) | Team-authored documentation for ACCESS resource providers (login, file transfer, storage, queue specs, top software, datasets), with resource-group inheritance. *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal), [Resource Information (CIDeR)](field-dictionary#resource_information_cider))* | Public | [API](https://support.access-ci.org/api/1.0/resources) |
| [SDS (Software Discovery Service)](field-dictionary#sds_software_discovery_service) | Software discovery: which software packages are available on which ACCESS resource providers. *(sourced from [Resource Information (CIDeR)](field-dictionary#resource_information_cider))* | Public | [MCP](https://mcp.access-ci.org/servers/software-discovery) · [API](https://sds-ara-api.access-ci.org/api/v1) |

## Resources

- [Fields](field-dictionary) — Field-level documentation
- [Connections](heb-visualization) — Interactive relationship visualization
- [Schema](erd) — Entity-relationship diagram
- [DBML](inventory.dbml) — Raw schema for dbdiagram.io
- [JSON](inventory.json) — Machine-readable export
- [Repository](https://github.com/Sweet-and-Fizzy/access-data-inventory) — Source files and contribution guide
