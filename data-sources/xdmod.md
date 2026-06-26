---
id: xdmod
name: XDMoD Metrics
description: HPC metrics, usage analytics, and resource specifications from the ACCESS XDMoD instance
category: Metrics & Reporting
track: Metrics
access_level: Varies
is_canonical: true
api_endpoint: https://xdmod.access-ci.org/controllers/user_interface.php
dynamic: true
priority: High

mcp:
  available: true
  package: "@access-mcp/xdmod"
  tools:
    - name: describe_realms
      method: POST
      description: List all available data realms with dimensions and statistics counts
    - name: describe_fields
      method: POST
      description: Get dimensions and statistics for a specific realm
    - name: get_dimension_values
      method: POST
      description: Get filter values for a dimension (e.g., all resources, institutions)
    - name: get_chart_data
      method: POST
      description: Get chart data and metadata for a statistic with optional filters
    - name: get_chart_image
      method: POST
      description: Get chart as SVG, PNG, or PDF image
    - name: get_chart_link
      method: GET
      description: Generate a URL to the interactive XDMoD portal chart

mcp_authenticated:
  available: true
  package: "@access-mcp/xdmod-data"
  notes: Authenticated access via XDMoD API token (xdmod-data Python package). Required for per-user data queries.
  tools:
    - name: get_user_data
      description: Get user-specific usage data by exact user identifier
    - name: get_raw_data
      description: Extract XDMoD metrics with complex filtering, timeseries/aggregate modes
    - name: describe_fields
      description: Discover dimensions and metrics in a specific realm
    - name: describe_realms
      description: List all available XDMoD data realms with capabilities
    - name: get_smart_filters
      description: Discover filter values for use with get_raw_data (resources, queues, institutions)
    - name: get_analysis_template
      description: Get pre-configured analysis patterns (14 templates for common scenarios)
    - name: integrate_nsf_xdmod
      description: Correlate NSF funding data with XDMoD computational usage patterns

use_cases:
  - How much CPU time was used across ACCESS last quarter?
  - Which resources have the highest GPU utilization?
  - How many jobs ran on Delta in January 2024?
  - What science gateways are most active?
  - How are allocations distributed across fields of science?
  - What is the total GPU capacity across ACCESS resources?
  - Show me wait times by resource for the past month
  - How many active users and PIs are there?

