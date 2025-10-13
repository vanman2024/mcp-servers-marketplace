-- MARKETING SECTIONS IMPORT
-- WARNING: These are marketing/landing page sections from Tailwind Plus templates
-- NOT for building applications - only for marketing websites!
-- Generated: 2025-07-17T20:15:00.749892


INSERT INTO sections (
    name,
    description,
    category,
    subcategory,
    source,
    react_template,
    template_type,
    is_template,
    published,
    tags,
    metadata,
    project_id
) VALUES (
    'Forms - Signupform - Marketing',
    'Marketing/Landing page component from Tailwind Plus Commit template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'forms',
    'tailwind-plus-marketing',
    'import { useId } from ''react''

import { Button } from ''@/components/Button''

export function SignUpForm() {
  let id = useId()

  return (
    <form className="relative isolate mt-8 flex items-center pr-1">
      <label htmlFor={id} className="sr-only">
        Email address
      </label>
      <input
        required
        type="email"
        autoComplete="email"
        name="email"
        id={id}
        placeholder="Email address"
        className="peer w-0 flex-auto bg-transparent px-4 py-2.5 text-base text-white placeholder:text-gray-500 focus:outline-hidden sm:text-[0.8125rem]/6"
      />
      <Button type="submit" arrow>
        Get updates
      </Button>
      <div className="absolute inset-0 -z-10 rounded-lg transition peer-focus:ring-4 peer-focus:ring-sky-300/15" />
      <div className="absolute inset-0 -z-10 rounded-lg bg-white/2.5 ring-1 ring-white/15 transition peer-focus:ring-sky-300" />
    </form>
  )
}
',
    'marketing-section',
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'commit', 'not-for-apps']::text[],
    '{"template_name": "tailwind-plus-commit", "component_type": "forms", "file_path": "tailwind-plus-commit/commit-ts/src/components/SignUpForm.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    metadata = EXCLUDED.metadata,
    updated_at = NOW();

INSERT INTO sections (
    name,
    description,
    category,
    subcategory,
    source,
    react_template,
    template_type,
    is_template,
    published,
    tags,
    metadata,
    project_id
) VALUES (
    'Site Navigation - Compass',
    'Marketing/Landing page component from Tailwind Plus Compass template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'navigation-layout',
    'tailwind-plus-marketing',
    '"use client";

import {
  Dropdown,
  DropdownButton,
  DropdownItem,
  DropdownMenu,
} from "@/components/dropdown";
import { IconButton } from "@/components/icon-button";
import { ChevronDownIcon } from "@/icons/chevron-down-icon";
import { CloseIcon } from "@/icons/close-icon";
import { MenuIcon } from "@/icons/menu-icon";
import {
  let id = useId()

  return (
    <form className="relative isolate mt-8 flex items-center pr-1">
      <label htmlFor={id} className="sr-only">
        Email address
      </label>
      <input
        required
        type="email"
        autoComplete="email"
        name="email"
        id={id}
        placeholder="Email address"
        className="peer w-0 flex-auto bg-transparent px-4 py-2.5 text-base text-white placeholder:text-gray-500 focus:outline-hidden sm:text-[0.8125rem]/6"
      />
      <Button type="submit" arrow>
        Get updates
      </Button>
      <div className="absolute inset-0 -z-10 rounded-lg transition peer-focus:ring-4 peer-focus:ring-sky-300/15" />
      <div className="absolute inset-0 -z-10 rounded-lg bg-white/2.5 ring-1 ring-white/15 transition peer-focus:ring-sky-300" />
    </form>
  )
}
',
    'forms',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'commit', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-commit", "component_type": "forms", "file_path": "tailwind-plus-commit/commit-ts/src/components/SignUpForm.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

