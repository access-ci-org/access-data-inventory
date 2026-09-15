---
layout: default
title: Data Inventory
---

# Data Inventory

{: .intro}
Unified documentation for ACCESS data sources, APIs, and MCP tools.

## Goals

The ACCESS ecosystem spans dozens of data sources across multiple teams and tracks. This project exists to bring clarity and structure to that landscape so teams can work with data more effectively.

- **Catalog every ACCESS data source** in a single, version-controlled inventory
- **Document fields, relationships, and access levels** so consumers know what's available and how to use it
- **Enable discovery across tracks** by generating browsable docs and interactive diagrams
- **Power AI tools and automation** by providing machine-readable metadata that integrates with MCP servers, agents, and other workflows

## Documentation Hubs

Front doors to the APIs and MCP servers catalogued below. Individual sources link to their own endpoint and MCP server in the table; these are the catalogs that list them all:

- **[ACCESS Support API docs](https://support.access-ci.org/api-docs)** — interactive Swagger documentation for the Support-track REST APIs (events, announcements, affinity groups, resource documentation, content, and more).
- **[ACCESS MCP servers](https://mcp.access-ci.org/docs/)** — the catalog of MCP servers that expose ACCESS data to AI tools and agents.

_Other teams' API-docs hubs can be added here as they come online._

## Data Sources

### ACO

| Source | Description | Access | |
|--------|-------------|--------|---|
| [Adoption Metrics](field-dictionary#adoption_metrics) | Adoption tracking | Internal Only |  |
| [Community Surveys](field-dictionary#community_surveys) | Community feedback; Section/group info *(sourced from google drive)* | Restricted |  |
| [EAB Action Items](field-dictionary#eab_action_items) | Action items accepted by the EC - tracking and implementation *(sourced from google sheets)* | Internal Only |  |
| [EAB Registration/Attendance](field-dictionary#eab_registration_attendance) | Registrations; Attendance; Ideas generated *(sourced from ideas generated google sheets)* | Restricted |  |
| [EAB Survey](field-dictionary#eab_survey) | Survey responses *(sourced from google drive)* | Restricted |  |
| [EAB-EC Reports](field-dictionary#eab_ec_reports) | EAB recommendations to EC and responses *(sourced from google sheets)* | Internal Only |  |
| [Engagement Tracker](field-dictionary#engagement_tracker) | Engagement metrics - tracking how many conferences and meetings ACO, EC go to and engage with users *(sourced from google sheets)* | Internal Only |  |
| [External Newsletter Content](field-dictionary#external_newsletter_content) | Science content (stories),  what are RPs doing with ACCESS, what are users doing with ACCESS, articles and awards, what is going on with ACCESS, publications *(sourced from monthly solicitation to working groups, standing committees, comms team and resource providers)* | Public |  |
| [Financial Reports](field-dictionary#financial_reports) | Finances for ACO, EC, EAB, and SDSC *(sourced from banner, google drive)* | Internal Only |  |
| [Internal Newsletter Content](field-dictionary#internal_newsletter_content) | Staff-focused information *(sourced from monthly solicitation to working groups, standing committees, comms team and resource providers)* | Internal Only |  |
| [Meeting Notes](field-dictionary#meeting_notes) | Notes; Attendance, decisions *(sourced from confluence)* | Internal Only |  |
| [Publications (non-catalog) - referenced in 3](field-dictionary#publications_non_catalog_referenced_in_3) | Publications not in main pub list | Public |  |
| [QM Survey](field-dictionary#qm_survey) | Quarterly meeting survey *(sourced from google drive)* | Restricted |  |
| [Quality Risk Assessment](field-dictionary#quality_risk_assessment) | Quality/risk assessment *(sourced from jira https access ci atlassian net jira core projects att list jql project 20 3d 20att 20and 20status 20 3d 20 22done 2fcomplete 22 20order 20by 20assignee 20asc 2c 20cf 5b10019 5d 20asc)* | Internal Only |  |
| [Quarterly Report Data](field-dictionary#quarterly_report_data) | Publications; New publications; Turnaround time; EC decisions; Lessons learned, metrics, risks, task tracking, financials, outreach, *(sourced from ga4, constant contact, hootsuite, jira, confluence, google drive)* | Internal Only |  |
| [Quarterly/Annual Reports](field-dictionary#quarterly_annual_reports) | Reports to NSF *(sourced from google drive, confluence)* | Internal Only |  |
| [RAC Registration/Attendance](field-dictionary#rac_registration_attendance) | Registrations; Attendance | Restricted |  |
| [RP Survey](field-dictionary#rp_survey) | Resource provider feedback *(sourced from google drive)* | Restricted |  |
| [SC/WG Reporting Schedules](field-dictionary#sc_wg_reporting_schedules) | SC/WG interaction schedule with the EC *(sourced from raci in confluence, google doc)* | Internal Only |  |
| [SWG Notes](field-dictionary#swg_notes) | Strategic working group notes *(sourced from confluence)* | Internal Only |  |
| [Social Media Reach](field-dictionary#social_media_reach) | Engagement metrics *(sourced from hootsuite)* | Internal Only |  |
| [Staff Survey](field-dictionary#staff_survey) | Staff feedback *(sourced from google drive)* | Sensitive |  |
| [Stories/Publications - referenced in 3](field-dictionary#stories_publications_referenced_in_3) | HPC Wire articles; Awards; science stories *(sourced from submissions from researchers or comms other institutions publication searches using allocations data)* | Public |  |
| [Website Stats](field-dictionary#website_stats) | Visits; Click-through rates *(sourced from google analytics 4)* | Internal Only |  |

### Allocations

| Source | Description | Access | |
|--------|-------------|--------|---|
| [Allocations/Projects](field-dictionary#allocations_projects) | Active projects; Resource allocations; PI info; Detailed Project info | Authenticated | [API](https://api.xras.org/) · [Docs](https://api.xras.org/) |
| [Annual Report Data](field-dictionary#annual_report_data) | Users; Institutions; Academic status; Allocation counts; Projects; Usage; Documents; Abstracts; FOS; Publications; RPs utilized | Public |  |
| [Current Projects](field-dictionary#current_projects) | Active Projects; Resource Allocations; PI Info | Public | [API](https://allocations.access-ci.org/current-projects) |
| [Metrics Framework](field-dictionary#metrics_framework) | KPIs; Democratization Index; Ecosystem access time; RP Satisfaction; XRAS uptime; Feedback responsiveness; Ticket resolution; Staff satisfaction | Public |  |
| [Publications](field-dictionary#publications_allocations) | List of publications by ACCESS researchers | Public | [API](https://allocations.access-ci.org/access-publications) |
| [Request Statistics](field-dictionary#request_statistics) | Request counts; Response times; Approval/decline rates | Internal Only | [API](https://allocations.access-ci.org/) |

### External

| Source | Description | Access | |
|--------|-------------|--------|---|
| [NSF Awards](field-dictionary#nsf_awards) | NSF funding data; Award details | Public |  |

### Metrics

| Source | Description | Access | |
|--------|-------------|--------|---|
| [ACCESS RP Monthly Reports](field-dictionary#access_rp_monthly_reports) | Curated report w/ analysis | Restricted |  |
| [ACCESS Reports](field-dictionary#access_reports) | Curated report w/ analysis | Authenticated |  |
| [ACCESS User Monthly Reports](field-dictionary#access_user_monthly_reports) | Curated report w/ analysis | Restricted |  |
| [ACCESS XDMoD Data Access Endpoints](field-dictionary#access_xdmod_data_access_endpoints) | Allocations Information, Compute Usage, HPC Job Performance & Power Data, Science Gateway Usage, Resource Quality of service data (via Application Kernels), HPC Job Efficiency Analytics, Commercial and Non-Commercial Cloud Usage, Open OnDemand Usage *(sourced from batch compute log file from resource provider, amie packet from resouce provider, xras data, cilogon information)* | Public and Authenticated | [Docs](https://open.xdmod.org/11.0/rest.html) |
| [ACCESS XDMoD Data Catalog](field-dictionary#access_xdmod_data_catalog) | List of available statistics and dimensions | Public |  |
| [ACCESS XDMoD User Manual](field-dictionary#access_xdmod_user_manual) | XDMoD Web Portal Documentation | Public |  |
| [Graphical Visualizations of data avaible in XDMoD](field-dictionary#graphical_visualizations_of_data_avaible_in_xdmod) | Chart Configurations, List of available visualizations | Public and Authenticated |  |
| [NetSage](field-dictionary#netsage) | Network Usage data | Public and Authenticated |  |
| [Publications](field-dictionary#publications) | List of published papers and presentations | Public |  |
| [Video Tutorials](field-dictionary#video_tutorials) | Playlist(s) of tutorial videos | Public |  |
| [XDMoD Metrics](field-dictionary#xdmod) | HPC metrics, usage analytics, and resource specifications from the ACCESS XDMoD instance | Varies | [MCP](https://mcp.access-ci.org/docs/servers/xdmod) · [API](https://xdmod.access-ci.org/controllers/user_interface.php) |
| [XDMoD Open API Documentation](field-dictionary#xdmod_open_api_documentation) | Descriptions of XDMoD Open API endpoints | Public | [Docs](https://open.xdmod.org/11.0/rest.html) |
| [xdmod-data GitHub Repository](field-dictionary#xdmod_data_github_repository) | Documentation for the XDMoD Python/R APIs | Public |  |
| [xdmod-notebooks GitHub Repository](field-dictionary#xdmod_notebooks_github_repository) | Jupyter notebook training materials and examples | Public |  |

### Operations

| Source | Description | Access | |
|--------|-------------|--------|---|
| [COManage/ACCESS Identity](field-dictionary#comanage) | Identity information; Teragrid.org identities *(sourced from database)* | Sensitive |  |
| [Eval Team Surveys](field-dictionary#eval_team_surveys) | Community; Staff; RP survey data | Restricted |  |
| [Internet2 Flow Data](field-dictionary#internet2_flow_data) | Network flow data | Restricted |  |
| [Nagios](field-dictionary#nagios) | Monitoring data | Internal Only |  |
| [Network Traffic](field-dictionary#network_traffic) | Historical traffic volumes | Internal Only |  |
| [Qualys](field-dictionary#qualys) | Host vulnerability data | Sensitive |  |
| [RP Integration Effort](field-dictionary#rp_integration_effort) | Time/effort for new RP integration | TBD |  |
| [RP Support Effort](field-dictionary#rp_support_effort) | Time/effort for ongoing RP support | TBD |  |
| [RP batch scheduler information (from IPF)](field-dictionary#rp_batch_scheduler_information_from_ipf) | Scheduler queue configuration but not queue contents or reservations | Public |  |
| [RP software modules (from IPF)](field-dictionary#rp_software_modules_from_ipf) | Software catalog from resources | Public |  |
| [Resource Description (CIDeR)](field-dictionary#resource_description_cider) | Organizations, resource descriptions, and integration information for ACCESS resource providers. | Public | [API](https://operations-api.access-ci.org/wh2/cider/v1/) |
| [Resource Integration Roadmaps and Badges](field-dictionary#resource_integration_roadmaps_and_badges) | Integration status, badges supported | Public |  |
| [Resource News/Outages](field-dictionary#resource_news_outages) | Outages; Maintenance; Announcements | Public |  |
| [STEP Application](field-dictionary#step_application) | Institution demographics | Restricted |  |
| [STEP Survey](field-dictionary#step_survey) | Survey responses | Sensitive |  |
| [Service Index](field-dictionary#service_index) | Service catalog and status *(sourced from database)* | Restricted |  |
| [System & Service Logs](field-dictionary#system_service_logs) | Security logs; Monitoring data | Sensitive |  |
| [Ticketing (ACCESS System)](field-dictionary#ticketing_access_system) | Full ticket data; Tags; Resolution data | Restricted |  |
| [Ticketing Statistics](field-dictionary#ticketing_statistics) | Time to resolution; Tags | Internal Only |  |
| [Web Stats (Google Analytics)](field-dictionary#web_stats_google_analytics) | Page hits and visits | Internal Only |  |
| [ciLogon](field-dictionary#cilogon) | Authentication logs | Sensitive |  |
| [perfSONAR](field-dictionary#perfsonar) | Network performance logs | Public |  |

### Support

| Source | Description | Access | |
|--------|-------------|--------|---|
| [ACCESS Pegasus](field-dictionary#access_pegasus) | Workflow usage and execution data | Authenticated |  |
| [ACCESS Support Drupal](field-dictionary#access_support_drupal) | ACCESS Support website CMS - canonical storage for support content | Varies | [API](https://support.access-ci.org) · [Docs](https://support.access-ci.org/api-docs) |
| [Affinity Groups](field-dictionary#affinity_groups) | Membership, events, announcements, KB resources *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public and Authenticated | [MCP](https://mcp.access-ci.org/affinity-groups/mcp) · [API](https://support.access-ci.org/api/1.1/affinity_groups) |
| [Announcements](field-dictionary#announcements) | RP and community announcements *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public and Authenticated | [MCP](https://mcp.access-ci.org/announcements/mcp) · [API](https://support.access-ci.org/api/2.2/announcements) · [Docs](https://support.access-ci.org/api-docs/announcements) |
| [CCEP Awards (Community Grant)](field-dictionary#ccep_awards_community_grant) | Applicants; Institution; Amount awarded; Fund usage | Internal Only |  |
| [CSSN Roles/skills/Interests](field-dictionary#cssn_roles_skills_interests) | Taxonomy for skills/interests and roles in the community | Authenticated |  |
| [Chatbot](field-dictionary#chatbot) | Questions; Answers; Ratings | Internal Only |  |
| [Content API](field-dictionary#content_api) | Plain-text page content and a discovery index for ACCESS Support pages, for RAG ingestion and search syndication. *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [API](https://support.access-ci.org/.well-known/content-index.json) · [Docs](https://support.access-ci.org/api-docs/content) |
| [Event Registrations](field-dictionary#event_registrations) | Registration and attendance data for events *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Restricted |  |
| [Events and Training](field-dictionary#events) | Workshops, webinars, training sessions, and office hours *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [MCP](https://mcp.access-ci.org/events/mcp) · [API](https://support.access-ci.org/api/2.2/events) · [Docs](https://support.access-ci.org/api-docs/events) |
| [Focus Groups (2023)](field-dictionary#focus_groups_2023) | User experience feedback; Website review findings | Internal Only |  |
| [MATCH Services](field-dictionary#match_services) | Service requests and requestors | Restricted |  |
| [NAIRR Underutilization Surveys](field-dictionary#nairr_underutilization_surveys) | Resource; Reason for underutilization; Support needs | Restricted |  |
| [NAIRR Underutilized Allocations](field-dictionary#nairr_underutilized_allocations) | 1:1 meeting notes; Resource; Reasons; Support needs | Restricted |  |
| [Office Hours](field-dictionary#office_hours) | Attendees; Concerns raised | Restricted |  |
| [Resource Documentation API](field-dictionary#resource_documentation_api) | Team-authored documentation for ACCESS resource providers (login, file transfer, storage, queue specs, top software, datasets), with resource-group inheritance. *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal), [Resource Description (CIDeR)](field-dictionary#resource_description_cider))* | Public | [API](https://support.access-ci.org/api/1.0/resources) · [Docs](https://support.access-ci.org/api-docs/resources) |
| [SDS (Software Discovery Service)](field-dictionary#sds_software_discovery_service) | Software discovery: which software packages are available on which ACCESS resource providers. *(sourced from [Resource Description (CIDeR)](field-dictionary#resource_description_cider))* | Public | [MCP](https://mcp.access-ci.org/software-discovery/mcp) · [API](https://sds-ara-api.access-ci.org/api/v1) · [Docs](https://support.access-ci.org/api-docs/sds) |
| [Support Digest](field-dictionary#support_digest) | Link clicks; Open rates | Internal Only |  |
| [Webinar Registration (NAIRR/ACCESS)](field-dictionary#webinar_registration_nairr_access) | Names; Institutions; ACCESS ID; Email; Referral source | Restricted |  |
| [Website Analytics](field-dictionary#website_analytics) | Institution; Login status; Carnegie classification; Geography; Session clicks; Referrers | Internal Only |  |
| [Workshop Surveys (CU)](field-dictionary#workshop_surveys_cu) | Pre/post surveys; Institution; Motivation; Experience feedback | Restricted |  |

## Resources

- [Fields](field-dictionary) — Field-level documentation
- [Data quality](data-quality) — Sheet cells that need attention, by track
- [Connections](heb-visualization) — Interactive relationship visualization
- [Schema](erd) — Entity-relationship diagram
- [DBML](inventory.dbml) — Raw schema for dbdiagram.io
- [JSON](inventory.json) — Machine-readable export
- [Repository](https://github.com/Sweet-and-Fizzy/access-data-inventory) — Source files and contribution guide
