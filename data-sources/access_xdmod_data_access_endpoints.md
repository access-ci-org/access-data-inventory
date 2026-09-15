---
id: access_xdmod_data_access_endpoints
name: ACCESS XDMoD Data Access Endpoints
track: Metrics
fields:
- name: Raw Data
  type: JSON
  access:
  - Public
  - Authenticated
- name: Aggregate Data
  type: JSON
  access:
  - Public
  - Authenticated
- name: Timeseries Data
  type: JSON
  access:
  - Public
  - Authenticated
category: Usage & Metrics
access_level: Public and Authenticated
priority: High
description: 'Allocations Information,

  Compute Usage,

  HPC Job Performance & Power Data,

  Science Gateway Usage,

  Resource Quality of service data (via Application Kernels),

  HPC Job Efficiency Analytics,

  Commercial and Non-Commercial Cloud Usage,

  Open OnDemand Usage'
storage_location: XDMoD Datawarehouse
data_access_mechanism: API, Web, MCP
docs_url: https://open.xdmod.org/11.0/rest.html
refresh_frequency: daily
sensitivity: High
is_canonical: false
canonical_source:
- batch_compute_log_file_from_resource_provider
- amie_packet_from_resouce_provider
- xras_data
- cilogon_information
mcp:
  available: false
---
