---
id: xdmod_data_github_repository
name: xdmod-data GitHub Repository
track: Metrics
fields:
- name: Source Code
  type: text
  access: Public
  description: Source code for Data Analytics Framework
  required: true
  semantic_type: entity_description
- name: Python Package Information
  type: text
  access: Public
  description: PyPI package information
  required: true
  semantic_type: entity_summary
- name: API Token Instructions
  type: text
  access: Public
  description: API Token generation instructions
  required: true
  semantic_type: entity_description
- name: Support & Feedback Information
  type: text
  access: Public
  required: true
  semantic_type: contact_info
- name: Licence Information
  type: text
  access: Public
  required: true
  semantic_type: entity_type
- name: Reference Citation
  type: text
  access: Public
  required: true
  semantic_type: entity_name
access_level: Public
priority: Low
description: Documentation for the XDMoD Python/R APIs
storage_location: Github
data_access_mechanism: Web
refresh_frequency: static
sensitivity: Low
is_canonical: true
mcp:
  available: false
---
