---
id: event_registrations
name: Event Registrations
description: Registration and attendance data for events
category: Events & Training
track: Support
access_level: Restricted
is_canonical: false
canonical_source:
- access_support_drupal
dynamic: false
priority: Medium
mcp:
  available: false
use_cases:
- How many people registered for a specific event?
- What is the attendance rate for training sessions?
- Which institutions are most represented at ACCESS events?
- How do registrants hear about ACCESS events?
constraints:
- type: privacy
  description: Contains PII (names, emails, ACCESS IDs). Must not be exposed through public APIs or AI tools.
- type: acceptable_use
  description: Registration data may only be used for event management, reporting, and outreach effectiveness analysis. Individual-level data must not be shared outside authorized teams.
fields:
- name: registration_id
  type: varchar
  access: Restricted
  description: Registration record ID
  required: true
  semantic_type: entity_id
  primary_key: true
- name: event_id
  type: int
  access: Restricted
  description: Associated event
  required: true
  references: events.id
- name: user_id
  type: varchar
  access: Restricted
  description: Registered user
  required: true
  references: users.user_id
- name: registration_date
  type: timestamp
  access: Restricted
  description: When the registration was submitted
  required: true
  semantic_type: date_created
- name: attendance_status
  type: varchar
  access: Restricted
  description: Registration and attendance status
  semantic_type: entity_status
- name: referral_source
  type: varchar
  access: Restricted
  description: How the registrant heard about the event
- name: registrant_name
  type: varchar
  access: Sensitive
  description: Registrant's name (PII)
  semantic_type: person_name
- name: registrant_email
  type: varchar
  access: Sensitive
  description: Registrant's email address (PII)
  semantic_type: person_email
- name: registrant_institution
  type: varchar
  access: Restricted
  description: Registrant's institutional affiliation
  semantic_type: institution
- name: registrant_access_id
  type: varchar
  access: Sensitive
  description: Registrant's ACCESS ID (PII)
  semantic_type: entity_id
relationships:
- type: belongs_to
  target: events
  field: event_id
  description: Each registration is for a specific event
- type: belongs_to
  target: users
  field: user_id
  description: Each registration is linked to a user
storage_location: ACCESS Support Drupal
data_access_mechanism: Web
---

## Overview

Event registration and attendance tracking data. This source contains records of who registered for events, whether they attended, and how they found out about the event.

## Notes

- Contains PII (names, emails, ACCESS IDs) - classified as Restricted/Sensitive
- Not exposed via MCP due to privacy concerns
- Partial event attendance counts may be available through the events MCP
- Useful for understanding training reach and effectiveness
- Referral source data helps track outreach effectiveness
