# Figma Design System Database Schema

This document describes the complete database schema for the Figma Design System project.

## Database Connection
- **Project ID**: `wsmhiiharnhqupdniwgw`
- **URL**: https://wsmhiiharnhqupdniwgw.supabase.co

## Table Overview

| Table Name | Record Count | Purpose |
|------------|--------------|---------|
| `figma_components` | 999 | Original component storage (legacy) |
| `sections` | 85 | New section-based architecture |
| `section_components` | 0 | Component mapping for sections |
| `design_systems` | - | Design system definitions |
| `project_specifications` | - | Project-specific configs |
| `section_templates` | - | Reusable section templates |
| `section_usage_analytics` | - | Usage tracking |

## Detailed Schema

### 1. `figma_components` Table (Legacy - 999 records)
Original component storage system - still used by main MCP server.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | NO | gen_random_uuid() | Primary key |
| `figma_id` | varchar(100) | NO | - | Figma's component ID |
| `name` | varchar(200) | NO | - | Component name |
| `description` | text | YES | - | Component description |
| `category_id` | uuid | YES | - | FK to component_categories |
| `figma_url` | text | NO | - | Figma file URL |
| `thumbnail_url` | text | YES | - | Preview image |
| `component_type` | varchar(50) | YES | - | Type (button, card, etc) |
| `tags` | text[] | YES | - | Searchable tags |
| `complexity_score` | integer | YES | 1 | 1-5 complexity rating |
| `popularity_score` | integer | YES | 0 | Usage popularity |
| `props` | jsonb | YES | - | Component properties |
| `css_classes` | text[] | YES | - | CSS class list |
| `dependencies` | text[] | YES | - | Required dependencies |
| `figma_node_type` | varchar(50) | YES | - | Figma node type |
| `figma_parent_id` | varchar(100) | YES | - | Parent component ID |
| `width` | numeric | YES | - | Component width |
| `height` | numeric | YES | - | Component height |
| `status` | varchar(20) | YES | 'active' | active/deprecated |
| `version` | varchar(20) | YES | '1.0' | Version number |
| `last_synced` | timestamptz | YES | now() | Last sync time |
| `search_vector` | tsvector | YES | - | Full-text search |
| `created_at` | timestamptz | YES | now() | Creation time |
| `updated_at` | timestamptz | YES | now() | Last update time |

### 2. `sections` Table (Current - 85 records)
New architecture for complete page sections containing multiple components.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | NO | gen_random_uuid() | Primary key |
| `name` | varchar(255) | NO | - | Section name |
| `description` | text | YES | - | Section description |
| `block_type` | varchar(50) | NO | - | hero/pricing/features/etc |
| `app_type` | varchar(50) | YES | - | marketing-site/e-commerce/app |
| `react_template` | text | NO | - | Full React code |
| `preview_image_url` | text | YES | - | Preview screenshot |
| `dependencies` | jsonb | YES | '[]' | NPM dependencies |
| `props_schema` | jsonb | YES | '{}' | Props validation schema |
| `example_props` | jsonb | YES | '{}' | Example prop values |
| `tags` | text[] | YES | '{}' | Searchable tags |
| `created_at` | timestamptz | YES | now() | Creation time |
| `updated_at` | timestamptz | YES | now() | Last update time |
| `source` | varchar(50) | YES | 'custom' | tailwind-plus-marketing/etc |
| `category` | varchar(100) | YES | - | marketing-landing/app-ui |
| `project_id` | uuid | YES | - | FK to projects |
| `design_spec_id` | uuid | YES | - | FK to design specs |
| `parent_section_id` | uuid | YES | - | For nested sections |
| `layout_config` | jsonb | YES | '{}' | Layout settings |
| `style_overrides` | jsonb | YES | '{}' | CSS overrides |
| `visibility_rules` | jsonb | YES | '{}' | Conditional rendering |
| `is_template` | boolean | YES | true | Template vs instance |
| `version` | varchar(20) | YES | '1.0.0' | Version number |
| `published` | boolean | YES | true | Published status |
| `search_vector` | tsvector | YES | - | Full-text search |

### 3. `section_components` Table (Empty - 0 records)
Maps individual components within sections.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | NO | gen_random_uuid() | Primary key |
| `section_id` | uuid | NO | - | FK to sections |
| `component_id` | uuid | YES | - | FK to figma_components |
| `component_name` | varchar(255) | YES | - | Component name |
| `position` | integer | NO | 0 | Order in section |
| `props` | jsonb | YES | '{}' | Component props |
| `style_overrides` | jsonb | YES | '{}' | CSS overrides |
| `conditional_rendering` | jsonb | YES | '{}' | Display conditions |
| `created_at` | timestamptz | YES | now() | Creation time |
| `updated_at` | timestamptz | YES | now() | Last update time |

## Current Data Status

### Sections Table Content (85 records)
- **All 85 sections are marketing-focused** (NOT application UI)
- **Source**: All from `tailwind-plus-marketing` templates
- **Categories**: All `marketing-landing`
- **Tags**: All tagged with `not-for-apps`

### Section Types Distribution:
Based on `block_type` field:
- hero sections
- pricing sections 
- features sections
- auth sections
- portfolio sections
- team sections
- testimonials sections
- newsletter sections
- contact sections
- footer sections
- header sections
- cta sections
- stats sections
- logos sections
- faq sections

### Key Issues:
1. **Main MCP server still uses `figma_components` table** (999 records)
2. **New `sections` table not connected to MCP server** (85 records)
3. **No application UI components** - only marketing sections
4. **`section_components` table is empty** - no component mapping yet

## Migration Status
- ✅ Database migrated from blocks to sections architecture
- ✅ 85 marketing sections imported from Tailwind Plus templates
- ❌ Main MCP server not updated to use sections table
- ❌ Application UI components not imported yet
- ❌ Component mapping (`section_components`) not populated