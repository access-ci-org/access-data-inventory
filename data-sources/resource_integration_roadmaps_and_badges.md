---
id: resource_integration_roadmaps_and_badges
name: Resource Integration Roadmaps and Badges
track: Operations
fields:
- name: Roadmap.badge_id
  type: int
  access: Public
- name: Roadmap.name
  type: varchar
  access: Public
- name: Roadmap.graphic
  type: image
  access: Public
- name: Roadmap.executive_summary
  type: text
  access: Public
  description: For RP leadership
- name: Roadmap.infrastructure_types
  type: varchar
  access: Public
  description: Types of infrastructure that can use this roadmap
- name: Roadmap.integration_coordinators
  type: varchar
  access: Public
  description: Coordinators
- name: Roadmap.status
  type: varchar
  access: Public
  description: Draft or Production
- name: Badge.badge_id
  type: int
  access: Public
- name: Badge.name
  type: varchar
  access: Public
- name: Badge.graphic
  type: image
  access: Public
- name: Badge.researcher_summary
  type: text
  access: Public
  description: For researching using the badges
- name: Badge.resource_provider_summary
  type: text
  access: Public
  description: Summary of what RPs provide and necessary support work
- name: Badge.verfication_summary
  type: text
  access: Public
  description: How is the badge verified
- name: Badge.verification_method
  type: varchar
  access: Public
  description: Manaul or Automated
- name: Badge.default_badge_access_url
  type: varchar
  access: Public
  description: URL for accessing this badge if the RP doesn't provide one
- name: Badge.default_badge_access_url_label
  type: varchar
  access: Public
  description: URL link label
- name: Task.task_id
  type: int
  access: Public
- name: Task.name
  type: varchar
  access: Public
- name: Task.technical_summary
  type: text
  access: Public
  description: Summary of what the RPs must do
- name: Task.implementor_roles
  type: varchar
  access: Public
  description: RP roles involved in implementation work
- name: Task.task_experts
  type: varchar
  access: Public
  description: Who can help with task
- name: Task.detailed_instructions_url
  type: varchar
  access: Public
  description: URL to task instructions
- name: Badge_Prerequisite_Badge.badge
  type: varchar
  access: Public
- name: Badge_Prerequisite_Badge.prerequisite_badge
  type: varchar
  access: Public
- name: Badge_Prerequisite_Badge.sequence_no
  type: int
  access: Public
  description: For ordering pre-requisites
- name: Roadmap_Badge.roadmap
  type: varchar
  access: Public
- name: Roadmap_Badge.badge
  type: varchar
  access: Public
- name: Roadmap_Badge.sequence_no
  type: int
  access: Public
  description: For ordering badges
- name: Roadmap_Badge.required
  type: boolean
  access: Public
  description: Is the badge required in this roadmap
- name: Badge_Task.badge
  type: varchar
  access: Public
- name: Badge_Task.task
  type: varchar
  access: Public
- name: Badge_Task.sequence_no
  type: int
  access: Public
  description: For ordering tasks
- name: Badge_Task.required
  type: boolean
  access: Public
  description: Is the task required in this badge
- name: Resource_Roadmap.info_resourceid
  type: varchar
  access: Public
  description: Which resource
- name: Resource_Roadmap.roadmap
  type: varchar
  access: Public
- name: Resource_Badge.info_resourceid
  type: varchar
  access: Public
  description: Which resource
- name: Resource_Badge.roadmap
  type: varchar
  access: Public
- name: Resource_Badge.badge
  type: varchar
  access: Public
- name: Resource_Badge.badge_access_url
  type: varchar
  access: Public
  description: URL for accessing this badge for a resource
- name: Resource_Badge_Worflow
  access: Public
  description: tracks resource-roadmap-badge status
- name: Resource_Badge_Task_Workflow
  access: Public
  description: tracks resource-roadmap-badge-task status
category: Resources
access_level: Public
priority: High
description: Integration status, badges supported
data_access_mechanism: API, Web
is_canonical: true
mcp:
  available: false
---
