---
id: announcements
name: Announcements
description: RP and community announcements
category: Community & Outreach
track: Support
access_level: Public and Authenticated
is_canonical: false
canonical_source:
- access_support_drupal
api_endpoint: https://support.access-ci.org/api/2.2/announcements
dynamic: false
priority: High
mcp:
  available: true
  url: https://mcp.access-ci.org/announcements/mcp
  tools:
  - name: search_announcements
    method: GET
    description: Search announcements with filters
  - name: get_my_announcements
    method: GET
    description: Get announcements authored by current user
  - name: create_announcement
    method: POST
    description: Create a new announcement
  - name: update_announcement
    method: PATCH
    description: Update an existing announcement
  - name: delete_announcement
    method: DELETE
    description: Delete an announcement
use_cases:
- What announcements have been published this week?
- Are there any announcements related to a specific affinity group?
- What resource provider updates have been shared recently?
fields:
- name: nid
  type: int
  access: Public
  description: Node ID
  required: true
  semantic_type: entity_id
  primary_key: true
- name: uuid
  type: varchar
  access: Public
  description: Unique identifier
  required: true
  mcp_name: uuid
  semantic_type: uuid
- name: title
  type: varchar
  access: Public
  description: Announcement title
  required: true
  mcp_name: title
  semantic_type: entity_name
- name: body
  type: text
  access: Public
  description: HTML content
  required: true
  mcp_name: body
  semantic_type: entity_description
- name: summary
  type: varchar
  access: Public
  description: Short summary text
  mcp_name: summary
  semantic_type: entity_summary
- name: published_date
  type: date
  access: Public
  description: When the announcement was published
  required: true
  mcp_name: published_date
  semantic_type: date_published
- name: affiliation
  type: varchar
  access: Public
  description: Whether this is an official ACCESS or community announcement
  mcp_name: affiliation
  semantic_type: affiliation
- name: external_link
  type: varchar
  access: Public
  description: Link to external resource
  mcp_name: external_link
  semantic_type: url_external
- name: where_to_share
  type: text
  access: Internal Only
  description: Distribution channels for this announcement
  mcp_name: where_to_share
- name: affinity_group_id
  type: int
  access: Public
  description: Associated affinity group
  mcp_name: affinity_group
  references: affinity_groups.nid
- name: image_id
  type: int
  access: Public
  description: Associated media image
  semantic_type: media_ref
relationships:
- type: belongs_to
  target: affinity_groups
  field: affinity_group_id
  description: Announcements can be associated with an affinity group
- type: has_many
  target: tags
  through: entity_tags
  description: Announcements can be tagged for categorization
notes: announcements MCP exists
data_access_mechanism: API, MCP, Web
docs_url: https://support.access-ci.org/api-docs/announcements
refresh_frequency: real-time
query_capacity: high
sensitivity: Low
---

## Overview

Announcements from resource providers and the ACCESS community. These are published on the ACCESS Support website and can be distributed via the bi-weekly digest email.

## Notes

- The announcements MCP supports full CRUD operations for authenticated users
- HTML content is preserved in the body field
- The `where_to_share` field is internal only - not exposed to public consumers
- Announcements can optionally be associated with an affinity group