realms:
  - name: Accounts
    description: ACCESS user account tracking — accounts associated with allocations and job activity
    access_level: Public
    dimensions: [none, resource, resource_type]
    statistics:
      - name: unique_account_count
        description: Number of Accounts Created
      - name: unique_account_with_jobs_count
        description: Number of Accounts Created with Jobs

  - name: Allocations
    description: Allocation and project tracking — active allocations, PIs, and resource usage in SUs/ACEs
    access_level: Public
    dimensions: [none, allocation, allocation_type, board_type, fieldofscience, nsfdirectorate, pi, parentscience, resource, resource_type]
    statistics:
      - name: active_allocation_count
        description: Number of Projects Active
      - name: active_pi_count
        description: Number of PIs Active
      - name: active_resallocation_count
        description: Number of Allocations Active
      - name: allocated_nu
        description: NUs Allocated
      - name: allocated_raw_su
        description: CPU Core Hours Allocated
      - name: allocated_su
        description: XD SUs Allocated
      - name: allocated_ace
        description: ACCESS Credit Equivalents Allocated (SU)
      - name: rate_of_usage
        description: Allocation Usage Rate (XD SU/Hour)
      - name: rate_of_usage_ace
        description: Allocation Usage Rate ACEs (SU/Hour)
      - name: used_su
        description: XD SUs Used
      - name: used_ace
        description: ACCESS Credit Equivalents Used (SU)

  - name: Cloud
    description: Cloud and virtualized compute environment metrics
    access_level: Public
    dimensions: [none, configuration, domain, instance_type, person, pi, project, provider, resource, resource_type, submission_venue, instance_state, institution, institution_country, institution_state, nsfdirectorate, parentscience, fieldofscience, pi_institution, pi_institution_country, pi_institution_state, vm_size, vm_size_cpu, vm_size_memory]
    statistics:
      - name: cloud_num_sessions_ended
        description: Number of Sessions Ended
      - name: cloud_num_sessions_started
        description: Number of Sessions Started
      - name: cloud_num_sessions_running
        description: Number of Sessions Active
      - name: cloud_wall_time
        description: Wall Hours Total
      - name: cloud_core_time
        description: CPU Hours Total
      - name: cloud_avg_wallduration_hours
        description: Wall Hours Per Session
      - name: cloud_avg_cores_reserved
        description: Average Cores Reserved Weighted By Wall Hours
      - name: cloud_avg_memory_reserved
        description: Average Memory Reserved Weighted By Wall Hours (Bytes)
      - name: cloud_avg_rv_storage_reserved
        description: Average Root Volume Storage Reserved (Bytes)
      - name: cloud_core_utilization
        description: Core Hour Utilization (%)
      - name: gateway_session_count
        description: Number of Sessions Ended via Gateway

  - name: Gateways
    description: Science gateway job metrics — jobs submitted through ACCESS gateways
    access_level: Public
    dimensions: [none, allocation, fieldofscience, gateway, gateway_user, grant_type, jobsize, jobwaittime, jobwalltime, nsfdirectorate, nodecount, pi, pi_institution, pi_institution_country, pi_institution_state, parentscience, queue, resource, resource_type, provider, person, institution, institution_country, institution_state]
    statistics:
      - name: job_count
        description: Number of Jobs Ended
      - name: running_job_count
        description: Number of Jobs Running
      - name: started_job_count
        description: Number of Jobs Started
      - name: submitted_job_count
        description: Number of Jobs Submitted
      - name: total_cpu_hours
        description: CPU Hours Total
      - name: total_node_hours
        description: Node Hours Total
      - name: total_wallduration_hours
        description: Wall Hours Total
      - name: total_waitduration_hours
        description: Wait Hours Total
      - name: avg_cpu_hours
        description: CPU Hours Per Job
      - name: avg_node_hours
        description: Node Hours Per Job
      - name: avg_wallduration_hours
        description: Wall Hours Per Job
      - name: avg_waitduration_hours
        description: Wait Hours Per Job
      - name: avg_processors
        description: Job Size Per Job (Core Count)
      - name: max_processors
        description: Job Size Max (Core Count)
      - name: min_processors
        description: Job Size Min (Core Count)
      - name: normalized_avg_processors
        description: Job Size Normalized (% of Total Cores)
      - name: total_su
        description: XD SUs Charged Total
      - name: avg_su
        description: XD SUs Charged Per Job
      - name: total_nu
        description: NUs Charged Total
      - name: avg_nu
        description: NUs Charged Per Job
      - name: total_ace
        description: ACCESS Credit Equivalents Charged Total (SU)
      - name: avg_ace
        description: ACCESS Credit Equivalents Charged Per Job (SU)
      - name: expansion_factor
        description: User Expansion Factor
      - name: utilization
        description: ACCESS CPU Utilization (%)
      - name: active_resource_count
        description: Number of Resources Active
      - name: active_institution_count
        description: Number of Institutions Active
      - name: active_gateway_count
        description: Number of Gateways Active
      - name: active_gwuser_count
        description: Number of Gateway Users Active

  - name: Jobs
    description: Job accounting and resource usage metrics from job schedulers
    access_level: Public
    dimensions: [none, allocation, fieldofscience, grant_type, jobsize, jobwaittime, jobwalltime, nsfdirectorate, nodecount, pi, pi_institution, pi_institution_country, pi_institution_state, parentscience, queue, resource, resource_type, provider, person, institution, institution_country, institution_state, username, qos, application]
    statistics:
      - name: job_count
        description: Number of Jobs Ended
      - name: running_job_count
        description: Number of Jobs Running
      - name: started_job_count
        description: Number of Jobs Started
      - name: submitted_job_count
        description: Number of Jobs Submitted
      - name: total_cpu_hours
        description: CPU Hours Total
      - name: total_node_hours
        description: Node Hours Total
      - name: total_wallduration_hours
        description: Wall Hours Total
      - name: total_waitduration_hours
        description: Wait Hours Total
      - name: avg_cpu_hours
        description: CPU Hours Per Job
      - name: avg_node_hours
        description: Node Hours Per Job
      - name: avg_wallduration_hours
        description: Wall Hours Per Job
      - name: avg_waitduration_hours
        description: Wait Hours Per Job
      - name: avg_processors
        description: Job Size Per Job (Core Count)
      - name: max_processors
        description: Job Size Max (Core Count)
      - name: min_processors
        description: Job Size Min (Core Count)
      - name: normalized_avg_processors
        description: Job Size Normalized (% of Total Cores)
      - name: total_su
        description: XD SUs Charged Total
      - name: avg_su
        description: XD SUs Charged Per Job
      - name: total_nu
        description: NUs Charged Total
      - name: avg_nu
        description: NUs Charged Per Job
      - name: total_ace
        description: ACCESS Credit Equivalents Charged Total (SU)
      - name: avg_ace
        description: ACCESS Credit Equivalents Charged Per Job (SU)
      - name: expansion_factor
        description: User Expansion Factor
      - name: utilization
        description: ACCESS CPU Utilization (%)
      - name: gateway_job_count
        description: Number of Jobs via Gateway
      - name: active_person_count
        description: Number of Users Active
      - name: active_pi_count
        description: Number of PIs Active
      - name: active_resource_count
        description: Number of Resources Active
      - name: active_allocation_count
        description: Number of Allocations Active
      - name: active_institution_count
        description: Number of Institutions Active

  - name: Requests
    description: Allocation request and proposal tracking
    access_level: Public
    dimensions: [none, fieldofscience, nsfdirectorate, parentscience]
    statistics:
      - name: request_count
        description: Number of Proposals
      - name: project_count
        description: Number of Projects

  - name: ResourceSpecifications
    description: Resource hardware specifications — CPU/GPU counts, node hours, and capacity metrics
    access_level: Public
    dimensions: [none, resource, resource_institution_country, resource_institution_state, resource_type]
    statistics:
      - name: total_cpu_core_hours
        description: CPU Hours Total
      - name: allocated_cpu_core_hours
        description: CPU Hours Allocated
      - name: total_gpu_hours
        description: GPU Hours Total
      - name: allocated_gpu_hours
        description: GPU Hours Allocated
      - name: total_gpu_node_hours
        description: GPU Node Hours Total
      - name: allocated_gpu_node_hours
        description: GPU Node Hours Allocated
      - name: total_cpu_node_hours
        description: CPU Node Hours Total
      - name: allocated_cpu_node_hours
        description: CPU Node Hours Allocated
      - name: total_avg_number_of_cpu_cores
        description: Average Number of CPU Cores Total
      - name: allocated_avg_number_of_cpu_cores
        description: Average Number of CPU Cores Allocated
      - name: total_avg_number_of_gpus
        description: Average Number of GPUs Total
      - name: allocated_avg_number_of_gpus
        description: Average Number of GPUs Allocated
      - name: total_avg_number_of_cpu_nodes
        description: Average Number of CPU Nodes Total
      - name: allocated_avg_number_of_cpu_nodes
        description: Average Number of CPU Nodes Allocated
      - name: total_avg_number_of_gpu_nodes
        description: Average Number of GPU Nodes Total
      - name: allocated_avg_number_of_gpu_nodes
        description: Average Number of GPU Nodes Allocated
      - name: ace_total
        description: ACCESS Credit Equivalents Available Total (SU)
      - name: ace_allocated
        description: ACCESS Credit Equivalents Available Allocated (SU)

  - name: Storage
    description: File system and storage usage metrics
    access_level: Public
    dimensions: []
    statistics:
      - name: user_count
        description: User Count
      - name: avg_physical_usage
        description: Physical Usage (Bytes)
      - name: avg_logical_usage
        description: Logical Usage (Bytes)
      - name: avg_file_count
        description: File Count
      - name: avg_hard_threshold
        description: Quota Hard Threshold (Bytes)
      - name: avg_soft_threshold
        description: Quota Soft Threshold (Bytes)

  - name: SUPREMM
    description: Detailed job performance analytics — CPU, GPU, memory, network, and I/O metrics from monitoring
    access_level: Public
    dimensions: [none, resource, person, pi, institution, jobsize, queue, fieldofscience, nsfdirectorate, parentscience, application, cpi, cpu, cpucv, cpuuser, datasource, exit_status, gpu_count, granted_pe, ibrxbyterate, jobwalltime, max_mem, mem_used, nodecount, pi_institution, provider, resource_type, shared, username, institution_country, institution_state]
    statistics:
      - name: job_count
        description: Number of Jobs Ended
      - name: short_job_count
        description: Number of Short Jobs Ended
      - name: running_job_count
        description: Number of Jobs Running
      - name: started_job_count
        description: Number of Jobs Started
      - name: submitted_job_count
        description: Number of Jobs Submitted
      - name: wall_time
        description: CPU Hours Total
      - name: wall_time_per_job
        description: Wall Hours Per Job
      - name: wait_time
        description: Wait Hours Total
      - name: wait_time_per_job
        description: Wait Hours Per Job
      - name: requested_wall_time
        description: Wall Hours Requested Total
      - name: requested_wall_time_per_job
        description: Wall Hours Requested Per Job
      - name: wall_time_accuracy
        description: Wall Time Accuracy (%)
      - name: cpu_time_user
        description: CPU Hours User Total
      - name: cpu_time_system
        description: CPU Hours System Total
      - name: cpu_time_idle
        description: CPU Hours Idle Total
      - name: avg_percent_cpu_user
        description: Avg CPU % User weighted by core-hour
      - name: avg_percent_cpu_system
        description: Avg CPU % System weighted by core-hour
      - name: avg_percent_cpu_idle
        description: Avg CPU % Idle weighted by core-hour
      - name: gpu_time
        description: GPU Hours Total
      - name: avg_percent_gpu_usage
        description: Avg GPU usage weighted by GPU hour (%)
      - name: avg_flops_per_core
        description: Avg FLOPS Per Core weighted by core-hour (ops/s)
      - name: avg_memory_per_core
        description: Avg Memory Per Core weighted by core-hour (bytes)
      - name: avg_total_memory_per_core
        description: Avg Total Memory Per Core weighted by core-hour (bytes)
      - name: avg_max_memory_per_core
        description: Avg Max Memory weighted by core-hour (%)
      - name: avg_mem_bw_per_core
        description: Avg Memory Bandwidth Per Core weighted by core-hour (bytes/s)
      - name: avg_ib_rx_bytes
        description: Avg InfiniBand rate Per Node weighted by node-hour (bytes/s)
      - name: avg_homogeneity
        description: Avg Homogeneity weighted by node-hour (%)
      - name: total_su
        description: XD SUs Charged Total
      - name: avg_su
        description: XD SUs Charged Per Job
      - name: total_ace
        description: ACCESS Credit Equivalents Charged Total (SU)
      - name: avg_ace
        description: ACCESS Credit Equivalents Charged Per Job (SU)
      - name: active_pi_count
        description: Number of PIs Active
      - name: active_app_count
        description: Number of Applications Active

