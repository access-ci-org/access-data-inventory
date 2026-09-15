---
layout: default
title: Fields
---

# Fields

Field-level documentation for all ACCESS data sources.

## Table of Contents

- [ACCESS Pegasus](#access_pegasus)
- [ACCESS RP Monthly Reports](#access_rp_monthly_reports)
- [ACCESS Reports](#access_reports)
- [ACCESS Support Drupal](#access_support_drupal)
- [ACCESS User Monthly Reports](#access_user_monthly_reports)
- [ACCESS XDMoD Data Access Endpoints](#access_xdmod_data_access_endpoints)
- [ACCESS XDMoD Data Catalog](#access_xdmod_data_catalog)
- [ACCESS XDMoD User Manual](#access_xdmod_user_manual)
- [Adoption Metrics](#adoption_metrics)
- [Affinity Groups](#affinity_groups)
- [Allocations/Projects](#allocations_projects)
- [Announcements](#announcements)
- [Annual Report Data](#annual_report_data)
- [CCEP Awards (Community Grant)](#ccep_awards_community_grant)
- [COManage/ACCESS Identity](#comanage)
- [CSSN Roles/skills/Interests](#cssn_roles_skills_interests)
- [Chatbot](#chatbot)
- [Community Surveys](#community_surveys)
- [Content API](#content_api)
- [Current Projects](#current_projects)
- [EAB Action Items](#eab_action_items)
- [EAB Registration/Attendance](#eab_registration_attendance)
- [EAB Survey](#eab_survey)
- [EAB-EC Reports](#eab_ec_reports)
- [Engagement Tracker](#engagement_tracker)
- [Eval Team Surveys](#eval_team_surveys)
- [Event Registrations](#event_registrations)
- [Events and Training](#events)
- [External Newsletter Content](#external_newsletter_content)
- [Financial Reports](#financial_reports)
- [Focus Groups (2023)](#focus_groups_2023)
- [Graphical Visualizations of data avaible in XDMoD](#graphical_visualizations_of_data_avaible_in_xdmod)
- [Internal Newsletter Content](#internal_newsletter_content)
- [Internet2 Flow Data](#internet2_flow_data)
- [MATCH Services](#match_services)
- [Meeting Notes](#meeting_notes)
- [Metrics Framework](#metrics_framework)
- [NAIRR Underutilization Surveys](#nairr_underutilization_surveys)
- [NAIRR Underutilized Allocations](#nairr_underutilized_allocations)
- [NSF Awards](#nsf_awards)
- [Nagios](#nagios)
- [NetSage](#netsage)
- [Network Traffic](#network_traffic)
- [Office Hours](#office_hours)
- [Publications](#publications)
- [Publications](#publications_allocations)
- [Publications (non-catalog) - referenced in 3](#publications_non_catalog_referenced_in_3)
- [QM Survey](#qm_survey)
- [Quality Risk Assessment](#quality_risk_assessment)
- [Qualys](#qualys)
- [Quarterly Report Data](#quarterly_report_data)
- [Quarterly/Annual Reports](#quarterly_annual_reports)
- [RAC Registration/Attendance](#rac_registration_attendance)
- [RP Integration Effort](#rp_integration_effort)
- [RP Support Effort](#rp_support_effort)
- [RP Survey](#rp_survey)
- [RP batch scheduler information (from IPF)](#rp_batch_scheduler_information_from_ipf)
- [RP software modules (from IPF)](#rp_software_modules_from_ipf)
- [Request Statistics](#request_statistics)
- [Resource Description (CIDeR)](#resource_description_cider)
- [Resource Documentation API](#resource_documentation_api)
- [Resource Integration Roadmaps and Badges](#resource_integration_roadmaps_and_badges)
- [Resource News/Outages](#resource_news_outages)
- [SC/WG Reporting Schedules](#sc_wg_reporting_schedules)
- [SDS (Software Discovery Service)](#sds_software_discovery_service)
- [STEP Application](#step_application)
- [STEP Survey](#step_survey)
- [SWG Notes](#swg_notes)
- [Service Index](#service_index)
- [Social Media Reach](#social_media_reach)
- [Staff Survey](#staff_survey)
- [Stories/Publications - referenced in 3](#stories_publications_referenced_in_3)
- [Support Digest](#support_digest)
- [System & Service Logs](#system_service_logs)
- [Ticketing (ACCESS System)](#ticketing_access_system)
- [Ticketing Statistics](#ticketing_statistics)
- [Video Tutorials](#video_tutorials)
- [Web Stats (Google Analytics)](#web_stats_google_analytics)
- [Webinar Registration (NAIRR/ACCESS)](#webinar_registration_nairr_access)
- [Website Analytics](#website_analytics)
- [Website Stats](#website_stats)
- [Workshop Surveys (CU)](#workshop_surveys_cu)
- [XDMoD Metrics](#xdmod)
- [XDMoD Open API Documentation](#xdmod_open_api_documentation)
- [ciLogon](#cilogon)
- [perfSONAR](#perfsonar)
- [xdmod-data GitHub Repository](#xdmod_data_github_repository)
- [xdmod-notebooks GitHub Repository](#xdmod_notebooks_github_repository)

<h2 id="access_pegasus">ACCESS Pegasus</h2>

*Workflow usage and execution data*

**Refresh frequency:** daily

*No fields documented.*

<h2 id="access_rp_monthly_reports">ACCESS RP Monthly Reports</h2>

*Curated report w/ analysis*

**Access mechanism:** Web

**Sensitivity:** Medium

*No fields documented.*

<h2 id="access_reports">ACCESS Reports</h2>

*Curated report w/ analysis*

**Access mechanism:** Web

**Sensitivity:** Medium

*No fields documented.*

<h2 id="access_support_drupal">ACCESS Support Drupal</h2>

*ACCESS Support website CMS - canonical storage for support content*

> **Authoritative source** for: [Announcements](#announcements), [Events and Training](#events), [Affinity Groups](#affinity_groups), [tags](#tags)

**Storage:** Drupal CMS database

**Access mechanism:** Web

**Refresh frequency:** realtime

**Query capacity:** moderate

**Sensitivity:** High

**Docs:** <https://support.access-ci.org/api-docs>

**Example questions this data can answer:**

- What content types are stored in the ACCESS Support CMS?
- When was a specific piece of content last modified?
- How many published nodes exist by content type?

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) | int | Public |  | Drupal node ID [entity_id] |
| `uuid` | varchar | Public |  | Drupal UUID [uuid] |
| `type` | varchar | Public |  | Drupal content type [entity_type] |
| `title` | varchar | Public |  | Content title [entity_name] |
| `body` | text | Public |  | Content body (HTML) [entity_description] |
| `status` | boolean | Internal Only |  | Published status [entity_status] |
| `created` | timestamp | Public |  | Content creation date [date_created] |
| `changed` | timestamp | Public |  | Last modification date [date_modified] |
| `uid` | int | Restricted |  | Author user ID |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Has Many** `announcements`: Stores announcement content
- **Has Many** `events`: Stores event content (series and instances)
- **Has Many** `affinity_groups`: Stores affinity group content
- **Has Many** `tags`: Stores taxonomy terms
- **Has Many** `users`: Stores user accounts (Drupal users, linked to COManage)

<h2 id="access_user_monthly_reports">ACCESS User Monthly Reports</h2>

*Curated report w/ analysis*

**Access mechanism:** Web

**Sensitivity:** High

*No fields documented.*

<h2 id="access_xdmod_data_access_endpoints">ACCESS XDMoD Data Access Endpoints</h2>

*Allocations Information,
Compute Usage,
HPC Job Performance & Power Data,
Science Gateway Usage,
Resource Quality of service data (via Application Kernels),
HPC Job Efficiency Analytics,
Commercial and Non-Commercial Cloud Usage,
Open OnDemand Usage*

> **Canonical source:** batch compute log file from resource provider, amie packet from resouce provider, xras data, cilogon information — this data is derived from the authoritative source(s) above.

**Storage:** XDMoD Datawarehouse

**Access mechanism:** API, Web, MCP

**Refresh frequency:** daily

**Sensitivity:** High

**Docs:** <https://open.xdmod.org/11.0/rest.html>

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `Raw Data` | JSON | Public, Authenticated |  |  |
| `Aggregate Data` | JSON | Public, Authenticated |  |  |
| `Timeseries Data` | JSON | Public, Authenticated |  |  |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="access_xdmod_data_catalog">ACCESS XDMoD Data Catalog</h2>

*List of available statistics and dimensions*

**Storage:** Metrics Website

**Access mechanism:** API, MCP, Web

**Sensitivity:** Low

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `Catalog overview` * | text | Public |  | Summary of XDMoD data catalog [entity_summary] |
| `Catalog name` * | varchar | Public |  | Name of information in data catalog [entity_name] |
| `Description` * | text | Public |  | Description of the data provided [entity_description] |
| `Realm` * | varchar | Public |  | The XDMoD realm that provides the data [entity_name] |
| `Type` * | varchar | Public |  | Is type of (Metric, Group By, Raw Data) [entity_type] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="access_xdmod_user_manual">ACCESS XDMoD User Manual</h2>

*XDMoD Web Portal Documentation*

**Storage:** XDMoD Web Portal

**Access mechanism:** MCP, Web

**Refresh frequency:** static

**Sensitivity:** Low

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `User Manual Pages` * | text | Public |  | Webpages that provide documentation on using the XDMoD portal [entity_description] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="adoption_metrics">Adoption Metrics</h2>

*Adoption tracking*

**Storage:** https://access-ci.atlassian.net/wiki/spaces/ACP/database/1648656385

**Access mechanism:** Web

**Refresh frequency:** static

**Query capacity:** limited

*No fields documented.*

<h2 id="affinity_groups">Affinity Groups</h2>

*Membership, events, announcements, KB resources*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source(s) above.

**Access mechanism:** API, MCP, Web

**Refresh frequency:** real-time

**Query capacity:** high

**Sensitivity:** Medium

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

<h2 id="allocations_projects">Allocations/Projects</h2>

*Active projects; Resource allocations; PI info; Detailed Project info*

**Storage:** Data gathered from XRAS Databases

**Access mechanism:** API, Web

**Refresh frequency:** real-time

**Query capacity:** high

**Sensitivity:** High

**Docs:** <https://api.xras.org/>

*No fields documented.*

<h2 id="announcements">Announcements</h2>

*RP and community announcements*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source(s) above.

**Access mechanism:** API, MCP, Web

**Refresh frequency:** real-time

**Query capacity:** high

**Sensitivity:** Low

**Docs:** <https://support.access-ci.org/api-docs/announcements>

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

<h2 id="annual_report_data">Annual Report Data</h2>

*Users; Institutions; Academic status; Allocation counts; Projects; Usage; Documents; Abstracts; FOS; Publications; RPs utilized*

**Storage:** Data gathered from XRAS Databases

**Access mechanism:** Web

**Refresh frequency:** annually

**Query capacity:** unknown

**Sensitivity:** N/A

*No fields documented.*

<h2 id="ccep_awards_community_grant">CCEP Awards (Community Grant)</h2>

*Applicants; Institution; Amount awarded; Fund usage*

**Refresh frequency:** static

*No fields documented.*

<h2 id="comanage">COManage/ACCESS Identity</h2>

*Identity information; Teragrid.org identities*

> **Canonical source:** database — this data is derived from the authoritative source(s) above.

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

<h2 id="cssn_roles_skills_interests">CSSN Roles/skills/Interests</h2>

*Taxonomy for skills/interests and roles in the community*

**Access mechanism:** Web

**Refresh frequency:** real-time

**Query capacity:** high

*No fields documented.*

<h2 id="chatbot">Chatbot</h2>

*Questions; Answers; Ratings*

**Refresh frequency:** daily

*No fields documented.*

<h2 id="community_surveys">Community Surveys</h2>

*Community feedback; Section/group info*

> **Canonical source:** google drive — this data is derived from the authoritative source(s) above.

**Storage:** Eval SC Folder

**Refresh frequency:** annually

**Query capacity:** limited

*No fields documented.*

<h2 id="content_api">Content API</h2>

*Plain-text page content and a discovery index for ACCESS Support pages, for RAG ingestion and search syndication.*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source(s) above.

**Storage:** support.access-ci.org

**Access mechanism:** API, Web

**Refresh frequency:** Real-time

**Query capacity:** high

**Sensitivity:** Low

**Docs:** <https://support.access-ci.org/api-docs/content>

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `id` * | int | Public |  | Drupal node ID of the page. [entity_id] (source: ACCESS Support Drupal) |
| `title` * | varchar | Public |  | Page title. [entity_name] (source: ACCESS Support Drupal) |
| `path` | varchar | Public |  | Absolute URL of the support page. [url_external] (source: ACCESS Support Drupal) |
| `content_type` | varchar | Public |  | Drupal content type of the page. [entity_type] (source: ACCESS Support Drupal) |
| `text` | text | Public |  | Full extracted plain text of the page (detail endpoint). (computed) [entity_description] (source: ACCESS Support Drupal) |
| `content_hash` | varchar | Public |  | SHA-256 hash of the extracted text for incremental ingestion. (computed) (source: ACCESS Support Drupal) |
| `last_modified` | timestamp | Public |  | ISO 8601 last-changed time. [date_modified] (source: ACCESS Support Drupal) |
| `content_url` | varchar | Public |  | URL of the per-page content endpoint (index entries). [url_external] (source: ACCESS Support Drupal) |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="current_projects">Current Projects</h2>

*Active Projects; Resource Allocations; PI Info*

**Storage:** Data gathered from XRAS Databases

**Access mechanism:** API, Web

**Refresh frequency:** real-time

**Query capacity:** high

**Sensitivity:** N/A

*No fields documented.*

<h2 id="eab_action_items">EAB Action Items</h2>

*Action items accepted by the EC - tracking and implementation*

> **Canonical source:** google sheets — this data is derived from the authoritative source(s) above.

**Storage:** https://docs.google.com/spreadsheets/d/1CtAMssCnj8RNfWk7M7K4RvZG-rBdNJsuFseFVQWuP5s/edit?gid=0#gid=0

**Access mechanism:** Web

**Refresh frequency:** weekly

**Query capacity:** limited

*No fields documented.*

<h2 id="eab_registration_attendance">EAB Registration/Attendance</h2>

*Registrations; Attendance; Ideas generated*

> **Canonical source:** ideas generated google sheets — this data is derived from the authoritative source(s) above.

**Storage:** EAB Wiki: attendance tracked in each meeting page

**Access mechanism:** Unknown

**Refresh frequency:** quarterly

**Query capacity:** moderate

*No fields documented.*

<h2 id="eab_survey">EAB Survey</h2>

*Survey responses*

> **Canonical source:** google drive — this data is derived from the authoritative source(s) above.

**Storage:** EAB Meeting Folder

**Access mechanism:** Web

**Refresh frequency:** quarterly

**Query capacity:** limited

*No fields documented.*

<h2 id="eab_ec_reports">EAB-EC Reports</h2>

*EAB recommendations to EC and responses*

> **Canonical source:** google sheets — this data is derived from the authoritative source(s) above.

**Storage:** EAB Meeting Folder

**Access mechanism:** Web

**Refresh frequency:** quarterly

**Query capacity:** moderate

*No fields documented.*

<h2 id="engagement_tracker">Engagement Tracker</h2>

*Engagement metrics - tracking how many conferences and meetings ACO, EC go to and engage with users*

> **Canonical source:** google sheets — this data is derived from the authoritative source(s) above.

**Storage:** https://docs.google.com/spreadsheets/d/1_EXKUOXmY-TVkDWaHR1-SuiKt404uGEnGSr6uQCkwzw/edit?gid=0#gid=0

**Access mechanism:** Web

**Refresh frequency:** real-time

**Query capacity:** high

*No fields documented.*

<h2 id="eval_team_surveys">Eval Team Surveys</h2>

*Community; Staff; RP survey data*

*No fields documented.*

<h2 id="event_registrations">Event Registrations</h2>

*Registration and attendance data for events*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source(s) above.

**Storage:** ACCESS Support Drupal

**Access mechanism:** Web

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

**Storage:** ACCESS Support Drupal

**Access mechanism:** API, MCP

**Refresh frequency:** realtime

**Query capacity:** high

**Sensitivity:** Low

**Docs:** <https://support.access-ci.org/api-docs/events>

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
| `tags` | text | Public | tags | Discovery tags [tags] |
| `affinity_group_id` | int | Public |  | Associated affinity group |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Belongs To** `affinity_groups`: Events can be associated with an affinity group
- **Has Many** `tags`: Events are tagged for discovery
- **Has Many** `event_registrations`: Registration records for this event

<h2 id="external_newsletter_content">External Newsletter Content</h2>

*Science content (stories),  what are RPs doing with ACCESS, what are users doing with ACCESS, articles and awards, what is going on with ACCESS, publications*

> **Canonical source:** monthly solicitation to working groups, standing committees, comms team and resource providers — this data is derived from the authoritative source(s) above.

**Storage:** These are all now on the wiki at: https://access-ci.atlassian.net/wiki/spaces/ACP/pages/104891248/ACCESS+Newsletter+Archive; also on access-ci.org/news

**Access mechanism:** Web

**Refresh frequency:** monthly

**Query capacity:** moderate

*No fields documented.*

<h2 id="financial_reports">Financial Reports</h2>

*Finances for ACO, EC, EAB, and SDSC*

> **Canonical source:** banner, google drive — this data is derived from the authoritative source(s) above.

**Storage:** Banner, Google Drive: https://drive.google.com/drive/u/0/folders/19u_GRcsIexcMujOJ1ckxxni-irxDK4sY?ths=true

**Access mechanism:** Web

**Refresh frequency:** monthly

**Query capacity:** limited

*No fields documented.*

<h2 id="focus_groups_2023">Focus Groups (2023)</h2>

*User experience feedback; Website review findings*

**Refresh frequency:** annually

*No fields documented.*

<h2 id="graphical_visualizations_of_data_avaible_in_xdmod">Graphical Visualizations of data avaible in XDMoD</h2>

*Chart Configurations, List of available visualizations*

**Access mechanism:** API, MCP, Web

**Refresh frequency:** daily

**Sensitivity:** High

*No fields documented.*

<h2 id="internal_newsletter_content">Internal Newsletter Content</h2>

*Staff-focused information*

> **Canonical source:** monthly solicitation to working groups, standing committees, comms team and resource providers — this data is derived from the authoritative source(s) above.

**Storage:** These are all now on the wiki at: https://access-ci.atlassian.net/wiki/spaces/ACP/pages/104891248/ACCESS+Newsletter+Archive

**Access mechanism:** Web

**Refresh frequency:** monthly

**Query capacity:** moderate

*No fields documented.*

<h2 id="internet2_flow_data">Internet2 Flow Data</h2>

*Network flow data*

*No fields documented.*

<h2 id="match_services">MATCH Services</h2>

*Service requests and requestors*

**Refresh frequency:** monthly

*No fields documented.*

<h2 id="meeting_notes">Meeting Notes</h2>

*Notes; Attendance, decisions*

> **Canonical source:** confluence — this data is derived from the authoritative source(s) above.

**Storage:** Confluence: https://access-ci.atlassian.net/wiki/spaces/ACP/pages/479199256/ACO+Easy+Access+Page

**Access mechanism:** Web

**Refresh frequency:** weekly

**Query capacity:** high

*No fields documented.*

<h2 id="metrics_framework">Metrics Framework</h2>

*KPIs; Democratization Index; Ecosystem access time; RP Satisfaction; XRAS uptime; Feedback responsiveness; Ticket resolution; Staff satisfaction*

**Access mechanism:** Web

**Query capacity:** unknown

*No fields documented.*

<h2 id="nairr_underutilization_surveys">NAIRR Underutilization Surveys</h2>

*Resource; Reason for underutilization; Support needs*

**Refresh frequency:** annually

*No fields documented.*

<h2 id="nairr_underutilized_allocations">NAIRR Underutilized Allocations</h2>

*1:1 meeting notes; Resource; Reasons; Support needs*

**Refresh frequency:** annually

*No fields documented.*

<h2 id="nsf_awards">NSF Awards</h2>

*NSF funding data; Award details*

*No fields documented.*

<h2 id="nagios">Nagios</h2>

*Monitoring data*

*No fields documented.*

<h2 id="netsage">NetSage</h2>

*Network Usage data*

**Sensitivity:** Medium

*No fields documented.*

<h2 id="network_traffic">Network Traffic</h2>

*Historical traffic volumes*

*No fields documented.*

<h2 id="office_hours">Office Hours</h2>

*Attendees; Concerns raised*

**Refresh frequency:** weekly

*No fields documented.*

<h2 id="publications">Publications</h2>

*List of published papers and presentations*

**Access mechanism:** Web

**Refresh frequency:** static

**Sensitivity:** Low

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `XDMoD Citation Reference` * | text | Public |  | Citation to use when referencing XDMoD [entity_name] |
| `Year` * | int | Public |  | Year of publications [date_published] |
| `Publication Reference` * | text | Public |  | Publication citation [entity_name] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="publications_allocations">Publications</h2>

*List of publications by ACCESS researchers*

**Storage:** Data gathered from XRAS Databases

**Access mechanism:** API, Web

**Refresh frequency:** real-time

**Query capacity:** high

**Sensitivity:** N/A

*No fields documented.*

<h2 id="publications_non_catalog_referenced_in_3">Publications (non-catalog) - referenced in 3</h2>

*Publications not in main pub list*

**Access mechanism:** Unknown

*No fields documented.*

<h2 id="qm_survey">QM Survey</h2>

*Quarterly meeting survey*

> **Canonical source:** google drive — this data is derived from the authoritative source(s) above.

**Storage:** Quarterly Meeting Folder

**Refresh frequency:** quarterly

**Query capacity:** limited

*No fields documented.*

<h2 id="quality_risk_assessment">Quality Risk Assessment</h2>

*Quality/risk assessment*

> **Canonical source:** jira https access ci atlassian net jira core projects att list jql project 20 3d 20att 20and 20status 20 3d 20 22done 2fcomplete 22 20order 20by 20assignee 20asc 2c 20cf 5b10019 5d 20asc — this data is derived from the authoritative source(s) above.

**Storage:** JIRA:https://access-ci.atlassian.net/jira/core/projects/ATT/list?jql=project%20%3D%20ATT%20AND%20status%20!%3D%20%22Done%2FComplete%22%20ORDER%20BY%20assignee%20ASC%2C%20cf%5B10019%5D%20ASC

**Access mechanism:** API, Unknown

**Refresh frequency:** quarterly

**Query capacity:** high

*No fields documented.*

<h2 id="qualys">Qualys</h2>

*Host vulnerability data*

*No fields documented.*

<h2 id="quarterly_report_data">Quarterly Report Data</h2>

*Publications; New publications; Turnaround time; EC decisions; Lessons learned, metrics, risks, task tracking, financials, outreach,*

> **Canonical source:** ga4, constant contact, hootsuite, jira, confluence, google drive — this data is derived from the authoritative source(s) above.

**Storage:** Links are in the reports themselves - data is stored in locations listed above

**Access mechanism:** Web

**Refresh frequency:** quarterly

**Query capacity:** high

*No fields documented.*

<h2 id="quarterly_annual_reports">Quarterly/Annual Reports</h2>

*Reports to NSF*

> **Canonical source:** google drive, confluence — this data is derived from the authoritative source(s) above.

**Storage:** Google Drive: https://drive.google.com/drive/u/0/folders/1NNImO8UjJWM59V3g2SdZTD2shGJjYiP5?ths=true

**Access mechanism:** Web

**Refresh frequency:** quarterly

**Query capacity:** moderate

*No fields documented.*

<h2 id="rac_registration_attendance">RAC Registration/Attendance</h2>

*Registrations; Attendance*

**Storage:** RAC Wiki: attedance tracked in each meeting

**Access mechanism:** Unknown

*No fields documented.*

<h2 id="rp_integration_effort">RP Integration Effort</h2>

*Time/effort for new RP integration*

*No fields documented.*

<h2 id="rp_support_effort">RP Support Effort</h2>

*Time/effort for ongoing RP support*

*No fields documented.*

<h2 id="rp_survey">RP Survey</h2>

*Resource provider feedback*

> **Canonical source:** google drive — this data is derived from the authoritative source(s) above.

**Storage:** Eval SC Folder

**Refresh frequency:** annually

**Query capacity:** limited

*No fields documented.*

<h2 id="rp_batch_scheduler_information_from_ipf">RP batch scheduler information (from IPF)</h2>

*Scheduler queue configuration but not queue contents or reservations*

**Access mechanism:** API, Web

*No fields documented.*

<h2 id="rp_software_modules_from_ipf">RP software modules (from IPF)</h2>

*Software catalog from resources*

**Access mechanism:** API, Web

*No fields documented.*

<h2 id="request_statistics">Request Statistics</h2>

*Request counts; Response times; Approval/decline rates*

**Storage:** Data gathered from XRAS Databases

**Access mechanism:** API, Web

**Refresh frequency:** real-time

**Query capacity:** moderate

**Sensitivity:** High

*No fields documented.*

<h2 id="resource_description_cider">Resource Description (CIDeR)</h2>

*Organizations, resource descriptions, and integration information for ACCESS resource providers.*

**Storage:** operations.access-ci.org

**Access mechanism:** API, Web

**Refresh frequency:** Daily

**Query capacity:** high

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `cider_resource_id` * | int | Public |  | CiDeR primary key |
| `info_resource_id` * | varchar | Public |  | Global human meaningful resource ID — Used across all Operations information repositories to identify a resource |
| `info_site_id` * | varchar | Public |  | Global human meaningful site ID — Used across all Operations information repositories to identify a site |
| `cider_type` * | varchar | Public |  | Compute, Storage, Gateway, Network, etc. |
| `organization_name` * | varchar | Public |  |  |
| `organization_url` * | varchar | Public |  |  |
| `organization_logo_url` * | varchar | Public |  |  |
| `groups` * | int | Public |  | list of resource groups this resource belongs to |
| `resource_descriptive_name` * | varchar | Public |  | Descriptive resource name |
| `resource_description` * | varchar | Public |  | Full resource description |
| `project_affiliation` * | varchar | Public |  | Resource affliation: ACCESS, NAIRR, etc. |
| `latest_status` * | varchar | Public |  | Coming soon, pre-production, production, post-production, or retired status |
| `latest_status_start` * | date | Public |  | What latest status starts |
| `latest_status_end` * | date | Public |  | What latest status ends |
| `resource_status` * | JSON | Public |  | Historical statuses with corresponding start and end dates |
| `compute.recommended_use` * | varchar | Public |  |  |
| `compute.access_description` * | varchar | Public |  |  |
| `compute.use_guide_url` * | varchar | Public |  |  |
| `compute.cpu_type` * | varchar | Public |  |  |
| `compute.operating_system` * | varchar | Public |  |  |
| `compute.gpu_description` * | varchar | Public |  |  |
| `compute.recommended_use` * | varchar | Public |  |  |
| `compute.job_manager` * | varchar | Public |  |  |
| `compute.batch_system` * | varchar | Public |  |  |
| `compute.interconnect` * | varchar | Public |  |  |
| `compute.storage_network` * | varchar | Public |  |  |
| `compute.machine_type` * | varchar | Public |  |  |
| `compute.cpu_speed_ghz` * | int | Public |  |  |
| `compute.platform_name` * | varchar | Public |  |  |
| `compute.memory_per_cpu_gb` * | int | Public |  |  |
| `compute.cpu_count_per_node` * | int | Public |  |  |
| `compute.xsedenet_participation` * | varchar | Public |  |  |
| `compute.node_count` * | int | Public |  |  |
| `compute.supports_sensitive_data` * | varchar | Public |  |  |
| `compute.sensitive_data_support_description` * | varchar | Public |  |  |
| `compute.local_storage_per_node_gb` * | int | Public |  |  |
| `storage.<multiple_attributes>` * | int | Public |  |  |
| `gateway.<multiple_attributes>` |  |  |  |  |
| `features` * | JSON | Public |  | Contains feature id, name, description, category_types, and feature_category |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="resource_documentation_api">Resource Documentation API</h2>

*Team-authored documentation for ACCESS resource providers (login, file transfer, storage, queue specs, top software, datasets), with resource-group inheritance.*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal), [Resource Description (CIDeR)](#resource_description_cider) — this data is derived from the authoritative source(s) above.

**Storage:** support.access-ci.org

**Access mechanism:** API, Web

**Refresh frequency:** Real-time

**Query capacity:** high

**Sensitivity:** Low

**Docs:** <https://support.access-ci.org/api-docs/resources>

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` * | int | Public |  | Drupal node ID of the resource. [entity_id] (source: ACCESS Support Drupal) |
| `title` * | varchar | Public |  | Resource title. [entity_name] (source: ACCESS Support Drupal) |
| `short_name` | varchar | Public |  | Short display name. [entity_name] (source: ACCESS Support Drupal) |
| `resource_id` * | varchar | Public |  | CIDER resource identifier. [entity_id] (source: ACCESS Support Drupal) |
| `global_resource_id` | varchar | Public |  | ACCESS global resource ID. [entity_id] (source: ACCESS Support Drupal) |
| `org_name` | varchar | Public |  | Organization that operates the resource. [institution] (source: ACCESS Support Drupal) |
| `resource_type` | varchar | Public |  | Resource type (Compute, Storage, Cloud, etc.). [entity_type] (source: ACCESS Support Drupal) |
| `description` | text | Public |  | Team-authored resource description (detail endpoint). [entity_description] (source: ACCESS Support Drupal) |
| `last_modified` | timestamp | Public |  | ISO 8601 last-changed time. [date_modified] (source: ACCESS Support Drupal) |
| `content_hash` | varchar | Public |  | Deterministic SHA-256 fingerprint of the resource payload (detail endpoint) for change detection. (computed) (source: ACCESS Support Drupal) |
| `url` | varchar | Public |  | Canonical URL of the resource documentation page. [url_external] (source: ACCESS Support Drupal) |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="resource_integration_roadmaps_and_badges">Resource Integration Roadmaps and Badges</h2>

*Integration status, badges supported*

**Access mechanism:** API, Web

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `Roadmap.badge_id` | int | Public |  |  |
| `Roadmap.name` | varchar | Public |  |  |
| `Roadmap.graphic` | image | Public |  |  |
| `Roadmap.executive_summary` | text | Public |  | For RP leadership |
| `Roadmap.infrastructure_types` | varchar | Public |  | Types of infrastructure that can use this roadmap |
| `Roadmap.integration_coordinators` | varchar | Public |  | Coordinators |
| `Roadmap.status` | varchar | Public |  | Draft or Production |
| `Badge.badge_id` | int | Public |  |  |
| `Badge.name` | varchar | Public |  |  |
| `Badge.graphic` | image | Public |  |  |
| `Badge.researcher_summary` | text | Public |  | For researching using the badges |
| `Badge.resource_provider_summary` | text | Public |  | Summary of what RPs provide and necessary support work |
| `Badge.verfication_summary` | text | Public |  | How is the badge verified |
| `Badge.verification_method` | varchar | Public |  | Manaul or Automated |
| `Badge.default_badge_access_url` | varchar | Public |  | URL for accessing this badge if the RP doesn't provide one |
| `Badge.default_badge_access_url_label` | varchar | Public |  | URL link label |
| `Task.task_id` | int | Public |  |  |
| `Task.name` | varchar | Public |  |  |
| `Task.technical_summary` | text | Public |  | Summary of what the RPs must do |
| `Task.implementor_roles` | varchar | Public |  | RP roles involved in implementation work |
| `Task.task_experts` | varchar | Public |  | Who can help with task |
| `Task.detailed_instructions_url` | varchar | Public |  | URL to task instructions |
| `Badge_Prerequisite_Badge.badge` | varchar | Public |  |  |
| `Badge_Prerequisite_Badge.prerequisite_badge` | varchar | Public |  |  |
| `Badge_Prerequisite_Badge.sequence_no` | int | Public |  | For ordering pre-requisites |
| `Roadmap_Badge.roadmap` | varchar | Public |  |  |
| `Roadmap_Badge.badge` | varchar | Public |  |  |
| `Roadmap_Badge.sequence_no` | int | Public |  | For ordering badges |
| `Roadmap_Badge.required` | boolean | Public |  | Is the badge required in this roadmap |
| `Badge_Task.badge` | varchar | Public |  |  |
| `Badge_Task.task` | varchar | Public |  |  |
| `Badge_Task.sequence_no` | int | Public |  | For ordering tasks |
| `Badge_Task.required` | boolean | Public |  | Is the task required in this badge |
| `Resource_Roadmap.info_resourceid` | varchar | Public |  | Which resource |
| `Resource_Roadmap.roadmap` | varchar | Public |  |  |
| `Resource_Badge.info_resourceid` | varchar | Public |  | Which resource |
| `Resource_Badge.roadmap` | varchar | Public |  |  |
| `Resource_Badge.badge` | varchar | Public |  |  |
| `Resource_Badge.badge_access_url` | varchar | Public |  | URL for accessing this badge for a resource |
| `Resource_Badge_Worflow` |  | Public |  | tracks resource-roadmap-badge status |
| `Resource_Badge_Task_Workflow` |  | Public |  | tracks resource-roadmap-badge-task status |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="resource_news_outages">Resource News/Outages</h2>

*Outages; Maintenance; Announcements*

**Access mechanism:** API, Web

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `News.Content` | text | Public |  |  |
| `News.Start` | timestamp | Public |  |  |
| `News.End` | timestamp | Public |  |  |
| `News.Type` | varchar | Public |  |  |
| `News.DistributionOptions` | varchar | Public |  |  |
| `News.WebURL` | varchar | Public |  |  |
| `News.Affiliation` | varchar | Public |  |  |
| `News.Publisher` | varchar | Public |  |  |
| `News_Associations` | varchar | Public |  | Associates news to infrastructure elements |
| `News_Publisher.OrganizationID` | varchar | Public |  |  |
| `News_Publisher.OrganizationName` | varchar | Public |  |  |
| `News_Publisher.NewsURNPrefix` | varchar | Public |  |  |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="sc_wg_reporting_schedules">SC/WG Reporting Schedules</h2>

*SC/WG interaction schedule with the EC*

> **Canonical source:** raci in confluence, google doc — this data is derived from the authoritative source(s) above.

**Storage:** Confluence: https://access-ci.atlassian.net/wiki/spaces/ACP/pages/2024767490/ACCESS+Standing+Committee+RACI+Documents Google: https://drive.google.com/drive/u/0/folders/1O_TKTQtvBXL_8wbPdsDmBX4HoXKhPGDU?ths=true

**Access mechanism:** Web

**Refresh frequency:** weekly

**Query capacity:** limited

*No fields documented.*

<h2 id="sds_software_discovery_service">SDS (Software Discovery Service)</h2>

*Software discovery: which software packages are available on which ACCESS resource providers.*

> **Canonical source:** [Resource Description (CIDeR)](#resource_description_cider) — this data is derived from the authoritative source(s) above.

**Storage:** sds-ara-api.access-ci.org

**Access mechanism:** API, MCP, Web

**Refresh frequency:** Daily

**Query capacity:** high

**Sensitivity:** Low

**Docs:** <https://support.access-ci.org/api-docs/sds>

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `rps` | json | Restricted (API key required) |  | Request param: array of Resource Provider names/IDs to filter by, case-insensitive. Conditional (rps and/or software). (source: SDS) — Request body field |
| `software` | json | Restricted (API key required) |  | Request param: array of software names to filter by, case-insensitive. Conditional (rps and/or software). [entity_name] (source: SDS) — Request body field |
| `columns` | json | Restricted (API key required) |  | Request param: array of fields to return. rp_software and software_name are always included. (source: SDS) — Request body field |
| `exclude` | boolean | Restricted (API key required) |  | Request param: when true, treat columns as an exclude list rather than an include list. Default false. (source: SDS) — Request body field |
| `fuzz_software` | boolean | Restricted (API key required) |  | Request param: enable fuzzy matching on software names. Default false. (source: SDS) — Request body field |
| `fuzz_rp` | boolean | Restricted (API key required) |  | Request param: enable fuzzy matching on RP names/IDs. Default false. (source: SDS) — Request body field |
| `collapse_resource_groups` | boolean | Restricted (API key required) |  | Request param: when false, emit separate entries per resource group. Default true. (source: SDS) — Request body field |
| `software_name` * | varchar | Restricted (API key required) |  | Response field: name of the software package. Results are sorted alphabetically by this field. [entity_name] (source: SDS) — Always present in responses |
| `rp_software` * | varchar | Restricted (API key required) |  | Response field: the software identifier as known to the resource provider. Always present in responses. (source: SDS) — Always present in responses |
| `resource_provider` | varchar | Restricted (API key required) |  | Response field: resource provider / resource group the software is available on. [institution] (source: SDS) — Response field |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="step_application">STEP Application</h2>

*Institution demographics*

*No fields documented.*

<h2 id="step_survey">STEP Survey</h2>

*Survey responses*

*No fields documented.*

<h2 id="swg_notes">SWG Notes</h2>

*Strategic working group notes*

> **Canonical source:** confluence — this data is derived from the authoritative source(s) above.

**Storage:** Confluence: https://access-ci.atlassian.net/wiki/spaces/ACP/pages/18055209/ACCESS+Working+Groups+and+Standing+Committees

**Access mechanism:** Web

**Refresh frequency:** weekly

**Query capacity:** high

*No fields documented.*

<h2 id="service_index">Service Index</h2>

*Service catalog and status*

> **Canonical source:** database — this data is derived from the authoritative source(s) above.

**Access mechanism:** API

*No fields documented.*

<h2 id="social_media_reach">Social Media Reach</h2>

*Engagement metrics*

> **Canonical source:** hootsuite — this data is derived from the authoritative source(s) above.

**Storage:** Is Dina the only one who can log into hootsuite for data?

**Access mechanism:** Web

**Refresh frequency:** real-time

**Query capacity:** high

*No fields documented.*

<h2 id="staff_survey">Staff Survey</h2>

*Staff feedback*

> **Canonical source:** google drive — this data is derived from the authoritative source(s) above.

**Storage:** Eval SC Folder

**Refresh frequency:** annually

**Query capacity:** limited

*No fields documented.*

<h2 id="stories_publications_referenced_in_3">Stories/Publications - referenced in 3</h2>

*HPC Wire articles; Awards; science stories*

> **Canonical source:** submissions from researchers or comms other institutions publication searches using allocations data — this data is derived from the authoritative source(s) above.

**Storage:** Website: https://access-ci.org/news/

**Access mechanism:** Web

**Refresh frequency:** real-time

**Query capacity:** high

*No fields documented.*

<h2 id="support_digest">Support Digest</h2>

*Link clicks; Open rates*

**Refresh frequency:** weekly

*No fields documented.*

<h2 id="system_service_logs">System & Service Logs</h2>

*Security logs; Monitoring data*

*No fields documented.*

<h2 id="ticketing_access_system">Ticketing (ACCESS System)</h2>

*Full ticket data; Tags; Resolution data*

*No fields documented.*

<h2 id="ticketing_statistics">Ticketing Statistics</h2>

*Time to resolution; Tags*

*No fields documented.*

<h2 id="video_tutorials">Video Tutorials</h2>

*Playlist(s) of tutorial videos*

**Storage:** XDMoD Youtube Channel

**Access mechanism:** Web

**Refresh frequency:** static

**Sensitivity:** Low

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `Use Case Playlist` * | text | Public |  | Playlist(s) that showcase different use cases of XDMoD [media_ref] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="web_stats_google_analytics">Web Stats (Google Analytics)</h2>

*Page hits and visits*

*No fields documented.*

<h2 id="webinar_registration_nairr_access">Webinar Registration (NAIRR/ACCESS)</h2>

*Names; Institutions; ACCESS ID; Email; Referral source*

**Access mechanism:** Web, API

**Refresh frequency:** real-time

**Query capacity:** high

*No fields documented.*

<h2 id="website_analytics">Website Analytics</h2>

*Institution; Login status; Carnegie classification; Geography; Session clicks; Referrers*

**Refresh frequency:** real-time

**Query capacity:** high

*No fields documented.*

<h2 id="website_stats">Website Stats</h2>

*Visits; Click-through rates*

> **Canonical source:** google analytics 4 — this data is derived from the authoritative source(s) above.

**Storage:** Google Drive: ACCESS Comms/web Metrics

**Access mechanism:** Web

**Refresh frequency:** real-time

**Query capacity:** high

*No fields documented.*

<h2 id="workshop_surveys_cu">Workshop Surveys (CU)</h2>

*Pre/post surveys; Institution; Motivation; Experience feedback*

**Refresh frequency:** quarterly

*No fields documented.*

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

<h2 id="xdmod_open_api_documentation">XDMoD Open API Documentation</h2>

*Descriptions of XDMoD Open API endpoints*

**Access mechanism:** Web

**Refresh frequency:** static

**Sensitivity:** Low

**Docs:** <https://open.xdmod.org/11.0/rest.html>

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `Endpoint Name` * | varchar | Public |  | XDMoD REST API Endpoint Name [entity_name] |
| `Endpoint Description` | text | Public |  | Purpose of endpoint [entity_summary] |
| `Authorizations` * | varchar | Public |  | Supported authentication methods [entity_type] |
| `Request Body Schema` | varchar | Public |  | Schema type [entity_type] |
| `Path Parameters` | text | Public |  | Path parameters and their descriptions [entity_description] |
| `Request Parameters` | text | Public |  | Query parameters and their descriptions [entity_description] |
| `Endpoint Responses` * | text | Public |  | Possible request responses [entity_description] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="cilogon">ciLogon</h2>

*Authentication logs*

*No fields documented.*

<h2 id="perfsonar">perfSONAR</h2>

*Network performance logs*

*No fields documented.*

<h2 id="xdmod_data_github_repository">xdmod-data GitHub Repository</h2>

*Documentation for the XDMoD Python/R APIs*

**Storage:** Github

**Access mechanism:** Web

**Refresh frequency:** static

**Sensitivity:** Low

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `Source Code` * | text | Public |  | Source code for Data Analytics Framework [entity_description] |
| `Python Package Information` * | text | Public |  | PyPI package information [entity_summary] |
| `API Token Instructions` * | text | Public |  | API Token generation instructions [entity_description] |
| `Support & Feedback Information` * | text | Public |  |  [contact_info] |
| `Licence Information` * | text | Public |  |  [entity_type] |
| `Reference Citation` * | text | Public |  |  [entity_name] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

<h2 id="xdmod_notebooks_github_repository">xdmod-notebooks GitHub Repository</h2>

*Jupyter notebook training materials and examples*

**Storage:** Github

**Access mechanism:** Web

**Refresh frequency:** static

**Sensitivity:** Low

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `Jupyter Notebooks` * | text | Public |  | Tutorial Jupyter notebooks showcasing the XDMoD Data Analytics Framework [entity_description] |
| `Notebook build instructions` * | text | Public |  | Instructions for building and running the notebooks [entity_summary] |

*PK = Primary Key, * = Required, [type] = Semantic Type*
