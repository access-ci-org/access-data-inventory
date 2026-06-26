---
id: resource_documentation_api
name: Resource Documentation API
track: Support
fields:
- name: nid
  type: int
  access: Public
  description: Drupal node ID of the resource.
  required: true
  semantic_type: entity_id
  authoritative_source: ACCESS Support Drupal
- name: title
  type: varchar
  access: Public
  description: Resource title.
  required: true
  semantic_type: entity_name
  authoritative_source: ACCESS Support Drupal
- name: short_name
  type: varchar
  access: Public
  description: Short display name.
  semantic_type: entity_name
  authoritative_source: ACCESS Support Drupal
- name: resource_id
  type: varchar
  access: Public
  description: CIDER resource identifier.
  required: true
  semantic_type: entity_id
  authoritative_source: ACCESS Support Drupal
- name: global_resource_id
  type: varchar
  access: Public
  description: ACCESS global resource ID.
  semantic_type: entity_id
  authoritative_source: ACCESS Support Drupal
- name: org_name
  type: varchar
  access: Public
  description: Organization that operates the resource.
  semantic_type: institution
  authoritative_source: ACCESS Support Drupal
- name: resource_type
  type: varchar
  access: Public
  description: Resource type (Compute, Storage, Cloud, etc.).
  semantic_type: entity_type
  authoritative_source: ACCESS Support Drupal
- name: description
  type: text
  access: Public
  description: Team-authored resource description (detail endpoint).
  semantic_type: entity_description
  authoritative_source: ACCESS Support Drupal
- name: last_modified
  type: timestamp
  access: Public
  description: ISO 8601 last-changed time.
  semantic_type: date_modified
  authoritative_source: ACCESS Support Drupal
- name: content_hash
  type: varchar
  access: Public
  description: Deterministic SHA-256 fingerprint of the resource payload (detail endpoint) for change detection.
  computed: true
  authoritative_source: ACCESS Support Drupal
- name: url
  type: varchar
  access: Public
  description: Canonical URL of the resource documentation page.
  semantic_type: url_external
  authoritative_source: ACCESS Support Drupal
category: Resources
access_level: Public
priority: Medium
description: Team-authored documentation for ACCESS resource providers (login, file transfer, storage, queue specs, top software, datasets), with resource-group inheritance.
notes: Detail responses include a content_hash for change detection. Documented on the portal at /api-docs/resources.
storage_location: support.access-ci.org
data_access_mechanism: API, Web
api_endpoint: https://support.access-ci.org/api/1.0/resources
refresh_frequency: Real-time
query_capacity: Per-resource and per-group lookups
is_canonical: false
canonical_source:
- access_support_drupal
- resource_information_cider
mcp:
  available: false
---