notes:
  - All statistics are available via public_user=true (no authentication required for aggregate data)
  - Personal/per-user data requires XDMoD API token authentication (xdmod-data Python package)
  - Statistics discovered from live API on 2026-02-22 using metaData.fields from get_data endpoint
  - SUPREMM has ~20 additional network I/O statistics (eth0, ib0, lustre, block device rates) not listed individually
  - Storage realm does not appear in menu queries but statistics work via direct get_data calls
---

## Overview

XDMoD (XD Metrics on Demand) provides comprehensive metrics on ACCESS cyberinfrastructure usage. It covers 9 realms of data from job accounting (Jobs), detailed performance monitoring (SUPREMM), cloud compute (Cloud), gateway usage (Gateways), allocation tracking (Allocations), user accounts (Accounts), allocation requests (Requests), resource hardware specifications (ResourceSpecifications), and storage (Storage).

Two MCP servers provide access at different tiers:
- **@access-mcp/xdmod** (TypeScript, 6 tools) — Public aggregate data via `public_user=true`. No auth required. Discovery, chart data, chart images, and portal links.
- **@access-mcp/xdmod-data** (Python, 7 tools) — Authenticated access via XDMoD API tokens. Per-user data, complex filtering, analysis templates, and NSF funding integration. Requires `XDMOD_API_TOKEN`.

## Notes

- The `public_user=true` parameter enables unauthenticated access to aggregate metrics
- Per-user and personal data queries require the `xdmod-data` Python package with an API token
- XDMoD is maintained by the University at Buffalo Center for Computational Research (CCR)
- The ACCESS instance at xdmod.access-ci.org includes ACCESS-specific realms (Accounts, Allocations, Requests, ResourceSpecifications) not in the open-source XDMoD
