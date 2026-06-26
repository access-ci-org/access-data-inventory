---
id: content_api
name: Content API
track: Support
fields:
- name: id
  type: int
  access: Public
  description: Drupal node ID of the page.
  required: true
  semantic_type: entity_id
  authoritative_source: ACCESS Support Drupal
- name: title
  type: varchar
  access: Public
  description: Page title.
  required: true
  semantic_type: entity_name
  authoritative_source: ACCESS Support Drupal
- name: path
  type: varchar
  access: Public
  description: Absolute URL of the support page.
  semantic_type: url_external
  authoritative_source: ACCESS Support Drupal
- name: content_type
  type: varchar
  access: Public
  description: Drupal content type of the page.
  semantic_type: entity_type
  authoritative_source: ACCESS Support Drupal
- name: text
  type: text
  access: Public
  description: Full extracted plain text of the page (detail endpoint).
  computed: true
  semantic_type: entity_description
  authoritative_source: ACCESS Support Drupal
- name: content_hash
  type: varchar
  access: Public
  description: SHA-256 hash of the extracted text for incremental ingestion.
  computed: true
  authoritative_source: ACCESS Support Drupal
- name: last_modified
  type: timestamp
  access: Public
  description: ISO 8601 last-changed time.
  semantic_type: date_modified
  authoritative_source: ACCESS Support Drupal
- name: content_url
  type: varchar
  access: Public
  description: URL of the per-page content endpoint (index entries).
  semantic_type: url_external
  authoritative_source: ACCESS Support Drupal
category: Content Management
access_level: Public
priority: Medium
description: Plain-text page content and a discovery index for ACCESS Support pages, for RAG ingestion and search syndication.
notes: Responses include content_hash (SHA-256 of extracted text) and last_modified for incremental ingestion. Documented on the portal at /api-docs/content.
storage_location: support.access-ci.org
data_access_mechanism: API, Web
api_endpoint: https://support.access-ci.org/.well-known/content-index.json
refresh_frequency: Real-time
query_capacity: Per-page by node ID or path alias
is_canonical: false
canonical_source:
- access_support_drupal
mcp:
  available: false
---
