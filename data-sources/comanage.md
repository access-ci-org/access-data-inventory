---
id: comanage
name: COManage/ACCESS Identity
description: User identity information
category: Users & Identity
track: Operations
access_level: Sensitive
is_canonical: true
canonical_source: null
api_endpoint: null
dynamic: false
priority: Low

mcp:
  available: false
  package: null
  tools: []
  notes: Identity data is sensitive and not suitable for AI/MCP exposure

use_cases:
  - How many unique users are registered in ACCESS?
  - Which institutions have the most ACCESS users?
  - Is a specific user affiliated with a particular institution?

constraints:
  - type: privacy
    description: Contains PII (names, emails, ACCESS IDs). Must not be exposed through public APIs, AI tools, or MCP servers.
  - type: acceptable_use
    description: Identity data may only be accessed by named individuals with legitimate need or systems with explicit authorization.
  - type: regulatory
    description: Subject to institutional data handling agreements and FERPA considerations for student researchers.

fields:
  - name: user_id
    type: varchar
    access: Sensitive
    primary_key: true
    description: Internal user identifier
    semantic_type: entity_id

  - name: access_id
    type: varchar
    access: Sensitive
    description: ACCESS username (e.g., jsmith)
    semantic_type: entity_id

  - name: email
    type: varchar
    access: Sensitive
    description: User email address (PII)
    semantic_type: person_email

  - name: name
    type: varchar
    access: Restricted
    description: User's display name
    semantic_type: person_name

  - name: institution
    type: varchar
    access: Restricted
    description: User's institutional affiliation
    semantic_type: institution

relationships:
  - type: has_many
    target: affinity_group_members
    description: Users can be members of affinity groups

  - type: has_many
    target: event_registrations
    description: Users register for events
---

## Overview

COManage is the identity management system for ACCESS. It stores user identity information including ACCESS IDs, email addresses, and institutional affiliations.

## Notes

- This data source contains PII and is classified as Sensitive
- Not suitable for AI/MCP exposure
- Other teams will contribute to the full user data model
- Users may have multiple ACCESS IDs (legacy XSEDE + ACCESS)
- Institutional affiliations may be outdated

## Access Considerations

Identity data should only be accessed by:
- Named individuals with legitimate need
- Systems with explicit authorization
- Never exposed through public APIs or AI tools
