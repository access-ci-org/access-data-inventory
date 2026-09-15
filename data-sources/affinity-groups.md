---
id: affinity_groups
name: Affinity Groups
description: Membership, events, announcements, KB resources
category: Community & Outreach
track: Support
access_level: Public and Authenticated
is_canonical: false
canonical_source:
- access_support_drupal
api_endpoint: https://support.access-ci.org/api/1.1/affinity_groups
dynamic: false
priority: High
mcp:
  available: true
  url: https://mcp.access-ci.org/affinity-groups/mcp
  tools:
  - name: search_affinity_groups
    method: GET
    description: Search and filter affinity groups
  - name: get_affinity_group_kb
    method: GET
    description: Get knowledge base resources for a group
  - name: get_affinity_group_events
    method: GET
    description: Get events associated with a group
use_cases:
- Which affinity groups are available for a specific research domain?
- Who coordinates a particular affinity group?
- What events are associated with an affinity group?
- How can I join or contact an affinity group?
constraints:
- type: privacy
  description: Mailing lists, private group flags, and membership lists are restricted and must not be exposed through public APIs or AI tools.
fields:
- name: nid
  type: int
  access: Public
  description: Node ID
  required: true
  semantic_type: entity_id
  primary_key: true
- name: uuid
  type: varchar
  access: Public
  description: Unique identifier
  required: true
  mcp_name: id
  semantic_type: uuid
- name: title
  type: varchar
  access: Public
  description: Group name
  required: true
  mcp_name: name
  semantic_type: entity_name
- name: body
  type: text
  access: Public
  description: Group description (HTML cleaned in MCP)
  mcp_name: description
  semantic_type: entity_description
- name: group_id
  type: varchar
  access: Public
  description: URL-friendly group identifier
  required: true
  mcp_name: id
  semantic_type: entity_id
- name: group_slug
  type: varchar
  access: Public
  description: URL slug for the group
- name: category
  type: varchar
  access: Public
  description: Whether this is an RP-specific or community group
  mcp_name: category
  semantic_type: entity_type
- name: goals
  type: text
  access: Public
  description: Group goals and objectives
  semantic_type: entity_summary
- name: coordinator_id
  type: int
  access: Public
  description: Group coordinator (exposed as name string in MCP)
  mcp_name: coordinator
  references: users.user_id
- name: slack_link
  type: varchar
  access: Public
  description: Link to Slack channel
  mcp_name: slack_link
  semantic_type: url_external
- name: mailing_list
  type: varchar
  access: Restricted
  description: Internal mailing list address
  semantic_type: contact_info
- name: external_email_list
  type: varchar
  access: Restricted
  description: External email list address
  semantic_type: contact_info
- name: github_org
  type: varchar
  access: Public
  description: GitHub organization URL
  semantic_type: url_external
- name: ask_ci_forum
  type: varchar
  access: Public
  description: Link to Ask.CI forum topic
  mcp_name: ask_ci_forum
  semantic_type: url_external
- name: meeting_notes_link
  type: varchar
  access: Public
  description: Link to meeting notes document
  semantic_type: url_external
- name: is_private
  type: boolean
  access: Restricted
  description: Whether the group is private
- name: private_users
  type: text
  access: Restricted
  description: List of users with access to private group
- name: image_id
  type: int
  access: Public
  description: Group logo/image
  semantic_type: media_ref
relationships:
- type: has_one
  target: users
  field: coordinator_id
  description: Each group has a coordinator
- type: has_many
  target: events
  through: affinity_group_events
  description: Groups host events
- type: has_many
  target: announcements
  through: affinity_group_announcements
  description: Groups publish announcements
- type: has_many
  target: users
  through: affinity_group_members
  description: Groups have members
- type: has_many
  target: tags
  through: entity_tags
  description: Groups can be tagged
notes: affinity-groups MCP exists
data_access_mechanism: API, MCP, Web
refresh_frequency: real-time
query_capacity: high
sensitivity: Medium
---

## Overview

Affinity groups are community-organized groups centered around shared interests, research domains, or resource provider communities. They provide a way for ACCESS users to connect with peers.

## Notes

- The MCP cleans HTML from the body field for cleaner display
- Coordinator is exposed as a name string in the MCP (not the user ID)
- Mailing list fields are restricted - not exposed via public API
- Private groups and their membership lists are restricted
