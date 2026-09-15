---
id: access_xdmod_data_catalog
name: ACCESS XDMoD Data Catalog
track: Metrics
fields:
- name: Catalog overview
  type: text
  access: Public
  description: Summary of XDMoD data catalog
  required: true
  semantic_type: entity_summary
- name: Catalog name
  type: varchar
  access: Public
  description: Name of information in data catalog
  required: true
  semantic_type: entity_name
- name: Description
  type: text
  access: Public
  description: Description of the data provided
  required: true
  semantic_type: entity_description
- name: Realm
  type: varchar
  access: Public
  description: The XDMoD realm that provides the data
  required: true
  semantic_type: entity_name
- name: Type
  type: varchar
  access: Public
  description: Is type of (Metric, Group By, Raw Data)
  required: true
  semantic_type: entity_type
access_level: Public
priority: High
description: List of available statistics and dimensions
storage_location: Metrics Website
data_access_mechanism: API, MCP, Web
sensitivity: Low
is_canonical: true
mcp:
  available: false
---
