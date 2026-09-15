---
id: access_support_drupal
name: ACCESS Support Drupal
description: ACCESS Support website CMS - canonical storage for support content
category: Content Management
track: Support
access_level: Varies
is_canonical: true
api_endpoint: https://support.access-ci.org
dynamic: true
priority: High
mcp:
  available: false
provides_data_for:
- announcements
- events
- affinity_groups
- tags
use_cases:
- What content types are stored in the ACCESS Support CMS?
- When was a specific piece of content last modified?
- How many published nodes exist by content type?
fields:
- name: nid
  type: int
  access: Public
  description: Drupal node ID
  semantic_type: entity_id
  primary_key: true
- name: uuid
  type: varchar
  access: Public
  description: Drupal UUID
  semantic_type: uuid
- name: type
  type: varchar
  access: Public
  description: Drupal content type
  semantic_type: entity_type
- name: title
  type: varchar
  access: Public
  description: Content title
  semantic_type: entity_name
- name: body
  type: text
  access: Public
  description: Content body (HTML)
  semantic_type: entity_description
- name: status
  type: boolean
  access: Internal Only
  description: Published status
  semantic_type: entity_status
- name: created
  type: timestamp
  access: Public
  description: Content creation date
  semantic_type: date_created
- name: changed
  type: timestamp
  access: Public
  description: Last modification date
  semantic_type: date_modified
- name: uid
  type: int
  access: Restricted
  description: Author user ID
  references: users.user_id
relationships:
- type: has_many
  target: announcements
  description: Stores announcement content
- type: has_many
  target: events
  description: Stores event content (series and instances)
- type: has_many
  target: affinity_groups
  description: Stores affinity group content
- type: has_many
  target: tags
  description: Stores taxonomy terms
- type: has_many
  target: users
  description: Stores user accounts (Drupal users, linked to COManage)
storage_location: Drupal CMS database
data_access_mechanism: Web
docs_url: https://support.access-ci.org/api-docs
refresh_frequency: realtime
query_capacity: moderate
sensitivity: High
---

## Overview

ACCESS Support Drupal is the content management system that serves as the canonical storage backend for most Support track content. It powers the ACCESS Support website and provides APIs that feed the various MCP servers.

## Notes

- This is the **canonical source** for announcements, events, and affinity groups
- Content is created and edited directly in Drupal by authorized users
- Specialized REST APIs expose content for consumption by MCP servers
- Not directly exposed as an MCP itself - data flows through content-specific MCPs
- Dynamic content - users can create/edit at any time

## Data Flow

```
ACCESS Support Drupal (canonical)
    │
    ├── /api/2.0/announcements → announcements MCP
    ├── /api/2.0/events → events MCP
    ├── /api/1.0/affinity_groups → affinity-groups MCP
    └── (direct) → tags, taxonomy
```

## Content Types

- **announcement** - News and updates from RPs and community
- **eventseries** - Recurring event definitions
- **eventinstance** - Specific occurrences of events
- **affinity_group** - Community group pages
- **page** - Static documentation pages
- **article** - General articles and guides
