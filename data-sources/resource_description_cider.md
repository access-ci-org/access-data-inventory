---
id: resource_description_cider
name: Resource Description (CIDeR)
track: Operations
fields:
- name: cider_resource_id
  type: int
  access: Public
  description: CiDeR primary key
  required: true
- name: info_resource_id
  type: varchar
  access: Public
  description: Global human meaningful resource ID
  required: true
  notes: Used across all Operations information repositories to identify a resource
- name: info_site_id
  type: varchar
  access: Public
  description: Global human meaningful site ID
  required: true
  notes: Used across all Operations information repositories to identify a site
- name: cider_type
  type: varchar
  access: Public
  description: Compute, Storage, Gateway, Network, etc.
  required: true
- name: organization_name
  type: varchar
  access: Public
  required: true
- name: organization_url
  type: varchar
  access: Public
  required: true
- name: organization_logo_url
  type: varchar
  access: Public
  required: true
- name: groups
  type: int
  access: Public
  description: list of resource groups this resource belongs to
  required: true
- name: resource_descriptive_name
  type: varchar
  access: Public
  description: Descriptive resource name
  required: true
- name: resource_description
  type: varchar
  access: Public
  description: Full resource description
  required: true
- name: project_affiliation
  type: varchar
  access: Public
  description: 'Resource affliation: ACCESS, NAIRR, etc.'
  required: true
- name: latest_status
  type: varchar
  access: Public
  description: Coming soon, pre-production, production, post-production, or retired status
  required: true
- name: latest_status_start
  type: date
  access: Public
  description: What latest status starts
  required: true
- name: latest_status_end
  type: date
  access: Public
  description: What latest status ends
  required: true
- name: resource_status
  type: JSON
  access: Public
  description: Historical statuses with corresponding start and end dates
  required: true
- name: compute.recommended_use
  type: varchar
  access: Public
  required: true
- name: compute.access_description
  type: varchar
  access: Public
  required: true
- name: compute.use_guide_url
  type: varchar
  access: Public
  required: true
- name: compute.cpu_type
  type: varchar
  access: Public
  required: true
- name: compute.operating_system
  type: varchar
  access: Public
  required: true
- name: compute.gpu_description
  type: varchar
  access: Public
  required: true
- name: compute.recommended_use
  type: varchar
  access: Public
  required: true
- name: compute.job_manager
  type: varchar
  access: Public
  required: true
- name: compute.batch_system
  type: varchar
  access: Public
  required: true
- name: compute.interconnect
  type: varchar
  access: Public
  required: true
- name: compute.storage_network
  type: varchar
  access: Public
  required: true
- name: compute.machine_type
  type: varchar
  access: Public
  required: true
- name: compute.cpu_speed_ghz
  type: int
  access: Public
  required: true
- name: compute.platform_name
  type: varchar
  access: Public
  required: true
- name: compute.memory_per_cpu_gb
  type: int
  access: Public
  required: true
- name: compute.cpu_count_per_node
  type: int
  access: Public
  required: true
- name: compute.xsedenet_participation
  type: varchar
  access: Public
  required: true
- name: compute.node_count
  type: int
  access: Public
  required: true
- name: compute.supports_sensitive_data
  type: varchar
  access: Public
  required: true
- name: compute.sensitive_data_support_description
  type: varchar
  access: Public
  required: true
- name: compute.local_storage_per_node_gb
  type: int
  access: Public
  required: true
- name: storage.<multiple_attributes>
  type: int
  access: Public
  required: true
- name: gateway.<multiple_attributes>
- name: features
  type: JSON
  access: Public
  description: Contains feature id, name, description, category_types, and feature_category
  required: true
category: Resources
access_level: Public
priority: High
description: Organizations, resource descriptions, and integration information for ACCESS resource providers.
notes: Source of record for ACCESS resource/organization data. The Resource Documentation API and SDS draw on CiDeR resource identifiers.
storage_location: operations.access-ci.org
data_access_mechanism: API, Web
api_endpoint: https://operations-api.access-ci.org/wh2/cider/v1/
refresh_frequency: Daily
query_capacity: high
is_canonical: true
mcp:
  available: false
---
