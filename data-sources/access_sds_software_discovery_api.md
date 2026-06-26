---
id: access_sds_software_discovery_api
name: ACCESS SDS (Software Discovery) API
track: Support
fields:
- name: rps
  type: json
  access: Restricted
  access_notes: API key required
  description: 'Request param: array of Resource Provider names/IDs to filter by, case-insensitive. Conditional (rps and/or software).'
  notes: Request body field
  authoritative_source: SDS
- name: software
  type: json
  access: Restricted
  access_notes: API key required
  description: 'Request param: array of software names to filter by, case-insensitive. Conditional (rps and/or software).'
  semantic_type: entity_name
  notes: Request body field
  authoritative_source: SDS
- name: columns
  type: json
  access: Restricted
  access_notes: API key required
  description: 'Request param: array of fields to return. rp_software and software_name are always included.'
  notes: Request body field
  authoritative_source: SDS
- name: exclude
  type: boolean
  access: Restricted
  access_notes: API key required
  description: 'Request param: when true, treat columns as an exclude list rather than an include list. Default false.'
  notes: Request body field
  authoritative_source: SDS
- name: fuzz_software
  type: boolean
  access: Restricted
  access_notes: API key required
  description: 'Request param: enable fuzzy matching on software names. Default false.'
  notes: Request body field
  authoritative_source: SDS
- name: fuzz_rp
  type: boolean
  access: Restricted
  access_notes: API key required
  description: 'Request param: enable fuzzy matching on RP names/IDs. Default false.'
  notes: Request body field
  authoritative_source: SDS
- name: collapse_resource_groups
  type: boolean
  access: Restricted
  access_notes: API key required
  description: 'Request param: when false, emit separate entries per resource group. Default true.'
  notes: Request body field
  authoritative_source: SDS
- name: software_name
  type: varchar
  access: Restricted
  access_notes: API key required
  description: 'Response field: name of the software package. Results are sorted alphabetically by this field.'
  required: true
  semantic_type: entity_name
  notes: Always present in responses
  authoritative_source: SDS
- name: rp_software
  type: varchar
  access: Restricted
  access_notes: API key required
  description: 'Response field: the software identifier as known to the resource provider. Always present in responses.'
  required: true
  notes: Always present in responses
  authoritative_source: SDS
- name: resource_provider
  type: varchar
  access: Restricted
  access_notes: API key required
  description: 'Response field: resource provider / resource group the software is available on.'
  semantic_type: institution
  notes: Response field
  authoritative_source: SDS
category: Resources
access_level: Restricted
priority: Medium
description: 'Software discovery: which software packages are available on which ACCESS resource providers.'
notes: Requires an X-API-Key header. Request a key by opening a ticket at https://support.access-ci.org/help-ticket. Documented on the portal at /api-docs/sds.
storage_location: sds-ara-api.access-ci.org
data_access_mechanism: POST-only HTTP/JSON API (single endpoint POST /api/v1; no GET endpoints)
api_endpoint: https://sds-ara-api.access-ci.org/api/v1
refresh_frequency: Daily
query_capacity: Per-request software/RP filtering with optional fuzzy matching and column selection
is_canonical: false
canonical_source:
- resource_documentation_api
mcp:
  available: false
---
