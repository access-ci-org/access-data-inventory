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
  package: "@access-mcp/events"
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
    required: true
    type: int
    access: Public
    primary_key: true
    description: Event ID
    semantic_type: entity_id

  - name: uuid
    required: true
    type: varchar
    access: Public
    description: Unique identifier
    semantic_type: uuid

  - name: title
    type: varchar
    access: Public
    required: true
    mcp_name: title
    description: Event title
    semantic_type: entity_name

  - name: description
    type: text
    access: Public
    mcp_name: description
    description: Event description
    semantic_type: entity_description

  - name: event_type
    type: varchar
    access: Public
    required: true
    mcp_name: type
    allowed_values: [Conference, Training, Office Hours, Other]
    description: Type of event
    semantic_type: entity_type

  - name: skill_level
    type: varchar
    access: Public
    mcp_name: skill
    allowed_values: [Beginner, Intermediate, Advanced]
    description: Target skill level for attendees
    semantic_type: skill_level

  - name: affiliation
    type: varchar
    access: Public
    allowed_values: [ACCESS Collaboration, Community]
    description: Whether this is an official ACCESS or community event
    semantic_type: affiliation

  - name: start_date
    required: true
    type: timestamp
    access: Public
    mcp_name: start_date
    description: Event start date and time
    semantic_type: date_start

  - name: end_date
    type: timestamp
    access: Public
    mcp_name: end_date
    description: Event end date and time
    semantic_type: date_end

  - name: duration_hours
    type: decimal
    access: Public
    computed: true
    mcp_name: duration_hours
    description: Calculated duration in hours
    semantic_type: duration

  - name: starts_in_hours
    type: decimal
    access: Public
    computed: true
    mcp_name: starts_in_hours
    description: Hours until event starts (negative if past)
    semantic_type: time_relative

  - name: location
    type: varchar
    access: Public
    description: Physical location if applicable
    semantic_type: location

  - name: virtual_meeting_link
    type: varchar
    access: Authenticated
    mcp_name: virtual_meeting_link
    description: Zoom/Teams link - requires authentication
    semantic_type: url_meeting

  - name: registration_url
    type: varchar
    access: Public
    mcp_name: registration_url
    description: Link to register for the event
    semantic_type: url_registration

  - name: contact
    type: varchar
    access: Public
    mcp_name: contact
    description: Contact person or email
    semantic_type: contact_info

  - name: speakers
    type: text
    access: Public
    description: Speaker names and affiliations
    semantic_type: person_name

  - name: tags
    type: text
    access: Public
    computed: true
    mcp_name: tags
    description: Parsed from comma-separated tag list
    semantic_type: tags

  - name: affinity_group_id
    type: int
    access: Public
    references: affinity_groups.nid
    description: Associated affinity group

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
---

## Overview

Workshops, webinars, training sessions, and office hours offered by ACCESS and the community. The events MCP combines data from Drupal's eventseries and eventinstance content types into a unified view.

## Notes

- The `virtual_meeting_link` field requires authentication - not exposed to anonymous users
- `duration_hours` and `starts_in_hours` are computed fields calculated by the MCP
- Some events require registration; check `registration_url` for the signup link
- Events can overlap with ACO governance meetings - canonical source TBD
