---
id: events
name: Events and Training
description: Workshops, webinars, training sessions, and office hours
category: Events & Training
track: Support
access_level: Public
is_canonical: false
canonical_source:
- access_support_drupal
api_endpoint: https://support.access-ci.org/api/2.2/events
dynamic: false
priority: High
mcp:
  available: true
  url: https://mcp.access-ci.org/events/mcp
  tools:
  - name: search_events
    method: GET
    description: Search events with filters for type, date, skill level
  - name: get_event_by_id
    method: GET
    description: Get detailed information about a specific event
  - name: get_events_by_tag
    method: GET
    description: Get events filtered by tag
use_cases:
- What training sessions are available for beginners this month?
- Which events are associated with a specific affinity group?
- How many office hours are scheduled for next week?
- What events require registration?
fields:
- name: id
  type: int
  access: Public
  description: Event ID
  required: true
  semantic_type: entity_id
  primary_key: true
- name: uuid
  type: varchar
  access: Public
  description: Unique identifier
  required: true
  semantic_type: uuid
- name: title
  type: varchar
  access: Public
  description: Event title
  required: true
  mcp_name: title
  semantic_type: entity_name
- name: description
  type: text
  access: Public
  description: Event description
  mcp_name: description
  semantic_type: entity_description
- name: event_type
  type: varchar
  access: Public
  description: Type of event
  required: true
  mcp_name: type
  semantic_type: entity_type
- name: skill_level
  type: varchar
  access: Public
  description: Target skill level for attendees
  mcp_name: skill
  semantic_type: skill_level
- name: affiliation
  type: varchar
  access: Public
  description: Whether this is an official ACCESS or community event
  semantic_type: affiliation
- name: start_date
  type: timestamp
  access: Public
  description: Event start date and time
  required: true
  mcp_name: start_date
  semantic_type: date_start
- name: end_date
  type: timestamp
  access: Public
  description: Event end date and time
  mcp_name: end_date
  semantic_type: date_end
- name: duration_hours
  type: decimal
  access: Public
  description: Calculated duration in hours
  computed: true
  mcp_name: duration_hours
  semantic_type: duration
- name: starts_in_hours
  type: decimal
  access: Public
  description: Hours until event starts (negative if past)
  computed: true
  mcp_name: starts_in_hours
  semantic_type: time_relative
- name: location
  type: varchar
  access: Public
  description: Physical location if applicable
  semantic_type: location
- name: virtual_meeting_link
  type: varchar
  access: Authenticated
  description: Zoom/Teams link - requires authentication
  mcp_name: virtual_meeting_link
  semantic_type: url_meeting
- name: registration_url
  type: varchar
  access: Public
  description: Link to register for the event
  mcp_name: registration_url
  semantic_type: url_registration
- name: contact
  type: varchar
  access: Public
  description: Contact person or email
  mcp_name: contact
  semantic_type: contact_info
- name: speakers
  type: text
  access: Public
  description: Speaker names and affiliations
  semantic_type: person_name
- name: tags
  type: text
  access: Public
  description: Discovery tags
  mcp_name: tags
  semantic_type: tags
- name: affinity_group_id
  type: int
  access: Public
  description: Associated affinity group
  references: affinity_groups.nid
relationships:
- type: belongs_to
  target: affinity_groups
  field: affinity_group_id
  description: Events can be associated with an affinity group
- type: has_many
  target: tags
  through: entity_tags
  description: Events are tagged for discovery
- type: has_many
  target: event_registrations
  description: Registration records for this event
storage_location: ACCESS Support Drupal
data_access_mechanism: API, MCP
docs_url: https://support.access-ci.org/api-docs/events
refresh_frequency: realtime
query_capacity: high
sensitivity: Low
---

## Overview

Workshops, webinars, training sessions, and office hours offered by ACCESS and the community. The events MCP combines data from Drupal's eventseries and eventinstance content types into a unified view.

## Notes

- The `virtual_meeting_link` field requires authentication - not exposed to anonymous users
- `duration_hours` and `starts_in_hours` are computed fields calculated by the MCP
- Some events require registration; check `registration_url` for the signup link
- Events can overlap with ACO governance meetings - canonical source TBD
