---
id: xdmod_open_api_documentation
name: XDMoD Open API Documentation
track: Metrics
fields:
- name: Endpoint Name
  type: varchar
  access: Public
  description: XDMoD REST API Endpoint Name
  required: true
  semantic_type: entity_name
- name: Endpoint Description
  type: text
  access: Public
  description: Purpose of endpoint
  semantic_type: entity_summary
- name: Authorizations
  type: varchar
  access: Public
  description: Supported authentication methods
  required: true
  semantic_type: entity_type
- name: Request Body Schema
  type: varchar
  access: Public
  description: Schema type
  semantic_type: entity_type
- name: Path Parameters
  type: text
  access: Public
  description: Path parameters and their descriptions
  semantic_type: entity_description
- name: Request Parameters
  type: text
  access: Public
  description: Query parameters and their descriptions
  semantic_type: entity_description
- name: Endpoint Responses
  type: text
  access: Public
  description: Possible request responses
  required: true
  semantic_type: entity_description
access_level: Public
priority: High
description: Descriptions of XDMoD Open API endpoints
data_access_mechanism: Web
docs_url: https://open.xdmod.org/11.0/rest.html
refresh_frequency: static
sensitivity: Low
is_canonical: true
mcp:
  available: false
---
