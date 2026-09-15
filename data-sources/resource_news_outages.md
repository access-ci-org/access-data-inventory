---
id: resource_news_outages
name: Resource News/Outages
track: Operations
fields:
- name: News.Content
  type: text
  access: Public
- name: News.Start
  type: timestamp
  access: Public
- name: News.End
  type: timestamp
  access: Public
- name: News.Type
  type: varchar
  access: Public
- name: News.DistributionOptions
  type: varchar
  access: Public
- name: News.WebURL
  type: varchar
  access: Public
- name: News.Affiliation
  type: varchar
  access: Public
- name: News.Publisher
  type: varchar
  access: Public
- name: News_Associations
  type: varchar
  access: Public
  description: Associates news to infrastructure elements
- name: News_Publisher.OrganizationID
  type: varchar
  access: Public
- name: News_Publisher.OrganizationName
  type: varchar
  access: Public
- name: News_Publisher.NewsURNPrefix
  type: varchar
  access: Public
category: Resources
access_level: Public
priority: High
description: Outages; Maintenance; Announcements
notes: system-status MCP exists
data_access_mechanism: API, Web
is_canonical: true
mcp:
  available: false
---
