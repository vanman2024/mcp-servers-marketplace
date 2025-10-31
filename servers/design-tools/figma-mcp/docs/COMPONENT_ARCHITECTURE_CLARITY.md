# Component Architecture - Clear Separation

## Three Distinct Layers

### 1. Base Components (`figma_components` table)
**What**: Individual, reusable UI elements
**Sources**: 
- ShadCN UI (981 components) ✓ Already imported
- Catalyst UI Kit (27 components) - Can be added
**Examples**: Button, Input, Dialog, Card, Select, DatePicker
**Purpose**: Building blocks for creating interfaces

### 2. Sections/Blocks (`sections` table)
**What**: Complete, designed page sections
**Sources**:
- Tailwind UI Templates (downloading now)
- Custom blocks (25 existing)
**Examples**: "Hero with Video Background", "3-Column Pricing", "Feature Grid"
**Purpose**: Pre-built sections that combine multiple base components

### 3. Component Relationships (`section_components` table)
**What**: Links sections to their component dependencies
**Purpose**: Track which base components each section uses
**Example**: "Pricing Section" uses → Button, Card, Badge components

## How They Work Together

```
┌─────────────────────────┐
│     SECTIONS TABLE      │ ← Tailwind UI Templates
│  (Complete Sections)    │ ← Custom Blocks
│                         │
│ - Hero Section          │
│ - Pricing Table         │
│ - Feature Grid          │
└───────────┬─────────────┘
            │ uses
            ↓
┌─────────────────────────┐
│  SECTION_COMPONENTS     │ ← Junction Table
│   (Relationships)       │
└───────────┬─────────────┘
            │ references
            ↓
┌─────────────────────────┐
│   FIGMA_COMPONENTS      │ ← ShadCN Components
│   (Base Components)     │ ← Catalyst Components
│                         │
│ - Button                │
│ - Card                  │
│ - Input                 │
└─────────────────────────┘
```

## No Confusion:
- **ShadCN/Catalyst** = Lego blocks
- **Tailwind UI** = Pre-built Lego structures
- They complement each other, not compete