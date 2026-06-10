---
layout: default
title: Fields
---

# Fields

Field-level documentation for all ACCESS data sources.

## Table of Contents

- [ACCESS Support Drupal](#access_support_drupal)
- [Affinity Groups](#affinity_groups)
- [Announcements](#announcements)
- [COManage/ACCESS Identity](#comanage)
- [Event Registrations](#event_registrations)
- [Events and Training](#events)
- [XDMoD Metrics](#xdmod)

<h2 id="access_support_drupal">ACCESS Support Drupal</h2>

*ACCESS Support website CMS - canonical storage for support content*

> **Authoritative source** for: [Announcements](#announcements), [Events and Training](#events), [Affinity Groups](#affinity_groups), [tags](#tags)

**Example questions this data can answer:**

- What content types are stored in the ACCESS Support CMS?
- When was a specific piece of content last modified?
- How many published nodes exist by content type?

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) * | int | Public |  | Drupal node ID [entity_id] |
| `uuid` * | varchar | Public |  | Drupal UUID [uuid] |
| `type` * | varchar | Public |  | Drupal content type [entity_type] |
| `title` * | varchar | Public |  | Content title [entity_name] |
| `body` | text | Public |  | Content body (HTML) [entity_description] |
| `status` * | boolean | Internal Only |  | Published status [entity_status] |
| `created` * | timestamp | Public |  | Content creation date [date_created] |
| `changed` * | timestamp | Public |  | Last modification date [date_modified] |
| `uid` * | int | Restricted |  | Author user ID |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Has Many** `announcements`: Stores announcement content
- **Has Many** `events`: Stores event content (series and instances)
- **Has Many** `affinity_groups`: Stores affinity group content
- **Has Many** `tags`: Stores taxonomy terms
- **Has Many** `users`: Stores user accounts (Drupal users, linked to COManage)

<h2 id="affinity_groups">Affinity Groups</h2>

*Community groups organized by interest or domain*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source(s) above.

**Example questions this data can answer:**

- Which affinity groups are available for a specific research domain?
- Who coordinates a particular affinity group?
- What events are associated with an affinity group?
- How can I join or contact an affinity group?

**Constraints:**

- **Privacy:** Mailing lists, private group flags, and membership lists are restricted and must not be exposed through public APIs or AI tools.

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) * | int | Public |  | Node ID [entity_id] |
| `uuid` * | varchar | Public | id | Unique identifier [uuid] |
| `title` * | varchar | Public | name | Group name [entity_name] |
| `body` | text | Public | description | Group description (HTML cleaned in MCP) [entity_description] |
| `group_id` * | varchar | Public | id | URL-friendly group identifier [entity_id] |
| `group_slug` | varchar | Public |  | URL slug for the group |
| `category` | varchar | Public | category | Whether this is an RP-specific or community group [entity_type] |
| `goals` | text | Public |  | Group goals and objectives [entity_summary] |
| `coordinator_id` | int | Public | coordinator | Group coordinator (exposed as name string in MCP) |
| `slack_link` | varchar | Public | slack_link | Link to Slack channel [url_external] |
| `mailing_list` | varchar | Restricted |  | Internal mailing list address [contact_info] |
| `external_email_list` | varchar | Restricted |  | External email list address [contact_info] |
| `github_org` | varchar | Public |  | GitHub organization URL [url_external] |
| `ask_ci_forum` | varchar | Public | ask_ci_forum | Link to Ask.CI forum topic [url_external] |
| `meeting_notes_link` | varchar | Public |  | Link to meeting notes document [url_external] |
| `is_private` | boolean | Restricted |  | Whether the group is private |
| `private_users` | text | Restricted |  | List of users with access to private group |
| `image_id` | int | Public |  | Group logo/image [media_ref] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Has One** `users`: Each group has a coordinator
- **Has Many** `events`: Groups host events
- **Has Many** `announcements`: Groups publish announcements
- **Has Many** `users`: Groups have members
- **Has Many** `tags`: Groups can be tagged

<h2 id="announcements">Announcements</h2>

*Resource provider and community announcements*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source(s) above.

**Example questions this data can answer:**

- What announcements have been published this week?
- Are there any announcements related to a specific affinity group?
- What resource provider updates have been shared recently?

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) * | int | Public |  | Node ID [entity_id] |
| `uuid` * | varchar | Public | uuid | Unique identifier [uuid] |
| `title` * | varchar | Public | title | Announcement title [entity_name] |
| `body` * | text | Public | body | HTML content [entity_description] |
| `summary` | varchar | Public | summary | Short summary text [entity_summary] |
| `published_date` * | date | Public | published_date | When the announcement was published [date_published] |
| `affiliation` | varchar | Public | affiliation | Whether this is an official ACCESS or community announcement [affiliation] |
| `external_link` | varchar | Public | external_link | Link to external resource [url_external] |
| `where_to_share` | text | Internal Only | where_to_share | Distribution channels for this announcement |
| `affinity_group_id` | int | Public | affinity_group | Associated affinity group |
| `image_id` | int | Public |  | Associated media image [media_ref] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Belongs To** `affinity_groups`: Announcements can be associated with an affinity group
- **Has Many** `tags`: Announcements can be tagged for categorization

<h2 id="comanage">COManage/ACCESS Identity</h2>

*User identity information*

**Example questions this data can answer:**

- How many unique users are registered in ACCESS?
- Which institutions have the most ACCESS users?
- Is a specific user affiliated with a particular institution?

**Constraints:**

- **Privacy:** Contains PII (names, emails, ACCESS IDs). Must not be exposed through public APIs, AI tools, or MCP servers.
- **Acceptable Use:** Identity data may only be accessed by named individuals with legitimate need or systems with explicit authorization.
- **Regulatory:** Subject to institutional data handling agreements and FERPA considerations for student researchers.

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `user_id` (PK) | varchar | Sensitive |  | Internal user identifier [entity_id] |
| `access_id` | varchar | Sensitive |  | ACCESS username (e.g., jsmith) [entity_id] |
| `email` | varchar | Sensitive |  | User email address (PII) [person_email] |
| `name` | varchar | Restricted |  | User's display name [person_name] |
| `institution` | varchar | Restricted |  | User's institutional affiliation [institution] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Has Many** `affinity_group_members`: Users can be members of affinity groups
- **Has Many** `event_registrations`: Users register for events

<h2 id="event_registrations">Event Registrations</h2>

*Registration and attendance data for events*

**Example questions this data can answer:**

- How many people registered for a specific event?
- What is the attendance rate for training sessions?
- Which institutions are most represented at ACCESS events?
- How do registrants hear about ACCESS events?

**Constraints:**

- **Privacy:** Contains PII (names, emails, ACCESS IDs). Must not be exposed through public APIs or AI tools.
- **Acceptable Use:** Registration data may only be used for event management, reporting, and outreach effectiveness analysis. Individual-level data must not be shared outside authorized teams.

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `registration_id` (PK) * | varchar | Restricted |  | Registration record ID [entity_id] |
| `event_id` * | int | Restricted |  | Associated event |
| `user_id` * | varchar | Restricted |  | Registered user |
| `registration_date` * | timestamp | Restricted |  | When the registration was submitted [date_created] |
| `attendance_status` | varchar | Restricted |  | Registration and attendance status [entity_status] |
| `referral_source` | varchar | Restricted |  | How the registrant heard about the event |
| `registrant_name` | varchar | Sensitive |  | Registrant's name (PII) [person_name] |
| `registrant_email` | varchar | Sensitive |  | Registrant's email address (PII) [person_email] |
| `registrant_institution` | varchar | Restricted |  | Registrant's institutional affiliation [institution] |
| `registrant_access_id` | varchar | Sensitive |  | Registrant's ACCESS ID (PII) [entity_id] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Belongs To** `events`: Each registration is for a specific event
- **Belongs To** `users`: Each registration is linked to a user

<h2 id="events">Events and Training</h2>

*Workshops, webinars, training sessions, and office hours*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source(s) above.

**Example questions this data can answer:**

- What training sessions are available for beginners this month?
- Which events are associated with a specific affinity group?
- How many office hours are scheduled for next week?
- What events require registration?

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `id` (PK) * | int | Public |  | Event ID [entity_id] |
| `uuid` * | varchar | Public |  | Unique identifier [uuid] |
| `title` * | varchar | Public | title | Event title [entity_name] |
| `description` | text | Public | description | Event description [entity_description] |
| `event_type` * | varchar | Public | type | Type of event [entity_type] |
| `skill_level` | varchar | Public | skill | Target skill level for attendees [skill_level] |
| `affiliation` | varchar | Public |  | Whether this is an official ACCESS or community event [affiliation] |
| `start_date` * | timestamp | Public | start_date | Event start date and time [date_start] |
| `end_date` | timestamp | Public | end_date | Event end date and time [date_end] |
| `duration_hours` | decimal | Public | duration_hours | Calculated duration in hours (computed) [duration] |
| `starts_in_hours` | decimal | Public | starts_in_hours | Hours until event starts (negative if past) (computed) [time_relative] |
| `location` | varchar | Public |  | Physical location if applicable [location] |
| `virtual_meeting_link` | varchar | Authenticated | virtual_meeting_link | Zoom/Teams link - requires authentication [url_meeting] |
| `registration_url` | varchar | Public | registration_url | Link to register for the event [url_registration] |
| `contact` | varchar | Public | contact | Contact person or email [contact_info] |
| `speakers` | text | Public |  | Speaker names and affiliations [person_name] |
| `tags` | text | Public | tags | Parsed from comma-separated tag list (computed) [tags] |
| `affinity_group_id` | int | Public |  | Associated affinity group |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Belongs To** `affinity_groups`: Events can be associated with an affinity group
- **Has Many** `tags`: Events are tagged for discovery
- **Has Many** `event_registrations`: Registration records for this event

<h2 id="xdmod">XDMoD Metrics</h2>

*HPC metrics, usage analytics, and resource specifications from the ACCESS XDMoD instance*

**Example questions this data can answer:**

- How much CPU time was used across ACCESS last quarter?
- Which resources have the highest GPU utilization?
- How many jobs ran on Delta in January 2024?
- What science gateways are most active?
- How are allocations distributed across fields of science?
- What is the total GPU capacity across ACCESS resources?
- Show me wait times by resource for the past month
- How many active users and PIs are there?

### Realms

XDMoD organizes data into **9 realms**, each with its own dimensions and statistics.

#### Accounts

*ACCESS user account tracking — accounts associated with allocations and job activity*

**Access:** Public

**Dimensions:** `resource`, `resource_type`

| Statistic | Description |
|-----------|-------------|
| `unique_account_count` | Number of Accounts Created |
| `unique_account_with_jobs_count` | Number of Accounts Created with Jobs |

#### Allocations

*Allocation and project tracking — active allocations, PIs, and resource usage in SUs/ACEs*

**Access:** Public

**Dimensions:** `allocation`, `allocation_type`, `board_type`, `fieldofscience`, `nsfdirectorate`, `pi`, `parentscience`, `resource`, `resource_type`

| Statistic | Description |
|-----------|-------------|
| `active_allocation_count` | Number of Projects Active |
| `active_pi_count` | Number of PIs Active |
| `active_resallocation_count` | Number of Allocations Active |
| `allocated_nu` | NUs Allocated |
| `allocated_raw_su` | CPU Core Hours Allocated |
| `allocated_su` | XD SUs Allocated |
| `allocated_ace` | ACCESS Credit Equivalents Allocated (SU) |
| `rate_of_usage` | Allocation Usage Rate (XD SU/Hour) |
| `rate_of_usage_ace` | Allocation Usage Rate ACEs (SU/Hour) |
| `used_su` | XD SUs Used |
| `used_ace` | ACCESS Credit Equivalents Used (SU) |

#### Cloud

*Cloud and virtualized compute environment metrics*

**Access:** Public

**Dimensions:** `configuration`, `domain`, `instance_type`, `person`, `pi`, `project`, `provider`, `resource`, `resource_type`, `submission_venue`, `instance_state`, `institution`, `institution_country`, `institution_state`, `nsfdirectorate`, `parentscience`, `fieldofscience`, `pi_institution`, `pi_institution_country`, `pi_institution_state`, `vm_size`, `vm_size_cpu`, `vm_size_memory`

| Statistic | Description |
|-----------|-------------|
| `cloud_num_sessions_ended` | Number of Sessions Ended |
| `cloud_num_sessions_started` | Number of Sessions Started |
| `cloud_num_sessions_running` | Number of Sessions Active |
| `cloud_wall_time` | Wall Hours Total |
| `cloud_core_time` | CPU Hours Total |
| `cloud_avg_wallduration_hours` | Wall Hours Per Session |
| `cloud_avg_cores_reserved` | Average Cores Reserved Weighted By Wall Hours |
| `cloud_avg_memory_reserved` | Average Memory Reserved Weighted By Wall Hours (Bytes) |
| `cloud_avg_rv_storage_reserved` | Average Root Volume Storage Reserved (Bytes) |
| `cloud_core_utilization` | Core Hour Utilization (%) |
| `gateway_session_count` | Number of Sessions Ended via Gateway |

#### Gateways

*Science gateway job metrics — jobs submitted through ACCESS gateways*

**Access:** Public

**Dimensions:** `allocation`, `fieldofscience`, `gateway`, `gateway_user`, `grant_type`, `jobsize`, `jobwaittime`, `jobwalltime`, `nsfdirectorate`, `nodecount`, `pi`, `pi_institution`, `pi_institution_country`, `pi_institution_state`, `parentscience`, `queue`, `resource`, `resource_type`, `provider`, `person`, `institution`, `institution_country`, `institution_state`

| Statistic | Description |
|-----------|-------------|
| `job_count` | Number of Jobs Ended |
| `running_job_count` | Number of Jobs Running |
| `started_job_count` | Number of Jobs Started |
| `submitted_job_count` | Number of Jobs Submitted |
| `total_cpu_hours` | CPU Hours Total |
| `total_node_hours` | Node Hours Total |
| `total_wallduration_hours` | Wall Hours Total |
| `total_waitduration_hours` | Wait Hours Total |
| `avg_cpu_hours` | CPU Hours Per Job |
| `avg_node_hours` | Node Hours Per Job |
| `avg_wallduration_hours` | Wall Hours Per Job |
| `avg_waitduration_hours` | Wait Hours Per Job |
| `avg_processors` | Job Size Per Job (Core Count) |
| `max_processors` | Job Size Max (Core Count) |
| `min_processors` | Job Size Min (Core Count) |
| `normalized_avg_processors` | Job Size Normalized (% of Total Cores) |
| `total_su` | XD SUs Charged Total |
| `avg_su` | XD SUs Charged Per Job |
| `total_nu` | NUs Charged Total |
| `avg_nu` | NUs Charged Per Job |
| `total_ace` | ACCESS Credit Equivalents Charged Total (SU) |
| `avg_ace` | ACCESS Credit Equivalents Charged Per Job (SU) |
| `expansion_factor` | User Expansion Factor |
| `utilization` | ACCESS CPU Utilization (%) |
| `active_resource_count` | Number of Resources Active |
| `active_institution_count` | Number of Institutions Active |
| `active_gateway_count` | Number of Gateways Active |
| `active_gwuser_count` | Number of Gateway Users Active |

#### Jobs

*Job accounting and resource usage metrics from job schedulers*

**Access:** Public

**Dimensions:** `allocation`, `fieldofscience`, `grant_type`, `jobsize`, `jobwaittime`, `jobwalltime`, `nsfdirectorate`, `nodecount`, `pi`, `pi_institution`, `pi_institution_country`, `pi_institution_state`, `parentscience`, `queue`, `resource`, `resource_type`, `provider`, `person`, `institution`, `institution_country`, `institution_state`, `username`, `qos`, `application`

| Statistic | Description |
|-----------|-------------|
| `job_count` | Number of Jobs Ended |
| `running_job_count` | Number of Jobs Running |
| `started_job_count` | Number of Jobs Started |
| `submitted_job_count` | Number of Jobs Submitted |
| `total_cpu_hours` | CPU Hours Total |
| `total_node_hours` | Node Hours Total |
| `total_wallduration_hours` | Wall Hours Total |
| `total_waitduration_hours` | Wait Hours Total |
| `avg_cpu_hours` | CPU Hours Per Job |
| `avg_node_hours` | Node Hours Per Job |
| `avg_wallduration_hours` | Wall Hours Per Job |
| `avg_waitduration_hours` | Wait Hours Per Job |
| `avg_processors` | Job Size Per Job (Core Count) |
| `max_processors` | Job Size Max (Core Count) |
| `min_processors` | Job Size Min (Core Count) |
| `normalized_avg_processors` | Job Size Normalized (% of Total Cores) |
| `total_su` | XD SUs Charged Total |
| `avg_su` | XD SUs Charged Per Job |
| `total_nu` | NUs Charged Total |
| `avg_nu` | NUs Charged Per Job |
| `total_ace` | ACCESS Credit Equivalents Charged Total (SU) |
| `avg_ace` | ACCESS Credit Equivalents Charged Per Job (SU) |
| `expansion_factor` | User Expansion Factor |
| `utilization` | ACCESS CPU Utilization (%) |
| `gateway_job_count` | Number of Jobs via Gateway |
| `active_person_count` | Number of Users Active |
| `active_pi_count` | Number of PIs Active |
| `active_resource_count` | Number of Resources Active |
| `active_allocation_count` | Number of Allocations Active |
| `active_institution_count` | Number of Institutions Active |

#### Requests

*Allocation request and proposal tracking*

**Access:** Public

**Dimensions:** `fieldofscience`, `nsfdirectorate`, `parentscience`

| Statistic | Description |
|-----------|-------------|
| `request_count` | Number of Proposals |
| `project_count` | Number of Projects |

#### ResourceSpecifications

*Resource hardware specifications — CPU/GPU counts, node hours, and capacity metrics*

**Access:** Public

**Dimensions:** `resource`, `resource_institution_country`, `resource_institution_state`, `resource_type`

| Statistic | Description |
|-----------|-------------|
| `total_cpu_core_hours` | CPU Hours Total |
| `allocated_cpu_core_hours` | CPU Hours Allocated |
| `total_gpu_hours` | GPU Hours Total |
| `allocated_gpu_hours` | GPU Hours Allocated |
| `total_gpu_node_hours` | GPU Node Hours Total |
| `allocated_gpu_node_hours` | GPU Node Hours Allocated |
| `total_cpu_node_hours` | CPU Node Hours Total |
| `allocated_cpu_node_hours` | CPU Node Hours Allocated |
| `total_avg_number_of_cpu_cores` | Average Number of CPU Cores Total |
| `allocated_avg_number_of_cpu_cores` | Average Number of CPU Cores Allocated |
| `total_avg_number_of_gpus` | Average Number of GPUs Total |
| `allocated_avg_number_of_gpus` | Average Number of GPUs Allocated |
| `total_avg_number_of_cpu_nodes` | Average Number of CPU Nodes Total |
| `allocated_avg_number_of_cpu_nodes` | Average Number of CPU Nodes Allocated |
| `total_avg_number_of_gpu_nodes` | Average Number of GPU Nodes Total |
| `allocated_avg_number_of_gpu_nodes` | Average Number of GPU Nodes Allocated |
| `ace_total` | ACCESS Credit Equivalents Available Total (SU) |
| `ace_allocated` | ACCESS Credit Equivalents Available Allocated (SU) |

#### Storage

*File system and storage usage metrics*

**Access:** Public

| Statistic | Description |
|-----------|-------------|
| `user_count` | User Count |
| `avg_physical_usage` | Physical Usage (Bytes) |
| `avg_logical_usage` | Logical Usage (Bytes) |
| `avg_file_count` | File Count |
| `avg_hard_threshold` | Quota Hard Threshold (Bytes) |
| `avg_soft_threshold` | Quota Soft Threshold (Bytes) |

#### SUPREMM

*Detailed job performance analytics — CPU, GPU, memory, network, and I/O metrics from monitoring*

**Access:** Public

**Dimensions:** `resource`, `person`, `pi`, `institution`, `jobsize`, `queue`, `fieldofscience`, `nsfdirectorate`, `parentscience`, `application`, `cpi`, `cpu`, `cpucv`, `cpuuser`, `datasource`, `exit_status`, `gpu_count`, `granted_pe`, `ibrxbyterate`, `jobwalltime`, `max_mem`, `mem_used`, `nodecount`, `pi_institution`, `provider`, `resource_type`, `shared`, `username`, `institution_country`, `institution_state`

| Statistic | Description |
|-----------|-------------|
| `job_count` | Number of Jobs Ended |
| `short_job_count` | Number of Short Jobs Ended |
| `running_job_count` | Number of Jobs Running |
| `started_job_count` | Number of Jobs Started |
| `submitted_job_count` | Number of Jobs Submitted |
| `wall_time` | CPU Hours Total |
| `wall_time_per_job` | Wall Hours Per Job |
| `wait_time` | Wait Hours Total |
| `wait_time_per_job` | Wait Hours Per Job |
| `requested_wall_time` | Wall Hours Requested Total |
| `requested_wall_time_per_job` | Wall Hours Requested Per Job |
| `wall_time_accuracy` | Wall Time Accuracy (%) |
| `cpu_time_user` | CPU Hours User Total |
| `cpu_time_system` | CPU Hours System Total |
| `cpu_time_idle` | CPU Hours Idle Total |
| `avg_percent_cpu_user` | Avg CPU % User weighted by core-hour |
| `avg_percent_cpu_system` | Avg CPU % System weighted by core-hour |
| `avg_percent_cpu_idle` | Avg CPU % Idle weighted by core-hour |
| `gpu_time` | GPU Hours Total |
| `avg_percent_gpu_usage` | Avg GPU usage weighted by GPU hour (%) |
| `avg_flops_per_core` | Avg FLOPS Per Core weighted by core-hour (ops/s) |
| `avg_memory_per_core` | Avg Memory Per Core weighted by core-hour (bytes) |
| `avg_total_memory_per_core` | Avg Total Memory Per Core weighted by core-hour (bytes) |
| `avg_max_memory_per_core` | Avg Max Memory weighted by core-hour (%) |
| `avg_mem_bw_per_core` | Avg Memory Bandwidth Per Core weighted by core-hour (bytes/s) |
| `avg_ib_rx_bytes` | Avg InfiniBand rate Per Node weighted by node-hour (bytes/s) |
| `avg_homogeneity` | Avg Homogeneity weighted by node-hour (%) |
| `total_su` | XD SUs Charged Total |
| `avg_su` | XD SUs Charged Per Job |
| `total_ace` | ACCESS Credit Equivalents Charged Total (SU) |
| `avg_ace` | ACCESS Credit Equivalents Charged Per Job (SU) |
| `active_pi_count` | Number of PIs Active |
| `active_app_count` | Number of Applications Active |
