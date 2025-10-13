-- MARKETING SECTIONS IMPORT
-- WARNING: These are marketing/landing page sections from Tailwind Plus templates
-- NOT for building applications - only for marketing websites!
-- Generated: 2025-07-17T20:18:19.443156

-- First ensure we have a default project
INSERT INTO project_specifications (name, description, design_tokens)
VALUES (
    'Default Project',
    'Default project for shared components',
    '{"colors": {}, "typography": {}}'::jsonb
) ON CONFLICT (name) DO NOTHING;


-- Forms - Signupform - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Forms - Signupform - Marketing',
    'Marketing/Landing page component from Tailwind Plus Commit template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
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

-- Site Navigation - Compass
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Navigation - Compass',
    'Marketing/Landing page component from Tailwind Plus Compass template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
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
  CloseButton,
  Dialog,
  DialogBackdrop,
  DialogPanel,
} from "@headlessui/react";
import { clsx } from "clsx";
import Link from "next/link";
import type React from "react";
import { useState } from "react";

export function Navbar({ children, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      className={clsx(
        "sticky top-0 z-10 bg-white/90 backdrop-blur-sm dark:bg-gray-950/90",
        "flex items-center justify-between gap-x-8 px-4 py-4 sm:px-6",
      )}
      {...props}
    >
      {children}
      <SiteNavigation />
    </div>
  );
}

function MobileNavigation({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  return (
    <Dialog open={open} onClose={onClose} className="lg:hidden">
      <DialogBackdrop className="fixed inset-0 bg-gray-950/25" />
      <div className="fixed inset-0 flex justify-end pl-11">
        <DialogPanel className="w-full max-w-2xs bg-white px-4 py-5 ring ring-gray-950/10 sm:px-6 dark:bg-gray-950 dark:ring-white/10">
          <div className="flex justify-end">
            <CloseButton as={IconButton} onClick={onClose}>
              <CloseIcon className="stroke-gray-950 dark:stroke-white" />
            </CloseButton>
          </div>
          <div className="mt-4">
            <div className="flex flex-col gap-y-2">
              {[
                ["Course", "/"],
                ["Interviews", "/interviews"],
                ["Resources", "/resources"],
              ].map(([title, href]) => (
                <CloseButton
                  as={Link}
                  key={href}
                  href={href}
                  className="block rounded-md px-4 py-1.5 text-lg/7 font-medium tracking-tight text-gray-950 hover:bg-gray-950/5 dark:text-white dark:hover:bg-white/5"
                >
                  {title}
                </CloseButton>
              ))}
            </div>
            <div className="mt-6 flex flex-col gap-y-2">
              <h3 className="px-4 py-1 text-sm/7 text-gray-500">Account</h3>
              {[
                ["Settings", "#"],
                ["Support", "#"],
                ["Sign out", "/login"],
              ].map(([title, href], index) => (
                <CloseButton
                  as={Link}
                  key={index}
                  href={href}
                  className="rounded-md px-4 py-1 text-sm/7 font-semibold text-gray-950 hover:bg-gray-950/5 dark:text-white dark:hover:bg-white/5"
                >
                  {title}
                </CloseButton>
              ))}
            </div>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  );
}

function SiteNavigation() {
  let [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="flex items-center">
      <IconButton className="lg:hidden" onClick={() => setMobileMenuOpen(true)}>
        <MenuIcon className="fill-gray-950 dark:fill-white" />
      </IconButton>
      <MobileNavigation
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
      />
      <div className="flex gap-x-6 text-sm/6 text-gray-950 max-lg:hidden dark:text-white">
        <Link href="/">Course</Link>
        <Link href="/interviews">Interviews</Link>
        <Link href="/resources">Resources</Link>
        <Dropdown>
          <DropdownButton className="inline-flex items-center gap-x-2 focus:not-data-focus:outline-none">
            Account
            <ChevronDownIcon className="stroke-gray-950 dark:stroke-white" />
          </DropdownButton>
          <DropdownMenu anchor="bottom end">
            <DropdownItem href="#">Settings</DropdownItem>
            <DropdownItem href="#">Support</DropdownItem>
            <DropdownItem href="/login">Sign out</DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </div>
    </nav>
  );
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'compass', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["next/link", "clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-compass", "component_type": "navigation", "file_path": "tailwind-plus-compass/compass-ts/src/components/navbar.tsx", "uses_components": ["Dialog"], "dependencies": ["next/link", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Auth - Layout - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Auth - Layout - Marketing',
    'Marketing/Landing page component from Tailwind Plus Compass template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Logo } from "@/components/logo";
import Link from "next/link";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-dvh flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-xs">
        <div className="flex justify-center">
          <Link href="/" aria-label="Compass">
            <Logo className="h-6 fill-gray-950 dark:fill-white" />
          </Link>
        </div>
        <div className="mt-10">{children}</div>
      </div>
    </div>
  );
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'compass', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-compass", "component_type": "auth", "file_path": "tailwind-plus-compass/compass-ts/src/app/(auth)/layout.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Auth - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Auth - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Compass template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Button } from "@/components/button";
import { OTPInput } from "@/components/input";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Enter one-time password - Compass",
};

export default function Page() {
  return (
    <>
      <h1 className="sr-only">Enter one-time password</h1>
      <p className="text-center text-sm/7 text-gray-950 dark:text-white">
        A 6-digit verification code has been sent to{" "}
        <span className="font-semibold">adam@example.com</span>.
      </p>
      <form action="/" className="mt-6">
        <OTPInput maxLength={6} />
        <p className="mt-6 text-center text-sm/7 text-gray-600 dark:text-gray-400">
          Didn''t receive a code?{" "}
          <button
            type="button"
            className="font-semibold text-gray-950 underline decoration-gray-950/25 underline-offset-2 hover:decoration-gray-950/50 dark:text-white dark:decoration-white/25 dark:hover:decoration-white/50"
          >
            Request new code
          </button>
        </p>
        <Button type="submit" className="mt-6 w-full">
          Verify
        </Button>
      </form>
      <p className="mt-6 text-center text-sm/7 dark:text-gray-400">
        <Link
          href="/login"
          className="font-semibold text-gray-950 dark:text-white"
        >
          Use a different email
        </Link>
      </p>
    </>
  );
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'compass', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-compass", "component_type": "auth", "file_path": "tailwind-plus-compass/compass-ts/src/app/(auth)/otp/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Navigation - Compass
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Navigation - Compass',
    'Marketing/Landing page component from Tailwind Plus Compass template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { clsx } from "clsx";
import Link, { type LinkProps } from "next/link";
import type React from "react";

export function Breadcrumbs(props: React.ComponentProps<"nav">) {
  return (
    <nav
      aria-label="Breadcrumb"
      className="flex items-center gap-x-2 text-sm/6"
      {...props}
    />
  );
}

export function BreadcrumbHome() {
  return (
    <Link href="/" className="min-w-0 shrink-0 text-gray-950 dark:text-white">
      Compass
    </Link>
  );
}

export function Breadcrumb({
  href,
  children,
  className,
}: {
  href?: LinkProps["href"];
  children: React.ReactNode;
  className?: string;
}) {
  if (href) {
    return (
      <Link
        href={href}
        className={clsx(
          className,
          "min-w-0 truncate text-gray-950 dark:text-white",
        )}
      >
        {children}
      </Link>
    );
  }

  return (
    <span
      className={clsx(
        className,
        "min-w-0 truncate text-gray-950 last:text-gray-600 dark:last:text-gray-400",
      )}
    >
      {children}
    </span>
  );
}

export function BreadcrumbSeparator({ className }: { className?: string }) {
  return (
    <span className={clsx(className, "text-gray-950/25 dark:text-white/25")}>
      /
    </span>
  );
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'compass', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-compass", "component_type": "navigation", "file_path": "tailwind-plus-compass/compass-ts/src/components/breadcrumbs.tsx", "uses_components": [], "dependencies": ["next/link", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Keynote
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Keynote',
    'Marketing/Landing page component from Tailwind Plus Keynote template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Container } from ''@/components/Container''
import { Logo } from ''@/components/Logo''

export function Footer() {
  return (
    <footer className="flex-none py-16">
      <Container className="flex flex-col items-center justify-between md:flex-row">
        <Logo className="h-12 w-auto text-slate-900" />
        <p className="mt-6 text-base text-slate-500 md:mt-0">
          Copyright &copy; {new Date().getFullYear()} DeceptiConf, LLC. All
          rights reserved.
        </p>
      </Container>
    </footer>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-keynote", "component_type": "footer", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Keynote
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Keynote',
    'Marketing/Landing page component from Tailwind Plus Keynote template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { DiamondIcon } from ''@/components/DiamondIcon''
import { Logo } from ''@/components/Logo''

export function Header() {
  return (
    <header className="relative z-50 flex-none lg:pt-11">
      <Container className="flex flex-wrap items-center justify-center sm:justify-between lg:flex-nowrap">
        <div className="mt-10 lg:mt-0 lg:grow lg:basis-0">
          <Logo className="h-12 w-auto text-slate-900" />
        </div>
        <div className="order-first -mx-4 flex flex-auto basis-full overflow-x-auto border-b border-blue-600/10 py-4 font-mono text-sm whitespace-nowrap text-blue-600 sm:-mx-6 lg:order-none lg:mx-0 lg:basis-auto lg:border-0 lg:py-0">
          <div className="mx-auto flex items-center gap-4 px-4">
            <p>
              <time dateTime="2022-04-04">04</time>-
              <time dateTime="2022-04-06">06 of April, 2022</time>
            </p>
            <DiamondIcon className="h-1.5 w-1.5 overflow-visible fill-current stroke-current" />
            <p>Los Angeles, CA</p>
          </div>
        </div>
        <div className="hidden sm:mt-10 sm:flex lg:mt-0 lg:grow lg:basis-0 lg:justify-end">
          <Button href="#">Get your tickets</Button>
        </div>
      </Container>
    </header>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-keynote", "component_type": "hero", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Keynote
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Keynote',
    'Marketing/Landing page component from Tailwind Plus Keynote template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { BackgroundImage } from ''@/components/BackgroundImage''
import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''

export function Hero() {
  return (
    <div className="relative py-20 sm:pt-36 sm:pb-24">
      <BackgroundImage className="-top-36 -bottom-14" />
      <Container className="relative">
        <div className="mx-auto max-w-2xl lg:max-w-4xl lg:px-12">
          <h1 className="font-display text-5xl font-bold tracking-tighter text-blue-600 sm:text-7xl">
            <span className="sr-only">DeceptiConf - </span>A design conference
            for the dark side.
          </h1>
          <div className="mt-6 space-y-6 font-display text-2xl tracking-tight text-blue-900">
            <p>
              The next generation of web users are tech-savvy and suspicious.
              They know how to use dev tools, they can detect a phishing scam
              from a mile away, and they certainly aren’t accepting any checks
              from Western Union.
            </p>
            <p>
              At DeceptiConf you’ll learn about the latest dark patterns being
              developed to trick even the smartest visitors, and you’ll learn
              how to deploy them without ever being detected.
            </p>
          </div>
          <Button href="#" className="mt-10 w-full sm:hidden">
            Get your tickets
          </Button>
          <dl className="mt-10 grid grid-cols-2 gap-x-10 gap-y-6 sm:mt-16 sm:gap-x-16 sm:gap-y-10 sm:text-center lg:auto-cols-auto lg:grid-flow-col lg:grid-cols-none lg:justify-start lg:text-left">
            {[
              [''Speakers'', ''18''],
              [''People Attending'', ''2,091''],
              [''Venue'', ''Staples Center''],
              [''Location'', ''Los Angeles''],
            ].map(([name, value]) => (
              <div key={name}>
                <dt className="font-mono text-sm text-blue-600">{name}</dt>
                <dd className="mt-0.5 text-2xl font-semibold tracking-tight text-blue-900">
                  {value}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </Container>
    </div>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-keynote", "component_type": "hero", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Forms - Newsletter - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Forms - Newsletter - Marketing',
    'Marketing/Landing page component from Tailwind Plus Keynote template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image from ''next/image''

import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import backgroundImage from ''@/images/background-newsletter.jpg''

function ArrowRightIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" {...props}>
      <path
        d="m14 7 5 5-5 5M19 12H5"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function Newsletter() {
  return (
    <section id="newsletter" aria-label="Newsletter">
      <Container>
        <div className="relative -mx-4 overflow-hidden bg-indigo-50 px-4 py-20 sm:-mx-6 sm:px-6 md:mx-0 md:rounded-5xl md:px-16 xl:px-24 xl:py-36">
          <Image
            className="absolute top-0 left-1/2 translate-x-[-10%] translate-y-[-45%] lg:translate-x-[-32%]"
            src={backgroundImage}
            alt=""
            width={919}
            height={1351}
            unoptimized
          />
          <div className="relative mx-auto grid max-w-2xl grid-cols-1 gap-x-32 gap-y-14 xl:max-w-none xl:grid-cols-2">
            <div>
              <p className="font-display text-4xl font-medium tracking-tighter text-blue-900 sm:text-5xl">
                Stay up to date
              </p>
              <p className="mt-4 text-lg tracking-tight text-blue-900">
                Get updates on all of our events and be the first to get
                notified when tickets go on sale.
              </p>
            </div>
            <form>
              <h3 className="text-lg font-semibold tracking-tight text-blue-900">
                Sign up to our newsletter <span aria-hidden="true">&darr;</span>
              </h3>
              <div className="mt-5 flex rounded-3xl bg-white py-2.5 pr-2.5 shadow-xl shadow-blue-900/5 focus-within:ring-2 focus-within:ring-blue-900">
                <input
                  type="email"
                  required
                  placeholder="Email address"
                  aria-label="Email address"
                  className="-my-2.5 flex-auto bg-transparent pr-2.5 pl-6 text-base text-slate-900 placeholder:text-slate-400 focus:outline-hidden"
                />
                <Button type="submit">
                  <span className="sr-only sm:not-sr-only">Sign up today</span>
                  <span className="sm:hidden">
                    <ArrowRightIcon className="h-6 w-6" />
                  </span>
                </Button>
              </div>
            </form>
          </div>
        </div>
      </Container>
    </section>
  )
}
',
    'forms',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-keynote", "component_type": "forms", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Newsletter.tsx", "uses_components": ["Button"], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Ecommerce - Speakers - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Ecommerce - Speakers - Marketing',
    'Marketing/Landing page component from Tailwind Plus Keynote template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useEffect, useId, useState } from ''react''
import Image from ''next/image''
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from ''@headlessui/react''
import clsx from ''clsx''

import { Container } from ''@/components/Container''
import { DiamondIcon } from ''@/components/DiamondIcon''
import andrewGreeneImage from ''@/images/avatars/andrew-greene.jpg''
import cathleneBurrageImage from ''@/images/avatars/cathlene-burrage.jpg''
import damarisKimuraImage from ''@/images/avatars/damaris-kimura.jpg''
import dianneGuilianelliImage from ''@/images/avatars/dianne-guilianelli.jpg''
import erhartCockrinImage from ''@/images/avatars/erhart-cockrin.jpg''
import giordanoSagucioImage from ''@/images/avatars/giordano-sagucio.jpg''
import gordonSandersonImage from ''@/images/avatars/gordon-sanderson.jpg''
import heatherTerryImage from ''@/images/avatars/heather-terry.jpg''
import ibrahimFraschImage from ''@/images/avatars/ibrahim-frasch.jpg''
import jaquelinIschImage from ''@/images/avatars/jaquelin-isch.jpg''
import kimberlyParsonsImage from ''@/images/avatars/kimberly-parsons.jpg''
import parkerJohnsonImage from ''@/images/avatars/parker-johnson.jpg''
import piersWilkinsImage from ''@/images/avatars/piers-wilkins.jpg''
import richardAstley from ''@/images/avatars/richard-astley.jpg''
import rinaldoBeynonImage from ''@/images/avatars/rinaldo-beynon.jpg''
import ronniCantadoreImage from ''@/images/avatars/ronni-cantadore.jpg''
import stevenMchailImage from ''@/images/avatars/steven-mchail.jpg''
import waylonHydenImage from ''@/images/avatars/waylon-hyden.jpg''

const days = [
  {
    name: ''Opening Day'',
    date: ''April 4'',
    dateTime: ''2022-04-04'',
    speakers: [
      {
        name: ''Steven McHail'',
        role: ''Designer at Globex Corporation'',
        image: stevenMchailImage,
      },
      {
        name: ''Jaquelin Isch'',
        role: ''UX Design at InGen'',
        image: jaquelinIschImage,
      },
      {
        name: ''Dianne Guilianelli'',
        role: ''General Manager at Initech'',
        image: dianneGuilianelliImage,
      },
      {
        name: ''Ronni Cantadore'',
        role: ''Design Engineer at Weyland-Yutani'',
        image: ronniCantadoreImage,
      },
      {
        name: ''Erhart Cockrin'',
        role: ''Product Lead at Cyberdyne Systems'',
        image: erhartCockrinImage,
      },
      {
        name: ''Parker Johnson'',
        role: ''UI Designer at MomCorp'',
        image: parkerJohnsonImage,
      },
    ],
  },
  {
    name: ''Speakers & Workshops'',
    date: ''April 5'',
    dateTime: ''2022-04-05'',
    speakers: [
      {
        name: ''Damaris Kimura'',
        role: ''Senior Engineer at OCP'',
        image: damarisKimuraImage,
      },
      {
        name: ''Ibrahim Frasch'',
        role: ''Programmer at Umbrella Corp'',
        image: ibrahimFraschImage,
      },
      {
        name: ''Cathlene Burrage'',
        role: ''Frontend Developer at Buy n Large'',
        image: cathleneBurrageImage,
      },
      {
        name: ''Rinaldo Beynon'',
        role: ''Data Scientist at Rekall'',
        image: rinaldoBeynonImage,
      },
      {
        name: ''Waylon Hyden'',
        role: ''DevOps at RDA Corporation'',
        image: waylonHydenImage,
      },
      {
        name: ''Giordano Sagucio'',
        role: ''Game Developer at Soylent Corp'',
        image: giordanoSagucioImage,
      },
    ],
  },
  {
    name: ''Interviews'',
    date: ''April 6'',
    dateTime: ''2022-04-06'',
    speakers: [
      {
        name: ''Andrew Greene'',
        role: ''Frontend Developer at Ultratech'',
        image: andrewGreeneImage,
      },
      {
        name: ''Heather Terry'',
        role: ''Backend Developer at Xanatos Enterprises'',
        image: heatherTerryImage,
      },
      {
        name: ''Piers Wilkins'',
        role: ''Full stack Developer at BiffCo'',
        image: piersWilkinsImage,
      },
      {
        name: ''Gordon Sanderson'',
        role: ''Mobile Developer at Cobra Industries'',
        image: gordonSandersonImage,
      },
      {
        name: ''Kimberly Parsons'',
        role: ''Game Developer at Tyrell Corporation'',
        image: kimberlyParsonsImage,
      },
      {
        name: ''Richard Astley'',
        role: ''CEO at Roll Out'',
        image: richardAstley,
      },
    ],
  },
]

function ImageClipPaths({
  id,
  ...props
}: React.ComponentPropsWithoutRef<''svg''> & { id: string }) {
  return (
    <svg aria-hidden="true" width={0} height={0} {...props}>
      <defs>
        <clipPath id={`${id}-0`} clipPathUnits="objectBoundingBox">
          <path d="M0,0 h0.729 v0.129 h0.121 l-0.016,0.032 C0.815,0.198,0.843,0.243,0.885,0.243 H1 v0.757 H0.271 v-0.086 l-0.121,0.057 v-0.214 c0,-0.032,-0.026,-0.057,-0.057,-0.057 H0 V0" />
        </clipPath>
        <clipPath id={`${id}-1`} clipPathUnits="objectBoundingBox">
          <path d="M1,1 H0.271 v-0.129 H0.15 l0.016,-0.032 C0.185,0.802,0.157,0.757,0.115,0.757 H0 V0 h0.729 v0.086 l0.121,-0.057 v0.214 c0,0.032,0.026,0.057,0.057,0.057 h0.093 v0.7" />
        </clipPath>
        <clipPath id={`${id}-2`} clipPathUnits="objectBoundingBox">
          <path d="M1,0 H0.271 v0.129 H0.15 l0.016,0.032 C0.185,0.198,0.157,0.243,0.115,0.243 H0 v0.757 h0.729 v-0.086 l0.121,0.057 v-0.214 c0,-0.032,0.026,-0.057,0.057,-0.057 h0.093 V0" />
        </clipPath>
      </defs>
    </svg>
  )
}

export function Speakers() {
  let id = useId()
  let [tabOrientation, setTabOrientation] = useState(''horizontal'')

  useEffect(() => {
    let lgMediaQuery = window.matchMedia(''(min-width: 1024px)'')

    function onMediaQueryChange({ matches }: { matches: boolean }) {
      setTabOrientation(matches ? ''vertical'' : ''horizontal'')
    }

    onMediaQueryChange(lgMediaQuery)
    lgMediaQuery.addEventListener(''change'', onMediaQueryChange)

    return () => {
      lgMediaQuery.removeEventListener(''change'', onMediaQueryChange)
    }
  }, [])

  return (
    <section
      id="speakers"
      aria-labelledby="speakers-title"
      className="py-20 sm:py-32"
    >
      <ImageClipPaths id={id} />
      <Container>
        <div className="mx-auto max-w-2xl lg:mx-0">
          <h2
            id="speakers-title"
            className="font-display text-4xl font-medium tracking-tighter text-blue-600 sm:text-5xl"
          >
            Speakers
          </h2>
          <p className="mt-4 font-display text-2xl tracking-tight text-blue-900">
            Learn from the experts on the cutting-edge of deception at the most
            sinister companies.
          </p>
        </div>
        <TabGroup
          className="mt-14 grid grid-cols-1 items-start gap-x-8 gap-y-8 sm:mt-16 sm:gap-y-16 lg:mt-24 lg:grid-cols-4"
          vertical={tabOrientation === ''vertical''}
        >
          <div className="relative -mx-4 flex overflow-x-auto pb-4 sm:mx-0 sm:block sm:overflow-visible sm:pb-0">
            <div className="absolute top-2 bottom-0 left-0.5 hidden w-px bg-slate-200 lg:block" />
            <TabList className="grid auto-cols-auto grid-flow-col justify-start gap-x-8 gap-y-10 px-4 whitespace-nowrap sm:mx-auto sm:max-w-2xl sm:grid-cols-3 sm:px-0 sm:text-center lg:grid-flow-row lg:grid-cols-1 lg:text-left">
              {({ selectedIndex }) => (
                <>
                  {days.map((day, dayIndex) => (
                    <div key={day.dateTime} className="relative lg:pl-8">
                      <DiamondIcon
                        className={clsx(
                          ''absolute top-2.25 left-[-0.5px] hidden h-1.5 w-1.5 overflow-visible lg:block'',
                          dayIndex === selectedIndex
                            ? ''fill-blue-600 stroke-blue-600''
                            : ''fill-transparent stroke-slate-400'',
                        )}
                      />
                      <div className="relative">
                        <div
                          className={clsx(
                            ''font-mono text-sm'',
                            dayIndex === selectedIndex
                              ? ''text-blue-600''
                              : ''text-slate-500'',
                          )}
                        >
                          <Tab className="data-selected:not-data-focus:outline-hidden">
                            <span className="absolute inset-0" />
                            {day.name}
                          </Tab>
                        </div>
                        <time
                          dateTime={day.dateTime}
                          className="mt-1.5 block text-2xl font-semibold tracking-tight text-blue-900"
                        >
                          {day.date}
                        </time>
                      </div>
                    </div>
                  ))}
                </>
              )}
            </TabList>
          </div>
          <TabPanels className="lg:col-span-3">
            {days.map((day) => (
              <TabPanel
                key={day.dateTime}
                className="grid grid-cols-1 gap-x-8 gap-y-10 data-selected:not-data-focus:outline-hidden sm:grid-cols-2 sm:gap-y-16 md:grid-cols-3"
                unmount={false}
              >
                {day.speakers.map((speaker, speakerIndex) => (
                  <div key={speakerIndex}>
                    <div className="group relative h-70 transform overflow-hidden rounded-4xl">
                      <div
                        className={clsx(
                          ''absolute top-0 right-4 bottom-6 left-0 rounded-4xl border transition duration-300 group-hover:scale-95 xl:right-6'',
                          [
                            ''border-blue-300'',
                            ''border-indigo-300'',
                            ''border-sky-300'',
                          ][speakerIndex % 3],
                        )}
                      />
                      <div
                        className="absolute inset-0 bg-indigo-50"
                        style={{ clipPath: `url(#${id}-${speakerIndex % 3})` }}
                      >
                        <Image
                          className="absolute inset-0 h-full w-full object-cover transition duration-300 group-hover:scale-110"
                          src={speaker.image}
                          alt=""
                          priority
                          sizes="(min-width: 1280px) 17.5rem, (min-width: 1024px) 25vw, (min-width: 768px) 33vw, (min-width: 640px) 50vw, 100vw"
                        />
                      </div>
                    </div>
                    <h3 className="mt-8 font-display text-xl font-bold tracking-tight text-slate-900">
                      {speaker.name}
                    </h3>
                    <p className="mt-1 text-base tracking-tight text-slate-500">
                      {speaker.role}
                    </p>
                  </div>
                ))}
              </TabPanel>
            ))}
          </TabPanels>
        </TabGroup>
      </Container>
    </section>
  )
}
',
    'ecommerce',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'ecommerce', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-keynote", "component_type": "ecommerce", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Speakers.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Error - Layout - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Error - Layout - Marketing',
    'Marketing/Landing page component from Tailwind Plus Keynote template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import { DM_Sans, Inter } from ''next/font/google''
import clsx from ''clsx''

import ''@/styles/tailwind.css''

const inter = Inter({
  subsets: [''latin''],
  display: ''swap'',
  variable: ''--font-inter'',
})

const dmSans = DM_Sans({
  subsets: [''latin''],
  weight: [''400'', ''500'', ''700''],
  display: ''swap'',
  variable: ''--font-dm-sans'',
})

export const metadata: Metadata = {
  title: {
    template: ''%s - DeceptiConf'',
    default: ''DeceptiConf - A community-driven design conference'',
  },
  description:
    ''At DeceptiConf you’ll learn about the latest dark patterns being developed to trick even the smartest visitors, and you’ll learn how to deploy them without ever being detected.'',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="en"
      className={clsx(
        ''h-full bg-white antialiased'',
        inter.variable,
        dmSans.variable,
      )}
    >
      <body className="flex min-h-full">
        <div className="flex w-full flex-col">{children}</div>
      </body>
    </html>
  )
}
',
    'error',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'error', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/font/google", "clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-keynote", "component_type": "error", "file_path": "tailwind-plus-keynote/keynote-ts/src/app/layout.tsx", "uses_components": [], "dependencies": ["next/font/google", "clsx"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Authlayout - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Authlayout - Marketing',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Link from ''next/link''

import { CirclesBackground } from ''@/components/CirclesBackground''
import { Logo } from ''@/components/Logo''

export function AuthLayout({
  title,
  subtitle,
  children,
}: {
  title: string
  subtitle: React.ReactNode
  children: React.ReactNode
}) {
  return (
    <main className="flex min-h-full overflow-hidden pt-16 sm:py-28">
      <div className="mx-auto flex w-full max-w-2xl flex-col px-4 sm:px-6">
        <Link href="/" aria-label="Home">
          <Logo className="mx-auto h-10 w-auto" />
        </Link>
        <div className="relative mt-12 sm:mt-16">
          <CirclesBackground
            width="1090"
            height="1090"
            className="absolute -top-7 left-1/2 -z-10 h-[788px] -translate-x-1/2 mask-[linear-gradient(to_bottom,white_20%,transparent_75%)] stroke-gray-300/30 sm:-top-9 sm:h-auto"
          />
          <h1 className="text-center text-2xl font-medium tracking-tight text-gray-900">
            {title}
          </h1>
          {subtitle && (
            <p className="mt-3 text-center text-lg text-gray-600">{subtitle}</p>
          )}
        </div>
        <div className="-mx-4 mt-10 flex-auto bg-white px-4 py-10 shadow-2xl shadow-gray-900/10 sm:mx-0 sm:flex-none sm:rounded-5xl sm:p-24">
          {children}
        </div>
      </div>
    </main>
  )
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "auth", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/AuthLayout.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Faqs - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Faqs - Marketing',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Container } from ''@/components/Container''

const faqs = [
  [
    {
      question: ''How do I know the tips are good?'',
      answer:
        ''Our whole business depends on our tips being good, so it’s in our best interest that they are. The results of our customers speak for themselves, just trust us.'',
    },
    {
      question: ''Isn’t this insider trading?'',
      answer:
        ''Yes exactly. But at scale! Historically you could only make insider trades with knowledge from your direct network. Pocket brings you insider trading tips from people you don’t even know.'',
    },
    {
      question: ''But isn’t insider trading illegal?'',
      answer:
        ''Here’s the thing: you’re the one doing the insider trading, not us. We’re just giving you the tips and some tools to make trades. We’re not doing anything wrong here.'',
    },
  ],
  [
    {
      question: ''Do the people giving you tips realize what they are doing?'',
      answer:
        ''Again I would argue this isn’t really our responsibility. People make their own choices. If they don’t research the consequences that’s on them, not on us.'',
    },
    {
      question: ''Where is Pocket based?'',
      answer:
        ''Let’s just say it’s not somewhere where the SEC is going to find us.'',
    },
    {
      question: ''Is there any age limit to trading on Pocket?'',
      answer:
        ''For our free plan, the age limit is based on the minimum age to trade in your country of residence. Our VIP plan uses advanced transaction anonymization though, so you can use that plan even if you’re 9 years old. Or a dog.'',
    },
  ],
  [
    {
      question: ''How did you get this on the App Store?'',
      answer:
        ''Honestly we were surprised too, but eventually we found out that the app reviewer found the app so compelling they approved it just so they could use it themselves.'',
    },
    {
      question: ''How do I explain the money I withdraw from Pocket to the IRS?'',
      answer:
        ''This feels like one-hundred percent a you problem. Pocket is not responsible in any way for your tax returns.'',
    },
    {
      question: ''How do I become an insider?'',
      answer:
        ''Contact us with some details about your industry and the type of access you have to apply for an insider account. Once approved, we’ll send you a guide on collecting insider information without being detected at work.'',
    },
  ],
]

export function Faqs() {
  return (
    <section
      id="faqs"
      aria-labelledby="faqs-title"
      className="border-t border-gray-200 py-20 sm:py-32"
    >
      <Container>
        <div className="mx-auto max-w-2xl lg:mx-0">
          <h2
            id="faqs-title"
            className="text-3xl font-medium tracking-tight text-gray-900"
          >
            Frequently asked questions
          </h2>
          <p className="mt-2 text-lg text-gray-600">
            If you have anything else you want to ask,{'' ''}
            <a
              href="mailto:info@example.com"
              className="text-gray-900 underline"
            >
              reach out to us
            </a>
            .
          </p>
        </div>
        <ul
          role="list"
          className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 sm:mt-20 lg:max-w-none lg:grid-cols-3"
        >
          {faqs.map((column, columnIndex) => (
            <li key={columnIndex}>
              <ul role="list" className="space-y-10">
                {column.map((faq, faqIndex) => (
                  <li key={faqIndex}>
                    <h3 className="text-lg/6 font-semibold text-gray-900">
                      {faq.question}
                    </h3>
                    <p className="mt-4 text-sm text-gray-700">{faq.answer}</p>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
',
    'faq',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'faq', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "faq", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Faqs.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Pocket
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Pocket',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image from ''next/image''
import Link from ''next/link''

import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { TextField } from ''@/components/Fields''
import { Logomark } from ''@/components/Logo''
import { NavLinks } from ''@/components/NavLinks''
import qrCode from ''@/images/qr-code.svg''

function QrCodeBorder(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 96 96" fill="none" aria-hidden="true" {...props}>
      <path
        d="M1 17V9a8 8 0 0 1 8-8h8M95 17V9a8 8 0 0 0-8-8h-8M1 79v8a8 8 0 0 0 8 8h8M95 79v8a8 8 0 0 1-8 8h-8"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  )
}

export function Footer() {
  return (
    <footer className="border-t border-gray-200">
      <Container>
        <div className="flex flex-col items-start justify-between gap-y-12 pt-16 pb-6 lg:flex-row lg:items-center lg:py-16">
          <div>
            <div className="flex items-center text-gray-900">
              <Logomark className="h-10 w-10 flex-none fill-cyan-500" />
              <div className="ml-4">
                <p className="text-base font-semibold">Pocket</p>
                <p className="mt-1 text-sm">Invest at the perfect time.</p>
              </div>
            </div>
            <nav className="mt-11 flex gap-8">
              <NavLinks />
            </nav>
          </div>
          <div className="group relative -mx-4 flex items-center self-stretch p-4 transition-colors hover:bg-gray-100 sm:self-auto sm:rounded-2xl lg:mx-0 lg:self-auto lg:p-6">
            <div className="relative flex h-24 w-24 flex-none items-center justify-center">
              <QrCodeBorder className="absolute inset-0 h-full w-full stroke-gray-300 transition-colors group-hover:stroke-cyan-500" />
              <Image src={qrCode} alt="" unoptimized />
            </div>
            <div className="ml-8 lg:w-64">
              <p className="text-base font-semibold text-gray-900">
                <Link href="#">
                  <span className="absolute inset-0 sm:rounded-2xl" />
                  Download the app
                </Link>
              </p>
              <p className="mt-1 text-sm text-gray-700">
                Scan the QR code to download the app from the App Store.
              </p>
            </div>
          </div>
        </div>
        <div className="flex flex-col items-center border-t border-gray-200 pt-8 pb-12 md:flex-row-reverse md:justify-between md:pt-6">
          <form className="flex w-full justify-center md:w-auto">
            <TextField
              type="email"
              aria-label="Email address"
              placeholder="Email address"
              autoComplete="email"
              required
              className="w-60 min-w-0 shrink"
            />
            <Button type="submit" color="cyan" className="ml-4 flex-none">
              <span className="hidden lg:inline">Join our newsletter</span>
              <span className="lg:hidden">Join newsletter</span>
            </Button>
          </form>
          <p className="mt-6 text-sm text-gray-500 md:mt-0">
            &copy; Copyright {new Date().getFullYear()}. All rights reserved.
          </p>
        </div>
      </Container>
    </footer>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "footer", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Footer.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Pocket
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Pocket',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import Link from ''next/link''
import {
  Popover,
  PopoverButton,
  PopoverBackdrop,
  PopoverPanel,
} from ''@headlessui/react''
import { AnimatePresence, motion } from ''framer-motion''

import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { Logo } from ''@/components/Logo''
import { NavLinks } from ''@/components/NavLinks''

function MenuIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path
        d="M5 6h14M5 18h14M5 12h14"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function ChevronUpIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path
        d="M17 14l-5-5-5 5"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function MobileNavLink(
  props: Omit<
    React.ComponentPropsWithoutRef<typeof PopoverButton<typeof Link>>,
    ''as'' | ''className''
  >,
) {
  return (
    <PopoverButton
      as={Link}
      className="block text-base/7 tracking-tight text-gray-700"
      {...props}
    />
  )
}

export function Header() {
  return (
    <header>
      <nav>
        <Container className="relative z-50 flex justify-between py-8">
          <div className="relative z-10 flex items-center gap-16">
            <Link href="/" aria-label="Home">
              <Logo className="h-10 w-auto" />
            </Link>
            <div className="hidden lg:flex lg:gap-10">
              <NavLinks />
            </div>
          </div>
          <div className="flex items-center gap-6">
            <Popover className="lg:hidden">
              {({ open }) => (
                <>
                  <PopoverButton
                    className="relative z-10 -m-2 inline-flex items-center rounded-lg stroke-gray-900 p-2 hover:bg-gray-200/50 hover:stroke-gray-600 focus:not-data-focus:outline-hidden active:stroke-gray-900"
                    aria-label="Toggle site navigation"
                  >
                    {({ open }) =>
                      open ? (
                        <ChevronUpIcon className="h-6 w-6" />
                      ) : (
                        <MenuIcon className="h-6 w-6" />
                      )
                    }
                  </PopoverButton>
                  <AnimatePresence initial={false}>
                    {open && (
                      <>
                        <PopoverBackdrop
                          static
                          as={motion.div}
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                          className="fixed inset-0 z-0 bg-gray-300/60 backdrop-blur-sm"
                        />
                        <PopoverPanel
                          static
                          as={motion.div}
                          initial={{ opacity: 0, y: -32 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{
                            opacity: 0,
                            y: -32,
                            transition: { duration: 0.2 },
                          }}
                          className="absolute inset-x-0 top-0 z-0 origin-top rounded-b-2xl bg-gray-50 px-6 pt-32 pb-6 shadow-2xl shadow-gray-900/20"
                        >
                          <div className="space-y-4">
                            <MobileNavLink href="/#features">
                              Features
                            </MobileNavLink>
                            <MobileNavLink href="/#reviews">
                              Reviews
                            </MobileNavLink>
                            <MobileNavLink href="/#pricing">
                              Pricing
                            </MobileNavLink>
                            <MobileNavLink href="/#faqs">FAQs</MobileNavLink>
                          </div>
                          <div className="mt-8 flex flex-col gap-4">
                            <Button href="/login" variant="outline">
                              Log in
                            </Button>
                            <Button href="#">Download the app</Button>
                          </div>
                        </PopoverPanel>
                      </>
                    )}
                  </AnimatePresence>
                </>
              )}
            </Popover>
            <div className="flex items-center gap-6 max-lg:hidden">
              <Button href="/login" variant="outline">
                Log in
              </Button>
              <Button href="#">Download</Button>
            </div>
          </div>
        </Container>
      </nav>
    </header>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "framer-motion"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "hero", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "framer-motion"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Pocket
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Pocket',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { useId } from ''react''
import Image from ''next/image''
import clsx from ''clsx''

import { AppDemo } from ''@/components/AppDemo''
import { AppStoreLink } from ''@/components/AppStoreLink''
import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { PhoneFrame } from ''@/components/PhoneFrame''
import logoBbc from ''@/images/logos/bbc.svg''
import logoCbs from ''@/images/logos/cbs.svg''
import logoCnn from ''@/images/logos/cnn.svg''
import logoFastCompany from ''@/images/logos/fast-company.svg''
import logoForbes from ''@/images/logos/forbes.svg''
import logoHuffpost from ''@/images/logos/huffpost.svg''
import logoTechcrunch from ''@/images/logos/techcrunch.svg''
import logoWired from ''@/images/logos/wired.svg''

function BackgroundIllustration(props: React.ComponentPropsWithoutRef<''div''>) {
  let id = useId()

  return (
    <div {...props}>
      <svg
        viewBox="0 0 1026 1026"
        fill="none"
        aria-hidden="true"
        className="absolute inset-0 h-full w-full animate-spin-slow"
      >
        <path
          d="M1025 513c0 282.77-229.23 512-512 512S1 795.77 1 513 230.23 1 513 1s512 229.23 512 512Z"
          stroke="#D4D4D4"
          strokeOpacity="0.7"
        />
        <path
          d="M513 1025C230.23 1025 1 795.77 1 513"
          stroke={`url(#${id}-gradient-1)`}
          strokeLinecap="round"
        />
        <defs>
          <linearGradient
            id={`${id}-gradient-1`}
            x1="1"
            y1="513"
            x2="1"
            y2="1025"
            gradientUnits="userSpaceOnUse"
          >
            <stop stopColor="#06b6d4" />
            <stop offset="1" stopColor="#06b6d4" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
      <svg
        viewBox="0 0 1026 1026"
        fill="none"
        aria-hidden="true"
        className="absolute inset-0 h-full w-full animate-spin-reverse-slower"
      >
        <path
          d="M913 513c0 220.914-179.086 400-400 400S113 733.914 113 513s179.086-400 400-400 400 179.086 400 400Z"
          stroke="#D4D4D4"
          strokeOpacity="0.7"
        />
        <path
          d="M913 513c0 220.914-179.086 400-400 400"
          stroke={`url(#${id}-gradient-2)`}
          strokeLinecap="round"
        />
        <defs>
          <linearGradient
            id={`${id}-gradient-2`}
            x1="913"
            y1="513"
            x2="913"
            y2="913"
            gradientUnits="userSpaceOnUse"
          >
            <stop stopColor="#06b6d4" />
            <stop offset="1" stopColor="#06b6d4" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  )
}

function PlayIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <circle cx="12" cy="12" r="11.5" stroke="#D4D4D4" />
      <path
        d="M9.5 14.382V9.618a.5.5 0 0 1 .724-.447l4.764 2.382a.5.5 0 0 1 0 .894l-4.764 2.382a.5.5 0 0 1-.724-.447Z"
        fill="#A3A3A3"
        stroke="#A3A3A3"
      />
    </svg>
  )
}

export function Hero() {
  return (
    <div className="overflow-hidden py-20 sm:py-32 lg:pb-32 xl:pb-36">
      <Container>
        <div className="lg:grid lg:grid-cols-12 lg:gap-x-8 lg:gap-y-20">
          <div className="relative z-10 mx-auto max-w-2xl lg:col-span-7 lg:max-w-none lg:pt-6 xl:col-span-6">
            <h1 className="text-4xl font-medium tracking-tight text-gray-900">
              Invest at the perfect time.
            </h1>
            <p className="mt-6 text-lg text-gray-600">
              By leveraging insights from our network of industry insiders,
              you’ll know exactly when to buy to maximize profit, and exactly
              when to sell to avoid painful losses.
            </p>
            <div className="mt-8 flex flex-wrap gap-x-6 gap-y-4">
              <AppStoreLink />
              <Button
                href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                variant="outline"
              >
                <PlayIcon className="h-6 w-6 flex-none" />
                <span className="ml-2.5">Watch the video</span>
              </Button>
            </div>
          </div>
          <div className="relative mt-10 sm:mt-20 lg:col-span-5 lg:row-span-2 lg:mt-0 xl:col-span-6">
            <BackgroundIllustration className="absolute top-4 left-1/2 h-[1026px] w-[1026px] -translate-x-1/3 mask-[linear-gradient(to_bottom,white_20%,transparent_75%)] stroke-gray-300/70 sm:top-16 sm:-translate-x-1/2 lg:-top-16 lg:ml-12 xl:-top-14 xl:ml-0" />
            <div className="-mx-4 h-[448px] mask-[linear-gradient(to_bottom,white_60%,transparent)] px-9 sm:mx-0 lg:absolute lg:-inset-x-10 lg:-top-10 lg:-bottom-20 lg:h-auto lg:px-0 lg:pt-10 xl:-bottom-32">
              <PhoneFrame className="mx-auto max-w-[366px]" priority>
                <AppDemo />
              </PhoneFrame>
            </div>
          </div>
          <div className="relative -mt-4 lg:col-span-7 lg:mt-0 xl:col-span-6">
            <p className="text-center text-sm font-semibold text-gray-900 lg:text-left">
              As featured in
            </p>
            <ul
              role="list"
              className="mx-auto mt-8 flex max-w-xl flex-wrap justify-center gap-x-10 gap-y-8 lg:mx-0 lg:justify-start"
            >
              {[
                [''Forbes'', logoForbes],
                [''TechCrunch'', logoTechcrunch],
                [''Wired'', logoWired],
                [''CNN'', logoCnn, ''hidden xl:block''],
                [''BBC'', logoBbc],
                [''CBS'', logoCbs],
                [''Fast Company'', logoFastCompany],
                [''HuffPost'', logoHuffpost, ''hidden xl:block''],
              ].map(([name, logo, className]) => (
                <li key={name} className={clsx(''flex'', className)}>
                  <Image src={logo} alt={name} className="h-8" unoptimized />
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Container>
    </div>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["clsx", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "hero", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": ["clsx", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Navigation - Pocket
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Navigation - Pocket',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useRef, useState } from ''react''
import Link from ''next/link''
import { AnimatePresence, motion } from ''framer-motion''

export function NavLinks() {
  let [hoveredIndex, setHoveredIndex] = useState<number | null>(null)
  let timeoutRef = useRef<number | null>(null)

  return [
    [''Features'', ''/#features''],
    [''Reviews'', ''/#reviews''],
    [''Pricing'', ''/#pricing''],
    [''FAQs'', ''/#faqs''],
  ].map(([label, href], index) => (
    <Link
      key={label}
      href={href}
      className="relative -mx-3 -my-2 rounded-lg px-3 py-2 text-sm text-gray-700 transition-colors delay-150 hover:text-gray-900 hover:delay-0"
      onMouseEnter={() => {
        if (timeoutRef.current) {
          window.clearTimeout(timeoutRef.current)
        }
        setHoveredIndex(index)
      }}
      onMouseLeave={() => {
        timeoutRef.current = window.setTimeout(() => {
          setHoveredIndex(null)
        }, 200)
      }}
    >
      <AnimatePresence>
        {hoveredIndex === index && (
          <motion.span
            className="absolute inset-0 rounded-lg bg-gray-100"
            layoutId="hoverBackground"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1, transition: { duration: 0.15 } }}
            exit={{
              opacity: 0,
              transition: { duration: 0.15 },
            }}
          />
        )}
      </AnimatePresence>
      <span className="relative z-10">{label}</span>
    </Link>
  ))
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "framer-motion"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "navigation", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/NavLinks.tsx", "uses_components": [], "dependencies": ["next/link", "framer-motion"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Pricing Section - Pocket
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Pricing Section - Pocket',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useState } from ''react''
import { Radio, RadioGroup } from ''@headlessui/react''
import clsx from ''clsx''

import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { Logomark } from ''@/components/Logo''

const plans = [
  {
    name: ''Starter'',
    featured: false,
    price: { Monthly: ''$0'', Annually: ''$0'' },
    description:
      ''You’re new to investing but want to do it right. Get started for free.'',
    button: {
      label: ''Get started for free'',
      href: ''/register'',
    },
    features: [
      ''Commission-free trading'',
      ''Multi-layered encryption'',
      ''One tip every day'',
      ''Invest up to $1,500 each month'',
    ],
    logomarkClassName: ''fill-gray-300'',
  },
  {
    name: ''Investor'',
    featured: false,
    price: { Monthly: ''$7'', Annually: ''$70'' },
    description:
      ''You’ve been investing for a while. Invest more and grow your wealth faster.'',
    button: {
      label: ''Subscribe'',
      href: ''/register'',
    },
    features: [
      ''Commission-free trading'',
      ''Multi-layered encryption'',
      ''One tip every hour'',
      ''Invest up to $15,000 each month'',
      ''Basic transaction anonymization'',
    ],
    logomarkClassName: ''fill-gray-500'',
  },
  {
    name: ''VIP'',
    featured: true,
    price: { Monthly: ''$199'', Annually: ''$1,990'' },
    description:
      ''You’ve got a huge amount of assets but it’s not enough. To the moon.'',
    button: {
      label: ''Subscribe'',
      href: ''/register'',
    },
    features: [
      ''Commission-free trading'',
      ''Multi-layered encryption'',
      ''Real-time tip notifications'',
      ''No investment limits'',
      ''Advanced transaction anonymization'',
      ''Automated tax-loss harvesting'',
    ],
    logomarkClassName: ''fill-cyan-500'',
  },
]

function CheckIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        d="M9.307 12.248a.75.75 0 1 0-1.114 1.004l1.114-1.004ZM11 15.25l-.557.502a.75.75 0 0 0 1.15-.043L11 15.25Zm4.844-5.041a.75.75 0 0 0-1.188-.918l1.188.918Zm-7.651 3.043 2.25 2.5 1.114-1.004-2.25-2.5-1.114 1.004Zm3.4 2.457 4.25-5.5-1.187-.918-4.25 5.5 1.188.918Z"
        fill="currentColor"
      />
      <circle
        cx="12"
        cy="12"
        r="8.25"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function Plan({
  name,
  price,
  description,
  button,
  features,
  activePeriod,
  logomarkClassName,
  featured = false,
}: {
  name: string
  price: {
    Monthly: string
    Annually: string
  }
  description: string
  button: {
    label: string
    href: string
  }
  features: Array<string>
  activePeriod: ''Monthly'' | ''Annually''
  logomarkClassName?: string
  featured?: boolean
}) {
  return (
    <section
      className={clsx(
        ''flex flex-col overflow-hidden rounded-3xl p-6 shadow-lg shadow-gray-900/5'',
        featured ? ''order-first bg-gray-900 lg:order-none'' : ''bg-white'',
      )}
    >
      <h3
        className={clsx(
          ''flex items-center text-sm font-semibold'',
          featured ? ''text-white'' : ''text-gray-900'',
        )}
      >
        <Logomark className={clsx(''h-6 w-6 flex-none'', logomarkClassName)} />
        <span className="ml-4">{name}</span>
      </h3>
      <p
        className={clsx(
          ''relative mt-5 flex text-3xl tracking-tight'',
          featured ? ''text-white'' : ''text-gray-900'',
        )}
      >
        {price.Monthly === price.Annually ? (
          price.Monthly
        ) : (
          <>
            <span
              aria-hidden={activePeriod === ''Annually''}
              className={clsx(
                ''transition duration-300'',
                activePeriod === ''Annually'' &&
                  ''pointer-events-none translate-x-6 opacity-0 select-none'',
              )}
            >
              {price.Monthly}
            </span>
            <span
              aria-hidden={activePeriod === ''Monthly''}
              className={clsx(
                ''absolute top-0 left-0 transition duration-300'',
                activePeriod === ''Monthly'' &&
                  ''pointer-events-none -translate-x-6 opacity-0 select-none'',
              )}
            >
              {price.Annually}
            </span>
          </>
        )}
      </p>
      <p
        className={clsx(
          ''mt-3 text-sm'',
          featured ? ''text-gray-300'' : ''text-gray-700'',
        )}
      >
        {description}
      </p>
      <div className="order-last mt-6">
        <ul
          role="list"
          className={clsx(
            ''-my-2 divide-y text-sm'',
            featured
              ? ''divide-gray-800 text-gray-300''
              : ''divide-gray-200 text-gray-700'',
          )}
        >
          {features.map((feature) => (
            <li key={feature} className="flex py-2">
              <CheckIcon
                className={clsx(
                  ''h-6 w-6 flex-none'',
                  featured ? ''text-white'' : ''text-cyan-500'',
                )}
              />
              <span className="ml-4">{feature}</span>
            </li>
          ))}
        </ul>
      </div>
      <Button
        href={button.href}
        color={featured ? ''cyan'' : ''gray''}
        className="mt-6"
        aria-label={`Get started with the ${name} plan for ${price}`}
      >
        {button.label}
      </Button>
    </section>
  )
}

export function Pricing() {
  let [activePeriod, setActivePeriod] = useState<''Monthly'' | ''Annually''>(
    ''Monthly'',
  )

  return (
    <section
      id="pricing"
      aria-labelledby="pricing-title"
      className="border-t border-gray-200 bg-gray-100 py-20 sm:py-32"
    >
      <Container>
        <div className="mx-auto max-w-2xl text-center">
          <h2
            id="pricing-title"
            className="text-3xl font-medium tracking-tight text-gray-900"
          >
            Flat pricing, no management fees.
          </h2>
          <p className="mt-2 text-lg text-gray-600">
            Whether you’re one person trying to get ahead or a big firm trying
            to take over the world, we’ve got a plan for you.
          </p>
        </div>

        <div className="mt-8 flex justify-center">
          <div className="relative">
            <RadioGroup
              value={activePeriod}
              onChange={setActivePeriod}
              className="grid grid-cols-2"
            >
              {[''Monthly'', ''Annually''].map((period) => (
                <Radio
                  key={period}
                  value={period}
                  className={clsx(
                    ''cursor-pointer border border-gray-300 px-[calc(--spacing(3)-1px)] py-[calc(--spacing(2)-1px)] text-sm text-gray-700 transition-colors hover:border-gray-400 data-focus:outline-2 data-focus:outline-offset-2'',
                    period === ''Monthly''
                      ? ''rounded-l-lg''
                      : ''-ml-px rounded-r-lg'',
                  )}
                >
                  {period}
                </Radio>
              ))}
            </RadioGroup>
            <div
              aria-hidden="true"
              className={clsx(
                ''pointer-events-none absolute inset-0 z-10 grid grid-cols-2 overflow-hidden rounded-lg bg-cyan-500 transition-all duration-300'',
                activePeriod === ''Monthly''
                  ? ''[clip-path:inset(0_50%_0_0)]''
                  : ''[clip-path:inset(0_0_0_calc(50%-1px))]'',
              )}
            >
              {[''Monthly'', ''Annually''].map((period) => (
                <div
                  key={period}
                  className={clsx(
                    ''py-2 text-center text-sm font-semibold text-white'',
                    period === ''Annually'' && ''-ml-px'',
                  )}
                >
                  {period}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 items-start gap-x-8 gap-y-10 sm:mt-20 lg:max-w-none lg:grid-cols-3">
          {plans.map((plan) => (
            <Plan key={plan.name} {...plan} activePeriod={activePeriod} />
          ))}
        </div>
      </Container>
    </section>
  )
}
',
    'pricing',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'pricing', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["clsx", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "pricing", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Pricing.tsx", "uses_components": ["Button"], "dependencies": ["clsx", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Primaryfeatures - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Primaryfeatures - Marketing',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { Fragment, useEffect, useId, useRef, useState } from ''react''
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from ''@headlessui/react''
import clsx from ''clsx''
import {
  type MotionProps,
  type Variant,
  type Variants,
  AnimatePresence,
  motion,
} from ''framer-motion''
import { useDebouncedCallback } from ''use-debounce''

import { AppScreen } from ''@/components/AppScreen''
import { CircleBackground } from ''@/components/CircleBackground''
import { Container } from ''@/components/Container''
import { PhoneFrame } from ''@/components/PhoneFrame''
import {
  DiageoLogo,
  LaravelLogo,
  MirageLogo,
  ReversableLogo,
  StatamicLogo,
  StaticKitLogo,
  TransistorLogo,
  TupleLogo,
} from ''@/components/StockLogos''

const MotionAppScreenHeader = motion(AppScreen.Header)
const MotionAppScreenBody = motion(AppScreen.Body)

interface CustomAnimationProps {
  isForwards: boolean
  changeCount: number
}

const features = [
  {
    name: ''Invite friends for better returns'',
    description:
      ''For every friend you invite to Pocket, you get insider notifications 5 seconds sooner. And it’s 10 seconds if you invite an insider.'',
    icon: DeviceUserIcon,
    screen: InviteScreen,
  },
  {
    name: ''Notifications on stock dips'',
    description:
      ''Get a push notification every time we find out something that’s going to lower the share price on your holdings so you can sell before the information hits the public markets.'',
    icon: DeviceNotificationIcon,
    screen: StocksScreen,
  },
  {
    name: ''Invest what you want'',
    description:
      ''We hide your stock purchases behind thousands of anonymous trading accounts, so suspicious activity can never be traced back to you.'',
    icon: DeviceTouchIcon,
    screen: InvestScreen,
  },
]

function DeviceUserIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" {...props}>
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M16 23a3 3 0 100-6 3 3 0 000 6zm-1 2a4 4 0 00-4 4v1a2 2 0 002 2h6a2 2 0 002-2v-1a4 4 0 00-4-4h-2z"
        fill="#737373"
      />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M5 4a4 4 0 014-4h14a4 4 0 014 4v24a4.002 4.002 0 01-3.01 3.877c-.535.136-.99-.325-.99-.877s.474-.98.959-1.244A2 2 0 0025 28V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9a2 2 0 00-2 2v24a2 2 0 001.041 1.756C8.525 30.02 9 30.448 9 31s-.455 1.013-.99.877A4.002 4.002 0 015 28V4z"
        fill="#A3A3A3"
      />
    </svg>
  )
}

function DeviceNotificationIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" {...props}>
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M9 0a4 4 0 00-4 4v24a4 4 0 004 4h14a4 4 0 004-4V4a4 4 0 00-4-4H9zm0 2a2 2 0 00-2 2v24a2 2 0 002 2h14a2 2 0 002-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9z"
        fill="#A3A3A3"
      />
      <path
        d="M9 8a2 2 0 012-2h10a2 2 0 012 2v2a2 2 0 01-2 2H11a2 2 0 01-2-2V8z"
        fill="#737373"
      />
    </svg>
  )
}

function DeviceTouchIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  let id = useId()

  return (
    <svg viewBox="0 0 32 32" fill="none" aria-hidden="true" {...props}>
      <defs>
        <linearGradient
          id={`${id}-gradient`}
          x1={14}
          y1={14.5}
          x2={7}
          y2={17}
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#737373" />
          <stop offset={1} stopColor="#D4D4D4" stopOpacity={0} />
        </linearGradient>
      </defs>
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M5 4a4 4 0 014-4h14a4 4 0 014 4v13h-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9a2 2 0 00-2 2v24a2 2 0 002 2h4v2H9a4 4 0 01-4-4V4z"
        fill="#A3A3A3"
      />
      <path
        d="M7 22c0-4.694 3.5-8 8-8"
        stroke={`url(#${id}-gradient)`}
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M21 20l.217-5.513a1.431 1.431 0 00-2.85-.226L17.5 21.5l-1.51-1.51a2.107 2.107 0 00-2.98 0 .024.024 0 00-.005.024l3.083 9.25A4 4 0 0019.883 32H25a4 4 0 004-4v-5a3 3 0 00-3-3h-5z"
        fill="#A3A3A3"
      />
    </svg>
  )
}

const headerAnimation: Variants = {
  initial: { opacity: 0, transition: { duration: 0.3 } },
  animate: { opacity: 1, transition: { duration: 0.3, delay: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.3 } },
}

const maxZIndex = 2147483647

const bodyVariantBackwards: Variant = {
  opacity: 0.4,
  scale: 0.8,
  zIndex: 0,
  filter: ''blur(4px)'',
  transition: { duration: 0.4 },
}

const bodyVariantForwards: Variant = (custom: CustomAnimationProps) => ({
  y: ''100%'',
  zIndex: maxZIndex - custom.changeCount,
  transition: { duration: 0.4 },
})

const bodyAnimation: MotionProps = {
  initial: ''initial'',
  animate: ''animate'',
  exit: ''exit'',
  variants: {
    initial: (custom: CustomAnimationProps, ...props) =>
      custom.isForwards
        ? bodyVariantForwards(custom, ...props)
        : bodyVariantBackwards,
    animate: (custom: CustomAnimationProps) => ({
      y: ''0%'',
      opacity: 1,
      scale: 1,
      zIndex: maxZIndex / 2 - custom.changeCount,
      filter: ''blur(0px)'',
      transition: { duration: 0.4 },
    }),
    exit: (custom: CustomAnimationProps, ...props) =>
      custom.isForwards
        ? bodyVariantBackwards
        : bodyVariantForwards(custom, ...props),
  },
}

type ScreenProps =
  | {
      animated: true
      custom: CustomAnimationProps
    }
  | { animated?: false }

function InviteScreen(props: ScreenProps) {
  return (
    <AppScreen className="w-full">
      <MotionAppScreenHeader {...(props.animated ? headerAnimation : {})}>
        <AppScreen.Title>Invite people</AppScreen.Title>
        <AppScreen.Subtitle>
          Get tips <span className="text-white">5s sooner</span> for every
          invite.
        </AppScreen.Subtitle>
      </MotionAppScreenHeader>
      <MotionAppScreenBody
        {...(props.animated ? { ...bodyAnimation, custom: props.custom } : {})}
      >
        <div className="px-4 py-6">
          <div className="space-y-6">
            {[
              { label: ''Full name'', value: ''Albert H. Wiggin'' },
              { label: ''Email address'', value: ''awiggin@chase.com'' },
            ].map((field) => (
              <div key={field.label}>
                <div className="text-sm text-gray-500">{field.label}</div>
                <div className="mt-2 border-b border-gray-200 pb-2 text-sm text-gray-900">
                  {field.value}
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 rounded-lg bg-cyan-500 px-3 py-2 text-center text-sm font-semibold text-white">
            Invite person
          </div>
        </div>
      </MotionAppScreenBody>
    </AppScreen>
  )
}

function StocksScreen(props: ScreenProps) {
  return (
    <AppScreen className="w-full">
      <MotionAppScreenHeader {...(props.animated ? headerAnimation : {})}>
        <AppScreen.Title>Stocks</AppScreen.Title>
        <AppScreen.Subtitle>March 9, 2022</AppScreen.Subtitle>
      </MotionAppScreenHeader>
      <MotionAppScreenBody
        {...(props.animated ? { ...bodyAnimation, custom: props.custom } : {})}
      >
        <div className="divide-y divide-gray-100">
          {[
            {
              name: ''Laravel'',
              price: ''4,098.01'',
              change: ''+4.98%'',
              color: ''#F9322C'',
              logo: LaravelLogo,
            },
            {
              name: ''Tuple'',
              price: ''5,451.10'',
              change: ''-3.38%'',
              color: ''#5A67D8'',
              logo: TupleLogo,
            },
            {
              name: ''Transistor'',
              price: ''4,098.41'',
              change: ''+6.25%'',
              color: ''#2A5B94'',
              logo: TransistorLogo,
            },
            {
              name: ''Diageo'',
              price: ''250.65'',
              change: ''+1.25%'',
              color: ''#3320A7'',
              logo: DiageoLogo,
            },
            {
              name: ''StaticKit'',
              price: ''250.65'',
              change: ''-3.38%'',
              color: ''#2A3034'',
              logo: StaticKitLogo,
            },
            {
              name: ''Statamic'',
              price: ''5,040.85'',
              change: ''-3.11%'',
              color: ''#0EA5E9'',
              logo: StatamicLogo,
            },
            {
              name: ''Mirage'',
              price: ''140.44'',
              change: ''+9.09%'',
              color: ''#16A34A'',
              logo: MirageLogo,
            },
            {
              name: ''Reversable'',
              price: ''550.60'',
              change: ''-1.25%'',
              color: ''#8D8D8D'',
              logo: ReversableLogo,
            },
          ].map((stock) => (
            <div key={stock.name} className="flex items-center gap-4 px-4 py-3">
              <div
                className="flex-none rounded-full"
                style={{ backgroundColor: stock.color }}
              >
                <stock.logo className="h-10 w-10" />
              </div>
              <div className="flex-auto text-sm text-gray-900">
                {stock.name}
              </div>
              <div className="flex-none text-right">
                <div className="text-sm font-medium text-gray-900">
                  {stock.price}
                </div>
                <div
                  className={clsx(
                    ''text-xs/5'',
                    stock.change.startsWith(''+'')
                      ? ''text-cyan-500''
                      : ''text-gray-500'',
                  )}
                >
                  {stock.change}
                </div>
              </div>
            </div>
          ))}
        </div>
      </MotionAppScreenBody>
    </AppScreen>
  )
}

function InvestScreen(props: ScreenProps) {
  return (
    <AppScreen className="w-full">
      <MotionAppScreenHeader {...(props.animated ? headerAnimation : {})}>
        <AppScreen.Title>Buy $LA</AppScreen.Title>
        <AppScreen.Subtitle>
          <span className="text-white">$34.28</span> per share
        </AppScreen.Subtitle>
      </MotionAppScreenHeader>
      <MotionAppScreenBody
        {...(props.animated ? { ...bodyAnimation, custom: props.custom } : {})}
      >
        <div className="px-4 py-6">
          <div className="space-y-4">
            {[
              { label: ''Number of shares'', value: ''100'' },
              {
                label: ''Current market price'',
                value: (
                  <div className="flex">
                    $34.28
                    <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6">
                      <path
                        d="M17 15V7H9M17 7 7 17"
                        stroke="#06B6D4"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                ),
              },
              { label: ''Estimated cost'', value: ''$3,428.00'' },
            ].map((item) => (
              <div
                key={item.label}
                className="flex justify-between border-b border-gray-100 pb-4"
              >
                <div className="text-sm text-gray-500">{item.label}</div>
                <div className="text-sm font-semibold text-gray-900">
                  {item.value}
                </div>
              </div>
            ))}
            <div className="rounded-lg bg-cyan-500 px-3 py-2 text-center text-sm font-semibold text-white">
              Buy shares
            </div>
          </div>
        </div>
      </MotionAppScreenBody>
    </AppScreen>
  )
}

function usePrevious<T>(value: T) {
  let ref = useRef<T>()

  useEffect(() => {
    ref.current = value
  }, [value])

  return ref.current
}

function FeaturesDesktop() {
  let [changeCount, setChangeCount] = useState(0)
  let [selectedIndex, setSelectedIndex] = useState(0)
  let prevIndex = usePrevious(selectedIndex)
  let isForwards = prevIndex === undefined ? true : selectedIndex > prevIndex

  let onChange = useDebouncedCallback(
    (selectedIndex) => {
      setSelectedIndex(selectedIndex)
      setChangeCount((changeCount) => changeCount + 1)
    },
    100,
    { leading: true },
  )

  return (
    <TabGroup
      className="grid grid-cols-12 items-center gap-8 lg:gap-16 xl:gap-24"
      selectedIndex={selectedIndex}
      onChange={onChange}
      vertical
    >
      <TabList className="relative z-10 order-last col-span-6 space-y-6">
        {features.map((feature, featureIndex) => (
          <div
            key={feature.name}
            className="relative rounded-2xl transition-colors hover:bg-gray-800/30"
          >
            {featureIndex === selectedIndex && (
              <motion.div
                layoutId="activeBackground"
                className="absolute inset-0 bg-gray-800"
                initial={{ borderRadius: 16 }}
              />
            )}
            <div className="relative z-10 p-8">
              <feature.icon className="h-8 w-8" />
              <h3 className="mt-6 text-lg font-semibold text-white">
                <Tab className="text-left data-selected:not-data-focus:outline-hidden">
                  <span className="absolute inset-0 rounded-2xl" />
                  {feature.name}
                </Tab>
              </h3>
              <p className="mt-2 text-sm text-gray-400">
                {feature.description}
              </p>
            </div>
          </div>
        ))}
      </TabList>
      <div className="relative col-span-6">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
          <CircleBackground color="#13B5C8" className="animate-spin-slower" />
        </div>
        <PhoneFrame className="z-10 mx-auto w-full max-w-[366px]">
          <TabPanels as={Fragment}>
            <AnimatePresence
              initial={false}
              custom={{ isForwards, changeCount }}
            >
              {features.map((feature, featureIndex) =>
                selectedIndex === featureIndex ? (
                  <TabPanel
                    static
                    key={feature.name + changeCount}
                    className="col-start-1 row-start-1 flex focus:outline-offset-32 data-selected:not-data-focus:outline-hidden"
                  >
                    <feature.screen
                      animated
                      custom={{ isForwards, changeCount }}
                    />
                  </TabPanel>
                ) : null,
              )}
            </AnimatePresence>
          </TabPanels>
        </PhoneFrame>
      </div>
    </TabGroup>
  )
}

function FeaturesMobile() {
  let [activeIndex, setActiveIndex] = useState(0)
  let slideContainerRef = useRef<React.ElementRef<''div''>>(null)
  let slideRefs = useRef<Array<React.ElementRef<''div''>>>([])

  useEffect(() => {
    let observer = new window.IntersectionObserver(
      (entries) => {
        for (let entry of entries) {
          if (entry.isIntersecting && entry.target instanceof HTMLDivElement) {
            setActiveIndex(slideRefs.current.indexOf(entry.target))
            break
          }
        }
      },
      {
        root: slideContainerRef.current,
        threshold: 0.6,
      },
    )

    for (let slide of slideRefs.current) {
      if (slide) {
        observer.observe(slide)
      }
    }

    return () => {
      observer.disconnect()
    }
  }, [slideContainerRef, slideRefs])

  return (
    <>
      <div
        ref={slideContainerRef}
        className="-mb-4 flex snap-x snap-mandatory -space-x-4 overflow-x-auto overscroll-x-contain scroll-smooth pb-4 [scrollbar-width:none] sm:-space-x-6 [&::-webkit-scrollbar]:hidden"
      >
        {features.map((feature, featureIndex) => (
          <div
            key={featureIndex}
            ref={(ref) => ref && (slideRefs.current[featureIndex] = ref)}
            className="w-full flex-none snap-center px-4 sm:px-6"
          >
            <div className="relative transform overflow-hidden rounded-2xl bg-gray-800 px-5 py-6">
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                <CircleBackground
                  color="#13B5C8"
                  className={featureIndex % 2 === 1 ? ''rotate-180'' : undefined}
                />
              </div>
              <PhoneFrame className="relative mx-auto w-full max-w-[366px]">
                <feature.screen />
              </PhoneFrame>
              <div className="absolute inset-x-0 bottom-0 bg-gray-800/95 p-6 backdrop-blur-sm sm:p-10">
                <feature.icon className="h-8 w-8" />
                <h3 className="mt-6 text-sm font-semibold text-white sm:text-lg">
                  {feature.name}
                </h3>
                <p className="mt-2 text-sm text-gray-400">
                  {feature.description}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6 flex justify-center gap-3">
        {features.map((_, featureIndex) => (
          <button
            type="button"
            key={featureIndex}
            className={clsx(
              ''relative h-0.5 w-4 rounded-full'',
              featureIndex === activeIndex ? ''bg-gray-300'' : ''bg-gray-500'',
            )}
            aria-label={`Go to slide ${featureIndex + 1}`}
            onClick={() => {
              slideRefs.current[featureIndex].scrollIntoView({
                block: ''nearest'',
                inline: ''nearest'',
              })
            }}
          >
            <span className="absolute -inset-x-1.5 -inset-y-3" />
          </button>
        ))}
      </div>
    </>
  )
}

export function PrimaryFeatures() {
  return (
    <section
      id="features"
      aria-label="Features for investing all your money"
      className="bg-gray-900 py-20 sm:py-32"
    >
      <Container>
        <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-3xl">
          <h2 className="text-3xl font-medium tracking-tight text-white">
            Every feature you need to win. Try it for yourself.
          </h2>
          <p className="mt-2 text-lg text-gray-400">
            Pocket was built for investors like you who play by their own rules
            and aren’t going to let SEC regulations get in the way of their
            dreams. If other investing tools are afraid to build it, Pocket has
            it.
          </p>
        </div>
      </Container>
      <div className="mt-16 md:hidden">
        <FeaturesMobile />
      </div>
      <Container className="hidden md:mt-20 md:block">
        <FeaturesDesktop />
      </Container>
    </section>
  )
}
',
    'features',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["use-debounce", "clsx", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "features", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/PrimaryFeatures.tsx", "uses_components": [], "dependencies": ["use-debounce", "clsx", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Testimonials - Pocket
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Testimonials - Pocket',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useEffect, useMemo, useRef, useState } from ''react''
import clsx from ''clsx''
import { useInView } from ''framer-motion''

import { Container } from ''@/components/Container''

interface Review {
  title: string
  body: string
  author: string
  rating: 1 | 2 | 3 | 4 | 5
}

const reviews: Array<Review> = [
  {
    title: ''It really works.'',
    body: ''I downloaded Pocket today and turned $5000 into $25,000 in half an hour.'',
    author: ''CrazyInvestor'',
    rating: 5,
  },
  {
    title: ''You need this app.'',
    body: ''I didn’t understand the stock market at all before Pocket. I still don’t, but at least I’m rich now.'',
    author: ''CluelessButRich'',
    rating: 5,
  },
  {
    title: ''This shouldn’t be legal.'',
    body: ''Pocket makes it so easy to win big in the stock market that I can’t believe it’s actually legal.'',
    author: ''LivingDaDream'',
    rating: 5,
  },
  {
    title: ''Screw financial advisors.'',
    body: ''I barely made any money investing in mutual funds. With Pocket, I’m doubling my net-worth every single month.'',
    author: ''JordanBelfort1962'',
    rating: 5,
  },
  {
    title: ''I love it!'',
    body: ''I started providing insider information myself and now I get new insider tips every 5 minutes. I don’t even have time to act on all of them. New Lamborghini is being delivered next week!'',
    author: ''MrBurns'',
    rating: 5,
  },
  {
    title: ''Too good to be true.'',
    body: ''I was making money so fast with Pocket that it felt like a scam. But I sold my shares and withdrew the money and it’s really there, right in my bank account. This app is crazy!'',
    author: ''LazyRich99'',
    rating: 5,
  },
  {
    title: ''Wish I could give 6 stars'',
    body: ''This is literally the most important app you will ever download in your life. Get on this before it’s so popular that everyone else is getting these tips too.'',
    author: ''SarahLuvzCash'',
    rating: 5,
  },
  {
    title: ''Bought an island.'',
    body: ''Yeah, you read that right. Want your own island too? Get Pocket.'',
    author: ''ScroogeMcduck'',
    rating: 5,
  },
  {
    title: ''No more debt!'',
    body: ''After 2 weeks of trading on Pocket I was debt-free. Why did I even go to school at all when Pocket exists?'',
    author: ''BruceWayne'',
    rating: 5,
  },
  {
    title: ''I’m 13 and I’m rich.'',
    body: ''I love that with Pocket’s transaction anonymization I could sign up and start trading when I was 12 years old. I had a million dollars before I had armpit hair!'',
    author: ''RichieRich'',
    rating: 5,
  },
  {
    title: ''Started an investment firm.'',
    body: ''I charge clients a 3% management fee and just throw all their investments into Pocket. Easy money!'',
    author: ''TheCountOfMonteChristo'',
    rating: 5,
  },
  {
    title: ''It’s like a superpower.'',
    body: ''Every tip Pocket has sent me has paid off. It’s like playing Blackjack but knowing exactly what card is coming next!'',
    author: ''ClarkKent'',
    rating: 5,
  },
  {
    title: ''Quit my job.'',
    body: ''I downloaded Pocket three days ago and quit my job today. I can’t believe no one else thought to build a stock trading app that works this way!'',
    author: ''GeorgeCostanza'',
    rating: 5,
  },
  {
    title: ''Don’t download this app'',
    body: ''Unless you want to have the best life ever! I am literally writing this from a yacht.'',
    author: ''JeffBezos'',
    rating: 5,
  },
]

function StarIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true" {...props}>
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
  )
}

function StarRating({ rating }: { rating: Review[''rating''] }) {
  return (
    <div className="flex">
      {[...Array(5).keys()].map((index) => (
        <StarIcon
          key={index}
          className={clsx(
            ''h-5 w-5'',
            rating > index ? ''fill-cyan-500'' : ''fill-gray-300'',
          )}
        />
      ))}
    </div>
  )
}

function Review({
  title,
  body,
  author,
  rating,
  className,
  ...props
}: Omit<React.ComponentPropsWithoutRef<''figure''>, keyof Review> & Review) {
  let animationDelay = useMemo(() => {
    let possibleAnimationDelays = [''0s'', ''0.1s'', ''0.2s'', ''0.3s'', ''0.4s'', ''0.5s'']
    return possibleAnimationDelays[
      Math.floor(Math.random() * possibleAnimationDelays.length)
    ]
  }, [])

  return (
    <figure
      className={clsx(
        ''animate-fade-in rounded-3xl bg-white p-6 opacity-0 shadow-md shadow-gray-900/5'',
        className,
      )}
      style={{ animationDelay }}
      {...props}
    >
      <blockquote className="text-gray-900">
        <StarRating rating={rating} />
        <p className="mt-4 text-lg/6 font-semibold before:content-[''“''] after:content-[''”'']">
          {title}
        </p>
        <p className="mt-3 text-base/7">{body}</p>
      </blockquote>
      <figcaption className="mt-3 text-sm text-gray-600 before:content-[''–_'']">
        {author}
      </figcaption>
    </figure>
  )
}

function splitArray<T>(array: Array<T>, numParts: number) {
  let result: Array<Array<T>> = []
  for (let i = 0; i < array.length; i++) {
    let index = i % numParts
    if (!result[index]) {
      result[index] = []
    }
    result[index].push(array[i])
  }
  return result
}

function ReviewColumn({
  reviews,
  className,
  reviewClassName,
  msPerPixel = 0,
}: {
  reviews: Array<Review>
  className?: string
  reviewClassName?: (reviewIndex: number) => string
  msPerPixel?: number
}) {
  let columnRef = useRef<React.ElementRef<''div''>>(null)
  let [columnHeight, setColumnHeight] = useState(0)
  let duration = `${columnHeight * msPerPixel}ms`

  useEffect(() => {
    if (!columnRef.current) {
      return
    }

    let resizeObserver = new window.ResizeObserver(() => {
      setColumnHeight(columnRef.current?.offsetHeight ?? 0)
    })

    resizeObserver.observe(columnRef.current)

    return () => {
      resizeObserver.disconnect()
    }
  }, [])

  return (
    <div
      ref={columnRef}
      className={clsx(''animate-marquee space-y-8 py-4'', className)}
      style={{ ''--marquee-duration'': duration } as React.CSSProperties}
    >
      {reviews.concat(reviews).map((review, reviewIndex) => (
        <Review
          key={reviewIndex}
          aria-hidden={reviewIndex >= reviews.length}
          className={reviewClassName?.(reviewIndex % reviews.length)}
          {...review}
        />
      ))}
    </div>
  )
}

function ReviewGrid() {
  let containerRef = useRef<React.ElementRef<''div''>>(null)
  let isInView = useInView(containerRef, { once: true, amount: 0.4 })
  let columns = splitArray(reviews, 3)
  let column1 = columns[0]
  let column2 = columns[1]
  let column3 = splitArray(columns[2], 2)

  return (
    <div
      ref={containerRef}
      className="relative -mx-4 mt-16 grid h-196 max-h-[150vh] grid-cols-1 items-start gap-8 overflow-hidden px-4 sm:mt-20 md:grid-cols-2 lg:grid-cols-3"
    >
      {isInView && (
        <>
          <ReviewColumn
            reviews={[...column1, ...column3.flat(), ...column2]}
            reviewClassName={(reviewIndex) =>
              clsx(
                reviewIndex >= column1.length + column3[0].length &&
                  ''md:hidden'',
                reviewIndex >= column1.length && ''lg:hidden'',
              )
            }
            msPerPixel={10}
          />
          <ReviewColumn
            reviews={[...column2, ...column3[1]]}
            className="hidden md:block"
            reviewClassName={(reviewIndex) =>
              reviewIndex >= column2.length ? ''lg:hidden'' : ''''
            }
            msPerPixel={15}
          />
          <ReviewColumn
            reviews={column3.flat()}
            className="hidden lg:block"
            msPerPixel={10}
          />
        </>
      )}
      <div className="pointer-events-none absolute inset-x-0 top-0 h-32 bg-linear-to-b from-gray-50" />
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-32 bg-linear-to-t from-gray-50" />
    </div>
  )
}

export function Reviews() {
  return (
    <section
      id="reviews"
      aria-labelledby="reviews-title"
      className="pt-20 pb-16 sm:pt-32 sm:pb-24"
    >
      <Container>
        <h2
          id="reviews-title"
          className="text-3xl font-medium tracking-tight text-gray-900 sm:text-center"
        >
          Everyone is changing their life with Pocket.
        </h2>
        <p className="mt-2 text-lg text-gray-600 sm:text-center">
          Thousands of people have doubled their net-worth in the last 30 days.
        </p>
        <ReviewGrid />
      </Container>
    </section>
  )
}
',
    'testimonials',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'testimonials', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["framer-motion", "clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "testimonials", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Reviews.tsx", "uses_components": [], "dependencies": ["framer-motion", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Secondaryfeatures - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Secondaryfeatures - Marketing',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { useId } from ''react''

import { Container } from ''@/components/Container''

const features = [
  {
    name: ''Invest any amount'',
    description:
      ''Whether it’s $1 or $1,000,000, we can put your money to work for you.'',
    icon: DeviceArrowIcon,
  },
  {
    name: ''Build a balanced portfolio'',
    description:
      ''Invest in different industries to find the most opportunities to win huge.'',
    icon: DeviceCardsIcon,
  },
  {
    name: ''Trade in real-time'',
    description:
      ''Get insider tips on big stock moves and act on them within seconds.'',
    icon: DeviceClockIcon,
  },
  {
    name: ''Profit from your network'',
    description:
      ''Invite new insiders to get tips faster and beat even other Pocket users.'',
    icon: DeviceListIcon,
  },
  {
    name: ''Encrypted and anonymized'',
    description:
      ''Cutting-edge security technology that even the NSA doesn’t know about keeps you hidden.'',
    icon: DeviceLockIcon,
  },
  {
    name: ''Portfolio tracking'',
    description:
      ''Watch your investments grow exponentially, leaving other investors in the dust.'',
    icon: DeviceChartIcon,
  },
]

function DeviceArrowIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M9 0a4 4 0 00-4 4v24a4 4 0 004 4h14a4 4 0 004-4V4a4 4 0 00-4-4H9zm0 2a2 2 0 00-2 2v24a2 2 0 002 2h14a2 2 0 002-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9z"
        fill="#737373"
      />
      <path
        d="M12 25l8-8m0 0h-6m6 0v6"
        stroke="#171717"
        strokeWidth={2}
        strokeLinecap="round"
      />
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
    </svg>
  )
}

function DeviceCardsIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  let id = useId()

  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M9 0a4 4 0 00-4 4v24a4 4 0 004 4h14a4 4 0 004-4V4a4 4 0 00-4-4H9zm0 2a2 2 0 00-2 2v24a2 2 0 002 2h14a2 2 0 002-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9z"
        fill="#737373"
      />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M9 13a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H10a1 1 0 01-1-1v-2zm0 6a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H10a1 1 0 01-1-1v-2zm1 5a1 1 0 00-1 1v2a1 1 0 001 1h12a1 1 0 001-1v-2a1 1 0 00-1-1H10z"
        fill={`url(#${id}-gradient)`}
      />
      <rect x={9} y={6} width={14} height={4} rx={1} fill="#171717" />
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
      <defs>
        <linearGradient
          id={`${id}-gradient`}
          x1={16}
          y1={12}
          x2={16}
          y2={28}
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#737373" />
          <stop offset={1} stopColor="#737373" stopOpacity={0} />
        </linearGradient>
      </defs>
    </svg>
  )
}

function DeviceClockIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" {...props}>
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M5 4a4 4 0 014-4h14a4 4 0 014 4v10h-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9a2 2 0 00-2 2v24a2 2 0 002 2h5v2H9a4 4 0 01-4-4V4z"
        fill="#737373"
      />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M24 32a8 8 0 100-16 8 8 0 000 16zm1-8.414V19h-2v5.414l4 4L28.414 27 25 23.586z"
        fill="#171717"
      />
    </svg>
  )
}

function DeviceListIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 32 32" fill="none" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M9 0a4 4 0 00-4 4v24a4 4 0 004 4h14a4 4 0 004-4V4a4 4 0 00-4-4H9zm0 2a2 2 0 00-2 2v24a2 2 0 002 2h14a2 2 0 002-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9z"
        fill="#737373"
      />
      <circle cx={11} cy={14} r={2} fill="#171717" />
      <circle cx={11} cy={20} r={2} fill="#171717" />
      <circle cx={11} cy={26} r={2} fill="#171717" />
      <path
        d="M16 14h6M16 20h6M16 26h6"
        stroke="#737373"
        strokeWidth={2}
        strokeLinecap="square"
      />
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
    </svg>
  )
}

function DeviceLockIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 32 32" aria-hidden="true" {...props}>
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M5 4a4 4 0 014-4h14a4 4 0 014 4v10h-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9a2 2 0 00-2 2v24a2 2 0 002 2h5v2H9a4 4 0 01-4-4V4z"
        fill="#737373"
      />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M18 19.5a3.5 3.5 0 117 0V22a2 2 0 012 2v6a2 2 0 01-2 2h-7a2 2 0 01-2-2v-6a2 2 0 012-2v-2.5zm2 2.5h3v-2.5a1.5 1.5 0 00-3 0V22z"
        fill="#171717"
      />
    </svg>
  )
}

function DeviceChartIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 32 32" fill="none" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M9 0a4 4 0 00-4 4v24a4 4 0 004 4h14a4 4 0 004-4V4a4 4 0 00-4-4H9zm0 2a2 2 0 00-2 2v24a2 2 0 002 2h14a2 2 0 002-2V4a2 2 0 00-2-2h-1.382a1 1 0 00-.894.553l-.448.894a1 1 0 01-.894.553h-6.764a1 1 0 01-.894-.553l-.448-.894A1 1 0 0010.382 2H9z"
        fill="#737373"
      />
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M23 13.838V26a2 2 0 01-2 2H11a2 2 0 01-2-2V15.65l2.57 3.212a1 1 0 001.38.175L15.4 17.2a1 1 0 011.494.353l1.841 3.681c.399.797 1.562.714 1.843-.13L23 13.837z"
        fill="#171717"
      />
      <path
        d="M10 12h12"
        stroke="#737373"
        strokeWidth={2}
        strokeLinecap="square"
      />
      <circle cx={16} cy={16} r={16} fill="#A3A3A3" fillOpacity={0.2} />
    </svg>
  )
}

export function SecondaryFeatures() {
  return (
    <section
      id="secondary-features"
      aria-label="Features for building a portfolio"
      className="py-20 sm:py-32"
    >
      <Container>
        <div className="mx-auto max-w-2xl sm:text-center">
          <h2 className="text-3xl font-medium tracking-tight text-gray-900">
            Now is the time to build your portfolio.
          </h2>
          <p className="mt-2 text-lg text-gray-600">
            With typical market returns, you have to start young to secure your
            future. With Pocket, it’s never too late to build your nest egg.
          </p>
        </div>
        <ul
          role="list"
          className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-6 text-sm sm:mt-20 sm:grid-cols-2 md:gap-y-10 lg:max-w-none lg:grid-cols-3"
        >
          {features.map((feature) => (
            <li
              key={feature.name}
              className="rounded-2xl border border-gray-200 p-8"
            >
              <feature.icon className="h-8 w-8" />
              <h3 className="mt-6 font-semibold text-gray-900">
                {feature.name}
              </h3>
              <p className="mt-2 text-gray-700">{feature.description}</p>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
',
    'features',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "features", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/SecondaryFeatures.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Auth - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Auth - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Pocket template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import Link from ''next/link''

import { AuthLayout } from ''@/components/AuthLayout''
import { Button } from ''@/components/Button''
import { SelectField, TextField } from ''@/components/Fields''

export const metadata: Metadata = {
  title: ''Sign Up'',
}

export default function Register() {
  return (
    <AuthLayout
      title="Sign up for an account"
      subtitle={
        <>
          Already registered?{'' ''}
          <Link href="/login" className="text-cyan-600">
            Sign in
          </Link>{'' ''}
          to your account.
        </>
      }
    >
      <form>
        <div className="grid grid-cols-2 gap-6">
          <TextField
            label="First name"
            name="first_name"
            type="text"
            autoComplete="given-name"
            required
          />
          <TextField
            label="Last name"
            name="last_name"
            type="text"
            autoComplete="family-name"
            required
          />
          <TextField
            className="col-span-full"
            label="Email address"
            name="email"
            type="email"
            autoComplete="email"
            required
          />
          <TextField
            className="col-span-full"
            label="Password"
            name="password"
            type="password"
            autoComplete="new-password"
            required
          />
          <SelectField
            className="col-span-full"
            label="How did you hear about us?"
            name="referral_source"
          >
            <option>AltaVista search</option>
            <option>Super Bowl commercial</option>
            <option>Our route 34 city bus ad</option>
            <option>The “Never Use This” podcast</option>
          </SelectField>
        </div>
        <Button type="submit" color="cyan" className="mt-8 w-full">
          Get started today
        </Button>
      </form>
    </AuthLayout>
  )
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-pocket", "component_type": "auth", "file_path": "tailwind-plus-pocket/pocket-ts/src/app/(auth)/register/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Author - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Author - Marketing',
    'Marketing/Landing page component from Tailwind Plus Primer template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image from ''next/image''
import Link from ''next/link''

import { GridPattern } from ''@/components/GridPattern''
import { SectionHeading } from ''@/components/SectionHeading''
import authorImage from ''@/images/avatars/author.png''

function XIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" {...props}>
      <path d="M13.6823 10.6218L20.2391 3H18.6854L12.9921 9.61788L8.44486 3H3.2002L10.0765 13.0074L3.2002 21H4.75404L10.7663 14.0113L15.5685 21H20.8132L13.6819 10.6218H13.6823ZM11.5541 13.0956L10.8574 12.0991L5.31391 4.16971H7.70053L12.1742 10.5689L12.8709 11.5655L18.6861 19.8835H16.2995L11.5541 13.096V13.0956Z" />
    </svg>
  )
}

export function Author() {
  return (
    <section
      id="author"
      aria-labelledby="author-title"
      className="relative scroll-mt-14 pt-8 pb-3 sm:scroll-mt-32 sm:pt-10 sm:pb-16 lg:pt-16"
    >
      <div className="absolute inset-x-0 top-1/2 bottom-0 mask-[linear-gradient(transparent,white)] text-slate-900/10">
        <GridPattern x="50%" y="100%" />
      </div>
      <div className="relative mx-auto max-w-5xl pt-16 sm:px-6">
        <div className="bg-slate-50 pt-px sm:rounded-6xl">
          <div className="relative mx-auto -mt-16 h-44 w-44 overflow-hidden rounded-full bg-slate-200 md:float-right md:h-64 md:w-64 md:[shape-outside:circle(40%)] lg:mr-20 lg:h-72 lg:w-72">
            <Image
              className="absolute inset-0 h-full w-full object-cover"
              src={authorImage}
              alt=""
              sizes="(min-width: 1024px) 18rem, (min-width: 768px) 16rem, 11rem"
            />
          </div>
          <div className="px-4 py-10 sm:px-10 sm:py-16 md:py-20 lg:px-20 lg:py-32">
            <SectionHeading number="5" id="author-title">
              Author
            </SectionHeading>
            <p className="mt-8 font-display text-5xl font-extrabold tracking-tight text-slate-900 sm:text-6xl">
              <span className="block text-blue-600">Mira Lindehoff –</span> Hey
              there, I’m the author behind ‘Everything Starts as a Square’.
            </p>
            <p className="mt-4 text-lg tracking-tight text-slate-700">
              I’ve been designing icons professionally for over a decade and
              have worked with dozens of the biggest brands to create custom
              sets for their products. I’m an accomplished conference speaker,
              and have been teaching icon design workshops every month for the
              last three years. I’ve worked with designers of all skill levels
              and honed my way of teaching to really click for anyone who has
              the itch to start designing their own icons.
            </p>
            <p className="mt-8">
              <Link
                href="#"
                className="inline-flex items-center text-base font-medium tracking-tight text-slate-900"
              >
                <XIcon className="h-10 w-10 fill-current" />
                <span className="ml-4">Follow on X</span>
              </Link>
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'primer', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-primer", "component_type": "auth", "file_path": "tailwind-plus-primer/primer-ts/src/components/Author.tsx", "uses_components": [], "dependencies": ["next/link", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Primer
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Primer',
    'Marketing/Landing page component from Tailwind Plus Primer template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { GridPattern } from ''@/components/GridPattern''

export function Footer() {
  return (
    <footer className="relative pt-5 pb-20 sm:pt-14 sm:pb-32">
      <div className="absolute inset-x-0 top-0 h-32 mask-[linear-gradient(white,transparent)] text-slate-900/10">
        <GridPattern x="50%" />
      </div>
      <div className="relative text-center text-sm text-slate-600">
        <p>Copyright &copy; {new Date().getFullYear()} Lindehoff Design, LLC</p>
        <p>All rights reserved.</p>
      </div>
    </footer>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'primer', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-primer", "component_type": "footer", "file_path": "tailwind-plus-primer/primer-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Primer
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Primer',
    'Marketing/Landing page component from Tailwind Plus Primer template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image from ''next/image''

import { Button } from ''@/components/Button''
import { GridPattern } from ''@/components/GridPattern''
import { StarRating } from ''@/components/StarRating''
import coverImage from ''@/images/cover.png''

function Testimonial() {
  return (
    <figure className="relative mx-auto max-w-md text-center lg:mx-0 lg:text-left">
      <div className="flex justify-center text-blue-600 lg:justify-start">
        <StarRating />
      </div>
      <blockquote className="mt-2">
        <p className="font-display text-xl font-medium text-slate-900">
          “This method of designing icons is genius. I wish I had known this
          method a lot sooner.”
        </p>
      </blockquote>
      <figcaption className="mt-2 text-sm text-slate-500">
        <strong className="font-semibold text-blue-600 before:content-[''—_'']">
          Stacey Solomon
        </strong>
        , Founder at Retail Park
      </figcaption>
    </figure>
  )
}

export function Hero() {
  return (
    <header className="overflow-hidden bg-slate-100 lg:bg-transparent lg:px-5">
      <div className="mx-auto grid max-w-6xl grid-cols-1 grid-rows-[auto_1fr] gap-y-16 pt-16 md:pt-20 lg:grid-cols-12 lg:gap-y-20 lg:px-3 lg:pt-20 lg:pb-36 xl:py-32">
        <div className="relative flex items-end lg:col-span-5 lg:row-span-2">
          <div className="absolute -top-20 right-1/2 -bottom-12 left-0 z-10 rounded-br-6xl bg-blue-600 text-white/10 md:bottom-8 lg:-inset-y-32 lg:right-full lg:left-[-100vw] lg:-mr-40">
            <GridPattern
              x="100%"
              y="100%"
              patternTransform="translate(112 64)"
            />
          </div>
          <div className="relative z-10 mx-auto flex w-64 rounded-xl bg-slate-600 shadow-xl md:w-80 lg:w-auto">
            <Image className="w-full" src={coverImage} alt="" priority />
          </div>
        </div>
        <div className="relative px-4 sm:px-6 lg:col-span-7 lg:pr-0 lg:pb-14 lg:pl-16 xl:pl-20">
          <div className="hidden lg:absolute lg:-top-32 lg:right-[-100vw] lg:bottom-0 lg:left-[-100vw] lg:block lg:bg-slate-100" />
          <Testimonial />
        </div>
        <div className="bg-white pt-16 lg:col-span-7 lg:bg-transparent lg:pt-0 lg:pl-16 xl:pl-20">
          <div className="mx-auto px-4 sm:px-6 md:max-w-2xl md:px-4 lg:px-0">
            <h1 className="font-display text-5xl font-extrabold text-slate-900 sm:text-6xl">
              Get lost in the world of icon design.
            </h1>
            <p className="mt-4 text-3xl text-slate-600">
              A book and video course that teaches you how to design your own
              icons from scratch.
            </p>
            <div className="mt-8 flex gap-4">
              <Button href="#free-chapters" color="blue">
                Get sample chapter
              </Button>
              <Button href="#pricing" variant="outline" color="blue">
                Buy book
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'primer', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-primer", "component_type": "hero", "file_path": "tailwind-plus-primer/primer-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Navigation - Primer
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Navigation - Primer',
    'Marketing/Landing page component from Tailwind Plus Primer template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useEffect, useRef, useState } from ''react''
import { Popover, PopoverButton, PopoverPanel } from ''@headlessui/react''
import clsx from ''clsx''

const sections = [
  {
    id: ''table-of-contents'',
    title: (
      <>
        <span className="hidden lg:inline">Table of contents</span>
        <span className="lg:hidden">Contents</span>
      </>
    ),
  },
  { id: ''screencasts'', title: ''Screencasts'' },
  { id: ''resources'', title: ''Resources'' },
  { id: ''pricing'', title: ''Pricing'' },
  { id: ''author'', title: ''Author'' },
]

function MenuIcon({
  open,
  ...props
}: React.ComponentPropsWithoutRef<''svg''> & {
  open: boolean
}) {
  return (
    <svg
      aria-hidden="true"
      fill="none"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      viewBox="0 0 24 24"
      {...props}
    >
      <path
        d={open ? ''M17 7 7 17M7 7l10 10'' : ''m15 16-3 3-3-3M15 8l-3-3-3 3''}
      />
    </svg>
  )
}

export function NavBar() {
  let navBarRef = useRef<React.ElementRef<''div''>>(null)
  let [activeIndex, setActiveIndex] = useState<number | null>(null)
  let mobileActiveIndex = activeIndex === null ? 0 : activeIndex

  useEffect(() => {
    function updateActiveIndex() {
      if (!navBarRef.current) {
        return
      }

      let newActiveIndex = null
      let elements = sections
        .map(({ id }) => document.getElementById(id))
        .filter((el): el is HTMLElement => el !== null)
      let bodyRect = document.body.getBoundingClientRect()
      let offset = bodyRect.top + navBarRef.current.offsetHeight + 1

      if (window.scrollY >= Math.floor(bodyRect.height) - window.innerHeight) {
        setActiveIndex(sections.length - 1)
        return
      }

      for (let index = 0; index < elements.length; index++) {
        if (
          window.scrollY >=
          elements[index].getBoundingClientRect().top - offset
        ) {
          newActiveIndex = index
        } else {
          break
        }
      }

      setActiveIndex(newActiveIndex)
    }

    updateActiveIndex()

    window.addEventListener(''resize'', updateActiveIndex)
    window.addEventListener(''scroll'', updateActiveIndex, { passive: true })

    return () => {
      window.removeEventListener(''resize'', updateActiveIndex)
      window.removeEventListener(''scroll'', updateActiveIndex)
    }
  }, [])

  return (
    <div ref={navBarRef} className="sticky top-0 z-50">
      <Popover className="sm:hidden">
        {({ open }) => (
          <>
            <div
              className={clsx(
                ''relative flex items-center px-4 py-3'',
                !open &&
                  ''bg-white/95 shadow-sm [@supports(backdrop-filter:blur(0))]:bg-white/80 [@supports(backdrop-filter:blur(0))]:backdrop-blur-sm'',
              )}
            >
              {!open && (
                <>
                  <span
                    aria-hidden="true"
                    className="font-mono text-sm text-blue-600"
                  >
                    {(mobileActiveIndex + 1).toString().padStart(2, ''0'')}
                  </span>
                  <span className="ml-4 text-base font-medium text-slate-900">
                    {sections[mobileActiveIndex].title}
                  </span>
                </>
              )}
              <PopoverButton
                className={clsx(
                  ''-mr-1 ml-auto flex h-8 w-8 items-center justify-center'',
                  open && ''relative z-10'',
                )}
                aria-label="Toggle navigation menu"
              >
                {!open && (
                  <>
                    {/* Increase hit area */}
                    <span className="absolute inset-0" />
                  </>
                )}
                <MenuIcon open={open} className="h-6 w-6 stroke-slate-700" />
              </PopoverButton>
            </div>
            <PopoverPanel className="absolute inset-x-0 top-0 bg-white/95 py-3.5 shadow-sm [@supports(backdrop-filter:blur(0))]:bg-white/80 [@supports(backdrop-filter:blur(0))]:backdrop-blur-sm">
              {sections.map((section, sectionIndex) => (
                <PopoverButton
                  as="a"
                  key={section.id}
                  href={`#${section.id}`}
                  className="flex items-center px-4 py-1.5"
                >
                  <span
                    aria-hidden="true"
                    className="font-mono text-sm text-blue-600"
                  >
                    {(sectionIndex + 1).toString().padStart(2, ''0'')}
                  </span>
                  <span className="ml-4 text-base font-medium text-slate-900">
                    {section.title}
                  </span>
                </PopoverButton>
              ))}
            </PopoverPanel>
            <div className="absolute inset-x-0 bottom-full z-10 h-4 bg-white" />
          </>
        )}
      </Popover>
      <div className="hidden sm:flex sm:h-32 sm:justify-center sm:border-b sm:border-slate-200 sm:bg-white/95 sm:[@supports(backdrop-filter:blur(0))]:bg-white/80 sm:[@supports(backdrop-filter:blur(0))]:backdrop-blur-sm">
        <ol
          role="list"
          className="mb-[-2px] grid auto-cols-[minmax(0,15rem)] grid-flow-col text-base font-medium text-slate-900 [counter-reset:section]"
        >
          {sections.map((section, sectionIndex) => (
            <li key={section.id} className="flex [counter-increment:section]">
              <a
                href={`#${section.id}`}
                className={clsx(
                  ''flex w-full flex-col items-center justify-center border-b-2 before:mb-2 before:font-mono before:text-sm before:content-[counter(section,decimal-leading-zero)]'',
                  sectionIndex === activeIndex
                    ? ''border-blue-600 bg-blue-50 text-blue-600 before:text-blue-600''
                    : ''border-transparent before:text-slate-500 hover:bg-blue-50/40 hover:before:text-slate-900'',
                )}
              >
                {section.title}
              </a>
            </li>
          ))}
        </ol>
      </div>
    </div>
  )
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'primer', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-primer", "component_type": "navigation", "file_path": "tailwind-plus-primer/primer-ts/src/components/NavBar.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Pricing Section - Primer
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Pricing Section - Primer',
    'Marketing/Landing page component from Tailwind Plus Primer template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import clsx from ''clsx''

import { Button } from ''@/components/Button''
import { CheckIcon } from ''@/components/CheckIcon''
import { Container } from ''@/components/Container''
import { GridPattern } from ''@/components/GridPattern''
import { SectionHeading } from ''@/components/SectionHeading''

function Plan({
  name,
  description,
  price,
  features,
  href,
  featured = false,
}: {
  name: string
  description: string
  price: string
  features: Array<string>
  href: string
  featured?: boolean
}) {
  return (
    <div
      className={clsx(
        ''relative px-4 py-16 sm:rounded-5xl sm:px-10 md:py-12 lg:px-12'',
        featured && ''bg-blue-600 sm:shadow-lg'',
      )}
    >
      {featured && (
        <div className="absolute inset-0 mask-[linear-gradient(white,transparent)] text-white/10">
          <GridPattern x="50%" y="50%" />
        </div>
      )}
      <div className="relative flex flex-col">
        <h3
          className={clsx(
            ''mt-7 text-lg font-semibold tracking-tight'',
            featured ? ''text-white'' : ''text-slate-900'',
          )}
        >
          {name}
        </h3>
        <p
          className={clsx(
            ''mt-2 text-lg tracking-tight'',
            featured ? ''text-white'' : ''text-slate-600'',
          )}
        >
          {description}
        </p>
        <p className="order-first flex font-display font-bold">
          <span
            className={clsx(
              ''text-[1.75rem]/9'',
              featured ? ''text-blue-200'' : ''text-slate-500'',
            )}
          >
            $
          </span>
          <span
            className={clsx(
              ''mt-1 ml-1 text-7xl tracking-tight'',
              featured ? ''text-white'' : ''text-slate-900'',
            )}
          >
            {price}
          </span>
        </p>
        <div className="order-last mt-8">
          <ul
            role="list"
            className={clsx(
              ''-my-2 divide-y text-base tracking-tight'',
              featured
                ? ''divide-white/10 text-white''
                : ''divide-slate-200 text-slate-900'',
            )}
          >
            {features.map((feature) => (
              <li key={feature} className="flex py-2">
                <CheckIcon
                  className={clsx(
                    ''h-8 w-8 flex-none'',
                    featured ? ''fill-white'' : ''fill-slate-600'',
                  )}
                />
                <span className="ml-4">{feature}</span>
              </li>
            ))}
          </ul>
        </div>
        <Button
          href={href}
          color={featured ? ''white'' : ''slate''}
          className="mt-8"
          aria-label={`Get started with the ${name} plan for $${price}`}
        >
          Get started
        </Button>
      </div>
    </div>
  )
}

export function Pricing() {
  return (
    <section
      id="pricing"
      aria-labelledby="pricing-title"
      className="scroll-mt-14 pt-16 pb-8 sm:scroll-mt-32 sm:pt-20 sm:pb-10 lg:pt-32 lg:pb-16"
    >
      <Container>
        <SectionHeading number="4" id="pricing-title">
          Pricing
        </SectionHeading>
        <p className="mt-8 font-display text-5xl font-extrabold tracking-tight text-slate-900 sm:text-6xl">
          Pick your package
        </p>
        <p className="mt-4 max-w-xl text-lg tracking-tight text-slate-600">
          “Everything Starts as a Square” is available in two different packages
          so you can pick the one that’s right for you.
        </p>
      </Container>
      <div className="mx-auto mt-16 max-w-5xl lg:px-6">
        <div className="grid bg-slate-50 sm:px-6 sm:pb-16 md:grid-cols-2 md:rounded-6xl md:px-8 md:pt-16 lg:p-20">
          <Plan
            name="Essential"
            description="The perfect starting point if you’re on a budget."
            price="15"
            href="#"
            features={[
              ''The 240-page ebook'',
              ''Figma icon templates'',
              ''Community access'',
            ]}
          />
          <Plan
            featured
            name="Complete"
            description="Everything icon resource you could ever ask for."
            price="229"
            href="#"
            features={[
              ''The 240-page ebook'',
              ''Figma icon templates'',
              ''Over an hour of screencasts'',
              ''Weekly icon teardowns'',
              ''Community access'',
            ]}
          />
        </div>
      </div>
    </section>
  )
}
',
    'pricing',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'pricing', 'primer', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-primer", "component_type": "pricing", "file_path": "tailwind-plus-primer/primer-ts/src/components/Pricing.tsx", "uses_components": ["Button"], "dependencies": ["clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Testimonials - Primer
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Testimonials - Primer',
    'Marketing/Landing page component from Tailwind Plus Primer template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image, { type ImageProps } from ''next/image''
import clsx from ''clsx''

import { Container } from ''@/components/Container''
import {
  Expandable,
  ExpandableButton,
  ExpandableItems,
} from ''@/components/Expandable''
import avatarImage3 from ''@/images/avatars/avatar-3.png''
import avatarImage4 from ''@/images/avatars/avatar-4.png''
import avatarImage5 from ''@/images/avatars/avatar-5.png''
import avatarImage6 from ''@/images/avatars/avatar-6.png''
import avatarImage7 from ''@/images/avatars/avatar-7.png''
import avatarImage8 from ''@/images/avatars/avatar-8.png''
import avatarImage9 from ''@/images/avatars/avatar-9.png''
import avatarImage10 from ''@/images/avatars/avatar-10.png''
import avatarImage11 from ''@/images/avatars/avatar-11.png''

const testimonials = [
  [
    {
      content:
        ''Mira’s teaching style is second to none. Everything was easy to follow every step of the way.'',
      author: {
        name: ''Antonio Littel'',
        role: ''Frontend Developer'',
        image: avatarImage3,
      },
    },
    {
      content:
        ''Even though I was excited to learn, I was pessimistic that I wouldn’t actually ever get good enough to design my own icons. I was wrong — this book is all I needed.'',
      author: {
        name: ''Lynn Nolan'',
        role: ''Growth Marketer'',
        image: avatarImage4,
      },
    },
    {
      content:
        ''I’ve been employed as a professional icon designer for years and still learned tons of new tricks that have made my work even better'',
      author: {
        name: ''Krista Prosacco'',
        role: ''Professional Designer'',
        image: avatarImage9,
      },
    },
  ],
  [
    {
      content:
        ''I run an ecommerce store selling rare vintage gummy bears and could never find a good gummy bear icon. Now I can design my own in minutes.'',
      author: {
        name: ''Cameron Considine'',
        role: ''Entrepreneur'',
        image: avatarImage7,
      },
    },
    {
      content:
        ''The complete package is worth it for the weekly teardown videos alone. I’ve learned so much watching Mira take apart other icons and recreate them from scratch.'',
      author: {
        name: ''Regina Wisoky'',
        role: ''Design Student'',
        image: avatarImage11,
      },
    },
    {
      content:
        ''I didn’t expect to find a lot of value in the community but now I’m in there for at least an hour every day picking up tips from other designers.'',
      author: {
        name: ''Vernon Cummerata'',
        role: ''UI Engineer'',
        image: avatarImage8,
      },
    },
  ],
  [
    {
      content:
        ''I couldn’t believe how fast Mira moved in Figma compared to my own workflow. I’m designing icons more accurately in half the time with the shortcuts I learned from her videos.'',
      author: {
        name: ''Steven Hackett'',
        role: ''Bootcamp Instructor'',
        image: avatarImage5,
      },
    },
    {
      content:
        ''I never thought I would enjoy designing icons but using the ideas in this book, it’s become a great way for me to relax while still being creative.'',
      author: {
        name: ''Carla Schoen'',
        role: ''Startup Founder'',
        image: avatarImage10,
      },
    },
    {
      content:
        ''All I can say is wow — this is easily the best icon design resource I’ve ever encountered.'',
      author: {
        name: ''Leah Kiehn'',
        role: ''Creative Director'',
        image: avatarImage6,
      },
    },
  ],
]

function Testimonial({
  author,
  children,
}: {
  author: { name: string; role: string; image: ImageProps[''src''] }
  children: React.ReactNode
}) {
  return (
    <figure className="rounded-4xl p-8 shadow-md ring-1 ring-slate-900/5">
      <blockquote>
        <p className="text-lg tracking-tight text-slate-900 before:content-[''“''] after:content-[''”'']">
          {children}
        </p>
      </blockquote>
      <figcaption className="mt-6 flex items-center">
        <div className="overflow-hidden rounded-full bg-slate-50">
          <Image
            className="h-12 w-12 object-cover"
            src={author.image}
            alt=""
            width={48}
            height={48}
          />
        </div>
        <div className="ml-4">
          <div className="text-base/6 font-medium tracking-tight text-slate-900">
            {author.name}
          </div>
          <div className="mt-1 text-sm text-slate-600">{author.role}</div>
        </div>
      </figcaption>
    </figure>
  )
}

export function Testimonials() {
  return (
    <section className="py-8 sm:py-10 lg:py-16">
      <Container className="text-center">
        <h2 className="font-display text-4xl font-bold tracking-tight text-slate-900">
          Some kind words from early customers...
        </h2>
        <p className="mt-4 text-lg tracking-tight text-slate-600">
          I worked with a small group of early access customers to make sure all
          of the content in the book was exactly what they needed. Hears what
          they had to say about the finished product.
        </p>
      </Container>
      <Expandable className="group mt-16">
        <ul
          role="list"
          className="mx-auto grid max-w-2xl grid-cols-1 gap-8 px-4 lg:max-w-7xl lg:grid-cols-3 lg:px-8"
        >
          {testimonials
            .map((column) => column[0])
            .map((testimonial, testimonialIndex) => (
              <li key={testimonialIndex} className="lg:hidden">
                <Testimonial author={testimonial.author}>
                  {testimonial.content}
                </Testimonial>
              </li>
            ))}
          {testimonials.map((column, columnIndex) => (
            <li
              key={columnIndex}
              className="hidden group-data-expanded:list-item lg:list-item"
            >
              <ul role="list">
                <ExpandableItems>
                  {column.map((testimonial, testimonialIndex) => (
                    <li
                      key={testimonialIndex}
                      className={clsx(
                        testimonialIndex === 0 && ''hidden lg:list-item'',
                        testimonialIndex === 1 && ''lg:mt-8'',
                        testimonialIndex > 1 && ''mt-8'',
                      )}
                    >
                      <Testimonial author={testimonial.author}>
                        {testimonial.content}
                      </Testimonial>
                    </li>
                  ))}
                </ExpandableItems>
              </ul>
            </li>
          ))}
        </ul>
        <ExpandableButton>Read more testimonials</ExpandableButton>
      </Expandable>
    </section>
  )
}
',
    'testimonials',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'testimonials', 'primer', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-primer", "component_type": "testimonials", "file_path": "tailwind-plus-primer/primer-ts/src/components/Testimonials.tsx", "uses_components": [], "dependencies": ["clsx", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Protocol
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Protocol',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import Link from ''next/link''
import { usePathname } from ''next/navigation''

import { Button } from ''@/components/Button''
import { navigation } from ''@/components/Navigation''

function PageLink({
  label,
  page,
  previous = false,
}: {
  label: string
  page: { href: string; title: string }
  previous?: boolean
}) {
  return (
    <>
      <Button
        href={page.href}
        aria-label={`${label}: ${page.title}`}
        variant="secondary"
        arrow={previous ? ''left'' : ''right''}
      >
        {label}
      </Button>
      <Link
        href={page.href}
        tabIndex={-1}
        aria-hidden="true"
        className="text-base font-semibold text-zinc-900 transition hover:text-zinc-600 dark:text-white dark:hover:text-zinc-300"
      >
        {page.title}
      </Link>
    </>
  )
}

function PageNavigation() {
  let pathname = usePathname()
  let allPages = navigation.flatMap((group) => group.links)
  let currentPageIndex = allPages.findIndex((page) => page.href === pathname)

  if (currentPageIndex === -1) {
    return null
  }

  let previousPage = allPages[currentPageIndex - 1]
  let nextPage = allPages[currentPageIndex + 1]

  if (!previousPage && !nextPage) {
    return null
  }

  return (
    <div className="flex">
      {previousPage && (
        <div className="flex flex-col items-start gap-3">
          <PageLink label="Previous" page={previousPage} previous />
        </div>
      )}
      {nextPage && (
        <div className="ml-auto flex flex-col items-end gap-3">
          <PageLink label="Next" page={nextPage} />
        </div>
      )}
    </div>
  )
}

function XIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true" {...props}>
      <path d="M11.1527 8.92804L16.2525 3H15.044L10.6159 8.14724L7.07919 3H3L8.34821 10.7835L3 17H4.20855L8.88474 11.5643L12.6198 17H16.699L11.1524 8.92804H11.1527ZM9.49748 10.8521L8.95559 10.077L4.644 3.90978H6.50026L9.97976 8.88696L10.5216 9.66202L15.0446 16.1316H13.1883L9.49748 10.8524V10.8521Z" />
    </svg>
  )
}

function GitHubIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M10 1.667c-4.605 0-8.334 3.823-8.334 8.544 0 3.78 2.385 6.974 5.698 8.106.417.075.573-.182.573-.406 0-.203-.011-.875-.011-1.592-2.093.397-2.635-.522-2.802-1.002-.094-.246-.5-1.005-.854-1.207-.291-.16-.708-.556-.01-.567.656-.01 1.124.62 1.281.876.75 1.292 1.948.93 2.427.705.073-.555.291-.93.531-1.143-1.854-.213-3.791-.95-3.791-4.218 0-.929.322-1.698.854-2.296-.083-.214-.375-1.09.083-2.265 0 0 .698-.224 2.292.876a7.576 7.576 0 0 1 2.083-.288c.709 0 1.417.096 2.084.288 1.593-1.11 2.291-.875 2.291-.875.459 1.174.167 2.05.084 2.263.53.599.854 1.357.854 2.297 0 3.278-1.948 4.005-3.802 4.219.302.266.563.78.563 1.58 0 1.143-.011 2.061-.011 2.35 0 .224.156.491.573.405a8.365 8.365 0 0 0 4.11-3.116 8.707 8.707 0 0 0 1.567-4.99c0-4.721-3.73-8.545-8.334-8.545Z"
      />
    </svg>
  )
}

function DiscordIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true" {...props}>
      <path d="M16.238 4.515a14.842 14.842 0 0 0-3.664-1.136.055.055 0 0 0-.059.027 10.35 10.35 0 0 0-.456.938 13.702 13.702 0 0 0-4.115 0 9.479 9.479 0 0 0-.464-.938.058.058 0 0 0-.058-.027c-1.266.218-2.497.6-3.664 1.136a.052.052 0 0 0-.024.02C1.4 8.023.76 11.424 1.074 14.782a.062.062 0 0 0 .024.042 14.923 14.923 0 0 0 4.494 2.272.058.058 0 0 0 .064-.02c.346-.473.654-.972.92-1.496a.057.057 0 0 0-.032-.08 9.83 9.83 0 0 1-1.404-.669.058.058 0 0 1-.029-.046.058.058 0 0 1 .023-.05c.094-.07.189-.144.279-.218a.056.056 0 0 1 .058-.008c2.946 1.345 6.135 1.345 9.046 0a.056.056 0 0 1 .059.007c.09.074.184.149.28.22a.058.058 0 0 1 .023.049.059.059 0 0 1-.028.046 9.224 9.224 0 0 1-1.405.669.058.058 0 0 0-.033.033.056.056 0 0 0 .002.047c.27.523.58 1.022.92 1.495a.056.056 0 0 0 .062.021 14.878 14.878 0 0 0 4.502-2.272.055.055 0 0 0 .016-.018.056.056 0 0 0 .008-.023c.375-3.883-.63-7.256-2.662-10.246a.046.046 0 0 0-.023-.021Zm-9.223 8.221c-.887 0-1.618-.814-1.618-1.814s.717-1.814 1.618-1.814c.908 0 1.632.821 1.618 1.814 0 1-.717 1.814-1.618 1.814Zm5.981 0c-.887 0-1.618-.814-1.618-1.814s.717-1.814 1.618-1.814c.908 0 1.632.821 1.618 1.814 0 1-.71 1.814-1.618 1.814Z" />
    </svg>
  )
}

function SocialLink({
  href,
  icon: Icon,
  children,
}: {
  href: string
  icon: React.ComponentType<{ className?: string }>
  children: React.ReactNode
}) {
  return (
    <Link href={href} className="group">
      <span className="sr-only">{children}</span>
      <Icon className="h-5 w-5 fill-zinc-700 transition group-hover:fill-zinc-900 dark:group-hover:fill-zinc-500" />
    </Link>
  )
}

function SmallPrint() {
  return (
    <div className="flex flex-col items-center justify-between gap-5 border-t border-zinc-900/5 pt-8 sm:flex-row dark:border-white/5">
      <p className="text-xs text-zinc-600 dark:text-zinc-400">
        &copy; Copyright {new Date().getFullYear()}. All rights reserved.
      </p>
      <div className="flex gap-4">
        <SocialLink href="#" icon={XIcon}>
          Follow us on X
        </SocialLink>
        <SocialLink href="#" icon={GitHubIcon}>
          Follow us on GitHub
        </SocialLink>
        <SocialLink href="#" icon={DiscordIcon}>
          Join our Discord server
        </SocialLink>
      </div>
    </div>
  )
}

export function Footer() {
  return (
    <footer className="mx-auto w-full max-w-2xl space-y-10 pb-16 lg:max-w-5xl">
      <PageNavigation />
      <SmallPrint />
    </footer>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "next/navigation"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "footer", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Footer.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "next/navigation"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Auth - Guides - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Auth - Guides - Marketing',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Button } from ''@/components/Button''
import { Heading } from ''@/components/Heading''

const guides = [
  {
    href: ''/authentication'',
    name: ''Authentication'',
    description: ''Learn how to authenticate your API requests.'',
  },
  {
    href: ''/pagination'',
    name: ''Pagination'',
    description: ''Understand how to work with paginated responses.'',
  },
  {
    href: ''/errors'',
    name: ''Errors'',
    description:
      ''Read about the different types of errors returned by the API.'',
  },
  {
    href: ''/webhooks'',
    name: ''Webhooks'',
    description:
      ''Learn how to programmatically configure webhooks for your app.'',
  },
]

export function Guides() {
  return (
    <div className="my-16 xl:max-w-none">
      <Heading level={2} id="guides">
        Guides
      </Heading>
      <div className="not-prose mt-4 grid grid-cols-1 gap-8 border-t border-zinc-900/5 pt-10 sm:grid-cols-2 xl:grid-cols-4 dark:border-white/5">
        {guides.map((guide) => (
          <div key={guide.href}>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white">
              {guide.name}
            </h3>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              {guide.description}
            </p>
            <p className="mt-4">
              <Button href={guide.href} variant="text" arrow="right">
                Read more
              </Button>
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "auth", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Guides.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Protocol
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Protocol',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import clsx from ''clsx''
import { motion, useScroll, useTransform } from ''framer-motion''
import Link from ''next/link''
import { forwardRef } from ''react''

import { Button } from ''@/components/Button''
import { Logo } from ''@/components/Logo''
import {
  MobileNavigation,
  useIsInsideMobileNavigation,
  useMobileNavigationStore,
} from ''@/components/MobileNavigation''
import { MobileSearch, Search } from ''@/components/Search''
import { ThemeToggle } from ''@/components/ThemeToggle''
import { CloseButton } from ''@headlessui/react''

function TopLevelNavItem({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  return (
    <li>
      <Link
        href={href}
        className="text-sm/5 text-zinc-600 transition hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white"
      >
        {children}
      </Link>
    </li>
  )
}

export const Header = forwardRef<
  React.ElementRef<''div''>,
  React.ComponentPropsWithoutRef<typeof motion.div>
>(function Header({ className, ...props }, ref) {
  let { isOpen: mobileNavIsOpen } = useMobileNavigationStore()
  let isInsideMobileNavigation = useIsInsideMobileNavigation()

  let { scrollY } = useScroll()
  let bgOpacityLight = useTransform(scrollY, [0, 72], [''50%'', ''90%''])
  let bgOpacityDark = useTransform(scrollY, [0, 72], [''20%'', ''80%''])

  return (
    <motion.div
      {...props}
      ref={ref}
      className={clsx(
        className,
        ''fixed inset-x-0 top-0 z-50 flex h-14 items-center justify-between gap-12 px-4 transition sm:px-6 lg:left-72 lg:z-30 lg:px-8 xl:left-80'',
        !isInsideMobileNavigation &&
          ''backdrop-blur-xs lg:left-72 xl:left-80 dark:backdrop-blur-sm'',
        isInsideMobileNavigation
          ? ''bg-white dark:bg-zinc-900''
          : ''bg-white/(--bg-opacity-light) dark:bg-zinc-900/(--bg-opacity-dark)'',
      )}
      style={
        {
          ''--bg-opacity-light'': bgOpacityLight,
          ''--bg-opacity-dark'': bgOpacityDark,
        } as React.CSSProperties
      }
    >
      <div
        className={clsx(
          ''absolute inset-x-0 top-full h-px transition'',
          (isInsideMobileNavigation || !mobileNavIsOpen) &&
            ''bg-zinc-900/7.5 dark:bg-white/7.5'',
        )}
      />
      <Search />
      <div className="flex items-center gap-5 lg:hidden">
        <MobileNavigation />
        <CloseButton as={Link} href="/" aria-label="Home">
          <Logo className="h-6" />
        </CloseButton>
      </div>
      <div className="flex items-center gap-5">
        <nav className="hidden md:block">
          <ul role="list" className="flex items-center gap-8">
            <TopLevelNavItem href="/">API</TopLevelNavItem>
            <TopLevelNavItem href="#">Documentation</TopLevelNavItem>
            <TopLevelNavItem href="#">Support</TopLevelNavItem>
          </ul>
        </nav>
        <div className="hidden md:block md:h-5 md:w-px md:bg-zinc-900/10 md:dark:bg-white/15" />
        <div className="flex gap-4">
          <MobileSearch />
          <ThemeToggle />
        </div>
        <div className="hidden min-[416px]:contents">
          <Button href="#">Sign in</Button>
        </div>
      </div>
    </motion.div>
  )
})
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "@headlessui/react", "clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "hero", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "@headlessui/react", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Protocol
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Protocol',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { GridPattern } from ''@/components/GridPattern''

export function HeroPattern() {
  return (
    <div className="absolute inset-0 -z-10 mx-0 max-w-none overflow-hidden">
      <div className="absolute top-0 left-1/2 ml-[-38rem] h-100 w-325 dark:mask-[linear-gradient(white,transparent)]">
        <div className="absolute inset-0 bg-linear-to-r from-[#36b49f] to-[#DBFF75] mask-[radial-gradient(farthest-side_at_top,white,transparent)] opacity-40 dark:from-[#36b49f]/30 dark:to-[#DBFF75]/30 dark:opacity-100">
          <GridPattern
            width={72}
            height={56}
            x={-12}
            y={4}
            squares={[
              [4, 3],
              [2, 1],
              [7, 3],
              [10, 6],
            ]}
            className="absolute inset-x-0 inset-y-[-50%] h-[200%] w-full skew-y-[-18deg] fill-black/40 stroke-black/50 mix-blend-overlay dark:fill-white/2.5 dark:stroke-white/5"
          />
        </div>
        <svg
          viewBox="0 0 1113 440"
          aria-hidden="true"
          className="absolute top-0 left-1/2 ml-[-19rem] w-278.25 fill-white blur-[26px] dark:hidden"
        >
          <path d="M.016 439.5s-9.5-300 434-300S882.516 20 882.516 20V0h230.004v439.5H.016Z" />
        </svg>
      </div>
    </div>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "hero", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/HeroPattern.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Mobilenavigation - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Mobilenavigation - Marketing',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
  TransitionChild,
} from ''@headlessui/react''
import { motion } from ''framer-motion''
import { Suspense, createContext, useContext } from ''react''
import { create } from ''zustand''

import { Header } from ''@/components/Header''
import { Navigation } from ''@/components/Navigation''

function MenuIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      viewBox="0 0 10 9"
      fill="none"
      strokeLinecap="round"
      aria-hidden="true"
      {...props}
    >
      <path d="M.5 1h9M.5 8h9M.5 4.5h9" />
    </svg>
  )
}

function XIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      viewBox="0 0 10 9"
      fill="none"
      strokeLinecap="round"
      aria-hidden="true"
      {...props}
    >
      <path d="m1.5 1 7 7M8.5 1l-7 7" />
    </svg>
  )
}

const IsInsideMobileNavigationContext = createContext(false)

function MobileNavigationDialog({
  isOpen,
  close,
}: {
  isOpen: boolean
  close: () => void
}) {
  return (
    <Dialog
      transition
      open={isOpen}
      onClose={close}
      className="fixed inset-0 z-50 lg:hidden"
    >
      <DialogBackdrop
        transition
        className="fixed inset-0 top-14 bg-zinc-400/20 backdrop-blur-xs data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in dark:bg-black/40"
      />

      <DialogPanel>
        <TransitionChild>
          <Header className="data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in" />
        </TransitionChild>

        <TransitionChild>
          <motion.div
            layoutScroll
            className="fixed top-14 bottom-0 left-0 w-full overflow-y-auto bg-white px-4 pt-6 pb-4 shadow-lg ring-1 shadow-zinc-900/10 ring-zinc-900/7.5 duration-500 ease-in-out data-closed:-translate-x-full min-[416px]:max-w-sm sm:px-6 sm:pb-10 dark:bg-zinc-900 dark:ring-zinc-800"
          >
            <Navigation />
          </motion.div>
        </TransitionChild>
      </DialogPanel>
    </Dialog>
  )
}

export function useIsInsideMobileNavigation() {
  return useContext(IsInsideMobileNavigationContext)
}

export const useMobileNavigationStore = create<{
  isOpen: boolean
  open: () => void
  close: () => void
  toggle: () => void
}>()((set) => ({
  isOpen: false,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
  toggle: () => set((state) => ({ isOpen: !state.isOpen })),
}))

export function MobileNavigation() {
  let isInsideMobileNavigation = useIsInsideMobileNavigation()
  let { isOpen, toggle, close } = useMobileNavigationStore()
  let ToggleIcon = isOpen ? XIcon : MenuIcon

  return (
    <IsInsideMobileNavigationContext.Provider value={true}>
      <button
        type="button"
        className="relative flex size-6 items-center justify-center rounded-md transition hover:bg-zinc-900/5 dark:hover:bg-white/5"
        aria-label="Toggle navigation"
        onClick={toggle}
      >
        <span className="absolute size-12 pointer-fine:hidden" />
        <ToggleIcon className="w-2.5 stroke-zinc-900 dark:stroke-white" />
      </button>
      {!isInsideMobileNavigation && (
        <Suspense fallback={null}>
          <MobileNavigationDialog isOpen={isOpen} close={close} />
        </Suspense>
      )}
    </IsInsideMobileNavigationContext.Provider>
  )
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["framer-motion", "zustand"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "navigation", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/MobileNavigation.tsx", "uses_components": ["Dialog"], "dependencies": ["framer-motion", "zustand"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Navigation - Protocol
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Navigation - Protocol',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import clsx from ''clsx''
import { AnimatePresence, motion, useIsPresent } from ''framer-motion''
import Link from ''next/link''
import { usePathname } from ''next/navigation''
import { useRef } from ''react''

import { Button } from ''@/components/Button''
import { useIsInsideMobileNavigation } from ''@/components/MobileNavigation''
import { useSectionStore } from ''@/components/SectionProvider''
import { Tag } from ''@/components/Tag''
import { remToPx } from ''@/lib/remToPx''
import { CloseButton } from ''@headlessui/react''

interface NavGroup {
  title: string
  links: Array<{
    title: string
    href: string
  }>
}

function useInitialValue<T>(value: T, condition = true) {
  let initialValue = useRef(value).current
  return condition ? initialValue : value
}

function TopLevelNavItem({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  return (
    <li className="md:hidden">
      <CloseButton
        as={Link}
        href={href}
        className="block py-1 text-sm text-zinc-600 transition hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white"
      >
        {children}
      </CloseButton>
    </li>
  )
}

function NavLink({
  href,
  children,
  tag,
  active = false,
  isAnchorLink = false,
}: {
  href: string
  children: React.ReactNode
  tag?: string
  active?: boolean
  isAnchorLink?: boolean
}) {
  return (
    <CloseButton
      as={Link}
      href={href}
      aria-current={active ? ''page'' : undefined}
      className={clsx(
        ''flex justify-between gap-2 py-1 pr-3 text-sm transition'',
        isAnchorLink ? ''pl-7'' : ''pl-4'',
        active
          ? ''text-zinc-900 dark:text-white''
          : ''text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white'',
      )}
    >
      <span className="truncate">{children}</span>
      {tag && (
        <Tag variant="small" color="zinc">
          {tag}
        </Tag>
      )}
    </CloseButton>
  )
}

function VisibleSectionHighlight({
  group,
  pathname,
}: {
  group: NavGroup
  pathname: string
}) {
  let [sections, visibleSections] = useInitialValue(
    [
      useSectionStore((s) => s.sections),
      useSectionStore((s) => s.visibleSections),
    ],
    useIsInsideMobileNavigation(),
  )

  let isPresent = useIsPresent()
  let firstVisibleSectionIndex = Math.max(
    0,
    [{ id: ''_top'' }, ...sections].findIndex(
      (section) => section.id === visibleSections[0],
    ),
  )
  let itemHeight = remToPx(2)
  let height = isPresent
    ? Math.max(1, visibleSections.length) * itemHeight
    : itemHeight
  let top =
    group.links.findIndex((link) => link.href === pathname) * itemHeight +
    firstVisibleSectionIndex * itemHeight

  return (
    <motion.div
      layout
      initial={{ opacity: 0 }}
      animate={{ opacity: 1, transition: { delay: 0.2 } }}
      exit={{ opacity: 0 }}
      className="absolute inset-x-0 top-0 bg-zinc-800/2.5 will-change-transform dark:bg-white/2.5"
      style={{ borderRadius: 8, height, top }}
    />
  )
}

function ActivePageMarker({
  group,
  pathname,
}: {
  group: NavGroup
  pathname: string
}) {
  let itemHeight = remToPx(2)
  let offset = remToPx(0.25)
  let activePageIndex = group.links.findIndex((link) => link.href === pathname)
  let top = offset + activePageIndex * itemHeight

  return (
    <motion.div
      layout
      className="absolute left-2 h-6 w-px bg-emerald-500"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1, transition: { delay: 0.2 } }}
      exit={{ opacity: 0 }}
      style={{ top }}
    />
  )
}

function NavigationGroup({
  group,
  className,
}: {
  group: NavGroup
  className?: string
}) {
  // If this is the mobile navigation then we always render the initial
  // state, so that the state does not change during the close animation.
  // The state will still update when we re-open (re-render) the navigation.
  let isInsideMobileNavigation = useIsInsideMobileNavigation()
  let [pathname, sections] = useInitialValue(
    [usePathname(), useSectionStore((s) => s.sections)],
    isInsideMobileNavigation,
  )

  let isActiveGroup =
    group.links.findIndex((link) => link.href === pathname) !== -1

  return (
    <li className={clsx(''relative mt-6'', className)}>
      <motion.h2
        layout="position"
        className="text-xs font-semibold text-zinc-900 dark:text-white"
      >
        {group.title}
      </motion.h2>
      <div className="relative mt-3 pl-2">
        <AnimatePresence initial={!isInsideMobileNavigation}>
          {isActiveGroup && (
            <VisibleSectionHighlight group={group} pathname={pathname} />
          )}
        </AnimatePresence>
        <motion.div
          layout
          className="absolute inset-y-0 left-2 w-px bg-zinc-900/10 dark:bg-white/5"
        />
        <AnimatePresence initial={false}>
          {isActiveGroup && (
            <ActivePageMarker group={group} pathname={pathname} />
          )}
        </AnimatePresence>
        <ul role="list" className="border-l border-transparent">
          {group.links.map((link) => (
            <motion.li key={link.href} layout="position" className="relative">
              <NavLink href={link.href} active={link.href === pathname}>
                {link.title}
              </NavLink>
              <AnimatePresence mode="popLayout" initial={false}>
                {link.href === pathname && sections.length > 0 && (
                  <motion.ul
                    role="list"
                    initial={{ opacity: 0 }}
                    animate={{
                      opacity: 1,
                      transition: { delay: 0.1 },
                    }}
                    exit={{
                      opacity: 0,
                      transition: { duration: 0.15 },
                    }}
                  >
                    {sections.map((section) => (
                      <li key={section.id}>
                        <NavLink
                          href={`${link.href}#${section.id}`}
                          tag={section.tag}
                          isAnchorLink
                        >
                          {section.title}
                        </NavLink>
                      </li>
                    ))}
                  </motion.ul>
                )}
              </AnimatePresence>
            </motion.li>
          ))}
        </ul>
      </div>
    </li>
  )
}

export const navigation: Array<NavGroup> = [
  {
    title: ''Guides'',
    links: [
      { title: ''Introduction'', href: ''/'' },
      { title: ''Quickstart'', href: ''/quickstart'' },
      { title: ''SDKs'', href: ''/sdks'' },
      { title: ''Authentication'', href: ''/authentication'' },
      { title: ''Pagination'', href: ''/pagination'' },
      { title: ''Errors'', href: ''/errors'' },
      { title: ''Webhooks'', href: ''/webhooks'' },
    ],
  },
  {
    title: ''Resources'',
    links: [
      { title: ''Contacts'', href: ''/contacts'' },
      { title: ''Conversations'', href: ''/conversations'' },
      { title: ''Messages'', href: ''/messages'' },
      { title: ''Groups'', href: ''/groups'' },
      { title: ''Attachments'', href: ''/attachments'' },
    ],
  },
]

export function Navigation(props: React.ComponentPropsWithoutRef<''nav''>) {
  return (
    <nav {...props}>
      <ul role="list">
        <TopLevelNavItem href="/">API</TopLevelNavItem>
        <TopLevelNavItem href="#">Documentation</TopLevelNavItem>
        <TopLevelNavItem href="#">Support</TopLevelNavItem>
        {navigation.map((group, groupIndex) => (
          <NavigationGroup
            key={group.title}
            group={group}
            className={groupIndex === 0 ? ''md:mt-0'' : ''''}
          />
        ))}
        <li className="sticky bottom-0 z-10 mt-6 min-[416px]:hidden">
          <Button href="#" variant="filled" className="w-full">
            Sign in
          </Button>
        </li>
      </ul>
    </nav>
  )
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "clsx", "@headlessui/react", "next/navigation"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "navigation", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Navigation.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "clsx", "@headlessui/react", "next/navigation"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Cta - Resources - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Cta - Resources - Marketing',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import {
  motion,
  useMotionTemplate,
  useMotionValue,
  type MotionValue,
} from ''framer-motion''
import Link from ''next/link''

import { GridPattern } from ''@/components/GridPattern''
import { Heading } from ''@/components/Heading''
import { ChatBubbleIcon } from ''@/components/icons/ChatBubbleIcon''
import { EnvelopeIcon } from ''@/components/icons/EnvelopeIcon''
import { UserIcon } from ''@/components/icons/UserIcon''
import { UsersIcon } from ''@/components/icons/UsersIcon''

interface Resource {
  href: string
  name: string
  description: string
  icon: React.ComponentType<{ className?: string }>
  pattern: Omit<
    React.ComponentPropsWithoutRef<typeof GridPattern>,
    ''width'' | ''height'' | ''x''
  >
}

const resources: Array<Resource> = [
  {
    href: ''/contacts'',
    name: ''Contacts'',
    description:
      ''Learn about the contact model and how to create, retrieve, update, delete, and list contacts.'',
    icon: UserIcon,
    pattern: {
      y: 16,
      squares: [
        [0, 1],
        [1, 3],
      ],
    },
  },
  {
    href: ''/conversations'',
    name: ''Conversations'',
    description:
      ''Learn about the conversation model and how to create, retrieve, update, delete, and list conversations.'',
    icon: ChatBubbleIcon,
    pattern: {
      y: -6,
      squares: [
        [-1, 2],
        [1, 3],
      ],
    },
  },
  {
    href: ''/messages'',
    name: ''Messages'',
    description:
      ''Learn about the message model and how to create, retrieve, update, delete, and list messages.'',
    icon: EnvelopeIcon,
    pattern: {
      y: 32,
      squares: [
        [0, 2],
        [1, 4],
      ],
    },
  },
  {
    href: ''/groups'',
    name: ''Groups'',
    description:
      ''Learn about the group model and how to create, retrieve, update, delete, and list groups.'',
    icon: UsersIcon,
    pattern: {
      y: 22,
      squares: [[0, 1]],
    },
  },
]

function ResourceIcon({ icon: Icon }: { icon: Resource[''icon''] }) {
  return (
    <div className="flex h-7 w-7 items-center justify-center rounded-full bg-zinc-900/5 ring-1 ring-zinc-900/25 backdrop-blur-[2px] transition duration-300 group-hover:bg-white/50 group-hover:ring-zinc-900/25 dark:bg-white/7.5 dark:ring-white/15 dark:group-hover:bg-emerald-300/10 dark:group-hover:ring-emerald-400">
      <Icon className="h-5 w-5 fill-zinc-700/10 stroke-zinc-700 transition-colors duration-300 group-hover:stroke-zinc-900 dark:fill-white/10 dark:stroke-zinc-400 dark:group-hover:fill-emerald-300/10 dark:group-hover:stroke-emerald-400" />
    </div>
  )
}

function ResourcePattern({
  mouseX,
  mouseY,
  ...gridProps
}: Resource[''pattern''] & {
  mouseX: MotionValue<number>
  mouseY: MotionValue<number>
}) {
  let maskImage = useMotionTemplate`radial-gradient(180px at ${mouseX}px ${mouseY}px, white, transparent)`
  let style = { maskImage, WebkitMaskImage: maskImage }

  return (
    <div className="pointer-events-none">
      <div className="absolute inset-0 rounded-2xl mask-[linear-gradient(white,transparent)] transition duration-300 group-hover:opacity-50">
        <GridPattern
          width={72}
          height={56}
          x="50%"
          className="absolute inset-x-0 inset-y-[-30%] h-[160%] w-full skew-y-[-18deg] fill-black/[0.02] stroke-black/5 dark:fill-white/1 dark:stroke-white/2.5"
          {...gridProps}
        />
      </div>
      <motion.div
        className="absolute inset-0 rounded-2xl bg-linear-to-r from-[#D7EDEA] to-[#F4FBDF] opacity-0 transition duration-300 group-hover:opacity-100 dark:from-[#202D2E] dark:to-[#303428]"
        style={style}
      />
      <motion.div
        className="absolute inset-0 rounded-2xl opacity-0 mix-blend-overlay transition duration-300 group-hover:opacity-100"
        style={style}
      >
        <GridPattern
          width={72}
          height={56}
          x="50%"
          className="absolute inset-x-0 inset-y-[-30%] h-[160%] w-full skew-y-[-18deg] fill-black/50 stroke-black/70 dark:fill-white/2.5 dark:stroke-white/10"
          {...gridProps}
        />
      </motion.div>
    </div>
  )
}

function Resource({ resource }: { resource: Resource }) {
  let mouseX = useMotionValue(0)
  let mouseY = useMotionValue(0)

  function onMouseMove({
    currentTarget,
    clientX,
    clientY,
  }: React.MouseEvent<HTMLDivElement>) {
    let { left, top } = currentTarget.getBoundingClientRect()
    mouseX.set(clientX - left)
    mouseY.set(clientY - top)
  }

  return (
    <div
      key={resource.href}
      onMouseMove={onMouseMove}
      className="group relative flex rounded-2xl bg-zinc-50 transition-shadow hover:shadow-md hover:shadow-zinc-900/5 dark:bg-white/2.5 dark:hover:shadow-black/5"
    >
      <ResourcePattern {...resource.pattern} mouseX={mouseX} mouseY={mouseY} />
      <div className="absolute inset-0 rounded-2xl ring-1 ring-zinc-900/7.5 ring-inset group-hover:ring-zinc-900/10 dark:ring-white/10 dark:group-hover:ring-white/20" />
      <div className="relative rounded-2xl px-4 pt-16 pb-4">
        <ResourceIcon icon={resource.icon} />
        <h3 className="mt-4 text-sm/7 font-semibold text-zinc-900 dark:text-white">
          <Link href={resource.href}>
            <span className="absolute inset-0 rounded-2xl" />
            {resource.name}
          </Link>
        </h3>
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
          {resource.description}
        </p>
      </div>
    </div>
  )
}

export function Resources() {
  return (
    <div className="my-16 xl:max-w-none">
      <Heading level={2} id="resources">
        Resources
      </Heading>
      <div className="not-prose mt-4 grid grid-cols-1 gap-8 border-t border-zinc-900/5 pt-10 sm:grid-cols-2 xl:grid-cols-4 dark:border-white/5">
        {resources.map((resource) => (
          <Resource key={resource.href} resource={resource} />
        ))}
      </div>
    </div>
  )
}
',
    'cta',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'cta', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "cta", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Resources.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Ecommerce - Carticon - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Ecommerce - Carticon - Marketing',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'export function CartIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true" {...props}>
      <path
        strokeWidth="0"
        d="M5.98 11.288 3.5 5.5h14l-2.48 5.788A2 2 0 0 1 13.18 12.5H7.82a2 2 0 0 1-1.838-1.212Z"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="m3.5 5.5 2.48 5.788A2 2 0 0 0 7.82 12.5h5.362a2 2 0 0 0 1.839-1.212L17.5 5.5h-14Zm0 0-1-2M6.5 14.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2ZM14.5 14.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z"
      />
    </svg>
  )
}
',
    'ecommerce',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'ecommerce', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "ecommerce", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/icons/CartIcon.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Forms - Feedback - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Forms - Feedback - Marketing',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { Transition } from ''@headlessui/react''
import clsx from ''clsx''
import { forwardRef, useState } from ''react''

function CheckIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" aria-hidden="true" {...props}>
      <circle cx="10" cy="10" r="10" strokeWidth="0" />
      <path
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.5"
        d="m6.75 10.813 2.438 2.437c1.218-4.469 4.062-6.5 4.062-6.5"
      />
    </svg>
  )
}

function FeedbackButton(
  props: Omit<React.ComponentPropsWithoutRef<''button''>, ''type'' | ''className''>,
) {
  return (
    <button
      type="submit"
      className="px-3 text-sm font-medium text-zinc-600 transition hover:bg-zinc-900/2.5 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-white/5 dark:hover:text-white"
      {...props}
    />
  )
}

const FeedbackForm = forwardRef<
  React.ElementRef<''form''>,
  React.ComponentPropsWithoutRef<''form''>
>(function FeedbackForm({ onSubmit, className, ...props }, ref) {
  return (
    <form
      {...props}
      ref={ref}
      onSubmit={onSubmit}
      className={clsx(
        className,
        ''absolute inset-0 flex items-center justify-center gap-6 md:justify-start'',
      )}
    >
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Was this page helpful?
      </p>
      <div className="group grid h-8 grid-cols-[1fr_1px_1fr] overflow-hidden rounded-full border border-zinc-900/10 dark:border-white/10">
        <FeedbackButton data-response="yes">Yes</FeedbackButton>
        <div className="bg-zinc-900/10 dark:bg-white/10" />
        <FeedbackButton data-response="no">No</FeedbackButton>
      </div>
    </form>
  )
})

const FeedbackThanks = forwardRef<
  React.ElementRef<''div''>,
  React.ComponentPropsWithoutRef<''div''>
>(function FeedbackThanks({ className, ...props }, ref) {
  return (
    <div
      {...props}
      ref={ref}
      className={clsx(
        className,
        ''absolute inset-0 flex justify-center md:justify-start'',
      )}
    >
      <div className="flex items-center gap-3 rounded-full bg-emerald-50/50 py-1 pr-3 pl-1.5 text-sm text-emerald-900 ring-1 ring-emerald-500/20 ring-inset dark:bg-emerald-500/5 dark:text-emerald-200 dark:ring-emerald-500/30">
        <CheckIcon className="h-5 w-5 flex-none fill-emerald-500 stroke-white dark:fill-emerald-200/20 dark:stroke-emerald-200" />
        Thanks for your feedback!
      </div>
    </div>
  )
})

export function Feedback() {
  let [submitted, setSubmitted] = useState(false)

  function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    // event.nativeEvent.submitter.dataset.response
    // => "yes" or "no"

    setSubmitted(true)
  }

  return (
    <div className="relative h-8">
      <Transition show={!submitted}>
        <FeedbackForm
          className="duration-300 data-closed:opacity-0 data-leave:pointer-events-none"
          onSubmit={onSubmit}
        />
      </Transition>
      <Transition show={submitted}>
        <FeedbackThanks className="delay-150 duration-300 data-closed:opacity-0" />
      </Transition>
    </div>
  )
}
',
    'forms',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "forms", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Feedback.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Forms - Search - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Forms - Search - Marketing',
    'Marketing/Landing page component from Tailwind Plus Protocol template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import {
  createAutocomplete,
  type AutocompleteApi,
  type AutocompleteCollection,
  type AutocompleteState,
} from ''@algolia/autocomplete-core''
import { Dialog, DialogBackdrop, DialogPanel } from ''@headlessui/react''
import clsx from ''clsx''
import { usePathname, useRouter, useSearchParams } from ''next/navigation''
import {
  Fragment,
  Suspense,
  forwardRef,
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
} from ''react''
import Highlighter from ''react-highlight-words''

import { navigation } from ''@/components/Navigation''
import { type Result } from ''@/mdx/search.mjs''
import { useMobileNavigationStore } from ''./MobileNavigation''

type EmptyObject = Record<string, never>

type Autocomplete = AutocompleteApi<
  Result,
  React.SyntheticEvent,
  React.MouseEvent,
  React.KeyboardEvent
>

function useAutocomplete({ onNavigate }: { onNavigate: () => void }) {
  let id = useId()
  let router = useRouter()
  let [autocompleteState, setAutocompleteState] = useState<
    AutocompleteState<Result> | EmptyObject
  >({})

  function navigate({ itemUrl }: { itemUrl?: string }) {
    if (itemUrl) {
      router.push(itemUrl)
    }

    onNavigate()
  }

  let [autocomplete] = useState<Autocomplete>(() =>
    createAutocomplete<
      Result,
      React.SyntheticEvent,
      React.MouseEvent,
      React.KeyboardEvent
    >({
      id,
      placeholder: ''Find something...'',
      defaultActiveItemId: 0,
      onStateChange({ state }) {
        setAutocompleteState(state)
      },
      shouldPanelOpen({ state }) {
        return state.query !== ''''
      },
      navigator: {
        navigate,
      },
      getSources({ query }) {
        return import(''@/mdx/search.mjs'').then(({ search }) => {
          return [
            {
              sourceId: ''documentation'',
              getItems() {
                return search(query, { limit: 5 })
              },
              getItemUrl({ item }) {
                return item.url
              },
              onSelect: navigate,
            },
          ]
        })
      },
    }),
  )

  return { autocomplete, autocompleteState }
}

function SearchIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" {...props}>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12.01 12a4.25 4.25 0 1 0-6.02-6 4.25 4.25 0 0 0 6.02 6Zm0 0 3.24 3.25"
      />
    </svg>
  )
}

function NoResultsIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" {...props}>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M12.01 12a4.237 4.237 0 0 0 1.24-3c0-.62-.132-1.207-.37-1.738M12.01 12A4.237 4.237 0 0 1 9 13.25c-.635 0-1.237-.14-1.777-.388M12.01 12l3.24 3.25m-3.715-9.661a4.25 4.25 0 0 0-5.975 5.908M4.5 15.5l11-11"
      />
    </svg>
  )
}

function LoadingIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  let id = useId()

  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" {...props}>
      <circle cx="10" cy="10" r="5.5" strokeLinejoin="round" />
      <path
        stroke={`url(#${id})`}
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15.5 10a5.5 5.5 0 1 0-5.5 5.5"
      />
      <defs>
        <linearGradient
          id={id}
          x1="13"
          x2="9.5"
          y1="9"
          y2="15"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="currentColor" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0" />
        </linearGradient>
      </defs>
    </svg>
  )
}

function HighlightQuery({ text, query }: { text: string; query: string }) {
  return (
    <Highlighter
      highlightClassName="underline bg-transparent text-emerald-500"
      searchWords={[query]}
      autoEscape={true}
      textToHighlight={text}
    />
  )
}

function SearchResult({
  result,
  resultIndex,
  autocomplete,
  collection,
  query,
}: {
  result: Result
  resultIndex: number
  autocomplete: Autocomplete
  collection: AutocompleteCollection<Result>
  query: string
}) {
  let id = useId()

  let sectionTitle = navigation.find((section) =>
    section.links.find((link) => link.href === result.url.split(''#'')[0]),
  )?.title
  let hierarchy = [sectionTitle, result.pageTitle].filter(
    (x): x is string => typeof x === ''string'',
  )

  return (
    <li
      className={clsx(
        ''group block cursor-default px-4 py-3 aria-selected:bg-zinc-50 dark:aria-selected:bg-zinc-800/50'',
        resultIndex > 0 && ''border-t border-zinc-100 dark:border-zinc-800'',
      )}
      aria-labelledby={`${id}-hierarchy ${id}-title`}
      {...autocomplete.getItemProps({
        item: result,
        source: collection.source,
      })}
    >
      <div
        id={`${id}-title`}
        aria-hidden="true"
        className="text-sm font-medium text-zinc-900 group-aria-selected:text-emerald-500 dark:text-white"
      >
        <HighlightQuery text={result.title} query={query} />
      </div>
      {hierarchy.length > 0 && (
        <div
          id={`${id}-hierarchy`}
          aria-hidden="true"
          className="mt-1 truncate text-2xs whitespace-nowrap text-zinc-500"
        >
          {hierarchy.map((item, itemIndex, items) => (
            <Fragment key={itemIndex}>
              <HighlightQuery text={item} query={query} />
              <span
                className={
                  itemIndex === items.length - 1
                    ? ''sr-only''
                    : ''mx-2 text-zinc-300 dark:text-zinc-700''
                }
              >
                /
              </span>
            </Fragment>
          ))}
        </div>
      )}
    </li>
  )
}

function SearchResults({
  autocomplete,
  query,
  collection,
}: {
  autocomplete: Autocomplete
  query: string
  collection: AutocompleteCollection<Result>
}) {
  if (collection.items.length === 0) {
    return (
      <div className="p-6 text-center">
        <NoResultsIcon className="mx-auto h-5 w-5 stroke-zinc-900 dark:stroke-zinc-600" />
        <p className="mt-2 text-xs text-zinc-700 dark:text-zinc-400">
          Nothing found for{'' ''}
          <strong className="font-semibold break-words text-zinc-900 dark:text-white">
            &lsquo;{query}&rsquo;
          </strong>
          . Please try again.
        </p>
      </div>
    )
  }

  return (
    <ul {...autocomplete.getListProps()}>
      {collection.items.map((result, resultIndex) => (
        <SearchResult
          key={result.url}
          result={result}
          resultIndex={resultIndex}
          autocomplete={autocomplete}
          collection={collection}
          query={query}
        />
      ))}
    </ul>
  )
}

const SearchInput = forwardRef<
  React.ElementRef<''input''>,
  {
    autocomplete: Autocomplete
    autocompleteState: AutocompleteState<Result> | EmptyObject
    onClose: () => void
  }
>(function SearchInput({ autocomplete, autocompleteState, onClose }, inputRef) {
  let inputProps = autocomplete.getInputProps({ inputElement: null })

  return (
    <div className="group relative flex h-12">
      <SearchIcon className="pointer-events-none absolute top-0 left-3 h-full w-5 stroke-zinc-500" />
      <input
        ref={inputRef}
        data-autofocus
        className={clsx(
          ''flex-auto appearance-none bg-transparent pl-10 text-zinc-900 outline-hidden placeholder:text-zinc-500 focus:w-full focus:flex-none sm:text-sm dark:text-white [&::-webkit-search-cancel-button]:hidden [&::-webkit-search-decoration]:hidden [&::-webkit-search-results-button]:hidden [&::-webkit-search-results-decoration]:hidden'',
          autocompleteState.status === ''stalled'' ? ''pr-11'' : ''pr-4'',
        )}
        {...inputProps}
        onKeyDown={(event) => {
          if (
            event.key === ''Escape'' &&
            !autocompleteState.isOpen &&
            autocompleteState.query === ''''
          ) {
            // In Safari, closing the dialog with the escape key can sometimes cause the scroll position to jump to the
            // bottom of the page. This is a workaround for that until we can figure out a proper fix in Headless UI.
            if (document.activeElement instanceof HTMLElement) {
              document.activeElement.blur()
            }

            onClose()
          } else {
            inputProps.onKeyDown(event)
          }
        }}
      />
      {autocompleteState.status === ''stalled'' && (
        <div className="absolute inset-y-0 right-3 flex items-center">
          <LoadingIcon className="h-5 w-5 animate-spin stroke-zinc-200 text-zinc-900 dark:stroke-zinc-800 dark:text-emerald-400" />
        </div>
      )}
    </div>
  )
})

function SearchDialog({
  open,
  setOpen,
  className,
  onNavigate = () => {},
}: {
  open: boolean
  setOpen: (open: boolean) => void
  className?: string
  onNavigate?: () => void
}) {
  let formRef = useRef<React.ElementRef<''form''>>(null)
  let panelRef = useRef<React.ElementRef<''div''>>(null)
  let inputRef = useRef<React.ElementRef<typeof SearchInput>>(null)
  let { autocomplete, autocompleteState } = useAutocomplete({
    onNavigate() {
      onNavigate()
      setOpen(false)
    },
  })
  let pathname = usePathname()
  let searchParams = useSearchParams()

  useEffect(() => {
    setOpen(false)
  }, [pathname, searchParams, setOpen])

  useEffect(() => {
    if (open) {
      return
    }

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === ''k'' && (event.metaKey || event.ctrlKey)) {
        event.preventDefault()
        setOpen(true)
      }
    }

    window.addEventListener(''keydown'', onKeyDown)

    return () => {
      window.removeEventListener(''keydown'', onKeyDown)
    }
  }, [open, setOpen])

  return (
    <Dialog
      open={open}
      onClose={() => {
        setOpen(false)
        autocomplete.setQuery('''')
      }}
      className={clsx(''fixed inset-0 z-50'', className)}
    >
      <DialogBackdrop
        transition
        className="fixed inset-0 bg-zinc-400/25 backdrop-blur-xs data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in dark:bg-black/40"
      />

      <div className="fixed inset-0 overflow-y-auto px-4 py-4 sm:px-6 sm:py-20 md:py-32 lg:px-8 lg:py-[15vh]">
        <DialogPanel
          transition
          className="mx-auto transform-gpu overflow-hidden rounded-lg bg-zinc-50 shadow-xl ring-1 ring-zinc-900/7.5 data-closed:scale-95 data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in sm:max-w-xl dark:bg-zinc-900 dark:ring-zinc-800"
        >
          <div {...autocomplete.getRootProps({})}>
            <form
              ref={formRef}
              {...autocomplete.getFormProps({
                inputElement: inputRef.current,
              })}
            >
              <SearchInput
                ref={inputRef}
                autocomplete={autocomplete}
                autocompleteState={autocompleteState}
                onClose={() => setOpen(false)}
              />
              <div
                ref={panelRef}
                className="border-t border-zinc-200 bg-white empty:hidden dark:border-zinc-100/5 dark:bg-white/2.5"
                {...autocomplete.getPanelProps({})}
              >
                {autocompleteState.isOpen && (
                  <SearchResults
                    autocomplete={autocomplete}
                    query={autocompleteState.query}
                    collection={autocompleteState.collections[0]}
                  />
                )}
              </div>
            </form>
          </div>
        </DialogPanel>
      </div>
    </Dialog>
  )
}

function useSearchProps() {
  let buttonRef = useRef<React.ElementRef<''button''>>(null)
  let [open, setOpen] = useState(false)

  return {
    buttonProps: {
      ref: buttonRef,
      onClick() {
        setOpen(true)
      },
    },
    dialogProps: {
      open,
      setOpen: useCallback(
        (open: boolean) => {
          let { width = 0, height = 0 } =
            buttonRef.current?.getBoundingClientRect() ?? {}
          if (!open || (width !== 0 && height !== 0)) {
            setOpen(open)
          }
        },
        [setOpen],
      ),
    },
  }
}

export function Search() {
  let [modifierKey, setModifierKey] = useState<string>()
  let { buttonProps, dialogProps } = useSearchProps()

  useEffect(() => {
    setModifierKey(
      /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform) ? ''⌘'' : ''Ctrl '',
    )
  }, [])

  return (
    <div className="hidden lg:block lg:max-w-md lg:flex-auto">
      <button
        type="button"
        className="hidden h-8 w-full items-center gap-2 rounded-full bg-white pr-3 pl-2 text-sm text-zinc-500 ring-1 ring-zinc-900/10 transition hover:ring-zinc-900/20 lg:flex dark:bg-white/5 dark:text-zinc-400 dark:ring-white/10 dark:ring-inset dark:hover:ring-white/20"
        {...buttonProps}
      >
        <SearchIcon className="h-5 w-5 stroke-current" />
        Find something...
        <kbd className="ml-auto text-2xs text-zinc-400 dark:text-zinc-500">
          <kbd className="font-sans">{modifierKey}</kbd>
          <kbd className="font-sans">K</kbd>
        </kbd>
      </button>
      <Suspense fallback={null}>
        <SearchDialog className="hidden lg:block" {...dialogProps} />
      </Suspense>
    </div>
  )
}

export function MobileSearch() {
  let { close } = useMobileNavigationStore()
  let { buttonProps, dialogProps } = useSearchProps()

  return (
    <div className="contents lg:hidden">
      <button
        type="button"
        className="relative flex size-6 items-center justify-center rounded-md transition hover:bg-zinc-900/5 lg:hidden dark:hover:bg-white/5"
        aria-label="Find something..."
        {...buttonProps}
      >
        <span className="absolute size-12 pointer-fine:hidden" />
        <SearchIcon className="h-5 w-5 stroke-zinc-900 dark:stroke-white" />
      </button>
      <Suspense fallback={null}>
        <SearchDialog
          className="lg:hidden"
          onNavigate={close}
          {...dialogProps}
        />
      </Suspense>
    </div>
  )
}
',
    'forms',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["clsx", "next/navigation", "@headlessui/react", "react-highlight-words"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-protocol", "component_type": "forms", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Search.tsx", "uses_components": ["Dialog"], "dependencies": ["clsx", "next/navigation", "@headlessui/react", "react-highlight-words"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Radiant
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Radiant',
    'Marketing/Landing page component from Tailwind Plus Radiant template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { PlusGrid, PlusGridItem, PlusGridRow } from ''@/components/plus-grid''
import { Button } from ''./button''
import { Container } from ''./container''
import { Gradient } from ''./gradient''
import { Link } from ''./link''
import { Logo } from ''./logo''
import { Subheading } from ''./text''

function CallToAction() {
  return (
    <div className="relative pt-20 pb-16 text-center sm:py-24">
      <hgroup>
        <Subheading>Get started</Subheading>
        <p className="mt-6 text-3xl font-medium tracking-tight text-gray-950 sm:text-5xl">
          Ready to dive in?
          <br />
          Start your free trial today.
        </p>
      </hgroup>
      <p className="mx-auto mt-6 max-w-xs text-sm/6 text-gray-500">
        Get the cheat codes for selling and unlock your team&apos;s revenue
        potential.
      </p>
      <div className="mt-6">
        <Button className="w-full sm:w-auto" href="#">
          Get started
        </Button>
      </div>
    </div>
  )
}

function SitemapHeading({ children }: { children: React.ReactNode }) {
  return <h3 className="text-sm/6 font-medium text-gray-950/50">{children}</h3>
}

function SitemapLinks({ children }: { children: React.ReactNode }) {
  return <ul className="mt-6 space-y-4 text-sm/6">{children}</ul>
}

function SitemapLink(props: React.ComponentPropsWithoutRef<typeof Link>) {
  return (
    <li>
      <Link
        {...props}
        className="font-medium text-gray-950 data-hover:text-gray-950/75"
      />
    </li>
  )
}

function Sitemap() {
  return (
    <>
      <div>
        <SitemapHeading>Product</SitemapHeading>
        <SitemapLinks>
          <SitemapLink href="/pricing">Pricing</SitemapLink>
          <SitemapLink href="#">Analysis</SitemapLink>
          <SitemapLink href="#">API</SitemapLink>
        </SitemapLinks>
      </div>
      <div>
        <SitemapHeading>Company</SitemapHeading>
        <SitemapLinks>
          <SitemapLink href="#">Careers</SitemapLink>
          <SitemapLink href="/blog">Blog</SitemapLink>
          <SitemapLink href="/company">Company</SitemapLink>
        </SitemapLinks>
      </div>
      <div>
        <SitemapHeading>Support</SitemapHeading>
        <SitemapLinks>
          <SitemapLink href="#">Help center</SitemapLink>
          <SitemapLink href="#">Community</SitemapLink>
        </SitemapLinks>
      </div>
      <div>
        <SitemapHeading>Company</SitemapHeading>
        <SitemapLinks>
          <SitemapLink href="#">Terms of service</SitemapLink>
          <SitemapLink href="#">Privacy policy</SitemapLink>
        </SitemapLinks>
      </div>
    </>
  )
}

function SocialIconX(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 16 16" fill="currentColor" {...props}>
      <path d="M12.6 0h2.454l-5.36 6.778L16 16h-4.937l-3.867-5.594L2.771 16H.316l5.733-7.25L0 0h5.063l3.495 5.114L12.6 0zm-.86 14.376h1.36L4.323 1.539H2.865l8.875 12.837z" />
    </svg>
  )
}

function SocialIconFacebook(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 16 16" fill="currentColor" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M16 8.05C16 3.603 12.418 0 8 0S0 3.604 0 8.05c0 4.016 2.926 7.346 6.75 7.95v-5.624H4.718V8.05H6.75V6.276c0-2.017 1.194-3.131 3.022-3.131.875 0 1.79.157 1.79.157v1.98h-1.008c-.994 0-1.304.62-1.304 1.257v1.51h2.219l-.355 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.95z"
      />
    </svg>
  )
}

function SocialIconLinkedIn(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 16 16" fill="currentColor" {...props}>
      <path d="M14.82 0H1.18A1.169 1.169 0 000 1.154v13.694A1.168 1.168 0 001.18 16h13.64A1.17 1.17 0 0016 14.845V1.15A1.171 1.171 0 0014.82 0zM4.744 13.64H2.369V5.996h2.375v7.644zm-1.18-8.684a1.377 1.377 0 11.52-.106 1.377 1.377 0 01-.527.103l.007.003zm10.075 8.683h-2.375V9.921c0-.885-.015-2.025-1.234-2.025-1.218 0-1.425.966-1.425 1.968v3.775H6.233V5.997H8.51v1.05h.032c.317-.601 1.09-1.235 2.246-1.235 2.405-.005 2.851 1.578 2.851 3.63v4.197z" />
    </svg>
  )
}

function SocialLinks() {
  return (
    <>
      <Link
        href="https://facebook.com"
        target="_blank"
        aria-label="Visit us on Facebook"
        className="text-gray-950 data-hover:text-gray-950/75"
      >
        <SocialIconFacebook className="size-4" />
      </Link>
      <Link
        href="https://x.com"
        target="_blank"
        aria-label="Visit us on X"
        className="text-gray-950 data-hover:text-gray-950/75"
      >
        <SocialIconX className="size-4" />
      </Link>
      <Link
        href="https://linkedin.com"
        target="_blank"
        aria-label="Visit us on LinkedIn"
        className="text-gray-950 data-hover:text-gray-950/75"
      >
        <SocialIconLinkedIn className="size-4" />
      </Link>
    </>
  )
}

function Copyright() {
  return (
    <div className="text-sm/6 text-gray-950">
      &copy; {new Date().getFullYear()} Radiant Inc.
    </div>
  )
}

export function Footer() {
  return (
    <footer>
      <Gradient className="relative">
        <div className="absolute inset-2 rounded-4xl bg-white/80" />
        <Container>
          <CallToAction />
          <PlusGrid className="pb-16">
            <PlusGridRow>
              <div className="grid grid-cols-2 gap-y-10 pb-6 lg:grid-cols-6 lg:gap-8">
                <div className="col-span-2 flex">
                  <PlusGridItem className="pt-6 lg:pb-6">
                    <Logo className="h-9" />
                  </PlusGridItem>
                </div>
                <div className="col-span-2 grid grid-cols-2 gap-x-8 gap-y-12 lg:col-span-4 lg:grid-cols-subgrid lg:pt-6">
                  <Sitemap />
                </div>
              </div>
            </PlusGridRow>
            <PlusGridRow className="flex justify-between">
              <div>
                <PlusGridItem className="py-3">
                  <Copyright />
                </PlusGridItem>
              </div>
              <div className="flex">
                <PlusGridItem className="flex items-center gap-8 py-3">
                  <SocialLinks />
                </PlusGridItem>
              </div>
            </PlusGridRow>
          </PlusGrid>
        </Container>
      </Gradient>
    </footer>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-radiant", "component_type": "footer", "file_path": "tailwind-plus-radiant/radiant-ts/src/components/footer.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Navigation - Radiant
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Navigation - Radiant',
    'Marketing/Landing page component from Tailwind Plus Radiant template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from ''@headlessui/react''
import { Bars2Icon } from ''@heroicons/react/24/solid''
import { motion } from ''framer-motion''
import { Link } from ''./link''
import { Logo } from ''./logo''
import { PlusGrid, PlusGridItem, PlusGridRow } from ''./plus-grid''

const links = [
  { href: ''/pricing'', label: ''Pricing'' },
  { href: ''/company'', label: ''Company'' },
  { href: ''/blog'', label: ''Blog'' },
  { href: ''/login'', label: ''Login'' },
]

function DesktopNav() {
  return (
    <nav className="relative hidden lg:flex">
      {links.map(({ href, label }) => (
        <PlusGridItem key={href} className="relative flex">
          <Link
            href={href}
            className="flex items-center px-4 py-3 text-base font-medium text-gray-950 bg-blend-multiply data-hover:bg-black/2.5"
          >
            {label}
          </Link>
        </PlusGridItem>
      ))}
    </nav>
  )
}

function MobileNavButton() {
  return (
    <DisclosureButton
      className="flex size-12 items-center justify-center self-center rounded-lg data-hover:bg-black/5 lg:hidden"
      aria-label="Open main menu"
    >
      <Bars2Icon className="size-6" />
    </DisclosureButton>
  )
}

function MobileNav() {
  return (
    <DisclosurePanel className="lg:hidden">
      <div className="flex flex-col gap-6 py-4">
        {links.map(({ href, label }, linkIndex) => (
          <motion.div
            initial={{ opacity: 0, rotateX: -90 }}
            animate={{ opacity: 1, rotateX: 0 }}
            transition={{
              duration: 0.15,
              ease: ''easeInOut'',
              rotateX: { duration: 0.3, delay: linkIndex * 0.1 },
            }}
            key={href}
          >
            <Link href={href} className="text-base font-medium text-gray-950">
              {label}
            </Link>
          </motion.div>
        ))}
      </div>
      <div className="absolute left-1/2 w-screen -translate-x-1/2">
        <div className="absolute inset-x-0 top-0 border-t border-black/5" />
        <div className="absolute inset-x-0 top-2 border-t border-black/5" />
      </div>
    </DisclosurePanel>
  )
}

export function Navbar({ banner }: { banner?: React.ReactNode }) {
  return (
    <Disclosure as="header" className="pt-12 sm:pt-16">
      <PlusGrid>
        <PlusGridRow className="relative flex justify-between">
          <div className="relative flex gap-6">
            <PlusGridItem className="py-3">
              <Link href="/" title="Home">
                <Logo className="h-9" />
              </Link>
            </PlusGridItem>
            {banner && (
              <div className="relative hidden items-center py-3 lg:flex">
                {banner}
              </div>
            )}
          </div>
          <DesktopNav />
          <MobileNavButton />
        </PlusGridRow>
      </PlusGrid>
      <MobileNav />
    </Disclosure>
  )
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["framer-motion", "@heroicons/react/24/solid"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-radiant", "component_type": "navigation", "file_path": "tailwind-plus-radiant/radiant-ts/src/components/navbar.tsx", "uses_components": [], "dependencies": ["framer-motion", "@heroicons/react/24/solid"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Blog - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Blog - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Radiant template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Button } from ''@/components/button''
import { Container } from ''@/components/container''
import { Footer } from ''@/components/footer''
import { GradientBackground } from ''@/components/gradient''
import { Link } from ''@/components/link''
import { Navbar } from ''@/components/navbar''
import { Heading, Subheading } from ''@/components/text''
import { image } from ''@/sanity/image''
import { getPost } from ''@/sanity/queries''
import { ChevronLeftIcon } from ''@heroicons/react/16/solid''
import dayjs from ''dayjs''
import type { Metadata } from ''next''
import { PortableText } from ''next-sanity''
import { notFound } from ''next/navigation''

export async function generateMetadata({
  params,
}: {
  params: { slug: string }
}): Promise<Metadata> {
  let post = await getPost(params.slug)

  return post ? { title: post.title, description: post.excerpt } : {}
}

export default async function BlogPost({
  params,
}: {
  params: { slug: string }
}) {
  let post = (await getPost(params.slug)) || notFound()

  return (
    <main className="overflow-hidden">
      <GradientBackground />
      <Container>
        <Navbar />
        <Subheading className="mt-16">
          {dayjs(post.publishedAt).format(''dddd, MMMM D, YYYY'')}
        </Subheading>
        <Heading as="h1" className="mt-2">
          {post.title}
        </Heading>
        <div className="mt-16 grid grid-cols-1 gap-8 pb-24 lg:grid-cols-[15rem_1fr] xl:grid-cols-[15rem_1fr_15rem]">
          <div className="flex flex-wrap items-center gap-8 max-lg:justify-between lg:flex-col lg:items-start">
            {post.author && (
              <div className="flex items-center gap-3">
                {post.author.image && (
                  <img
                    alt=""
                    src={image(post.author.image).size(64, 64).url()}
                    className="aspect-square size-6 rounded-full object-cover"
                  />
                )}
                <div className="text-sm/5 text-gray-700">
                  {post.author.name}
                </div>
              </div>
            )}
            {Array.isArray(post.categories) && (
              <div className="flex flex-wrap gap-2">
                {post.categories.map((category) => (
                  <Link
                    key={category.slug}
                    href={`/blog?category=${category.slug}`}
                    className="rounded-full border border-dotted border-gray-300 bg-gray-50 px-2 text-sm/6 font-medium text-gray-500"
                  >
                    {category.title}
                  </Link>
                ))}
              </div>
            )}
          </div>
          <div className="text-gray-700">
            <div className="max-w-2xl xl:mx-auto">
              {post.mainImage && (
                <img
                  alt={post.mainImage.alt || ''''}
                  src={image(post.mainImage).size(2016, 1344).url()}
                  className="mb-10 aspect-3/2 w-full rounded-2xl object-cover shadow-xl"
                />
              )}
              {post.body && (
                <PortableText
                  value={post.body}
                  components={{
                    block: {
                      normal: ({ children }) => (
                        <p className="my-10 text-base/8 first:mt-0 last:mb-0">
                          {children}
                        </p>
                      ),
                      h2: ({ children }) => (
                        <h2 className="mt-12 mb-10 text-2xl/8 font-medium tracking-tight text-gray-950 first:mt-0 last:mb-0">
                          {children}
                        </h2>
                      ),
                      h3: ({ children }) => (
                        <h3 className="mt-12 mb-10 text-xl/8 font-medium tracking-tight text-gray-950 first:mt-0 last:mb-0">
                          {children}
                        </h3>
                      ),
                      blockquote: ({ children }) => (
                        <blockquote className="my-10 border-l-2 border-l-gray-300 pl-6 text-base/8 text-gray-950 first:mt-0 last:mb-0">
                          {children}
                        </blockquote>
                      ),
                    },
                    types: {
                      image: ({ value }) => (
                        <img
                          alt={value.alt || ''''}
                          src={image(value).width(2000).url()}
                          className="w-full rounded-2xl"
                        />
                      ),
                      separator: ({ value }) => {
                        switch (value.style) {
                          case ''line'':
                            return (
                              <hr className="my-8 border-t border-gray-200" />
                            )
                          case ''space'':
                            return <div className="my-8" />
                          default:
                            return null
                        }
                      },
                    },
                    list: {
                      bullet: ({ children }) => (
                        <ul className="list-disc pl-4 text-base/8 marker:text-gray-400">
                          {children}
                        </ul>
                      ),
                      number: ({ children }) => (
                        <ol className="list-decimal pl-4 text-base/8 marker:text-gray-400">
                          {children}
                        </ol>
                      ),
                    },
                    listItem: {
                      bullet: ({ children }) => {
                        return (
                          <li className="my-2 pl-2 has-[br]:mb-8">
                            {children}
                          </li>
                        )
                      },
                      number: ({ children }) => {
                        return (
                          <li className="my-2 pl-2 has-[br]:mb-8">
                            {children}
                          </li>
                        )
                      },
                    },
                    marks: {
                      strong: ({ children }) => (
                        <strong className="font-semibold text-gray-950">
                          {children}
                        </strong>
                      ),
                      code: ({ children }) => (
                        <>
                          <span aria-hidden>`</span>
                          <code className="text-[15px]/8 font-semibold text-gray-950">
                            {children}
                          </code>
                          <span aria-hidden>`</span>
                        </>
                      ),
                      link: ({ value, children }) => {
                        return (
                          <Link
                            href={value.href}
                            className="font-medium text-gray-950 underline decoration-gray-400 underline-offset-4 data-hover:decoration-gray-600"
                          >
                            {children}
                          </Link>
                        )
                      },
                    },
                  }}
                />
              )}
              <div className="mt-10">
                <Button variant="outline" href="/blog">
                  <ChevronLeftIcon className="size-4" />
                  Back to blog
                </Button>
              </div>
            </div>
          </div>
        </div>
      </Container>
      <Footer />
    </main>
  )
}
',
    'blog',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/navigation", "dayjs", "@heroicons/react/16/solid", "next-sanity"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-radiant", "component_type": "blog", "file_path": "tailwind-plus-radiant/radiant-ts/src/app/blog/[slug]/page.tsx", "uses_components": ["Button"], "dependencies": ["next/navigation", "dayjs", "@heroicons/react/16/solid", "next-sanity"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Auth - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Auth - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Radiant template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Button } from ''@/components/button''
import { GradientBackground } from ''@/components/gradient''
import { Link } from ''@/components/link''
import { Mark } from ''@/components/logo''
import { Checkbox, Field, Input, Label } from ''@headlessui/react''
import { CheckIcon } from ''@heroicons/react/16/solid''
import { clsx } from ''clsx''
import type { Metadata } from ''next''

export const metadata: Metadata = {
  title: ''Login'',
  description: ''Sign in to your account to continue.'',
}

export default function Login() {
  return (
    <main className="overflow-hidden bg-gray-50">
      <GradientBackground />
      <div className="isolate flex min-h-dvh items-center justify-center p-6 lg:p-8">
        <div className="w-full max-w-md rounded-xl bg-white shadow-md ring-1 ring-black/5">
          <form action="#" method="POST" className="p-7 sm:p-11">
            <div className="flex items-start">
              <Link href="/" title="Home">
                <Mark className="h-9 fill-black" />
              </Link>
            </div>
            <h1 className="mt-8 text-base/6 font-medium">Welcome back!</h1>
            <p className="mt-1 text-sm/5 text-gray-600">
              Sign in to your account to continue.
            </p>
            <Field className="mt-8 space-y-3">
              <Label className="text-sm/5 font-medium">Email</Label>
              <Input
                required
                autoFocus
                type="email"
                name="email"
                className={clsx(
                  ''block w-full rounded-lg border border-transparent shadow-sm ring-1 ring-black/10'',
                  ''px-[calc(--spacing(2)-1px)] py-[calc(--spacing(1.5)-1px)] text-base/6 sm:text-sm/6'',
                  ''data-focus:outline-2 data-focus:-outline-offset-1 data-focus:outline-black'',
                )}
              />
            </Field>
            <Field className="mt-8 space-y-3">
              <Label className="text-sm/5 font-medium">Password</Label>
              <Input
                required
                type="password"
                name="password"
                className={clsx(
                  ''block w-full rounded-lg border border-transparent shadow-sm ring-1 ring-black/10'',
                  ''px-[calc(--spacing(2)-1px)] py-[calc(--spacing(1.5)-1px)] text-base/6 sm:text-sm/6'',
                  ''data-focus:outline-2 data-focus:-outline-offset-1 data-focus:outline-black'',
                )}
              />
            </Field>
            <div className="mt-8 flex items-center justify-between text-sm/5">
              <Field className="flex items-center gap-3">
                <Checkbox
                  name="remember-me"
                  className={clsx(
                    ''group block size-4 rounded-sm border border-transparent shadow-sm ring-1 ring-black/10'',
                    ''data-checked:bg-black data-checked:ring-black'',
                    ''data-focus:outline-2 data-focus:outline-offset-2 data-focus:outline-black'',
                  )}
                >
                  <CheckIcon className="fill-white opacity-0 group-data-checked:opacity-100" />
                </Checkbox>
                <Label>Remember me</Label>
              </Field>
              <Link href="#" className="font-medium hover:text-gray-600">
                Forgot password?
              </Link>
            </div>
            <div className="mt-8">
              <Button type="submit" className="w-full">
                Sign in
              </Button>
            </div>
          </form>
          <div className="m-1.5 rounded-lg bg-gray-50 py-4 text-center text-sm/5 ring-1 ring-black/5">
            Not a member?{'' ''}
            <Link href="#" className="font-medium hover:text-gray-600">
              Create an account
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Input", "Button"], "dependencies": ["clsx", "@heroicons/react/16/solid", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-radiant", "component_type": "auth", "file_path": "tailwind-plus-radiant/radiant-ts/src/app/login/page.tsx", "uses_components": ["Input", "Button"], "dependencies": ["clsx", "@heroicons/react/16/solid", "@headlessui/react"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Pricing Section - Radiant
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Pricing Section - Radiant',
    'Marketing/Landing page component from Tailwind Plus Radiant template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Button } from ''@/components/button''
import { Container } from ''@/components/container''
import { Footer } from ''@/components/footer''
import { Gradient, GradientBackground } from ''@/components/gradient''
import { Link } from ''@/components/link''
import { LogoCloud } from ''@/components/logo-cloud''
import { Navbar } from ''@/components/navbar''
import { Heading, Lead, Subheading } from ''@/components/text''
import { Menu, MenuButton, MenuItem, MenuItems } from ''@headlessui/react''
import {
  CheckIcon,
  ChevronUpDownIcon,
  MinusIcon,
} from ''@heroicons/react/16/solid''
import type { Metadata } from ''next''

export const metadata: Metadata = {
  title: ''Pricing'',
  description:
    ''Companies all over the world have closed millions of deals with Radiant. Sign up today and start selling smarter.'',
}

const tiers = [
  {
    name: ''Starter'' as const,
    slug: ''starter'',
    description: ''Everything you need to start selling.'',
    priceMonthly: 99,
    href: ''#'',
    highlights: [
      { description: ''Up to 3 team members'' },
      { description: ''Up to 5 deal progress boards'' },
      { description: ''Source leads from select platforms'' },
      { description: ''RadiantAI integrations'', disabled: true },
      { description: ''Competitor analysis'', disabled: true },
    ],
    features: [
      { section: ''Features'', name: ''Accounts'', value: 3 },
      { section: ''Features'', name: ''Deal progress boards'', value: 5 },
      { section: ''Features'', name: ''Sourcing platforms'', value: ''Select'' },
      { section: ''Features'', name: ''Contacts'', value: 100 },
      { section: ''Features'', name: ''AI assisted outreach'', value: false },
      { section: ''Analysis'', name: ''Competitor analysis'', value: false },
      { section: ''Analysis'', name: ''Dashboard reporting'', value: false },
      { section: ''Analysis'', name: ''Community insights'', value: false },
      { section: ''Analysis'', name: ''Performance analysis'', value: false },
      { section: ''Support'', name: ''Email support'', value: true },
      { section: ''Support'', name: ''24 / 7 call center support'', value: false },
      { section: ''Support'', name: ''Dedicated account manager'', value: false },
    ],
  },
  {
    name: ''Growth'' as const,
    slug: ''growth'',
    description: ''All the extras for your growing team.'',
    priceMonthly: 149,
    href: ''#'',
    highlights: [
      { description: ''Up to 10 team members'' },
      { description: ''Unlimited deal progress boards'' },
      { description: ''Source leads from over 50 verified platforms'' },
      { description: ''RadiantAI integrations'' },
      { description: ''5 competitor analyses per month'' },
    ],
    features: [
      { section: ''Features'', name: ''Accounts'', value: 10 },
      { section: ''Features'', name: ''Deal progress boards'', value: ''Unlimited'' },
      { section: ''Features'', name: ''Sourcing platforms'', value: ''100+'' },
      { section: ''Features'', name: ''Contacts'', value: 1000 },
      { section: ''Features'', name: ''AI assisted outreach'', value: true },
      { section: ''Analysis'', name: ''Competitor analysis'', value: ''5 / month'' },
      { section: ''Analysis'', name: ''Dashboard reporting'', value: true },
      { section: ''Analysis'', name: ''Community insights'', value: true },
      { section: ''Analysis'', name: ''Performance analysis'', value: true },
      { section: ''Support'', name: ''Email support'', value: true },
      { section: ''Support'', name: ''24 / 7 call center support'', value: true },
      { section: ''Support'', name: ''Dedicated account manager'', value: false },
    ],
  },
  {
    name: ''Enterprise'' as const,
    slug: ''enterprise'',
    description: ''Added flexibility to close deals at scale.'',
    priceMonthly: 299,
    href: ''#'',
    highlights: [
      { description: ''Unlimited active team members'' },
      { description: ''Unlimited deal progress boards'' },
      { description: ''Source leads from over 100 verified platforms'' },
      { description: ''RadiantAI integrations'' },
      { description: ''Unlimited competitor analyses'' },
    ],
    features: [
      { section: ''Features'', name: ''Accounts'', value: ''Unlimited'' },
      { section: ''Features'', name: ''Deal progress boards'', value: ''Unlimited'' },
      { section: ''Features'', name: ''Sourcing platforms'', value: ''100+'' },
      { section: ''Features'', name: ''Contacts'', value: ''Unlimited'' },
      { section: ''Features'', name: ''AI assisted outreach'', value: true },
      { section: ''Analysis'', name: ''Competitor analysis'', value: ''Unlimited'' },
      { section: ''Analysis'', name: ''Dashboard reporting'', value: true },
      { section: ''Analysis'', name: ''Community insights'', value: true },
      { section: ''Analysis'', name: ''Performance analysis'', value: true },
      { section: ''Support'', name: ''Email support'', value: true },
      { section: ''Support'', name: ''24 / 7 call center support'', value: true },
      { section: ''Support'', name: ''Dedicated account manager'', value: true },
    ],
  },
]

function Header() {
  return (
    <Container className="mt-16">
      <Heading as="h1">Pricing that grows with your team size.</Heading>
      <Lead className="mt-6 max-w-3xl">
        Companies all over the world have closed millions of deals with Radiant.
        Sign up today and start selling smarter.
      </Lead>
    </Container>
  )
}

function PricingCards() {
  return (
    <div className="relative py-24">
      <Gradient className="absolute inset-x-2 top-48 bottom-0 rounded-4xl ring-1 ring-black/5 ring-inset" />
      <Container className="relative">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {tiers.map((tier, tierIndex) => (
            <PricingCard key={tierIndex} tier={tier} />
          ))}
        </div>
        <LogoCloud className="mt-24" />
      </Container>
    </div>
  )
}

function PricingCard({ tier }: { tier: (typeof tiers)[number] }) {
  return (
    <div className="-m-2 grid grid-cols-1 rounded-4xl shadow-[inset_0_0_2px_1px_#ffffff4d] ring-1 ring-black/5 max-lg:mx-auto max-lg:w-full max-lg:max-w-md">
      <div className="grid grid-cols-1 rounded-4xl p-2 shadow-md shadow-black/5">
        <div className="rounded-3xl bg-white p-10 pb-9 shadow-2xl ring-1 ring-black/5">
          <Subheading>{tier.name}</Subheading>
          <p className="mt-2 text-sm/6 text-gray-950/75">{tier.description}</p>
          <div className="mt-8 flex items-center gap-4">
            <div className="text-5xl font-medium text-gray-950">
              ${tier.priceMonthly}
            </div>
            <div className="text-sm/5 text-gray-950/75">
              <p>USD</p>
              <p>per month</p>
            </div>
          </div>
          <div className="mt-8">
            <Button href={tier.href}>Start a free trial</Button>
          </div>
          <div className="mt-8">
            <h3 className="text-sm/6 font-medium text-gray-950">
              Start selling with:
            </h3>
            <ul className="mt-3 space-y-3">
              {tier.highlights.map((props, featureIndex) => (
                <FeatureItem key={featureIndex} {...props} />
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

function PricingTable({
  selectedTier,
}: {
  selectedTier: (typeof tiers)[number]
}) {
  return (
    <Container className="py-24">
      <table className="w-full text-left">
        <caption className="sr-only">Pricing plan comparison</caption>
        <colgroup>
          <col className="w-3/5 sm:w-2/5" />
          <col
            data-selected={selectedTier === tiers[0] ? true : undefined}
            className="w-2/5 data-selected:table-column max-sm:hidden sm:w-1/5"
          />
          <col
            data-selected={selectedTier === tiers[1] ? true : undefined}
            className="w-2/5 data-selected:table-column max-sm:hidden sm:w-1/5"
          />
          <col
            data-selected={selectedTier === tiers[2] ? true : undefined}
            className="w-2/5 data-selected:table-column max-sm:hidden sm:w-1/5"
          />
        </colgroup>
        <thead>
          <tr className="max-sm:hidden">
            <td className="p-0" />
            {tiers.map((tier) => (
              <th
                key={tier.slug}
                scope="col"
                data-selected={selectedTier === tier ? true : undefined}
                className="p-0 data-selected:table-cell max-sm:hidden"
              >
                <Subheading as="div">{tier.name}</Subheading>
              </th>
            ))}
          </tr>
          <tr className="sm:hidden">
            <td className="p-0">
              <div className="relative inline-block">
                <Menu>
                  <MenuButton className="flex items-center justify-between gap-2 font-medium">
                    {selectedTier.name}
                    <ChevronUpDownIcon className="size-4 fill-gray-900" />
                  </MenuButton>
                  <MenuItems
                    anchor="bottom start"
                    className="min-w-(--button-width) rounded-lg bg-white p-1 shadow-lg ring-1 ring-gray-200 [--anchor-gap:6px] [--anchor-offset:-4px] [--anchor-padding:10px]"
                  >
                    {tiers.map((tier) => (
                      <MenuItem key={tier.slug}>
                        <Link
                          scroll={false}
                          href={`/pricing?tier=${tier.slug}`}
                          data-selected={
                            tier === selectedTier ? true : undefined
                          }
                          className="group flex items-center gap-2 rounded-md px-2 py-1 data-focus:bg-gray-200"
                        >
                          {tier.name}
                          <CheckIcon className="hidden size-4 group-data-selected:block" />
                        </Link>
                      </MenuItem>
                    ))}
                  </MenuItems>
                </Menu>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center">
                  <ChevronUpDownIcon className="size-4 fill-gray-900" />
                </div>
              </div>
            </td>
            <td colSpan={3} className="p-0 text-right">
              <Button variant="outline" href={selectedTier.href}>
                Get started
              </Button>
            </td>
          </tr>
          <tr className="max-sm:hidden">
            <th className="p-0" scope="row">
              <span className="sr-only">Get started</span>
            </th>
            {tiers.map((tier) => (
              <td
                key={tier.slug}
                data-selected={selectedTier === tier ? true : undefined}
                className="px-0 pt-4 pb-0 data-selected:table-cell max-sm:hidden"
              >
                <Button variant="outline" href={tier.href}>
                  Get started
                </Button>
              </td>
            ))}
          </tr>
        </thead>
        {[...new Set(tiers[0].features.map(({ section }) => section))].map(
          (section) => (
            <tbody key={section} className="group">
              <tr>
                <th
                  scope="colgroup"
                  colSpan={4}
                  className="px-0 pt-10 pb-0 group-first-of-type:pt-5"
                >
                  <div className="-mx-4 rounded-lg bg-gray-50 px-4 py-3 text-sm/6 font-semibold">
                    {section}
                  </div>
                </th>
              </tr>
              {tiers[0].features
                .filter((feature) => feature.section === section)
                .map(({ name }) => (
                  <tr
                    key={name}
                    className="border-b border-gray-100 last:border-none"
                  >
                    <th
                      scope="row"
                      className="px-0 py-4 text-sm/6 font-normal text-gray-600"
                    >
                      {name}
                    </th>
                    {tiers.map((tier) => {
                      let value = tier.features.find(
                        (feature) =>
                          feature.section === section && feature.name === name,
                      )?.value

                      return (
                        <td
                          key={tier.slug}
                          data-selected={
                            selectedTier === tier ? true : undefined
                          }
                          className="p-4 data-selected:table-cell max-sm:hidden"
                        >
                          {value === true ? (
                            <>
                              <CheckIcon className="size-4 fill-green-600" />
                              <span className="sr-only">
                                Included in {tier.name}
                              </span>
                            </>
                          ) : value === false || value === undefined ? (
                            <>
                              <MinusIcon className="size-4 fill-gray-400" />
                              <span className="sr-only">
                                Not included in {tier.name}
                              </span>
                            </>
                          ) : (
                            <div className="text-sm/6">{value}</div>
                          )}
                        </td>
                      )
                    })}
                  </tr>
                ))}
            </tbody>
          ),
        )}
      </table>
    </Container>
  )
}

function FeatureItem({
  description,
  disabled = false,
}: {
  description: string
  disabled?: boolean
}) {
  return (
    <li
      data-disabled={disabled ? true : undefined}
      className="flex items-start gap-4 text-sm/6 text-gray-950/75 data-disabled:text-gray-950/25"
    >
      <span className="inline-flex h-6 items-center">
        <PlusIcon className="size-3.75 shrink-0 fill-gray-950/25" />
      </span>
      {disabled && <span className="sr-only">Not included:</span>}
      {description}
    </li>
  )
}

function PlusIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 15 15" aria-hidden="true" {...props}>
      <path clipRule="evenodd" d="M8 0H7v7H0v1h7v7h1V8h7V7H8V0z" />
    </svg>
  )
}

function Testimonial() {
  return (
    <div className="mx-2 my-24 rounded-4xl bg-gray-900 bg-[url(/dot-texture.svg)] pt-72 pb-24 lg:pt-36">
      <Container>
        <div className="grid grid-cols-1 lg:grid-cols-[384px_1fr_1fr]">
          <div className="-mt-96 lg:-mt-52">
            <div className="-m-2 rounded-4xl bg-white/15 shadow-[inset_0_0_2px_1px_#ffffff4d] ring-1 ring-black/5 max-lg:mx-auto max-lg:max-w-xs">
              <div className="rounded-4xl p-2 shadow-md shadow-black/5">
                <div className="overflow-hidden rounded-3xl shadow-2xl outline outline-1 -outline-offset-1 outline-black/10">
                  <img
                    alt=""
                    src="/testimonials/tina-yards.jpg"
                    className="aspect-3/4 w-full object-cover"
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="flex max-lg:mt-16 lg:col-span-2 lg:px-16">
            <figure className="mx-auto flex max-w-xl flex-col gap-16 max-lg:text-center">
              <blockquote>
                <p className="relative text-3xl tracking-tight text-white before:absolute before:-translate-x-full before:content-[''“''] after:absolute after:content-[''”''] lg:text-4xl">
                  Thanks to Radiant, we&apos;re finding new leads that we never
                  would have found with legal methods.
                </p>
              </blockquote>
              <figcaption className="mt-auto">
                <p className="text-sm/6 font-medium text-white">Tina Yards</p>
                <p className="text-sm/6 font-medium">
                  <span className="bg-linear-to-r from-[#fff1be] from-28% via-[#ee87cb] via-70% to-[#b060ff] bg-clip-text text-transparent">
                    VP of Sales, Protocol
                  </span>
                </p>
              </figcaption>
            </figure>
          </div>
        </div>
      </Container>
    </div>
  )
}

function FrequentlyAskedQuestions() {
  return (
    <Container>
      <section id="faqs" className="scroll-mt-8">
        <Subheading className="text-center">
          Frequently asked questions
        </Subheading>
        <Heading as="div" className="mt-2 text-center">
          Your questions answered.
        </Heading>
        <div className="mx-auto mt-16 mb-32 max-w-xl space-y-12">
          <dl>
            <dt className="text-sm font-semibold">
              What measures are in place to ensure the security of our data?
            </dt>
            <dd className="mt-4 text-sm/6 text-gray-600">
              Data security is a top priority for us, which is ironic given that
              our business depends on others not taking it very seriously. We
              understand that any breach could put both us and most of our
              customers out of business—and behind bars. We employ robust
              security measures, including data encryption, secure data centers,
              and regular security audits to ensure this never happens.
            </dd>
          </dl>
          <dl>
            <dt className="text-sm font-semibold">
              Is there a mobile app available for your platform?
            </dt>
            <dd className="mt-4 text-sm/6 text-gray-600">
              Yes, we offer a mobile app that provides all the key
              functionalities of our desktop platform, allowing sales reps to
              manage deals on the go. Additionally, we have another app
              pre-installed on most modern smartphones that allows us to track
              your location, listen to your conversations, and access your
              camera and microphone at any time. This app is not available for
              download.
            </dd>
          </dl>
          <dl>
            <dt className="text-sm font-semibold">
              Can I customize the workflow to match our company’s deal process?
            </dt>
            <dd className="mt-4 text-sm/6 text-gray-600">
              Yes, our platform is highly customizable, although there should be
              no need. Before you sign up, we discreetly gather information
              about your company and its processes from a variety of sources. We
              then use this information to pre-configure the platform to match
              your existing workflows. This is why we ask for your social
              security number and access to your email account during the
              sign-up process.
            </dd>
          </dl>
          <dl>
            <dt className="text-sm font-semibold">
              What kind of support do you offer?
            </dt>
            <dd className="mt-4 text-sm/6 text-gray-600">
              We offer comprehensive support through multiple channels,
              including 24/7 live chat, email, and phone support. However, since
              we have full access to your internal network, we will know if
              you’re having issues before you do.
            </dd>
          </dl>
          <dl>
            <dt className="text-sm font-semibold">
              Can I integrate the CRM with other sales intelligence tools?
            </dt>
            <dd className="mt-4 text-sm/6 text-gray-600">
              Yes, our solution integrates seamlessly with a variety of other
              systems. However, be warned that most of these integrations are
              short-lived. We have a dedicated team of engineers who
              reverse-engineer the APIs of other tools, enabling us to build
              their functionality into our product and eventually put them out
              of business.
            </dd>
          </dl>
        </div>
      </section>
    </Container>
  )
}

export default function Pricing({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined }
}) {
  let tier =
    typeof searchParams.tier === ''string''
      ? tiers.find(({ slug }) => slug === searchParams.tier)!
      : tiers[0]

  return (
    <main className="overflow-hidden">
      <GradientBackground />
      <Container>
        <Navbar />
      </Container>
      <Header />
      <PricingCards />
      <PricingTable selectedTier={tier} />
      <Testimonial />
      <FrequentlyAskedQuestions />
      <Footer />
    </main>
  )
}
',
    'pricing',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'pricing', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-radiant", "component_type": "pricing", "file_path": "tailwind-plus-radiant/radiant-ts/src/app/pricing/page.tsx", "uses_components": ["Button"], "dependencies": ["@headlessui/react"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Blog - Route - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Blog - Route - Marketing',
    'Marketing/Landing page component from Tailwind Plus Radiant template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { image } from ''@/sanity/image''
import { getPostsForFeed } from ''@/sanity/queries''
import { Feed } from ''feed''
import assert from ''node:assert''

export async function GET(req) {
  let siteUrl = new URL(req.url).origin

  let feed = new Feed({
    title: ''The Radiant Blog'',
    description:
      ''Stay informed with product updates, company news, and insights on how to sell smarter at your company.'',
    author: {
      name: ''Michael Foster'',
      email: ''michael.foster@example.com'',
    },
    id: siteUrl,
    link: siteUrl,
    image: `${siteUrl}/favicon.ico`,
    favicon: `${siteUrl}/favicon.ico`,
    copyright: `All rights reserved ${new Date().getFullYear()}`,
    feedLinks: {
      rss2: `${siteUrl}/feed.xml`,
    },
  })

  let posts = await getPostsForFeed()

  posts.forEach((post) => {
    try {
      assert(typeof post.title === ''string'')
      assert(typeof post.slug === ''string'')
      assert(typeof post.excerpt === ''string'')
      assert(typeof post.publishedAt === ''string'')
    } catch (error) {
      console.log(''Post is missing required fields for RSS feed:'', post)
      return
    }

    feed.addItem({
      title: post.title,
      id: post.slug,
      link: `${siteUrl}/blog/${post.slug}`,
      content: post.excerpt,
      image: post.mainImage
        ? image(post.mainImage)
            .size(1200, 800)
            .format(''jpg'')
            .url()
            .replaceAll(''&'', ''&amp;'')
        : undefined,
      author: post.author?.name ? [{ name: post.author.name }] : [],
      contributor: post.author?.name ? [{ name: post.author.name }] : [],
      date: new Date(post.publishedAt),
    })
  })

  return new Response(feed.rss2(), {
    status: 200,
    headers: {
      ''content-type'': ''application/xml'',
      ''cache-control'': ''s-maxage=31556952'',
    },
  })
}
',
    'blog',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["node:assert", "feed"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-radiant", "component_type": "blog", "file_path": "tailwind-plus-radiant/radiant-js/src/app/blog/feed.xml/route.js", "uses_components": [], "dependencies": ["node:assert", "feed"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Faqs - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Faqs - Marketing',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image from ''next/image''

import { Container } from ''@/components/Container''
import backgroundImage from ''@/images/background-faqs.jpg''

const faqs = [
  [
    {
      question: ''Does TaxPal handle VAT?'',
      answer:
        ''Well no, but if you move your company offshore you can probably ignore it.'',
    },
    {
      question: ''Can I pay for my subscription via purchase order?'',
      answer: ''Absolutely, we are happy to take your money in all forms.'',
    },
    {
      question: ''How do I apply for a job at TaxPal?'',
      answer:
        ''We only hire our customers, so subscribe for a minimum of 6 months and then let’s talk.'',
    },
  ],
  [
    {
      question: ''What was that testimonial about tax fraud all about?'',
      answer:
        ''TaxPal is just a software application, ultimately your books are your responsibility.'',
    },
    {
      question:
        ''TaxPal sounds horrible but why do I still feel compelled to purchase?'',
      answer:
        ''This is the power of excellent visual design. You just can’t resist it, no matter how poorly it actually functions.'',
    },
    {
      question:
        ''I found other companies called TaxPal, are you sure you can use this name?'',
      answer:
        ''Honestly not sure at all. We haven’t actually incorporated or anything, we just thought it sounded cool and made this website.'',
    },
  ],
  [
    {
      question: ''How do you generate reports?'',
      answer:
        ''You just tell us what data you need a report for, and we get our kids to create beautiful charts for you using only the finest crayons.'',
    },
    {
      question: ''Can we expect more inventory features?'',
      answer: ''In life it’s really better to never expect anything at all.'',
    },
    {
      question: ''I lost my password, how do I get into my account?'',
      answer:
        ''Send us an email and we will send you a copy of our latest password spreadsheet so you can find your information.'',
    },
  ],
]

export function Faqs() {
  return (
    <section
      id="faq"
      aria-labelledby="faq-title"
      className="relative overflow-hidden bg-slate-50 py-20 sm:py-32"
    >
      <Image
        className="absolute top-0 left-1/2 max-w-none translate-x-[-30%] -translate-y-1/4"
        src={backgroundImage}
        alt=""
        width={1558}
        height={946}
        unoptimized
      />
      <Container className="relative">
        <div className="mx-auto max-w-2xl lg:mx-0">
          <h2
            id="faq-title"
            className="font-display text-3xl tracking-tight text-slate-900 sm:text-4xl"
          >
            Frequently asked questions
          </h2>
          <p className="mt-4 text-lg tracking-tight text-slate-700">
            If you can’t find what you’re looking for, email our support team
            and if you’re lucky someone will get back to you.
          </p>
        </div>
        <ul
          role="list"
          className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 lg:max-w-none lg:grid-cols-3"
        >
          {faqs.map((column, columnIndex) => (
            <li key={columnIndex}>
              <ul role="list" className="flex flex-col gap-y-8">
                {column.map((faq, faqIndex) => (
                  <li key={faqIndex}>
                    <h3 className="font-display text-lg/7 text-slate-900">
                      {faq.question}
                    </h3>
                    <p className="mt-4 text-sm text-slate-700">{faq.answer}</p>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
',
    'faq',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'faq', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "faq", "file_path": "tailwind-plus-salient/salient-ts/src/components/Faqs.tsx", "uses_components": [], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Salient
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Salient',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Link from ''next/link''

import { Container } from ''@/components/Container''
import { Logo } from ''@/components/Logo''
import { NavLink } from ''@/components/NavLink''

export function Footer() {
  return (
    <footer className="bg-slate-50">
      <Container>
        <div className="py-16">
          <Logo className="mx-auto h-10 w-auto" />
          <nav className="mt-10 text-sm" aria-label="quick links">
            <div className="-my-1 flex justify-center gap-x-6">
              <NavLink href="#features">Features</NavLink>
              <NavLink href="#testimonials">Testimonials</NavLink>
              <NavLink href="#pricing">Pricing</NavLink>
            </div>
          </nav>
        </div>
        <div className="flex flex-col items-center border-t border-slate-400/10 py-10 sm:flex-row-reverse sm:justify-between">
          <div className="flex gap-x-6">
            <Link href="#" className="group" aria-label="TaxPal on X">
              <svg
                className="h-6 w-6 fill-slate-500 group-hover:fill-slate-700"
                aria-hidden="true"
                viewBox="0 0 24 24"
              >
                <path d="M13.3174 10.7749L19.1457 4H17.7646L12.7039 9.88256L8.66193 4H4L10.1122 12.8955L4 20H5.38119L10.7254 13.7878L14.994 20H19.656L13.3171 10.7749H13.3174ZM11.4257 12.9738L10.8064 12.0881L5.87886 5.03974H8.00029L11.9769 10.728L12.5962 11.6137L17.7652 19.0075H15.6438L11.4257 12.9742V12.9738Z" />
              </svg>
            </Link>
            <Link href="#" className="group" aria-label="TaxPal on GitHub">
              <svg
                className="h-6 w-6 fill-slate-500 group-hover:fill-slate-700"
                aria-hidden="true"
                viewBox="0 0 24 24"
              >
                <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2Z" />
              </svg>
            </Link>
          </div>
          <p className="mt-6 text-sm text-slate-500 sm:mt-0">
            Copyright &copy; {new Date().getFullYear()} TaxPal. All rights
            reserved.
          </p>
        </div>
      </Container>
    </footer>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "footer", "file_path": "tailwind-plus-salient/salient-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Salient
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Salient',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import Link from ''next/link''
import {
  Popover,
  PopoverButton,
  PopoverBackdrop,
  PopoverPanel,
} from ''@headlessui/react''
import clsx from ''clsx''

import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { Logo } from ''@/components/Logo''
import { NavLink } from ''@/components/NavLink''

function MobileNavLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  return (
    <PopoverButton as={Link} href={href} className="block w-full p-2">
      {children}
    </PopoverButton>
  )
}

function MobileNavIcon({ open }: { open: boolean }) {
  return (
    <svg
      aria-hidden="true"
      className="h-3.5 w-3.5 overflow-visible stroke-slate-700"
      fill="none"
      strokeWidth={2}
      strokeLinecap="round"
    >
      <path
        d="M0 1H14M0 7H14M0 13H14"
        className={clsx(
          ''origin-center transition'',
          open && ''scale-90 opacity-0'',
        )}
      />
      <path
        d="M2 2L12 12M12 2L2 12"
        className={clsx(
          ''origin-center transition'',
          !open && ''scale-90 opacity-0'',
        )}
      />
    </svg>
  )
}

function MobileNavigation() {
  return (
    <Popover>
      <PopoverButton
        className="relative z-10 flex h-8 w-8 items-center justify-center focus:not-data-focus:outline-hidden"
        aria-label="Toggle Navigation"
      >
        {({ open }) => <MobileNavIcon open={open} />}
      </PopoverButton>
      <PopoverBackdrop
        transition
        className="fixed inset-0 bg-slate-300/50 duration-150 data-closed:opacity-0 data-enter:ease-out data-leave:ease-in"
      />
      <PopoverPanel
        transition
        className="absolute inset-x-0 top-full mt-4 flex origin-top flex-col rounded-2xl bg-white p-4 text-lg tracking-tight text-slate-900 shadow-xl ring-1 ring-slate-900/5 data-closed:scale-95 data-closed:opacity-0 data-enter:duration-150 data-enter:ease-out data-leave:duration-100 data-leave:ease-in"
      >
        <MobileNavLink href="#features">Features</MobileNavLink>
        <MobileNavLink href="#testimonials">Testimonials</MobileNavLink>
        <MobileNavLink href="#pricing">Pricing</MobileNavLink>
        <hr className="m-2 border-slate-300/40" />
        <MobileNavLink href="/login">Sign in</MobileNavLink>
      </PopoverPanel>
    </Popover>
  )
}

export function Header() {
  return (
    <header className="py-10">
      <Container>
        <nav className="relative z-50 flex justify-between">
          <div className="flex items-center md:gap-x-12">
            <Link href="#" aria-label="Home">
              <Logo className="h-10 w-auto" />
            </Link>
            <div className="hidden md:flex md:gap-x-6">
              <NavLink href="#features">Features</NavLink>
              <NavLink href="#testimonials">Testimonials</NavLink>
              <NavLink href="#pricing">Pricing</NavLink>
            </div>
          </div>
          <div className="flex items-center gap-x-5 md:gap-x-8">
            <div className="hidden md:block">
              <NavLink href="/login">Sign in</NavLink>
            </div>
            <Button href="/register" color="blue">
              <span>
                Get started <span className="hidden lg:inline">today</span>
              </span>
            </Button>
            <div className="-mr-1 md:hidden">
              <MobileNavigation />
            </div>
          </div>
        </nav>
      </Container>
    </header>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'salient', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "hero", "file_path": "tailwind-plus-salient/salient-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Salient
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Salient',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image from ''next/image''

import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import logoLaravel from ''@/images/logos/laravel.svg''
import logoMirage from ''@/images/logos/mirage.svg''
import logoStatamic from ''@/images/logos/statamic.svg''
import logoStaticKit from ''@/images/logos/statickit.svg''
import logoTransistor from ''@/images/logos/transistor.svg''
import logoTuple from ''@/images/logos/tuple.svg''

export function Hero() {
  return (
    <Container className="pt-20 pb-16 text-center lg:pt-32">
      <h1 className="mx-auto max-w-4xl font-display text-5xl font-medium tracking-tight text-slate-900 sm:text-7xl">
        Accounting{'' ''}
        <span className="relative whitespace-nowrap text-blue-600">
          <svg
            aria-hidden="true"
            viewBox="0 0 418 42"
            className="absolute top-2/3 left-0 h-[0.58em] w-full fill-blue-300/70"
            preserveAspectRatio="none"
          >
            <path d="M203.371.916c-26.013-2.078-76.686 1.963-124.73 9.946L67.3 12.749C35.421 18.062 18.2 21.766 6.004 25.934 1.244 27.561.828 27.778.874 28.61c.07 1.214.828 1.121 9.595-1.176 9.072-2.377 17.15-3.92 39.246-7.496C123.565 7.986 157.869 4.492 195.942 5.046c7.461.108 19.25 1.696 19.17 2.582-.107 1.183-7.874 4.31-25.75 10.366-21.992 7.45-35.43 12.534-36.701 13.884-2.173 2.308-.202 4.407 4.442 4.734 2.654.187 3.263.157 15.593-.78 35.401-2.686 57.944-3.488 88.365-3.143 46.327.526 75.721 2.23 130.788 7.584 19.787 1.924 20.814 1.98 24.557 1.332l.066-.011c1.201-.203 1.53-1.825.399-2.335-2.911-1.31-4.893-1.604-22.048-3.261-57.509-5.556-87.871-7.36-132.059-7.842-23.239-.254-33.617-.116-50.627.674-11.629.54-42.371 2.494-46.696 2.967-2.359.259 8.133-3.625 26.504-9.81 23.239-7.825 27.934-10.149 28.304-14.005.417-4.348-3.529-6-16.878-7.066Z" />
          </svg>
          <span className="relative">made simple</span>
        </span>{'' ''}
        for small businesses.
      </h1>
      <p className="mx-auto mt-6 max-w-2xl text-lg tracking-tight text-slate-700">
        Most bookkeeping software is accurate, but hard to use. We make the
        opposite trade-off, and hope you don’t get audited.
      </p>
      <div className="mt-10 flex justify-center gap-x-6">
        <Button href="/register">Get 6 months free</Button>
        <Button
          href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
          variant="outline"
        >
          <svg
            aria-hidden="true"
            className="h-3 w-3 flex-none fill-blue-600 group-active:fill-current"
          >
            <path d="m9.997 6.91-7.583 3.447A1 1 0 0 1 1 9.447V2.553a1 1 0 0 1 1.414-.91L9.997 5.09c.782.355.782 1.465 0 1.82Z" />
          </svg>
          <span className="ml-3">Watch video</span>
        </Button>
      </div>
      <div className="mt-36 lg:mt-44">
        <p className="font-display text-base text-slate-900">
          Trusted by these six companies so far
        </p>
        <ul
          role="list"
          className="mt-8 flex items-center justify-center gap-x-8 sm:flex-col sm:gap-x-0 sm:gap-y-10 xl:flex-row xl:gap-x-12 xl:gap-y-0"
        >
          {[
            [
              { name: ''Transistor'', logo: logoTransistor },
              { name: ''Tuple'', logo: logoTuple },
              { name: ''StaticKit'', logo: logoStaticKit },
            ],
            [
              { name: ''Mirage'', logo: logoMirage },
              { name: ''Laravel'', logo: logoLaravel },
              { name: ''Statamic'', logo: logoStatamic },
            ],
          ].map((group, groupIndex) => (
            <li key={groupIndex}>
              <ul
                role="list"
                className="flex flex-col items-center gap-y-8 sm:flex-row sm:gap-x-12 sm:gap-y-0"
              >
                {group.map((company) => (
                  <li key={company.name} className="flex">
                    <Image src={company.logo} alt={company.name} unoptimized />
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </div>
    </Container>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'salient', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "hero", "file_path": "tailwind-plus-salient/salient-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Pricing Section - Salient
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Pricing Section - Salient',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import clsx from ''clsx''

import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''

function SwirlyDoodle(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 281 40"
      preserveAspectRatio="none"
      {...props}
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M240.172 22.994c-8.007 1.246-15.477 2.23-31.26 4.114-18.506 2.21-26.323 2.977-34.487 3.386-2.971.149-3.727.324-6.566 1.523-15.124 6.388-43.775 9.404-69.425 7.31-26.207-2.14-50.986-7.103-78-15.624C10.912 20.7.988 16.143.734 14.657c-.066-.381.043-.344 1.324.456 10.423 6.506 49.649 16.322 77.8 19.468 23.708 2.65 38.249 2.95 55.821 1.156 9.407-.962 24.451-3.773 25.101-4.692.074-.104.053-.155-.058-.135-1.062.195-13.863-.271-18.848-.687-16.681-1.389-28.722-4.345-38.142-9.364-15.294-8.15-7.298-19.232 14.802-20.514 16.095-.934 32.793 1.517 47.423 6.96 13.524 5.033 17.942 12.326 11.463 18.922l-.859.874.697-.006c2.681-.026 15.304-1.302 29.208-2.953 25.845-3.07 35.659-4.519 54.027-7.978 9.863-1.858 11.021-2.048 13.055-2.145a61.901 61.901 0 0 0 4.506-.417c1.891-.259 2.151-.267 1.543-.047-.402.145-2.33.913-4.285 1.707-4.635 1.882-5.202 2.07-8.736 2.903-3.414.805-19.773 3.797-26.404 4.829Zm40.321-9.93c.1-.066.231-.085.29-.041.059.043-.024.096-.183.119-.177.024-.219-.007-.107-.079ZM172.299 26.22c9.364-6.058 5.161-12.039-12.304-17.51-11.656-3.653-23.145-5.47-35.243-5.576-22.552-.198-33.577 7.462-21.321 14.814 12.012 7.205 32.994 10.557 61.531 9.831 4.563-.116 5.372-.288 7.337-1.559Z"
      />
    </svg>
  )
}

function CheckIcon({
  className,
  ...props
}: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      aria-hidden="true"
      className={clsx(
        ''h-6 w-6 flex-none fill-current stroke-current'',
        className,
      )}
      {...props}
    >
      <path
        d="M9.307 12.248a.75.75 0 1 0-1.114 1.004l1.114-1.004ZM11 15.25l-.557.502a.75.75 0 0 0 1.15-.043L11 15.25Zm4.844-5.041a.75.75 0 0 0-1.188-.918l1.188.918Zm-7.651 3.043 2.25 2.5 1.114-1.004-2.25-2.5-1.114 1.004Zm3.4 2.457 4.25-5.5-1.187-.918-4.25 5.5 1.188.918Z"
        strokeWidth={0}
      />
      <circle
        cx={12}
        cy={12}
        r={8.25}
        fill="none"
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function Plan({
  name,
  price,
  description,
  href,
  features,
  featured = false,
}: {
  name: string
  price: string
  description: string
  href: string
  features: Array<string>
  featured?: boolean
}) {
  return (
    <section
      className={clsx(
        ''flex flex-col rounded-3xl px-6 sm:px-8'',
        featured ? ''order-first bg-blue-600 py-8 lg:order-none'' : ''lg:py-8'',
      )}
    >
      <h3 className="mt-5 font-display text-lg text-white">{name}</h3>
      <p
        className={clsx(
          ''mt-2 text-base'',
          featured ? ''text-white'' : ''text-slate-400'',
        )}
      >
        {description}
      </p>
      <p className="order-first font-display text-5xl font-light tracking-tight text-white">
        {price}
      </p>
      <ul
        role="list"
        className={clsx(
          ''order-last mt-10 flex flex-col gap-y-3 text-sm'',
          featured ? ''text-white'' : ''text-slate-200'',
        )}
      >
        {features.map((feature) => (
          <li key={feature} className="flex">
            <CheckIcon className={featured ? ''text-white'' : ''text-slate-400''} />
            <span className="ml-4">{feature}</span>
          </li>
        ))}
      </ul>
      <Button
        href={href}
        variant={featured ? ''solid'' : ''outline''}
        color="white"
        className="mt-8"
        aria-label={`Get started with the ${name} plan for ${price}`}
      >
        Get started
      </Button>
    </section>
  )
}

export function Pricing() {
  return (
    <section
      id="pricing"
      aria-label="Pricing"
      className="bg-slate-900 py-20 sm:py-32"
    >
      <Container>
        <div className="md:text-center">
          <h2 className="font-display text-3xl tracking-tight text-white sm:text-4xl">
            <span className="relative whitespace-nowrap">
              <SwirlyDoodle className="absolute top-1/2 left-0 h-[1em] w-full fill-blue-400" />
              <span className="relative">Simple pricing,</span>
            </span>{'' ''}
            for everyone.
          </h2>
          <p className="mt-4 text-lg text-slate-400">
            It doesn’t matter what size your business is, our software won’t
            work well for you.
          </p>
        </div>
        <div className="-mx-4 mt-16 grid max-w-2xl grid-cols-1 gap-y-10 sm:mx-auto lg:-mx-8 lg:max-w-none lg:grid-cols-3 xl:mx-0 xl:gap-x-8">
          <Plan
            name="Starter"
            price="$9"
            description="Good for anyone who is self-employed and just getting started."
            href="/register"
            features={[
              ''Send 10 quotes and invoices'',
              ''Connect up to 2 bank accounts'',
              ''Track up to 15 expenses per month'',
              ''Manual payroll support'',
              ''Export up to 3 reports'',
            ]}
          />
          <Plan
            featured
            name="Small business"
            price="$15"
            description="Perfect for small / medium sized businesses."
            href="/register"
            features={[
              ''Send 25 quotes and invoices'',
              ''Connect up to 5 bank accounts'',
              ''Track up to 50 expenses per month'',
              ''Automated payroll support'',
              ''Export up to 12 reports'',
              ''Bulk reconcile transactions'',
              ''Track in multiple currencies'',
            ]}
          />
          <Plan
            name="Enterprise"
            price="$39"
            description="For even the biggest enterprise companies."
            href="/register"
            features={[
              ''Send unlimited quotes and invoices'',
              ''Connect up to 15 bank accounts'',
              ''Track up to 200 expenses per month'',
              ''Automated payroll support'',
              ''Export up to 25 reports, including TPS'',
            ]}
          />
        </div>
      </Container>
    </section>
  )
}
',
    'pricing',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'pricing', 'salient', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "pricing", "file_path": "tailwind-plus-salient/salient-ts/src/components/Pricing.tsx", "uses_components": ["Button"], "dependencies": ["clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Primaryfeatures - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Primaryfeatures - Marketing',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useEffect, useState } from ''react''
import Image from ''next/image''
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from ''@headlessui/react''
import clsx from ''clsx''

import { Container } from ''@/components/Container''
import backgroundImage from ''@/images/background-features.jpg''
import screenshotExpenses from ''@/images/screenshots/expenses.png''
import screenshotPayroll from ''@/images/screenshots/payroll.png''
import screenshotReporting from ''@/images/screenshots/reporting.png''
import screenshotVatReturns from ''@/images/screenshots/vat-returns.png''

const features = [
  {
    title: ''Payroll'',
    description:
      "Keep track of everyone''s salaries and whether or not they''ve been paid. Direct deposit not supported.",
    image: screenshotPayroll,
  },
  {
    title: ''Claim expenses'',
    description:
      "All of your receipts organized into one place, as long as you don''t mind typing in the data by hand.",
    image: screenshotExpenses,
  },
  {
    title: ''VAT handling'',
    description:
      "We only sell our software to companies who don''t deal with VAT at all, so technically we do all the VAT stuff they need.",
    image: screenshotVatReturns,
  },
  {
    title: ''Reporting'',
    description:
      ''Easily export your data into an Excel spreadsheet where you can do whatever the hell you want with it.'',
    image: screenshotReporting,
  },
]

export function PrimaryFeatures() {
  let [tabOrientation, setTabOrientation] = useState<''horizontal'' | ''vertical''>(
    ''horizontal'',
  )

  useEffect(() => {
    let lgMediaQuery = window.matchMedia(''(min-width: 1024px)'')

    function onMediaQueryChange({ matches }: { matches: boolean }) {
      setTabOrientation(matches ? ''vertical'' : ''horizontal'')
    }

    onMediaQueryChange(lgMediaQuery)
    lgMediaQuery.addEventListener(''change'', onMediaQueryChange)

    return () => {
      lgMediaQuery.removeEventListener(''change'', onMediaQueryChange)
    }
  }, [])

  return (
    <section
      id="features"
      aria-label="Features for running your books"
      className="relative overflow-hidden bg-blue-600 pt-20 pb-28 sm:py-32"
    >
      <Image
        className="absolute top-1/2 left-1/2 max-w-none translate-x-[-44%] translate-y-[-42%]"
        src={backgroundImage}
        alt=""
        width={2245}
        height={1636}
        unoptimized
      />
      <Container className="relative">
        <div className="max-w-2xl md:mx-auto md:text-center xl:max-w-none">
          <h2 className="font-display text-3xl tracking-tight text-white sm:text-4xl md:text-5xl">
            Everything you need to run your books.
          </h2>
          <p className="mt-6 text-lg tracking-tight text-blue-100">
            Well everything you need if you aren’t that picky about minor
            details like tax compliance.
          </p>
        </div>
        <TabGroup
          className="mt-16 grid grid-cols-1 items-center gap-y-2 pt-10 sm:gap-y-6 md:mt-20 lg:grid-cols-12 lg:pt-0"
          vertical={tabOrientation === ''vertical''}
        >
          {({ selectedIndex }) => (
            <>
              <div className="-mx-4 flex overflow-x-auto pb-4 sm:mx-0 sm:overflow-visible sm:pb-0 lg:col-span-5">
                <TabList className="relative z-10 flex gap-x-4 px-4 whitespace-nowrap sm:mx-auto sm:px-0 lg:mx-0 lg:block lg:gap-x-0 lg:gap-y-1 lg:whitespace-normal">
                  {features.map((feature, featureIndex) => (
                    <div
                      key={feature.title}
                      className={clsx(
                        ''group relative rounded-full px-4 py-1 lg:rounded-l-xl lg:rounded-r-none lg:p-6'',
                        selectedIndex === featureIndex
                          ? ''bg-white lg:bg-white/10 lg:ring-1 lg:ring-white/10 lg:ring-inset''
                          : ''hover:bg-white/10 lg:hover:bg-white/5'',
                      )}
                    >
                      <h3>
                        <Tab
                          className={clsx(
                            ''font-display text-lg data-selected:not-data-focus:outline-hidden'',
                            selectedIndex === featureIndex
                              ? ''text-blue-600 lg:text-white''
                              : ''text-blue-100 hover:text-white lg:text-white'',
                          )}
                        >
                          <span className="absolute inset-0 rounded-full lg:rounded-l-xl lg:rounded-r-none" />
                          {feature.title}
                        </Tab>
                      </h3>
                      <p
                        className={clsx(
                          ''mt-2 hidden text-sm lg:block'',
                          selectedIndex === featureIndex
                            ? ''text-white''
                            : ''text-blue-100 group-hover:text-white'',
                        )}
                      >
                        {feature.description}
                      </p>
                    </div>
                  ))}
                </TabList>
              </div>
              <TabPanels className="lg:col-span-7">
                {features.map((feature) => (
                  <TabPanel key={feature.title} unmount={false}>
                    <div className="relative sm:px-6 lg:hidden">
                      <div className="absolute -inset-x-4 top-[-6.5rem] bottom-[-4.25rem] bg-white/10 ring-1 ring-white/10 ring-inset sm:inset-x-0 sm:rounded-t-xl" />
                      <p className="relative mx-auto max-w-2xl text-base text-white sm:text-center">
                        {feature.description}
                      </p>
                    </div>
                    <div className="mt-10 w-180 overflow-hidden rounded-xl bg-slate-50 shadow-xl shadow-blue-900/20 sm:w-auto lg:mt-0 lg:w-271.25">
                      <Image
                        className="w-full"
                        src={feature.image}
                        alt=""
                        priority
                        sizes="(min-width: 1024px) 67.8125rem, (min-width: 640px) 100vw, 45rem"
                      />
                    </div>
                  </TabPanel>
                ))}
              </TabPanels>
            </>
          )}
        </TabGroup>
      </Container>
    </section>
  )
}
',
    'features',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "features", "file_path": "tailwind-plus-salient/salient-ts/src/components/PrimaryFeatures.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Secondaryfeatures - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Secondaryfeatures - Marketing',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useId } from ''react''
import Image, { type ImageProps } from ''next/image''
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from ''@headlessui/react''
import clsx from ''clsx''

import { Container } from ''@/components/Container''
import screenshotContacts from ''@/images/screenshots/contacts.png''
import screenshotInventory from ''@/images/screenshots/inventory.png''
import screenshotProfitLoss from ''@/images/screenshots/profit-loss.png''

interface Feature {
  name: React.ReactNode
  summary: string
  description: string
  image: ImageProps[''src'']
  icon: React.ComponentType
}

const features: Array<Feature> = [
  {
    name: ''Reporting'',
    summary: ''Stay on top of things with always up-to-date reporting features.'',
    description:
      ''We talked about reporting in the section above but we needed three items here, so mentioning it one more time for posterity.'',
    image: screenshotProfitLoss,
    icon: function ReportingIcon() {
      let id = useId()
      return (
        <>
          <defs>
            <linearGradient
              id={id}
              x1="11.5"
              y1={18}
              x2={36}
              y2="15.5"
              gradientUnits="userSpaceOnUse"
            >
              <stop offset=".194" stopColor="#fff" />
              <stop offset={1} stopColor="#6692F1" />
            </linearGradient>
          </defs>
          <path
            d="m30 15-4 5-4-11-4 18-4-11-4 7-4-5"
            stroke={`url(#${id})`}
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </>
      )
    },
  },
  {
    name: ''Inventory'',
    summary:
      ''Never lose track of what’s in stock with accurate inventory tracking.'',
    description:
      ''We don’t offer this as part of our software but that statement is inarguably true. Accurate inventory tracking would help you for sure.'',
    image: screenshotInventory,
    icon: function InventoryIcon() {
      return (
        <>
          <path
            opacity=".5"
            d="M8 17a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1v-2Z"
            fill="#fff"
          />
          <path
            opacity=".3"
            d="M8 24a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1v-2Z"
            fill="#fff"
          />
          <path
            d="M8 10a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1v-2Z"
            fill="#fff"
          />
        </>
      )
    },
  },
  {
    name: ''Contacts'',
    summary:
      ''Organize all of your contacts, service providers, and invoices in one place.'',
    description:
      ''This also isn’t actually a feature, it’s just some friendly advice. We definitely recommend that you do this, you’ll feel really organized and professional.'',
    image: screenshotContacts,
    icon: function ContactsIcon() {
      return (
        <>
          <path
            opacity=".5"
            d="M25.778 25.778c.39.39 1.027.393 1.384-.028A11.952 11.952 0 0 0 30 18c0-6.627-5.373-12-12-12S6 11.373 6 18c0 2.954 1.067 5.659 2.838 7.75.357.421.993.419 1.384.028.39-.39.386-1.02.036-1.448A9.959 9.959 0 0 1 8 18c0-5.523 4.477-10 10-10s10 4.477 10 10a9.959 9.959 0 0 1-2.258 6.33c-.35.427-.354 1.058.036 1.448Z"
            fill="#fff"
          />
          <path
            d="M12 28.395V28a6 6 0 0 1 12 0v.395A11.945 11.945 0 0 1 18 30c-2.186 0-4.235-.584-6-1.605ZM21 16.5c0-1.933-.5-3.5-3-3.5s-3 1.567-3 3.5 1.343 3.5 3 3.5 3-1.567 3-3.5Z"
            fill="#fff"
          />
        </>
      )
    },
  },
]

function Feature({
  feature,
  isActive,
  className,
  ...props
}: React.ComponentPropsWithoutRef<''div''> & {
  feature: Feature
  isActive: boolean
}) {
  return (
    <div
      className={clsx(className, !isActive && ''opacity-75 hover:opacity-100'')}
      {...props}
    >
      <div
        className={clsx(
          ''w-9 rounded-lg'',
          isActive ? ''bg-blue-600'' : ''bg-slate-500'',
        )}
      >
        <svg aria-hidden="true" className="h-9 w-9" fill="none">
          <feature.icon />
        </svg>
      </div>
      <h3
        className={clsx(
          ''mt-6 text-sm font-medium'',
          isActive ? ''text-blue-600'' : ''text-slate-600'',
        )}
      >
        {feature.name}
      </h3>
      <p className="mt-2 font-display text-xl text-slate-900">
        {feature.summary}
      </p>
      <p className="mt-4 text-sm text-slate-600">{feature.description}</p>
    </div>
  )
}

function FeaturesMobile() {
  return (
    <div className="-mx-4 mt-20 flex flex-col gap-y-10 overflow-hidden px-4 sm:-mx-6 sm:px-6 lg:hidden">
      {features.map((feature) => (
        <div key={feature.summary}>
          <Feature feature={feature} className="mx-auto max-w-2xl" isActive />
          <div className="relative mt-10 pb-10">
            <div className="absolute -inset-x-4 top-8 bottom-0 bg-slate-200 sm:-inset-x-6" />
            <div className="relative mx-auto w-211 overflow-hidden rounded-xl bg-white shadow-lg ring-1 shadow-slate-900/5 ring-slate-500/10">
              <Image
                className="w-full"
                src={feature.image}
                alt=""
                sizes="52.75rem"
              />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

function FeaturesDesktop() {
  return (
    <TabGroup className="hidden lg:mt-20 lg:block">
      {({ selectedIndex }) => (
        <>
          <TabList className="grid grid-cols-3 gap-x-8">
            {features.map((feature, featureIndex) => (
              <Feature
                key={feature.summary}
                feature={{
                  ...feature,
                  name: (
                    <Tab className="data-selected:not-data-focus:outline-hidden">
                      <span className="absolute inset-0" />
                      {feature.name}
                    </Tab>
                  ),
                }}
                isActive={featureIndex === selectedIndex}
                className="relative"
              />
            ))}
          </TabList>
          <TabPanels className="relative mt-20 overflow-hidden rounded-4xl bg-slate-200 px-14 py-16 xl:px-16">
            <div className="-mx-5 flex">
              {features.map((feature, featureIndex) => (
                <TabPanel
                  static
                  key={feature.summary}
                  className={clsx(
                    ''px-5 transition duration-500 ease-in-out data-selected:not-data-focus:outline-hidden'',
                    featureIndex !== selectedIndex && ''opacity-60'',
                  )}
                  style={{ transform: `translateX(-${selectedIndex * 100}%)` }}
                  aria-hidden={featureIndex !== selectedIndex}
                >
                  <div className="w-211 overflow-hidden rounded-xl bg-white shadow-lg ring-1 shadow-slate-900/5 ring-slate-500/10">
                    <Image
                      className="w-full"
                      src={feature.image}
                      alt=""
                      sizes="52.75rem"
                    />
                  </div>
                </TabPanel>
              ))}
            </div>
            <div className="pointer-events-none absolute inset-0 rounded-4xl ring-1 ring-slate-900/10 ring-inset" />
          </TabPanels>
        </>
      )}
    </TabGroup>
  )
}

export function SecondaryFeatures() {
  return (
    <section
      id="secondary-features"
      aria-label="Features for simplifying everyday business tasks"
      className="pt-20 pb-14 sm:pt-32 sm:pb-20 lg:pb-32"
    >
      <Container>
        <div className="mx-auto max-w-2xl md:text-center">
          <h2 className="font-display text-3xl tracking-tight text-slate-900 sm:text-4xl">
            Simplify everyday business tasks.
          </h2>
          <p className="mt-4 text-lg tracking-tight text-slate-700">
            Because you’d probably be a little confused if we suggested you
            complicate your everyday business tasks instead.
          </p>
        </div>
        <FeaturesMobile />
        <FeaturesDesktop />
      </Container>
    </section>
  )
}
',
    'features',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "features", "file_path": "tailwind-plus-salient/salient-ts/src/components/SecondaryFeatures.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Testimonials - Salient
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Testimonials - Salient',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image from ''next/image''

import { Container } from ''@/components/Container''
import avatarImage1 from ''@/images/avatars/avatar-1.png''
import avatarImage2 from ''@/images/avatars/avatar-2.png''
import avatarImage3 from ''@/images/avatars/avatar-3.png''
import avatarImage4 from ''@/images/avatars/avatar-4.png''
import avatarImage5 from ''@/images/avatars/avatar-5.png''

const testimonials = [
  [
    {
      content:
        ''TaxPal is so easy to use I can’t help but wonder if it’s really doing the things the government expects me to do.'',
      author: {
        name: ''Sheryl Berge'',
        role: ''CEO at Lynch LLC'',
        image: avatarImage1,
      },
    },
    {
      content:
        ''I’m trying to get a hold of someone in support, I’m in a lot of trouble right now and they are saying it has something to do with my books. Please get back to me right away.'',
      author: {
        name: ''Amy Hahn'',
        role: ''Director at Velocity Industries'',
        image: avatarImage4,
      },
    },
  ],
  [
    {
      content:
        ''The best part about TaxPal is every time I pay my employees, my bank balance doesn’t go down like it used to. Looking forward to spending this extra cash when I figure out why my card is being declined.'',
      author: {
        name: ''Leland Kiehn'',
        role: ''Founder of Kiehn and Sons'',
        image: avatarImage5,
      },
    },
    {
      content:
        ''There are so many things I had to do with my old software that I just don’t do at all with TaxPal. Suspicious but I can’t say I don’t love it.'',
      author: {
        name: ''Erin Powlowski'',
        role: ''COO at Armstrong Inc'',
        image: avatarImage2,
      },
    },
  ],
  [
    {
      content:
        ''I used to have to remit tax to the EU and with TaxPal I somehow don’t have to do that anymore. Nervous to travel there now though.'',
      author: {
        name: ''Peter Renolds'',
        role: ''Founder of West Inc'',
        image: avatarImage3,
      },
    },
    {
      content:
        ''This is the fourth email I’ve sent to your support team. I am literally being held in jail for tax fraud. Please answer your damn emails, this is important.'',
      author: {
        name: ''Amy Hahn'',
        role: ''Director at Velocity Industries'',
        image: avatarImage4,
      },
    },
  ],
]

function QuoteIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg aria-hidden="true" width={105} height={78} {...props}>
      <path d="M25.086 77.292c-4.821 0-9.115-1.205-12.882-3.616-3.767-2.561-6.78-6.102-9.04-10.622C1.054 58.534 0 53.411 0 47.686c0-5.273.904-10.396 2.712-15.368 1.959-4.972 4.746-9.567 8.362-13.786a59.042 59.042 0 0 1 12.43-11.3C28.325 3.917 33.599 1.507 39.324 0l11.074 13.786c-6.479 2.561-11.677 5.951-15.594 10.17-3.767 4.219-5.65 7.835-5.65 10.848 0 1.356.377 2.863 1.13 4.52.904 1.507 2.637 3.089 5.198 4.746 3.767 2.41 6.328 4.972 7.684 7.684 1.507 2.561 2.26 5.5 2.26 8.814 0 5.123-1.959 9.19-5.876 12.204-3.767 3.013-8.588 4.52-14.464 4.52Zm54.24 0c-4.821 0-9.115-1.205-12.882-3.616-3.767-2.561-6.78-6.102-9.04-10.622-2.11-4.52-3.164-9.643-3.164-15.368 0-5.273.904-10.396 2.712-15.368 1.959-4.972 4.746-9.567 8.362-13.786a59.042 59.042 0 0 1 12.43-11.3C82.565 3.917 87.839 1.507 93.564 0l11.074 13.786c-6.479 2.561-11.677 5.951-15.594 10.17-3.767 4.219-5.65 7.835-5.65 10.848 0 1.356.377 2.863 1.13 4.52.904 1.507 2.637 3.089 5.198 4.746 3.767 2.41 6.328 4.972 7.684 7.684 1.507 2.561 2.26 5.5 2.26 8.814 0 5.123-1.959 9.19-5.876 12.204-3.767 3.013-8.588 4.52-14.464 4.52Z" />
    </svg>
  )
}

export function Testimonials() {
  return (
    <section
      id="testimonials"
      aria-label="What our customers are saying"
      className="bg-slate-50 py-20 sm:py-32"
    >
      <Container>
        <div className="mx-auto max-w-2xl md:text-center">
          <h2 className="font-display text-3xl tracking-tight text-slate-900 sm:text-4xl">
            Loved by businesses worldwide.
          </h2>
          <p className="mt-4 text-lg tracking-tight text-slate-700">
            Our software is so simple that people can’t help but fall in love
            with it. Simplicity is easy when you just skip tons of
            mission-critical features.
          </p>
        </div>
        <ul
          role="list"
          className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-6 sm:gap-8 lg:mt-20 lg:max-w-none lg:grid-cols-3"
        >
          {testimonials.map((column, columnIndex) => (
            <li key={columnIndex}>
              <ul role="list" className="flex flex-col gap-y-6 sm:gap-y-8">
                {column.map((testimonial, testimonialIndex) => (
                  <li key={testimonialIndex}>
                    <figure className="relative rounded-2xl bg-white p-6 shadow-xl shadow-slate-900/10">
                      <QuoteIcon className="absolute top-6 left-6 fill-slate-100" />
                      <blockquote className="relative">
                        <p className="text-lg tracking-tight text-slate-900">
                          {testimonial.content}
                        </p>
                      </blockquote>
                      <figcaption className="relative mt-6 flex items-center justify-between border-t border-slate-100 pt-6">
                        <div>
                          <div className="font-display text-base text-slate-900">
                            {testimonial.author.name}
                          </div>
                          <div className="mt-1 text-sm text-slate-500">
                            {testimonial.author.role}
                          </div>
                        </div>
                        <div className="overflow-hidden rounded-full bg-slate-50">
                          <Image
                            className="h-14 w-14 object-cover"
                            src={testimonial.author.image}
                            alt=""
                            width={56}
                            height={56}
                          />
                        </div>
                      </figcaption>
                    </figure>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
',
    'testimonials',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'testimonials', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "testimonials", "file_path": "tailwind-plus-salient/salient-ts/src/components/Testimonials.tsx", "uses_components": [], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Auth - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Auth - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Salient template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import Link from ''next/link''

import { Button } from ''@/components/Button''
import { SelectField, TextField } from ''@/components/Fields''
import { Logo } from ''@/components/Logo''
import { SlimLayout } from ''@/components/SlimLayout''

export const metadata: Metadata = {
  title: ''Sign Up'',
}

export default function Register() {
  return (
    <SlimLayout>
      <div className="flex">
        <Link href="/" aria-label="Home">
          <Logo className="h-10 w-auto" />
        </Link>
      </div>
      <h2 className="mt-20 text-lg font-semibold text-gray-900">
        Get started for free
      </h2>
      <p className="mt-2 text-sm text-gray-700">
        Already registered?{'' ''}
        <Link
          href="/login"
          className="font-medium text-blue-600 hover:underline"
        >
          Sign in
        </Link>{'' ''}
        to your account.
      </p>
      <form
        action="#"
        className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-2"
      >
        <TextField
          label="First name"
          name="first_name"
          type="text"
          autoComplete="given-name"
          required
        />
        <TextField
          label="Last name"
          name="last_name"
          type="text"
          autoComplete="family-name"
          required
        />
        <TextField
          className="col-span-full"
          label="Email address"
          name="email"
          type="email"
          autoComplete="email"
          required
        />
        <TextField
          className="col-span-full"
          label="Password"
          name="password"
          type="password"
          autoComplete="new-password"
          required
        />
        <SelectField
          className="col-span-full"
          label="How did you hear about us?"
          name="referral_source"
        >
          <option>AltaVista search</option>
          <option>Super Bowl commercial</option>
          <option>Our route 34 city bus ad</option>
          <option>The “Never Use This” podcast</option>
        </SelectField>
        <div className="col-span-full">
          <Button type="submit" variant="solid" color="blue" className="w-full">
            <span>
              Sign up <span aria-hidden="true">&rarr;</span>
            </span>
          </Button>
        </div>
      </form>
    </SlimLayout>
  )
}
',
    'auth',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'salient', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-salient", "component_type": "auth", "file_path": "tailwind-plus-salient/salient-ts/src/app/(auth)/register/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Spotlight
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Spotlight',
    'Marketing/Landing page component from Tailwind Plus Spotlight template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Link from ''next/link''

import { ContainerInner, ContainerOuter } from ''@/components/Container''

function NavLink({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  return (
    <Link
      href={href}
      className="transition hover:text-teal-500 dark:hover:text-teal-400"
    >
      {children}
    </Link>
  )
}

export function Footer() {
  return (
    <footer className="mt-32 flex-none">
      <ContainerOuter>
        <div className="border-t border-zinc-100 pt-10 pb-16 dark:border-zinc-700/40">
          <ContainerInner>
            <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
              <div className="flex flex-wrap justify-center gap-x-6 gap-y-1 text-sm font-medium text-zinc-800 dark:text-zinc-200">
                <NavLink href="/about">About</NavLink>
                <NavLink href="/projects">Projects</NavLink>
                <NavLink href="/speaking">Speaking</NavLink>
                <NavLink href="/uses">Uses</NavLink>
              </div>
              <p className="text-sm text-zinc-400 dark:text-zinc-500">
                &copy; {new Date().getFullYear()} Spencer Sharp. All rights
                reserved.
              </p>
            </div>
          </ContainerInner>
        </div>
      </ContainerOuter>
    </footer>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'spotlight', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-spotlight", "component_type": "footer", "file_path": "tailwind-plus-spotlight/spotlight-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Spotlight
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Spotlight',
    'Marketing/Landing page component from Tailwind Plus Spotlight template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useEffect, useRef, useState } from ''react''
import Image from ''next/image''
import Link from ''next/link''
import { usePathname } from ''next/navigation''
import { useTheme } from ''next-themes''
import {
  Popover,
  PopoverButton,
  PopoverBackdrop,
  PopoverPanel,
} from ''@headlessui/react''
import clsx from ''clsx''

import { Container } from ''@/components/Container''
import avatarImage from ''@/images/avatar.jpg''

function CloseIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        d="m17.25 6.75-10.5 10.5M6.75 6.75l10.5 10.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function ChevronDownIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 8 6" aria-hidden="true" {...props}>
      <path
        d="M1.75 1.75 4 4.25l2.25-2.5"
        fill="none"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function SunIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      viewBox="0 0 24 24"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...props}
    >
      <path d="M8 12.25A4.25 4.25 0 0 1 12.25 8v0a4.25 4.25 0 0 1 4.25 4.25v0a4.25 4.25 0 0 1-4.25 4.25v0A4.25 4.25 0 0 1 8 12.25v0Z" />
      <path
        d="M12.25 3v1.5M21.5 12.25H20M18.791 18.791l-1.06-1.06M18.791 5.709l-1.06 1.06M12.25 20v1.5M4.5 12.25H3M6.77 6.77 5.709 5.709M6.77 17.73l-1.061 1.061"
        fill="none"
      />
    </svg>
  )
}

function MoonIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        d="M17.25 16.22a6.937 6.937 0 0 1-9.47-9.47 7.451 7.451 0 1 0 9.47 9.47ZM12.75 7C17 7 17 2.75 17 2.75S17 7 21.25 7C17 7 17 11.25 17 11.25S17 7 12.75 7Z"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function MobileNavItem({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  return (
    <li>
      <PopoverButton as={Link} href={href} className="block py-2">
        {children}
      </PopoverButton>
    </li>
  )
}

function MobileNavigation(
  props: React.ComponentPropsWithoutRef<typeof Popover>,
) {
  return (
    <Popover {...props}>
      <PopoverButton className="group flex items-center rounded-full bg-white/90 px-4 py-2 text-sm font-medium text-zinc-800 shadow-lg ring-1 shadow-zinc-800/5 ring-zinc-900/5 backdrop-blur-sm dark:bg-zinc-800/90 dark:text-zinc-200 dark:ring-white/10 dark:hover:ring-white/20">
        Menu
        <ChevronDownIcon className="ml-3 h-auto w-2 stroke-zinc-500 group-hover:stroke-zinc-700 dark:group-hover:stroke-zinc-400" />
      </PopoverButton>
      <PopoverBackdrop
        transition
        className="fixed inset-0 z-50 bg-zinc-800/40 backdrop-blur-xs duration-150 data-closed:opacity-0 data-enter:ease-out data-leave:ease-in dark:bg-black/80"
      />
      <PopoverPanel
        focus
        transition
        className="fixed inset-x-4 top-8 z-50 origin-top rounded-3xl bg-white p-8 ring-1 ring-zinc-900/5 duration-150 data-closed:scale-95 data-closed:opacity-0 data-enter:ease-out data-leave:ease-in dark:bg-zinc-900 dark:ring-zinc-800"
      >
        <div className="flex flex-row-reverse items-center justify-between">
          <PopoverButton aria-label="Close menu" className="-m-1 p-1">
            <CloseIcon className="h-6 w-6 text-zinc-500 dark:text-zinc-400" />
          </PopoverButton>
          <h2 className="text-sm font-medium text-zinc-600 dark:text-zinc-400">
            Navigation
          </h2>
        </div>
        <nav className="mt-6">
          <ul className="-my-2 divide-y divide-zinc-100 text-base text-zinc-800 dark:divide-zinc-100/5 dark:text-zinc-300">
            <MobileNavItem href="/about">About</MobileNavItem>
            <MobileNavItem href="/articles">Articles</MobileNavItem>
            <MobileNavItem href="/projects">Projects</MobileNavItem>
            <MobileNavItem href="/speaking">Speaking</MobileNavItem>
            <MobileNavItem href="/uses">Uses</MobileNavItem>
          </ul>
        </nav>
      </PopoverPanel>
    </Popover>
  )
}

function NavItem({
  href,
  children,
}: {
  href: string
  children: React.ReactNode
}) {
  let isActive = usePathname() === href

  return (
    <li>
      <Link
        href={href}
        className={clsx(
          ''relative block px-3 py-2 transition'',
          isActive
            ? ''text-teal-500 dark:text-teal-400''
            : ''hover:text-teal-500 dark:hover:text-teal-400'',
        )}
      >
        {children}
        {isActive && (
          <span className="absolute inset-x-1 -bottom-px h-px bg-linear-to-r from-teal-500/0 via-teal-500/40 to-teal-500/0 dark:from-teal-400/0 dark:via-teal-400/40 dark:to-teal-400/0" />
        )}
      </Link>
    </li>
  )
}

function DesktopNavigation(props: React.ComponentPropsWithoutRef<''nav''>) {
  return (
    <nav {...props}>
      <ul className="flex rounded-full bg-white/90 px-3 text-sm font-medium text-zinc-800 shadow-lg ring-1 shadow-zinc-800/5 ring-zinc-900/5 backdrop-blur-sm dark:bg-zinc-800/90 dark:text-zinc-200 dark:ring-white/10">
        <NavItem href="/about">About</NavItem>
        <NavItem href="/articles">Articles</NavItem>
        <NavItem href="/projects">Projects</NavItem>
        <NavItem href="/speaking">Speaking</NavItem>
        <NavItem href="/uses">Uses</NavItem>
      </ul>
    </nav>
  )
}

function ThemeToggle() {
  let { resolvedTheme, setTheme } = useTheme()
  let otherTheme = resolvedTheme === ''dark'' ? ''light'' : ''dark''
  let [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  return (
    <button
      type="button"
      aria-label={mounted ? `Switch to ${otherTheme} theme` : ''Toggle theme''}
      className="group rounded-full bg-white/90 px-3 py-2 shadow-lg ring-1 shadow-zinc-800/5 ring-zinc-900/5 backdrop-blur-sm transition dark:bg-zinc-800/90 dark:ring-white/10 dark:hover:ring-white/20"
      onClick={() => setTheme(otherTheme)}
    >
      <SunIcon className="h-6 w-6 fill-zinc-100 stroke-zinc-500 transition group-hover:fill-zinc-200 group-hover:stroke-zinc-700 dark:hidden [@media(prefers-color-scheme:dark)]:fill-teal-50 [@media(prefers-color-scheme:dark)]:stroke-teal-500 [@media(prefers-color-scheme:dark)]:group-hover:fill-teal-50 [@media(prefers-color-scheme:dark)]:group-hover:stroke-teal-600" />
      <MoonIcon className="hidden h-6 w-6 fill-zinc-700 stroke-zinc-500 transition not-[@media_(prefers-color-scheme:dark)]:fill-teal-400/10 not-[@media_(prefers-color-scheme:dark)]:stroke-teal-500 dark:block [@media(prefers-color-scheme:dark)]:group-hover:stroke-zinc-400" />
    </button>
  )
}

function clamp(number: number, a: number, b: number) {
  let min = Math.min(a, b)
  let max = Math.max(a, b)
  return Math.min(Math.max(number, min), max)
}

function AvatarContainer({
  className,
  ...props
}: React.ComponentPropsWithoutRef<''div''>) {
  return (
    <div
      className={clsx(
        className,
        ''h-10 w-10 rounded-full bg-white/90 p-0.5 shadow-lg ring-1 shadow-zinc-800/5 ring-zinc-900/5 backdrop-blur-sm dark:bg-zinc-800/90 dark:ring-white/10'',
      )}
      {...props}
    />
  )
}

function Avatar({
  large = false,
  className,
  ...props
}: Omit<React.ComponentPropsWithoutRef<typeof Link>, ''href''> & {
  large?: boolean
}) {
  return (
    <Link
      href="/"
      aria-label="Home"
      className={clsx(className, ''pointer-events-auto'')}
      {...props}
    >
      <Image
        src={avatarImage}
        alt=""
        sizes={large ? ''4rem'' : ''2.25rem''}
        className={clsx(
          ''rounded-full bg-zinc-100 object-cover dark:bg-zinc-800'',
          large ? ''h-16 w-16'' : ''h-9 w-9'',
        )}
        priority
      />
    </Link>
  )
}

export function Header() {
  let isHomePage = usePathname() === ''/''

  let headerRef = useRef<React.ElementRef<''div''>>(null)
  let avatarRef = useRef<React.ElementRef<''div''>>(null)
  let isInitial = useRef(true)

  useEffect(() => {
    let downDelay = avatarRef.current?.offsetTop ?? 0
    let upDelay = 64

    function setProperty(property: string, value: string) {
      document.documentElement.style.setProperty(property, value)
    }

    function removeProperty(property: string) {
      document.documentElement.style.removeProperty(property)
    }

    function updateHeaderStyles() {
      if (!headerRef.current) {
        return
      }

      let { top, height } = headerRef.current.getBoundingClientRect()
      let scrollY = clamp(
        window.scrollY,
        0,
        document.body.scrollHeight - window.innerHeight,
      )

      if (isInitial.current) {
        setProperty(''--header-position'', ''sticky'')
      }

      setProperty(''--content-offset'', `${downDelay}px`)

      if (isInitial.current || scrollY < downDelay) {
        setProperty(''--header-height'', `${downDelay + height}px`)
        setProperty(''--header-mb'', `${-downDelay}px`)
      } else if (top + height < -upDelay) {
        let offset = Math.max(height, scrollY - upDelay)
        setProperty(''--header-height'', `${offset}px`)
        setProperty(''--header-mb'', `${height - offset}px`)
      } else if (top === 0) {
        setProperty(''--header-height'', `${scrollY + height}px`)
        setProperty(''--header-mb'', `${-scrollY}px`)
      }

      if (top === 0 && scrollY > 0 && scrollY >= downDelay) {
        setProperty(''--header-inner-position'', ''fixed'')
        removeProperty(''--header-top'')
        removeProperty(''--avatar-top'')
      } else {
        removeProperty(''--header-inner-position'')
        setProperty(''--header-top'', ''0px'')
        setProperty(''--avatar-top'', ''0px'')
      }
    }

    function updateAvatarStyles() {
      if (!isHomePage) {
        return
      }

      let fromScale = 1
      let toScale = 36 / 64
      let fromX = 0
      let toX = 2 / 16

      let scrollY = downDelay - window.scrollY

      let scale = (scrollY * (fromScale - toScale)) / downDelay + toScale
      scale = clamp(scale, fromScale, toScale)

      let x = (scrollY * (fromX - toX)) / downDelay + toX
      x = clamp(x, fromX, toX)

      setProperty(
        ''--avatar-image-transform'',
        `translate3d(${x}rem, 0, 0) scale(${scale})`,
      )

      let borderScale = 1 / (toScale / scale)
      let borderX = (-toX + x) * borderScale
      let borderTransform = `translate3d(${borderX}rem, 0, 0) scale(${borderScale})`

      setProperty(''--avatar-border-transform'', borderTransform)
      setProperty(''--avatar-border-opacity'', scale === toScale ? ''1'' : ''0'')
    }

    function updateStyles() {
      updateHeaderStyles()
      updateAvatarStyles()
      isInitial.current = false
    }

    updateStyles()
    window.addEventListener(''scroll'', updateStyles, { passive: true })
    window.addEventListener(''resize'', updateStyles)

    return () => {
      window.removeEventListener(''scroll'', updateStyles)
      window.removeEventListener(''resize'', updateStyles)
    }
  }, [isHomePage])

  return (
    <>
      <header
        className="pointer-events-none relative z-50 flex flex-none flex-col"
        style={{
          height: ''var(--header-height)'',
          marginBottom: ''var(--header-mb)'',
        }}
      >
        {isHomePage && (
          <>
            <div
              ref={avatarRef}
              className="order-last mt-[calc(--spacing(16)-(--spacing(3)))]"
            />
            <Container
              className="top-0 order-last -mb-3 pt-3"
              style={{
                position:
                  ''var(--header-position)'' as React.CSSProperties[''position''],
              }}
            >
              <div
                className="top-(--avatar-top,--spacing(3)) w-full"
                style={{
                  position:
                    ''var(--header-inner-position)'' as React.CSSProperties[''position''],
                }}
              >
                <div className="relative">
                  <AvatarContainer
                    className="absolute top-3 left-0 origin-left transition-opacity"
                    style={{
                      opacity: ''var(--avatar-border-opacity, 0)'',
                      transform: ''var(--avatar-border-transform)'',
                    }}
                  />
                  <Avatar
                    large
                    className="block h-16 w-16 origin-left"
                    style={{ transform: ''var(--avatar-image-transform)'' }}
                  />
                </div>
              </div>
            </Container>
          </>
        )}
        <div
          ref={headerRef}
          className="top-0 z-10 h-16 pt-6"
          style={{
            position:
              ''var(--header-position)'' as React.CSSProperties[''position''],
          }}
        >
          <Container
            className="top-(--header-top,--spacing(6)) w-full"
            style={{
              position:
                ''var(--header-inner-position)'' as React.CSSProperties[''position''],
            }}
          >
            <div className="relative flex gap-4">
              <div className="flex flex-1">
                {!isHomePage && (
                  <AvatarContainer>
                    <Avatar />
                  </AvatarContainer>
                )}
              </div>
              <div className="flex flex-1 justify-end md:justify-center">
                <MobileNavigation className="pointer-events-auto md:hidden" />
                <DesktopNavigation className="pointer-events-auto hidden md:block" />
              </div>
              <div className="flex justify-end md:flex-1">
                <div className="pointer-events-auto">
                  <ThemeToggle />
                </div>
              </div>
            </div>
          </Container>
        </div>
      </header>
      {isHomePage && (
        <div
          className="flex-none"
          style={{ height: ''var(--content-offset)'' }}
        />
      )}
    </>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'spotlight', 'not-for-apps']::text[],
    '{"uses_components": ["Avatar"], "dependencies": ["next/link", "clsx", "next/image", "next-themes", "next/navigation"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-spotlight", "component_type": "hero", "file_path": "tailwind-plus-spotlight/spotlight-ts/src/components/Header.tsx", "uses_components": ["Avatar"], "dependencies": ["next/link", "clsx", "next/image", "next-themes", "next/navigation"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Ecommerce - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Ecommerce - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Spotlight template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Image, { type ImageProps } from ''next/image''
import Link from ''next/link''
import clsx from ''clsx''

import { Button } from ''@/components/Button''
import { Card } from ''@/components/Card''
import { Container } from ''@/components/Container''
import {
  GitHubIcon,
  InstagramIcon,
  LinkedInIcon,
  XIcon,
} from ''@/components/SocialIcons''
import logoAirbnb from ''@/images/logos/airbnb.svg''
import logoFacebook from ''@/images/logos/facebook.svg''
import logoPlanetaria from ''@/images/logos/planetaria.svg''
import logoStarbucks from ''@/images/logos/starbucks.svg''
import image1 from ''@/images/photos/image-1.jpg''
import image2 from ''@/images/photos/image-2.jpg''
import image3 from ''@/images/photos/image-3.jpg''
import image4 from ''@/images/photos/image-4.jpg''
import image5 from ''@/images/photos/image-5.jpg''
import { type ArticleWithSlug, getAllArticles } from ''@/lib/articles''
import { formatDate } from ''@/lib/formatDate''

function MailIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...props}
    >
      <path
        d="M2.75 7.75a3 3 0 0 1 3-3h12.5a3 3 0 0 1 3 3v8.5a3 3 0 0 1-3 3H5.75a3 3 0 0 1-3-3v-8.5Z"
        className="fill-zinc-100 stroke-zinc-400 dark:fill-zinc-100/10 dark:stroke-zinc-500"
      />
      <path
        d="m4 6 6.024 5.479a2.915 2.915 0 0 0 3.952 0L20 6"
        className="stroke-zinc-400 dark:stroke-zinc-500"
      />
    </svg>
  )
}

function BriefcaseIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...props}
    >
      <path
        d="M2.75 9.75a3 3 0 0 1 3-3h12.5a3 3 0 0 1 3 3v8.5a3 3 0 0 1-3 3H5.75a3 3 0 0 1-3-3v-8.5Z"
        className="fill-zinc-100 stroke-zinc-400 dark:fill-zinc-100/10 dark:stroke-zinc-500"
      />
      <path
        d="M3 14.25h6.249c.484 0 .952-.002 1.316.319l.777.682a.996.996 0 0 0 1.316 0l.777-.682c.364-.32.832-.319 1.316-.319H21M8.75 6.5V4.75a2 2 0 0 1 2-2h2.5a2 2 0 0 1 2 2V6.5"
        className="stroke-zinc-400 dark:stroke-zinc-500"
      />
    </svg>
  )
}

function ArrowDownIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 16 16" fill="none" aria-hidden="true" {...props}>
      <path
        d="M4.75 8.75 8 12.25m0 0 3.25-3.5M8 12.25v-8.5"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function Article({ article }: { article: ArticleWithSlug }) {
  return (
    <Card as="article">
      <Card.Title href={`/articles/${article.slug}`}>
        {article.title}
      </Card.Title>
      <Card.Eyebrow as="time" dateTime={article.date} decorate>
        {formatDate(article.date)}
      </Card.Eyebrow>
      <Card.Description>{article.description}</Card.Description>
      <Card.Cta>Read article</Card.Cta>
    </Card>
  )
}

function SocialLink({
  icon: Icon,
  ...props
}: React.ComponentPropsWithoutRef<typeof Link> & {
  icon: React.ComponentType<{ className?: string }>
}) {
  return (
    <Link className="group -m-1 p-1" {...props}>
      <Icon className="h-6 w-6 fill-zinc-500 transition group-hover:fill-zinc-600 dark:fill-zinc-400 dark:group-hover:fill-zinc-300" />
    </Link>
  )
}

function Newsletter() {
  return (
    <form
      action="/thank-you"
      className="rounded-2xl border border-zinc-100 p-6 dark:border-zinc-700/40"
    >
      <h2 className="flex text-sm font-semibold text-zinc-900 dark:text-zinc-100">
        <MailIcon className="h-6 w-6 flex-none" />
        <span className="ml-3">Stay up to date</span>
      </h2>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
        Get notified when I publish something new, and unsubscribe at any time.
      </p>
      <div className="mt-6 flex items-center">
        <span className="flex min-w-0 flex-auto p-px">
          <input
            type="email"
            placeholder="Email address"
            aria-label="Email address"
            required
            className="w-full appearance-none rounded-[calc(var(--radius-md)-1px)] bg-white px-3 py-[calc(--spacing(2)-1px)] shadow-md shadow-zinc-800/5 outline outline-zinc-900/10 placeholder:text-zinc-400 focus:ring-4 focus:ring-teal-500/10 focus:outline-teal-500 sm:text-sm dark:bg-zinc-700/[0.15] dark:text-zinc-200 dark:outline-zinc-700 dark:placeholder:text-zinc-500 dark:focus:ring-teal-400/10 dark:focus:outline-teal-400"
          />
        </span>
        <Button type="submit" className="ml-4 flex-none">
          Join
        </Button>
      </div>
    </form>
  )
}

interface Role {
  company: string
  title: string
  logo: ImageProps[''src'']
  start: string | { label: string; dateTime: string }
  end: string | { label: string; dateTime: string }
}

function Role({ role }: { role: Role }) {
  let startLabel =
    typeof role.start === ''string'' ? role.start : role.start.label
  let startDate =
    typeof role.start === ''string'' ? role.start : role.start.dateTime

  let endLabel = typeof role.end === ''string'' ? role.end : role.end.label
  let endDate = typeof role.end === ''string'' ? role.end : role.end.dateTime

  return (
    <li className="flex gap-4">
      <div className="relative mt-1 flex h-10 w-10 flex-none items-center justify-center rounded-full shadow-md ring-1 shadow-zinc-800/5 ring-zinc-900/5 dark:border dark:border-zinc-700/50 dark:bg-zinc-800 dark:ring-0">
        <Image src={role.logo} alt="" className="h-7 w-7" unoptimized />
      </div>
      <dl className="flex flex-auto flex-wrap gap-x-2">
        <dt className="sr-only">Company</dt>
        <dd className="w-full flex-none text-sm font-medium text-zinc-900 dark:text-zinc-100">
          {role.company}
        </dd>
        <dt className="sr-only">Role</dt>
        <dd className="text-xs text-zinc-500 dark:text-zinc-400">
          {role.title}
        </dd>
        <dt className="sr-only">Date</dt>
        <dd
          className="ml-auto text-xs text-zinc-400 dark:text-zinc-500"
          aria-label={`${startLabel} until ${endLabel}`}
        >
          <time dateTime={startDate}>{startLabel}</time>{'' ''}
          <span aria-hidden="true">—</span>{'' ''}
          <time dateTime={endDate}>{endLabel}</time>
        </dd>
      </dl>
    </li>
  )
}

function Resume() {
  let resume: Array<Role> = [
    {
      company: ''Planetaria'',
      title: ''CEO'',
      logo: logoPlanetaria,
      start: ''2019'',
      end: {
        label: ''Present'',
        dateTime: new Date().getFullYear().toString(),
      },
    },
    {
      company: ''Airbnb'',
      title: ''Product Designer'',
      logo: logoAirbnb,
      start: ''2014'',
      end: ''2019'',
    },
    {
      company: ''Facebook'',
      title: ''iOS Software Engineer'',
      logo: logoFacebook,
      start: ''2011'',
      end: ''2014'',
    },
    {
      company: ''Starbucks'',
      title: ''Shift Supervisor'',
      logo: logoStarbucks,
      start: ''2008'',
      end: ''2011'',
    },
  ]

  return (
    <div className="rounded-2xl border border-zinc-100 p-6 dark:border-zinc-700/40">
      <h2 className="flex text-sm font-semibold text-zinc-900 dark:text-zinc-100">
        <BriefcaseIcon className="h-6 w-6 flex-none" />
        <span className="ml-3">Work</span>
      </h2>
      <ol className="mt-6 space-y-4">
        {resume.map((role, roleIndex) => (
          <Role key={roleIndex} role={role} />
        ))}
      </ol>
      <Button href="#" variant="secondary" className="group mt-6 w-full">
        Download CV
        <ArrowDownIcon className="h-4 w-4 stroke-zinc-400 transition group-active:stroke-zinc-600 dark:group-hover:stroke-zinc-50 dark:group-active:stroke-zinc-50" />
      </Button>
    </div>
  )
}

function Photos() {
  let rotations = [''rotate-2'', ''-rotate-2'', ''rotate-2'', ''rotate-2'', ''-rotate-2'']

  return (
    <div className="mt-16 sm:mt-20">
      <div className="-my-4 flex justify-center gap-5 overflow-hidden py-4 sm:gap-8">
        {[image1, image2, image3, image4, image5].map((image, imageIndex) => (
          <div
            key={image.src}
            className={clsx(
              ''relative aspect-9/10 w-44 flex-none overflow-hidden rounded-xl bg-zinc-100 sm:w-72 sm:rounded-2xl dark:bg-zinc-800'',
              rotations[imageIndex % rotations.length],
            )}
          >
            <Image
              src={image}
              alt=""
              sizes="(min-width: 640px) 18rem, 11rem"
              className="absolute inset-0 h-full w-full object-cover"
            />
          </div>
        ))}
      </div>
    </div>
  )
}

export default async function Home() {
  let articles = (await getAllArticles()).slice(0, 4)

  return (
    <>
      <Container className="mt-9">
        <div className="max-w-2xl">
          <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
            Software designer, founder, and amateur astronaut.
          </h1>
          <p className="mt-6 text-base text-zinc-600 dark:text-zinc-400">
            I’m Spencer, a software designer and entrepreneur based in New York
            City. I’m the founder and CEO of Planetaria, where we develop
            technologies that empower regular people to explore space on their
            own terms.
          </p>
          <div className="mt-6 flex gap-6">
            <SocialLink href="#" aria-label="Follow on X" icon={XIcon} />
            <SocialLink
              href="#"
              aria-label="Follow on Instagram"
              icon={InstagramIcon}
            />
            <SocialLink
              href="#"
              aria-label="Follow on GitHub"
              icon={GitHubIcon}
            />
            <SocialLink
              href="#"
              aria-label="Follow on LinkedIn"
              icon={LinkedInIcon}
            />
          </div>
        </div>
      </Container>
      <Photos />
      <Container className="mt-24 md:mt-28">
        <div className="mx-auto grid max-w-xl grid-cols-1 gap-y-20 lg:max-w-none lg:grid-cols-2">
          <div className="flex flex-col gap-16">
            {articles.map((article) => (
              <Article key={article.slug} article={article} />
            ))}
          </div>
          <div className="space-y-10 lg:pl-16 xl:pl-24">
            <Newsletter />
            <Resume />
          </div>
        </div>
      </Container>
    </>
  )
}
',
    'ecommerce',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'ecommerce', 'spotlight', 'not-for-apps']::text[],
    '{"uses_components": ["Card", "Button"], "dependencies": ["next/link", "clsx", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-spotlight", "component_type": "ecommerce", "file_path": "tailwind-plus-spotlight/spotlight-ts/src/app/page.tsx", "uses_components": ["Card", "Button"], "dependencies": ["next/link", "clsx", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Team - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Team - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Spotlight template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import Image from ''next/image''
import Link from ''next/link''
import clsx from ''clsx''

import { Container } from ''@/components/Container''
import {
  GitHubIcon,
  InstagramIcon,
  LinkedInIcon,
  XIcon,
} from ''@/components/SocialIcons''
import portraitImage from ''@/images/portrait.jpg''

function SocialLink({
  className,
  href,
  children,
  icon: Icon,
}: {
  className?: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  children: React.ReactNode
}) {
  return (
    <li className={clsx(className, ''flex'')}>
      <Link
        href={href}
        className="group flex text-sm font-medium text-zinc-800 transition hover:text-teal-500 dark:text-zinc-200 dark:hover:text-teal-500"
      >
        <Icon className="h-6 w-6 flex-none fill-zinc-500 transition group-hover:fill-teal-500" />
        <span className="ml-4">{children}</span>
      </Link>
    </li>
  )
}

function MailIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        d="M6 5a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3V8a3 3 0 0 0-3-3H6Zm.245 2.187a.75.75 0 0 0-.99 1.126l6.25 5.5a.75.75 0 0 0 .99 0l6.25-5.5a.75.75 0 0 0-.99-1.126L12 12.251 6.245 7.187Z"
      />
    </svg>
  )
}

export const metadata: Metadata = {
  title: ''About'',
  description:
    ''I’m Spencer Sharp. I live in New York City, where I design the future.'',
}

export default function About() {
  return (
    <Container className="mt-16 sm:mt-32">
      <div className="grid grid-cols-1 gap-y-16 lg:grid-cols-2 lg:grid-rows-[auto_1fr] lg:gap-y-12">
        <div className="lg:pl-20">
          <div className="max-w-xs px-2.5 lg:max-w-none">
            <Image
              src={portraitImage}
              alt=""
              sizes="(min-width: 1024px) 32rem, 20rem"
              className="aspect-square rotate-3 rounded-2xl bg-zinc-100 object-cover dark:bg-zinc-800"
            />
          </div>
        </div>
        <div className="lg:order-first lg:row-span-2">
          <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
            I’m Spencer Sharp. I live in New York City, where I design the
            future.
          </h1>
          <div className="mt-6 space-y-7 text-base text-zinc-600 dark:text-zinc-400">
            <p>
              I’ve loved making things for as long as I can remember, and wrote
              my first program when I was 6 years old, just two weeks after my
              mom brought home the brand new Macintosh LC 550 that I taught
              myself to type on.
            </p>
            <p>
              The only thing I loved more than computers as a kid was space.
              When I was 8, I climbed the 40-foot oak tree at the back of our
              yard while wearing my older sister’s motorcycle helmet, counted
              down from three, and jumped — hoping the tree was tall enough that
              with just a bit of momentum I’d be able to get to orbit.
            </p>
            <p>
              I spent the next few summers indoors working on a rocket design,
              while I recovered from the multiple surgeries it took to fix my
              badly broken legs. It took nine iterations, but when I was 15 I
              sent my dad’s Blackberry into orbit and was able to transmit a
              photo back down to our family computer from space.
            </p>
            <p>
              Today, I’m the founder of Planetaria, where we’re working on
              civilian space suits and manned shuttle kits you can assemble at
              home so that the next generation of kids really <em>can</em> make
              it to orbit — from the comfort of their own backyards.
            </p>
          </div>
        </div>
        <div className="lg:pl-20">
          <ul role="list">
            <SocialLink href="#" icon={XIcon}>
              Follow on X
            </SocialLink>
            <SocialLink href="#" icon={InstagramIcon} className="mt-4">
              Follow on Instagram
            </SocialLink>
            <SocialLink href="#" icon={GitHubIcon} className="mt-4">
              Follow on GitHub
            </SocialLink>
            <SocialLink href="#" icon={LinkedInIcon} className="mt-4">
              Follow on LinkedIn
            </SocialLink>
            <SocialLink
              href="mailto:spencer@planetaria.tech"
              icon={MailIcon}
              className="mt-8 border-t border-zinc-100 pt-8 dark:border-zinc-700/40"
            >
              spencer@planetaria.tech
            </SocialLink>
          </ul>
        </div>
      </div>
    </Container>
  )
}
',
    'team',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'team', 'spotlight', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "clsx", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-spotlight", "component_type": "team", "file_path": "tailwind-plus-spotlight/spotlight-ts/src/app/about/page.tsx", "uses_components": [], "dependencies": ["next/link", "clsx", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Blog - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Blog - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Spotlight template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''

import { Card } from ''@/components/Card''
import { SimpleLayout } from ''@/components/SimpleLayout''
import { type ArticleWithSlug, getAllArticles } from ''@/lib/articles''
import { formatDate } from ''@/lib/formatDate''

function Article({ article }: { article: ArticleWithSlug }) {
  return (
    <article className="md:grid md:grid-cols-4 md:items-baseline">
      <Card className="md:col-span-3">
        <Card.Title href={`/articles/${article.slug}`}>
          {article.title}
        </Card.Title>
        <Card.Eyebrow
          as="time"
          dateTime={article.date}
          className="md:hidden"
          decorate
        >
          {formatDate(article.date)}
        </Card.Eyebrow>
        <Card.Description>{article.description}</Card.Description>
        <Card.Cta>Read article</Card.Cta>
      </Card>
      <Card.Eyebrow
        as="time"
        dateTime={article.date}
        className="mt-1 max-md:hidden"
      >
        {formatDate(article.date)}
      </Card.Eyebrow>
    </article>
  )
}

export const metadata: Metadata = {
  title: ''Articles'',
  description:
    ''All of my long-form thoughts on programming, leadership, product design, and more, collected in chronological order.'',
}

export default async function ArticlesIndex() {
  let articles = await getAllArticles()

  return (
    <SimpleLayout
      title="Writing on software design, company building, and the aerospace industry."
      intro="All of my long-form thoughts on programming, leadership, product design, and more, collected in chronological order."
    >
      <div className="md:border-l md:border-zinc-100 md:pl-6 md:dark:border-zinc-700/40">
        <div className="flex max-w-3xl flex-col space-y-16">
          {articles.map((article) => (
            <Article key={article.slug} article={article} />
          ))}
        </div>
      </div>
    </SimpleLayout>
  )
}
',
    'blog',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'spotlight', 'not-for-apps']::text[],
    '{"uses_components": ["Card"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-spotlight", "component_type": "blog", "file_path": "tailwind-plus-spotlight/spotlight-ts/src/app/articles/page.tsx", "uses_components": ["Card"], "dependencies": [], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Portfolio - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Portfolio - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Spotlight template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Card } from ''@/components/Card''
import { Section } from ''@/components/Section''
import { SimpleLayout } from ''@/components/SimpleLayout''

function ToolsSection({
  children,
  ...props
}: React.ComponentPropsWithoutRef<typeof Section>) {
  return (
    <Section {...props}>
      <ul role="list" className="space-y-16">
        {children}
      </ul>
    </Section>
  )
}

function Tool({
  title,
  href,
  children,
}: {
  title: string
  href?: string
  children: React.ReactNode
}) {
  return (
    <Card as="li">
      <Card.Title as="h3" href={href}>
        {title}
      </Card.Title>
      <Card.Description>{children}</Card.Description>
    </Card>
  )
}

export const metadata = {
  title: ''Uses'',
  description: ''Software I use, gadgets I love, and other things I recommend.'',
}

export default function Uses() {
  return (
    <SimpleLayout
      title="Software I use, gadgets I love, and other things I recommend."
      intro="I get asked a lot about the things I use to build software, stay productive, or buy to fool myself into thinking I’m being productive when I’m really just procrastinating. Here’s a big list of all of my favorite stuff."
    >
      <div className="space-y-20">
        <ToolsSection title="Workstation">
          <Tool title="16” MacBook Pro, M1 Max, 64GB RAM (2021)">
            I was using an Intel-based 16” MacBook Pro prior to this and the
            difference is night and day. I’ve never heard the fans turn on a
            single time, even under the incredibly heavy loads I put it through
            with our various launch simulations.
          </Tool>
          <Tool title="Apple Pro Display XDR (Standard Glass)">
            The only display on the market if you want something HiDPI and
            bigger than 27”. When you’re working at planetary scale, every pixel
            you can get counts.
          </Tool>
          <Tool title="IBM Model M SSK Industrial Keyboard">
            They don’t make keyboards the way they used to. I buy these any time
            I see them go up for sale and keep them in storage in case I need
            parts or need to retire my main.
          </Tool>
          <Tool title="Apple Magic Trackpad">
            Something about all the gestures makes me feel like a wizard with
            special powers. I really like feeling like a wizard with special
            powers.
          </Tool>
          <Tool title="Herman Miller Aeron Chair">
            If I’m going to slouch in the worst ergonomic position imaginable
            all day, I might as well do it in an expensive chair.
          </Tool>
        </ToolsSection>
        <ToolsSection title="Development tools">
          <Tool title="Sublime Text 4">
            I don’t care if it’s missing all of the fancy IDE features everyone
            else relies on, Sublime Text is still the best text editor ever
            made.
          </Tool>
          <Tool title="iTerm2">
            I’m honestly not even sure what features I get with this that aren’t
            just part of the macOS Terminal but it’s what I use.
          </Tool>
          <Tool title="TablePlus">
            Great software for working with databases. Has saved me from
            building about a thousand admin interfaces for my various projects
            over the years.
          </Tool>
        </ToolsSection>
        <ToolsSection title="Design">
          <Tool title="Figma">
            We started using Figma as just a design tool but now it’s become our
            virtual whiteboard for the entire company. Never would have expected
            the collaboration features to be the real hook.
          </Tool>
        </ToolsSection>
        <ToolsSection title="Productivity">
          <Tool title="Alfred">
            It’s not the newest kid on the block but it’s still the fastest. The
            Sublime Text of the application launcher world.
          </Tool>
          <Tool title="Reflect">
            Using a daily notes system instead of trying to keep things
            organized by topics has been super powerful for me. And with
            Reflect, it’s still easy for me to keep all of that stuff
            discoverable by topic even though all of my writing happens in the
            daily note.
          </Tool>
          <Tool title="SavvyCal">
            Great tool for scheduling meetings while protecting my calendar and
            making sure I still have lots of time for deep work during the week.
          </Tool>
          <Tool title="Focus">
            Simple tool for blocking distracting websites when I need to just do
            the work and get some momentum going.
          </Tool>
        </ToolsSection>
      </div>
    </SimpleLayout>
  )
}
',
    'portfolio',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'portfolio', 'spotlight', 'not-for-apps']::text[],
    '{"uses_components": ["Card"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-spotlight", "component_type": "portfolio", "file_path": "tailwind-plus-spotlight/spotlight-ts/src/app/uses/page.tsx", "uses_components": ["Card"], "dependencies": [], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Cta - Contactsection - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Cta - Contactsection - Marketing',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { FadeIn } from ''@/components/FadeIn''
import { Offices } from ''@/components/Offices''

export function ContactSection() {
  return (
    <Container className="mt-24 sm:mt-32 lg:mt-40">
      <FadeIn className="-mx-6 rounded-4xl bg-neutral-950 px-6 py-20 sm:mx-0 sm:py-32 md:px-12">
        <div className="mx-auto max-w-4xl">
          <div className="max-w-xl">
            <h2 className="font-display text-3xl font-medium text-balance text-white sm:text-4xl">
              Tell us about your project
            </h2>
            <div className="mt-6 flex">
              <Button href="/contact" invert>
                Say Hej
              </Button>
            </div>
            <div className="mt-10 border-t border-white/10 pt-10">
              <h3 className="font-display text-base font-semibold text-white">
                Our offices
              </h3>
              <Offices
                invert
                className="mt-6 grid grid-cols-1 gap-8 sm:grid-cols-2"
              />
            </div>
          </div>
        </div>
      </FadeIn>
    </Container>
  )
}
',
    'cta',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'cta', 'studio', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "cta", "file_path": "tailwind-plus-studio/studio-ts/src/components/ContactSection.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Footer - Studio
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Footer - Studio',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Link from ''next/link''

import { Container } from ''@/components/Container''
import { FadeIn } from ''@/components/FadeIn''
import { Logo } from ''@/components/Logo''
import { socialMediaProfiles } from ''@/components/SocialMedia''

const navigation = [
  {
    title: ''Work'',
    links: [
      { title: ''FamilyFund'', href: ''/work/family-fund'' },
      { title: ''Unseal'', href: ''/work/unseal'' },
      { title: ''Phobia'', href: ''/work/phobia'' },
      {
        title: (
          <>
            See all <span aria-hidden="true">&rarr;</span>
          </>
        ),
        href: ''/work'',
      },
    ],
  },
  {
    title: ''Company'',
    links: [
      { title: ''About'', href: ''/about'' },
      { title: ''Process'', href: ''/process'' },
      { title: ''Blog'', href: ''/blog'' },
      { title: ''Contact us'', href: ''/contact'' },
    ],
  },
  {
    title: ''Connect'',
    links: socialMediaProfiles,
  },
]

function Navigation() {
  return (
    <nav>
      <ul role="list" className="grid grid-cols-2 gap-8 sm:grid-cols-3">
        {navigation.map((section, sectionIndex) => (
          <li key={sectionIndex}>
            <div className="font-display text-sm font-semibold tracking-wider text-neutral-950">
              {section.title}
            </div>
            <ul role="list" className="mt-4 text-sm text-neutral-700">
              {section.links.map((link, linkIndex) => (
                <li key={linkIndex} className="mt-4">
                  <Link
                    href={link.href}
                    className="transition hover:text-neutral-950"
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </nav>
  )
}

function ArrowIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg viewBox="0 0 16 6" aria-hidden="true" {...props}>
      <path
        fill="currentColor"
        fillRule="evenodd"
        clipRule="evenodd"
        d="M16 3 10 .5v2H0v1h10v2L16 3Z"
      />
    </svg>
  )
}

function NewsletterForm() {
  return (
    <form className="max-w-sm">
      <h2 className="font-display text-sm font-semibold tracking-wider text-neutral-950">
        Sign up for our newsletter
      </h2>
      <p className="mt-4 text-sm text-neutral-700">
        Subscribe to get the latest design news, articles, resources and
        inspiration.
      </p>
      <div className="relative mt-6">
        <input
          type="email"
          placeholder="Email address"
          autoComplete="email"
          aria-label="Email address"
          className="block w-full rounded-2xl border border-neutral-300 bg-transparent py-4 pr-20 pl-6 text-base/6 text-neutral-950 ring-4 ring-transparent transition placeholder:text-neutral-500 focus:border-neutral-950 focus:ring-neutral-950/5 focus:outline-hidden"
        />
        <div className="absolute inset-y-1 right-1 flex justify-end">
          <button
            type="submit"
            aria-label="Submit"
            className="flex aspect-square h-full items-center justify-center rounded-xl bg-neutral-950 text-white transition hover:bg-neutral-800"
          >
            <ArrowIcon className="w-4" />
          </button>
        </div>
      </div>
    </form>
  )
}

export function Footer() {
  return (
    <Container as="footer" className="mt-24 w-full sm:mt-32 lg:mt-40">
      <FadeIn>
        <div className="grid grid-cols-1 gap-x-8 gap-y-16 lg:grid-cols-2">
          <Navigation />
          <div className="flex lg:justify-end">
            <NewsletterForm />
          </div>
        </div>
        <div className="mt-24 mb-20 flex flex-wrap items-end justify-between gap-x-6 gap-y-4 border-t border-neutral-950/10 pt-12">
          <Link href="/" aria-label="Home">
            <Logo className="h-8" fillOnHover />
          </Link>
          <p className="text-sm text-neutral-700">
            © Studio Agency Inc. {new Date().getFullYear()}
          </p>
        </div>
      </FadeIn>
    </Container>
  )
}
',
    'footer',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "footer", "file_path": "tailwind-plus-studio/studio-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Features Section - Studio
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Features Section - Studio',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import Image from ''next/image''
import Link from ''next/link''

import { ContactSection } from ''@/components/ContactSection''
import { Container } from ''@/components/Container''
import { FadeIn, FadeInStagger } from ''@/components/FadeIn''
import { List, ListItem } from ''@/components/List''
import { SectionIntro } from ''@/components/SectionIntro''
import { StylizedImage } from ''@/components/StylizedImage''
import { Testimonial } from ''@/components/Testimonial''
import logoBrightPath from ''@/images/clients/bright-path/logo-light.svg''
import logoFamilyFund from ''@/images/clients/family-fund/logo-light.svg''
import logoGreenLife from ''@/images/clients/green-life/logo-light.svg''
import logoHomeWork from ''@/images/clients/home-work/logo-light.svg''
import logoMailSmirk from ''@/images/clients/mail-smirk/logo-light.svg''
import logoNorthAdventures from ''@/images/clients/north-adventures/logo-light.svg''
import logoPhobiaDark from ''@/images/clients/phobia/logo-dark.svg''
import logoPhobiaLight from ''@/images/clients/phobia/logo-light.svg''
import logoUnseal from ''@/images/clients/unseal/logo-light.svg''
import imageLaptop from ''@/images/laptop.jpg''
import { type CaseStudy, type MDXEntry, loadCaseStudies } from ''@/lib/mdx''
import { RootLayout } from ''@/components/RootLayout''

const clients = [
  [''Phobia'', logoPhobiaLight],
  [''Family Fund'', logoFamilyFund],
  [''Unseal'', logoUnseal],
  [''Mail Smirk'', logoMailSmirk],
  [''Home Work'', logoHomeWork],
  [''Green Life'', logoGreenLife],
  [''Bright Path'', logoBrightPath],
  [''North Adventures'', logoNorthAdventures],
]

function Clients() {
  return (
    <div className="mt-24 rounded-4xl bg-neutral-950 py-20 sm:mt-32 sm:py-32 lg:mt-56">
      <Container>
        <FadeIn className="flex items-center gap-x-8">
          <h2 className="text-center font-display text-sm font-semibold tracking-wider text-white sm:text-left">
            We’ve worked with hundreds of amazing people
          </h2>
          <div className="h-px flex-auto bg-neutral-800" />
        </FadeIn>
        <FadeInStagger faster>
          <ul
            role="list"
            className="mt-10 grid grid-cols-2 gap-x-8 gap-y-10 lg:grid-cols-4"
          >
            {clients.map(([client, logo]) => (
              <li key={client}>
                <FadeIn>
                  <Image src={logo} alt={client} unoptimized />
                </FadeIn>
              </li>
            ))}
          </ul>
        </FadeInStagger>
      </Container>
    </div>
  )
}

function CaseStudies({
  caseStudies,
}: {
  caseStudies: Array<MDXEntry<CaseStudy>>
}) {
  return (
    <>
      <SectionIntro
        title="Harnessing technology for a brighter future"
        className="mt-24 sm:mt-32 lg:mt-40"
      >
        <p>
          We believe technology is the answer to the world’s greatest
          challenges. It’s also the cause, so we find ourselves in bit of a
          catch 22 situation.
        </p>
      </SectionIntro>
      <Container className="mt-16">
        <FadeInStagger className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {caseStudies.map((caseStudy) => (
            <FadeIn key={caseStudy.href} className="flex">
              <article className="relative flex w-full flex-col rounded-3xl p-6 ring-1 ring-neutral-950/5 transition hover:bg-neutral-50 sm:p-8">
                <h3>
                  <Link href={caseStudy.href}>
                    <span className="absolute inset-0 rounded-3xl" />
                    <Image
                      src={caseStudy.logo}
                      alt={caseStudy.client}
                      className="h-16 w-16"
                      unoptimized
                    />
                  </Link>
                </h3>
                <p className="mt-6 flex gap-x-2 text-sm text-neutral-950">
                  <time
                    dateTime={caseStudy.date.split(''-'')[0]}
                    className="font-semibold"
                  >
                    {caseStudy.date.split(''-'')[0]}
                  </time>
                  <span className="text-neutral-300" aria-hidden="true">
                    /
                  </span>
                  <span>Case study</span>
                </p>
                <p className="mt-6 font-display text-2xl font-semibold text-neutral-950">
                  {caseStudy.title}
                </p>
                <p className="mt-4 text-base text-neutral-600">
                  {caseStudy.description}
                </p>
              </article>
            </FadeIn>
          ))}
        </FadeInStagger>
      </Container>
    </>
  )
}

function Services() {
  return (
    <>
      <SectionIntro
        eyebrow="Services"
        title="We help you identify, explore and respond to new opportunities."
        className="mt-24 sm:mt-32 lg:mt-40"
      >
        <p>
          As long as those opportunities involve giving us money to re-purpose
          old projects — we can come up with an endless number of those.
        </p>
      </SectionIntro>
      <Container className="mt-16">
        <div className="lg:flex lg:items-center lg:justify-end">
          <div className="flex justify-center lg:w-1/2 lg:justify-end lg:pr-12">
            <FadeIn className="w-135 flex-none lg:w-180">
              <StylizedImage
                src={imageLaptop}
                sizes="(min-width: 1024px) 41rem, 31rem"
                className="justify-center lg:justify-end"
              />
            </FadeIn>
          </div>
          <List className="mt-16 lg:mt-0 lg:w-1/2 lg:min-w-132 lg:pl-4">
            <ListItem title="Web development">
              We specialise in crafting beautiful, high quality marketing pages.
              The rest of the website will be a shell that uses lorem ipsum
              everywhere.
            </ListItem>
            <ListItem title="Application development">
              We have a team of skilled developers who are experts in the latest
              app frameworks, like Angular 1 and Google Web Toolkit.
            </ListItem>
            <ListItem title="E-commerce">
              We are at the forefront of modern e-commerce development. Which
              mainly means adding your logo to the Shopify store template we’ve
              used for the past six years.
            </ListItem>
            <ListItem title="Custom content management">
              At Studio we understand the importance of having a robust and
              customised CMS. That’s why we run all of our client projects out
              of a single, enormous Joomla instance.
            </ListItem>
          </List>
        </div>
      </Container>
    </>
  )
}

export const metadata: Metadata = {
  description:
    ''We are a development studio working at the intersection of design and technology.'',
}

export default async function Home() {
  let caseStudies = (await loadCaseStudies()).slice(0, 3)

  return (
    <RootLayout>
      <Container className="mt-24 sm:mt-32 md:mt-56">
        <FadeIn className="max-w-3xl">
          <h1 className="font-display text-5xl font-medium tracking-tight text-balance text-neutral-950 sm:text-7xl">
            Award-winning development studio based in Denmark.
          </h1>
          <p className="mt-6 text-xl text-neutral-600">
            We are a development studio working at the intersection of design
            and technology. It’s a really busy intersection though — a lot of
            our staff have been involved in hit and runs.
          </p>
        </FadeIn>
      </Container>

      <Clients />

      <CaseStudies caseStudies={caseStudies} />

      <Testimonial
        className="mt-24 sm:mt-32 lg:mt-40"
        client={{ name: ''Phobia'', logo: logoPhobiaDark }}
      >
        The team at Studio went above and beyond with our onboarding, even
        finding a way to access the user’s microphone without triggering one of
        those annoying permission dialogs.
      </Testimonial>

      <Services />

      <ContactSection />
    </RootLayout>
  )
}
',
    'features',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "features", "file_path": "tailwind-plus-studio/studio-ts/src/app/page.tsx", "uses_components": [], "dependencies": ["next/link", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Team - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Team - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import Image from ''next/image''

import { Border } from ''@/components/Border''
import { ContactSection } from ''@/components/ContactSection''
import { Container } from ''@/components/Container''
import { FadeIn, FadeInStagger } from ''@/components/FadeIn''
import { GridList, GridListItem } from ''@/components/GridList''
import { PageIntro } from ''@/components/PageIntro''
import { PageLinks } from ''@/components/PageLinks''
import { SectionIntro } from ''@/components/SectionIntro''
import { StatList, StatListItem } from ''@/components/StatList''
import imageAngelaFisher from ''@/images/team/angela-fisher.jpg''
import imageBenjaminRussel from ''@/images/team/benjamin-russel.jpg''
import imageBlakeReid from ''@/images/team/blake-reid.jpg''
import imageChelseaHagon from ''@/images/team/chelsea-hagon.jpg''
import imageDriesVincent from ''@/images/team/dries-vincent.jpg''
import imageEmmaDorsey from ''@/images/team/emma-dorsey.jpg''
import imageJeffreyWebb from ''@/images/team/jeffrey-webb.jpg''
import imageKathrynMurphy from ''@/images/team/kathryn-murphy.jpg''
import imageLeonardKrasner from ''@/images/team/leonard-krasner.jpg''
import imageLeslieAlexander from ''@/images/team/leslie-alexander.jpg''
import imageMichaelFoster from ''@/images/team/michael-foster.jpg''
import imageWhitneyFrancis from ''@/images/team/whitney-francis.jpg''
import { loadArticles } from ''@/lib/mdx''
import { RootLayout } from ''@/components/RootLayout''

function Culture() {
  return (
    <div className="mt-24 rounded-4xl bg-neutral-950 py-24 sm:mt-32 lg:mt-40 lg:py-32">
      <SectionIntro
        eyebrow="Our culture"
        title="Balance your passion with your passion for life."
        invert
      >
        <p>
          We are a group of like-minded people who share the same core values.
        </p>
      </SectionIntro>
      <Container className="mt-16">
        <GridList>
          <GridListItem title="Loyalty" invert>
            Our team has been with us since the beginning because none of them
            are allowed to have LinkedIn profiles.
          </GridListItem>
          <GridListItem title="Trust" invert>
            We don’t care when our team works just as long as they are working
            every waking second.
          </GridListItem>
          <GridListItem title="Compassion" invert>
            You never know what someone is going through at home and we make
            sure to never find out.
          </GridListItem>
        </GridList>
      </Container>
    </div>
  )
}

const team = [
  {
    title: ''Leadership'',
    people: [
      {
        name: ''Leslie Alexander'',
        role: ''Co-Founder / CEO'',
        image: { src: imageLeslieAlexander },
      },
      {
        name: ''Michael Foster'',
        role: ''Co-Founder / CTO'',
        image: { src: imageMichaelFoster },
      },
      {
        name: ''Dries Vincent'',
        role: ''Partner & Business Relations'',
        image: { src: imageDriesVincent },
      },
    ],
  },
  {
    title: ''Team'',
    people: [
      {
        name: ''Chelsea Hagon'',
        role: ''Senior Developer'',
        image: { src: imageChelseaHagon },
      },
      {
        name: ''Emma Dorsey'',
        role: ''Senior Designer'',
        image: { src: imageEmmaDorsey },
      },
      {
        name: ''Leonard Krasner'',
        role: ''VP, User Experience'',
        image: { src: imageLeonardKrasner },
      },
      {
        name: ''Blake Reid'',
        role: ''Junior Copywriter'',
        image: { src: imageBlakeReid },
      },
      {
        name: ''Kathryn Murphy'',
        role: ''VP, Human Resources'',
        image: { src: imageKathrynMurphy },
      },
      {
        name: ''Whitney Francis'',
        role: ''Content Specialist'',
        image: { src: imageWhitneyFrancis },
      },
      {
        name: ''Jeffrey Webb'',
        role: ''Account Coordinator'',
        image: { src: imageJeffreyWebb },
      },
      {
        name: ''Benjamin Russel'',
        role: ''Senior Developer'',
        image: { src: imageBenjaminRussel },
      },
      {
        name: ''Angela Fisher'',
        role: ''Front-end Developer'',
        image: { src: imageAngelaFisher },
      },
    ],
  },
]

function Team() {
  return (
    <Container className="mt-24 sm:mt-32 lg:mt-40">
      <div className="space-y-24">
        {team.map((group) => (
          <FadeInStagger key={group.title}>
            <Border as={FadeIn} />
            <div className="grid grid-cols-1 gap-6 pt-12 sm:pt-16 lg:grid-cols-4 xl:gap-8">
              <FadeIn>
                <h2 className="font-display text-2xl font-semibold text-neutral-950">
                  {group.title}
                </h2>
              </FadeIn>
              <div className="lg:col-span-3">
                <ul
                  role="list"
                  className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-8"
                >
                  {group.people.map((person) => (
                    <li key={person.name}>
                      <FadeIn>
                        <div className="group relative overflow-hidden rounded-3xl bg-neutral-100">
                          <Image
                            alt=""
                            {...person.image}
                            className="h-96 w-full object-cover grayscale transition duration-500 motion-safe:group-hover:scale-105"
                          />
                          <div className="absolute inset-0 flex flex-col justify-end bg-linear-to-t from-black to-black/0 to-40% p-6">
                            <p className="font-display text-base/6 font-semibold tracking-wide text-white">
                              {person.name}
                            </p>
                            <p className="mt-2 text-sm text-white">
                              {person.role}
                            </p>
                          </div>
                        </div>
                      </FadeIn>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </FadeInStagger>
        ))}
      </div>
    </Container>
  )
}

export const metadata: Metadata = {
  title: ''About Us'',
  description:
    ''We believe that our strength lies in our collaborative approach, which puts our clients at the center of everything we do.'',
}

export default async function About() {
  let blogArticles = (await loadArticles()).slice(0, 2)

  return (
    <RootLayout>
      <PageIntro eyebrow="About us" title="Our strength is collaboration">
        <p>
          We believe that our strength lies in our collaborative approach, which
          puts our clients at the center of everything we do.
        </p>
        <div className="mt-10 max-w-2xl space-y-6 text-base">
          <p>
            Studio was started by three friends who noticed that developer
            studios were charging clients double what an in-house team would
            cost. Since the beginning, we have been committed to doing things
            differently by charging triple instead.
          </p>
          <p>
            At Studio, we’re more than just colleagues — we’re a family. This
            means we pay very little and expect people to work late. We want our
            employees to bring their whole selves to work. In return, we just
            ask that they keep themselves there until at least 6:30pm.
          </p>
        </div>
      </PageIntro>
      <Container className="mt-16">
        <StatList>
          <StatListItem value="35" label="Underpaid employees" />
          <StatListItem value="52" label="Placated clients" />
          <StatListItem value="$25M" label="Invoices billed" />
        </StatList>
      </Container>

      <Culture />

      <Team />

      <PageLinks
        className="mt-24 sm:mt-32 lg:mt-40"
        title="From the blog"
        intro="Our team of experienced designers and developers has just one thing on their mind; working on your ideas to draw a smile on the face of your users worldwide. From conducting Brand Sprints to UX Design."
        pages={blogArticles}
      />

      <ContactSection />
    </RootLayout>
  )
}
',
    'team',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'team', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "team", "file_path": "tailwind-plus-studio/studio-ts/src/app/about/page.tsx", "uses_components": [], "dependencies": ["next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Blog - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Blog - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import Image from ''next/image''
import Link from ''next/link''

import { Border } from ''@/components/Border''
import { Button } from ''@/components/Button''
import { ContactSection } from ''@/components/ContactSection''
import { Container } from ''@/components/Container''
import { FadeIn } from ''@/components/FadeIn''
import { PageIntro } from ''@/components/PageIntro''
import { RootLayout } from ''@/components/RootLayout''
import { formatDate } from ''@/lib/formatDate''
import { loadArticles } from ''@/lib/mdx''

export const metadata: Metadata = {
  title: ''Blog'',
  description:
    ''Stay up-to-date with the latest industry news as our marketing teams finds new ways to re-purpose old CSS tricks articles.'',
}

export default async function Blog() {
  let articles = await loadArticles()

  return (
    <RootLayout>
      <PageIntro eyebrow="Blog" title="The latest articles and news">
        <p>
          Stay up-to-date with the latest industry news as our marketing teams
          finds new ways to re-purpose old CSS tricks articles.
        </p>
      </PageIntro>

      <Container className="mt-24 sm:mt-32 lg:mt-40">
        <div className="space-y-24 lg:space-y-32">
          {articles.map((article) => (
            <FadeIn key={article.href}>
              <article>
                <Border className="pt-16">
                  <div className="relative lg:-mx-4 lg:flex lg:justify-end">
                    <div className="pt-10 lg:w-2/3 lg:flex-none lg:px-4 lg:pt-0">
                      <h2 className="font-display text-2xl font-semibold text-neutral-950">
                        <Link href={article.href}>{article.title}</Link>
                      </h2>
                      <dl className="lg:absolute lg:top-0 lg:left-0 lg:w-1/3 lg:px-4">
                        <dt className="sr-only">Published</dt>
                        <dd className="absolute top-0 left-0 text-sm text-neutral-950 lg:static">
                          <time dateTime={article.date}>
                            {formatDate(article.date)}
                          </time>
                        </dd>
                        <dt className="sr-only">Author</dt>
                        <dd className="mt-6 flex gap-x-4">
                          <div className="flex-none overflow-hidden rounded-xl bg-neutral-100">
                            <Image
                              alt=""
                              {...article.author.image}
                              className="h-12 w-12 object-cover grayscale"
                            />
                          </div>
                          <div className="text-sm text-neutral-950">
                            <div className="font-semibold">
                              {article.author.name}
                            </div>
                            <div>{article.author.role}</div>
                          </div>
                        </dd>
                      </dl>
                      <p className="mt-6 max-w-2xl text-base text-neutral-600">
                        {article.description}
                      </p>
                      <Button
                        href={article.href}
                        aria-label={`Read more: ${article.title}`}
                        className="mt-8"
                      >
                        Read more
                      </Button>
                    </div>
                  </div>
                </Border>
              </article>
            </FadeIn>
          ))}
        </div>
      </Container>

      <ContactSection />
    </RootLayout>
  )
}
',
    'blog',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'studio', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "blog", "file_path": "tailwind-plus-studio/studio-ts/src/app/blog/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Blog - Wrapper - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Blog - Wrapper - Marketing',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { ContactSection } from ''@/components/ContactSection''
import { Container } from ''@/components/Container''
import { FadeIn } from ''@/components/FadeIn''
import { MDXComponents } from ''@/components/MDXComponents''
import { PageLinks } from ''@/components/PageLinks''
import { RootLayout } from ''@/components/RootLayout''
import { formatDate } from ''@/lib/formatDate''
import { type Article, type MDXEntry, loadArticles } from ''@/lib/mdx''

export default async function BlogArticleWrapper({
  article,
  children,
}: {
  article: MDXEntry<Article>
  children: React.ReactNode
}) {
  let allArticles = await loadArticles()
  let moreArticles = allArticles
    .filter(({ metadata }) => metadata !== article)
    .slice(0, 2)

  return (
    <RootLayout>
      <Container as="article" className="mt-24 sm:mt-32 lg:mt-40">
        <FadeIn>
          <header className="mx-auto flex max-w-5xl flex-col text-center">
            <h1 className="mt-6 font-display text-5xl font-medium tracking-tight text-balance text-neutral-950 sm:text-6xl">
              {article.title}
            </h1>
            <time
              dateTime={article.date}
              className="order-first text-sm text-neutral-950"
            >
              {formatDate(article.date)}
            </time>
            <p className="mt-6 text-sm font-semibold text-neutral-950">
              by {article.author.name}, {article.author.role}
            </p>
          </header>
        </FadeIn>

        <FadeIn>
          <MDXComponents.wrapper className="mt-24 sm:mt-32 lg:mt-40">
            {children}
          </MDXComponents.wrapper>
        </FadeIn>
      </Container>

      {moreArticles.length > 0 && (
        <PageLinks
          className="mt-24 sm:mt-32 lg:mt-40"
          title="More articles"
          pages={moreArticles}
        />
      )}

      <ContactSection />
    </RootLayout>
  )
}
',
    'blog',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "blog", "file_path": "tailwind-plus-studio/studio-ts/src/app/blog/wrapper.tsx", "uses_components": [], "dependencies": [], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Cta - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Cta - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { useId } from ''react''
import { type Metadata } from ''next''
import Link from ''next/link''

import { Border } from ''@/components/Border''
import { Button } from ''@/components/Button''
import { Container } from ''@/components/Container''
import { FadeIn } from ''@/components/FadeIn''
import { Offices } from ''@/components/Offices''
import { PageIntro } from ''@/components/PageIntro''
import { SocialMedia } from ''@/components/SocialMedia''
import { RootLayout } from ''@/components/RootLayout''

function TextInput({
  label,
  ...props
}: React.ComponentPropsWithoutRef<''input''> & { label: string }) {
  let id = useId()

  return (
    <div className="group relative z-0 transition-all focus-within:z-10">
      <input
        type="text"
        id={id}
        {...props}
        placeholder=" "
        className="peer block w-full border border-neutral-300 bg-transparent px-6 pt-12 pb-4 text-base/6 text-neutral-950 ring-4 ring-transparent transition group-first:rounded-t-2xl group-last:rounded-b-2xl focus:border-neutral-950 focus:ring-neutral-950/5 focus:outline-hidden"
      />
      <label
        htmlFor={id}
        className="pointer-events-none absolute top-1/2 left-6 -mt-3 origin-left text-base/6 text-neutral-500 transition-all duration-200 peer-not-placeholder-shown:-translate-y-4 peer-not-placeholder-shown:scale-75 peer-not-placeholder-shown:font-semibold peer-not-placeholder-shown:text-neutral-950 peer-focus:-translate-y-4 peer-focus:scale-75 peer-focus:font-semibold peer-focus:text-neutral-950"
      >
        {label}
      </label>
    </div>
  )
}

function RadioInput({
  label,
  ...props
}: React.ComponentPropsWithoutRef<''input''> & { label: string }) {
  return (
    <label className="flex gap-x-3">
      <input
        type="radio"
        {...props}
        className="h-6 w-6 flex-none appearance-none rounded-full border border-neutral-950/20 outline-hidden checked:border-[0.5rem] checked:border-neutral-950 focus-visible:ring-1 focus-visible:ring-neutral-950 focus-visible:ring-offset-2"
      />
      <span className="text-base/6 text-neutral-950">{label}</span>
    </label>
  )
}

function ContactForm() {
  return (
    <FadeIn className="lg:order-last">
      <form>
        <h2 className="font-display text-base font-semibold text-neutral-950">
          Work inquiries
        </h2>
        <div className="isolate mt-6 -space-y-px rounded-2xl bg-white/50">
          <TextInput label="Name" name="name" autoComplete="name" />
          <TextInput
            label="Email"
            type="email"
            name="email"
            autoComplete="email"
          />
          <TextInput
            label="Company"
            name="company"
            autoComplete="organization"
          />
          <TextInput label="Phone" type="tel" name="phone" autoComplete="tel" />
          <TextInput label="Message" name="message" />
          <div className="border border-neutral-300 px-6 py-8 first:rounded-t-2xl last:rounded-b-2xl">
            <fieldset>
              <legend className="text-base/6 text-neutral-500">Budget</legend>
              <div className="mt-6 grid grid-cols-1 gap-8 sm:grid-cols-2">
                <RadioInput label="$25K – $50K" name="budget" value="25" />
                <RadioInput label="$50K – $100K" name="budget" value="50" />
                <RadioInput label="$100K – $150K" name="budget" value="100" />
                <RadioInput label="More than $150K" name="budget" value="150" />
              </div>
            </fieldset>
          </div>
        </div>
        <Button type="submit" className="mt-10">
          Let’s work together
        </Button>
      </form>
    </FadeIn>
  )
}

function ContactDetails() {
  return (
    <FadeIn>
      <h2 className="font-display text-base font-semibold text-neutral-950">
        Our offices
      </h2>
      <p className="mt-6 text-base text-neutral-600">
        Prefer doing things in person? We don’t but we have to list our
        addresses here for legal reasons.
      </p>

      <Offices className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2" />

      <Border className="mt-16 pt-16">
        <h2 className="font-display text-base font-semibold text-neutral-950">
          Email us
        </h2>
        <dl className="mt-6 grid grid-cols-1 gap-8 text-sm sm:grid-cols-2">
          {[
            [''Careers'', ''careers@studioagency.com''],
            [''Press'', ''press@studioagency.com''],
          ].map(([label, email]) => (
            <div key={email}>
              <dt className="font-semibold text-neutral-950">{label}</dt>
              <dd>
                <Link
                  href={`mailto:${email}`}
                  className="text-neutral-600 hover:text-neutral-950"
                >
                  {email}
                </Link>
              </dd>
            </div>
          ))}
        </dl>
      </Border>

      <Border className="mt-16 pt-16">
        <h2 className="font-display text-base font-semibold text-neutral-950">
          Follow us
        </h2>
        <SocialMedia className="mt-6" />
      </Border>
    </FadeIn>
  )
}

export const metadata: Metadata = {
  title: ''Contact Us'',
  description: ''Let’s work together. We can’t wait to hear from you.'',
}

export default function Contact() {
  return (
    <RootLayout>
      <PageIntro eyebrow="Contact us" title="Let’s work together">
        <p>We can’t wait to hear from you.</p>
      </PageIntro>

      <Container className="mt-24 sm:mt-32 lg:mt-40">
        <div className="grid grid-cols-1 gap-x-8 gap-y-24 lg:grid-cols-2">
          <ContactForm />
          <ContactDetails />
        </div>
      </Container>
    </RootLayout>
  )
}
',
    'cta',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'cta', 'studio', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "cta", "file_path": "tailwind-plus-studio/studio-ts/src/app/contact/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Portfolio - - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Portfolio - - Marketing',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { type Metadata } from ''next''
import Image from ''next/image''
import Link from ''next/link''

import { Blockquote } from ''@/components/Blockquote''
import { Border } from ''@/components/Border''
import { Button } from ''@/components/Button''
import { ContactSection } from ''@/components/ContactSection''
import { Container } from ''@/components/Container''
import { FadeIn, FadeInStagger } from ''@/components/FadeIn''
import { PageIntro } from ''@/components/PageIntro''
import { Testimonial } from ''@/components/Testimonial''
import logoBrightPath from ''@/images/clients/bright-path/logo-dark.svg''
import logoFamilyFund from ''@/images/clients/family-fund/logo-dark.svg''
import logoGreenLife from ''@/images/clients/green-life/logo-dark.svg''
import logoHomeWork from ''@/images/clients/home-work/logo-dark.svg''
import logoMailSmirk from ''@/images/clients/mail-smirk/logo-dark.svg''
import logoNorthAdventures from ''@/images/clients/north-adventures/logo-dark.svg''
import logoPhobia from ''@/images/clients/phobia/logo-dark.svg''
import logoUnseal from ''@/images/clients/unseal/logo-dark.svg''
import { formatDate } from ''@/lib/formatDate''
import { type CaseStudy, type MDXEntry, loadCaseStudies } from ''@/lib/mdx''
import { RootLayout } from ''@/components/RootLayout''

function CaseStudies({
  caseStudies,
}: {
  caseStudies: Array<MDXEntry<CaseStudy>>
}) {
  return (
    <Container className="mt-40">
      <FadeIn>
        <h2 className="font-display text-2xl font-semibold text-neutral-950">
          Case studies
        </h2>
      </FadeIn>
      <div className="mt-10 space-y-20 sm:space-y-24 lg:space-y-32">
        {caseStudies.map((caseStudy) => (
          <FadeIn key={caseStudy.client}>
            <article>
              <Border className="grid grid-cols-3 gap-x-8 gap-y-8 pt-16">
                <div className="col-span-full sm:flex sm:items-center sm:justify-between sm:gap-x-8 lg:col-span-1 lg:block">
                  <div className="sm:flex sm:items-center sm:gap-x-6 lg:block">
                    <Image
                      src={caseStudy.logo}
                      alt=""
                      className="h-16 w-16 flex-none"
                      unoptimized
                    />
                    <h3 className="mt-6 text-sm font-semibold text-neutral-950 sm:mt-0 lg:mt-8">
                      {caseStudy.client}
                    </h3>
                  </div>
                  <div className="mt-1 flex gap-x-4 sm:mt-0 lg:block">
                    <p className="text-sm tracking-tight text-neutral-950 after:ml-4 after:font-semibold after:text-neutral-300 after:content-[''/''] lg:mt-2 lg:after:hidden">
                      {caseStudy.service}
                    </p>
                    <p className="text-sm text-neutral-950 lg:mt-2">
                      <time dateTime={caseStudy.date}>
                        {formatDate(caseStudy.date)}
                      </time>
                    </p>
                  </div>
                </div>
                <div className="col-span-full lg:col-span-2 lg:max-w-2xl">
                  <p className="font-display text-4xl font-medium text-neutral-950">
                    <Link href={caseStudy.href}>{caseStudy.title}</Link>
                  </p>
                  <div className="mt-6 space-y-6 text-base text-neutral-600">
                    {caseStudy.summary.map((paragraph) => (
                      <p key={paragraph}>{paragraph}</p>
                    ))}
                  </div>
                  <div className="mt-8 flex">
                    <Button
                      href={caseStudy.href}
                      aria-label={`Read case study: ${caseStudy.client}`}
                    >
                      Read case study
                    </Button>
                  </div>
                  {caseStudy.testimonial && (
                    <Blockquote
                      author={caseStudy.testimonial.author}
                      className="mt-12"
                    >
                      {caseStudy.testimonial.content}
                    </Blockquote>
                  )}
                </div>
              </Border>
            </article>
          </FadeIn>
        ))}
      </div>
    </Container>
  )
}

const clients = [
  [''Phobia'', logoPhobia],
  [''Family Fund'', logoFamilyFund],
  [''Unseal'', logoUnseal],
  [''Mail Smirk'', logoMailSmirk],
  [''Home Work'', logoHomeWork],
  [''Green Life'', logoGreenLife],
  [''Bright Path'', logoBrightPath],
  [''North Adventures'', logoNorthAdventures],
]

function Clients() {
  return (
    <Container className="mt-24 sm:mt-32 lg:mt-40">
      <FadeIn>
        <h2 className="font-display text-2xl font-semibold text-neutral-950">
          You’re in good company
        </h2>
      </FadeIn>
      <FadeInStagger className="mt-10" faster>
        <Border as={FadeIn} />
        <ul
          role="list"
          className="grid grid-cols-2 gap-x-8 gap-y-12 sm:grid-cols-3 lg:grid-cols-4"
        >
          {clients.map(([client, logo]) => (
            <li key={client} className="group">
              <FadeIn className="overflow-hidden">
                <Border className="pt-12 group-nth-[-n+2]:-mt-px sm:group-nth-3:-mt-px lg:group-nth-4:-mt-px">
                  <Image src={logo} alt={client} unoptimized />
                </Border>
              </FadeIn>
            </li>
          ))}
        </ul>
      </FadeInStagger>
    </Container>
  )
}

export const metadata: Metadata = {
  title: ''Our Work'',
  description:
    ''We believe in efficiency and maximizing our resources to provide the best value to our clients.'',
}

export default async function Work() {
  let caseStudies = await loadCaseStudies()

  return (
    <RootLayout>
      <PageIntro
        eyebrow="Our work"
        title="Proven solutions for real-world problems."
      >
        <p>
          We believe in efficiency and maximizing our resources to provide the
          best value to our clients. The primary way we do that is by re-using
          the same five projects we’ve been developing for the past decade.
        </p>
      </PageIntro>

      <CaseStudies caseStudies={caseStudies} />

      <Testimonial
        className="mt-24 sm:mt-32 lg:mt-40"
        client={{ name: ''Mail Smirk'', logo: logoMailSmirk }}
      >
        We approached <em>Studio</em> because we loved their past work. They
        delivered something remarkably similar in record time.
      </Testimonial>

      <Clients />

      <ContactSection />
    </RootLayout>
  )
}
',
    'portfolio',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'portfolio', 'studio', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "portfolio", "file_path": "tailwind-plus-studio/studio-ts/src/app/work/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Portfolio - Wrapper - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Portfolio - Wrapper - Marketing',
    'Marketing/Landing page component from Tailwind Plus Studio template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { ContactSection } from ''@/components/ContactSection''
import { Container } from ''@/components/Container''
import { FadeIn } from ''@/components/FadeIn''
import { GrayscaleTransitionImage } from ''@/components/GrayscaleTransitionImage''
import { MDXComponents } from ''@/components/MDXComponents''
import { PageIntro } from ''@/components/PageIntro''
import { PageLinks } from ''@/components/PageLinks''
import { RootLayout } from ''@/components/RootLayout''
import { type CaseStudy, type MDXEntry, loadCaseStudies } from ''@/lib/mdx''

export default async function CaseStudyLayout({
  caseStudy,
  children,
}: {
  caseStudy: MDXEntry<CaseStudy>
  children: React.ReactNode
}) {
  let allCaseStudies = await loadCaseStudies()
  let moreCaseStudies = allCaseStudies
    .filter(({ metadata }) => metadata !== caseStudy)
    .slice(0, 2)

  return (
    <RootLayout>
      <article className="mt-24 sm:mt-32 lg:mt-40">
        <header>
          <PageIntro eyebrow="Case Study" title={caseStudy.title} centered>
            <p>{caseStudy.description}</p>
          </PageIntro>

          <FadeIn>
            <div className="mt-24 border-t border-neutral-200 bg-white/50 sm:mt-32 lg:mt-40">
              <Container>
                <div className="mx-auto max-w-5xl">
                  <dl className="-mx-6 grid grid-cols-1 text-sm text-neutral-950 sm:mx-0 sm:grid-cols-3">
                    <div className="border-t border-neutral-200 px-6 py-4 first:border-t-0 sm:border-t-0 sm:border-l">
                      <dt className="font-semibold">Client</dt>
                      <dd>{caseStudy.client}</dd>
                    </div>
                    <div className="border-t border-neutral-200 px-6 py-4 first:border-t-0 sm:border-t-0 sm:border-l">
                      <dt className="font-semibold">Year</dt>
                      <dd>
                        <time dateTime={caseStudy.date.split(''-'')[0]}>
                          {caseStudy.date.split(''-'')[0]}
                        </time>
                      </dd>
                    </div>
                    <div className="border-t border-neutral-200 px-6 py-4 first:border-t-0 sm:border-t-0 sm:border-l">
                      <dt className="font-semibold">Service</dt>
                      <dd>{caseStudy.service}</dd>
                    </div>
                  </dl>
                </div>
              </Container>
            </div>

            <div className="border-y border-neutral-200 bg-neutral-100">
              <div className="mx-auto -my-px max-w-304 bg-neutral-200">
                <GrayscaleTransitionImage
                  {...caseStudy.image}
                  quality={90}
                  className="w-full"
                  sizes="(min-width: 1216px) 76rem, 100vw"
                  priority
                />
              </div>
            </div>
          </FadeIn>
        </header>

        <Container className="mt-24 sm:mt-32 lg:mt-40">
          <FadeIn>
            <MDXComponents.wrapper>{children}</MDXComponents.wrapper>
          </FadeIn>
        </Container>
      </article>

      {moreCaseStudies.length > 0 && (
        <PageLinks
          className="mt-24 sm:mt-32 lg:mt-40"
          title="More case studies"
          pages={moreCaseStudies}
        />
      )}

      <ContactSection />
    </RootLayout>
  )
}
',
    'portfolio',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'portfolio', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-studio", "component_type": "portfolio", "file_path": "tailwind-plus-studio/studio-ts/src/app/work/wrapper.tsx", "uses_components": [], "dependencies": [], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Syntax
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Syntax',
    'Marketing/Landing page component from Tailwind Plus Syntax template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { usePathname } from ''next/navigation''

import { navigation } from ''@/lib/navigation''

export function DocsHeader({ title }: { title?: string }) {
  let pathname = usePathname()
  let section = navigation.find((section) =>
    section.links.find((link) => link.href === pathname),
  )

  if (!title && !section) {
    return null
  }

  return (
    <header className="mb-9 space-y-1">
      {section && (
        <p className="font-display text-sm font-medium text-sky-500">
          {section.title}
        </p>
      )}
      {title && (
        <h1 className="font-display text-3xl tracking-tight text-slate-900 dark:text-white">
          {title}
        </h1>
      )}
    </header>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/navigation"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-syntax", "component_type": "hero", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/DocsHeader.tsx", "uses_components": [], "dependencies": ["next/navigation"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Syntax
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Syntax',
    'Marketing/Landing page component from Tailwind Plus Syntax template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { Fragment } from ''react''
import Image from ''next/image''
import clsx from ''clsx''
import { Highlight } from ''prism-react-renderer''

import { Button } from ''@/components/Button''
import { HeroBackground } from ''@/components/HeroBackground''
import blurCyanImage from ''@/images/blur-cyan.png''
import blurIndigoImage from ''@/images/blur-indigo.png''

const codeLanguage = ''javascript''
const code = `export default {
  strategy: ''predictive'',
  engine: {
    cpus: 12,
    backups: [''./storage/cache.wtf''],
  },
}`

const tabs = [
  { name: ''cache-advance.config.js'', isActive: true },
  { name: ''package.json'', isActive: false },
]

function TrafficLightsIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg aria-hidden="true" viewBox="0 0 42 10" fill="none" {...props}>
      <circle cx="5" cy="5" r="4.5" />
      <circle cx="21" cy="5" r="4.5" />
      <circle cx="37" cy="5" r="4.5" />
    </svg>
  )
}

export function Hero() {
  return (
    <div className="overflow-hidden bg-slate-900 dark:mt-[-4.75rem] dark:-mb-32 dark:pt-19 dark:pb-32">
      <div className="py-16 sm:px-2 lg:relative lg:px-0 lg:py-20">
        <div className="mx-auto grid max-w-2xl grid-cols-1 items-center gap-x-8 gap-y-16 px-4 lg:max-w-8xl lg:grid-cols-2 lg:px-8 xl:gap-x-16 xl:px-12">
          <div className="relative z-10 md:text-center lg:text-left">
            <Image
              className="absolute right-full bottom-full -mr-72 -mb-56 opacity-50"
              src={blurCyanImage}
              alt=""
              width={530}
              height={530}
              unoptimized
              priority
            />
            <div className="relative">
              <p className="inline bg-linear-to-r from-indigo-200 via-sky-400 to-indigo-200 bg-clip-text font-display text-5xl tracking-tight text-transparent">
                Never miss the cache again.
              </p>
              <p className="mt-3 text-2xl tracking-tight text-slate-400">
                Cache every single thing your app could ever do ahead of time,
                so your code never even has to run at all.
              </p>
              <div className="mt-8 flex gap-4 md:justify-center lg:justify-start">
                <Button href="/">Get started</Button>
                <Button href="/" variant="secondary">
                  View on GitHub
                </Button>
              </div>
            </div>
          </div>
          <div className="relative lg:static xl:pl-10">
            <div className="absolute inset-x-[-50vw] -top-32 -bottom-48 mask-[linear-gradient(transparent,white,white)] lg:-top-32 lg:right-0 lg:-bottom-32 lg:left-[calc(50%+14rem)] lg:mask-none dark:mask-[linear-gradient(transparent,white,transparent)] lg:dark:mask-[linear-gradient(white,white,transparent)]">
              <HeroBackground className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 lg:left-0 lg:translate-x-0 lg:translate-y-[-60%]" />
            </div>
            <div className="relative">
              <Image
                className="absolute -top-64 -right-64"
                src={blurCyanImage}
                alt=""
                width={530}
                height={530}
                unoptimized
                priority
              />
              <Image
                className="absolute -right-44 -bottom-40"
                src={blurIndigoImage}
                alt=""
                width={567}
                height={567}
                unoptimized
                priority
              />
              <div className="absolute inset-0 rounded-2xl bg-linear-to-tr from-sky-300 via-sky-300/70 to-blue-300 opacity-10 blur-lg" />
              <div className="absolute inset-0 rounded-2xl bg-linear-to-tr from-sky-300 via-sky-300/70 to-blue-300 opacity-10" />
              <div className="relative rounded-2xl bg-[#0A101F]/80 ring-1 ring-white/10 backdrop-blur-sm">
                <div className="absolute -top-px right-11 left-20 h-px bg-linear-to-r from-sky-300/0 via-sky-300/70 to-sky-300/0" />
                <div className="absolute right-20 -bottom-px left-11 h-px bg-linear-to-r from-blue-400/0 via-blue-400 to-blue-400/0" />
                <div className="pt-4 pl-4">
                  <TrafficLightsIcon className="h-2.5 w-auto stroke-slate-500/30" />
                  <div className="mt-4 flex space-x-2 text-xs">
                    {tabs.map((tab) => (
                      <div
                        key={tab.name}
                        className={clsx(
                          ''flex h-6 rounded-full'',
                          tab.isActive
                            ? ''bg-linear-to-r from-sky-400/30 via-sky-400 to-sky-400/30 p-px font-medium text-sky-300''
                            : ''text-slate-500'',
                        )}
                      >
                        <div
                          className={clsx(
                            ''flex items-center rounded-full px-2.5'',
                            tab.isActive && ''bg-slate-800'',
                          )}
                        >
                          {tab.name}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-6 flex items-start px-1 text-sm">
                    <div
                      aria-hidden="true"
                      className="border-r border-slate-300/5 pr-4 font-mono text-slate-600 select-none"
                    >
                      {Array.from({
                        length: code.split(''\n'').length,
                      }).map((_, index) => (
                        <Fragment key={index}>
                          {(index + 1).toString().padStart(2, ''0'')}
                          <br />
                        </Fragment>
                      ))}
                    </div>
                    <Highlight
                      code={code}
                      language={codeLanguage}
                      theme={{ plain: {}, styles: [] }}
                    >
                      {({
                        className,
                        style,
                        tokens,
                        getLineProps,
                        getTokenProps,
                      }) => (
                        <pre
                          className={clsx(
                            className,
                            ''flex overflow-x-auto pb-6'',
                          )}
                          style={style}
                        >
                          <code className="px-4">
                            {tokens.map((line, lineIndex) => (
                              <div key={lineIndex} {...getLineProps({ line })}>
                                {line.map((token, tokenIndex) => (
                                  <span
                                    key={tokenIndex}
                                    {...getTokenProps({ token })}
                                  />
                                ))}
                              </div>
                            ))}
                          </code>
                        </pre>
                      )}
                    </Highlight>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["prism-react-renderer", "clsx", "next/image"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-syntax", "component_type": "hero", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": ["prism-react-renderer", "clsx", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Marketing Hero - Syntax
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Marketing Hero - Syntax',
    'Marketing/Landing page component from Tailwind Plus Syntax template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { useId } from ''react''

export function HeroBackground(props: React.ComponentPropsWithoutRef<''svg''>) {
  let id = useId()

  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 668 1069"
      width={668}
      height={1069}
      fill="none"
      {...props}
    >
      <defs>
        <clipPath id={`${id}-clip-path`}>
          <path
            fill="#fff"
            transform="rotate(-180 334 534.4)"
            d="M0 0h668v1068.8H0z"
          />
        </clipPath>
      </defs>
      <g opacity=".4" clipPath={`url(#${id}-clip-path)`} strokeWidth={4}>
        <path
          opacity=".3"
          d="M584.5 770.4v-474M484.5 770.4v-474M384.5 770.4v-474M283.5 769.4v-474M183.5 768.4v-474M83.5 767.4v-474"
          stroke="#334155"
        />
        <path
          d="M83.5 221.275v6.587a50.1 50.1 0 0 0 22.309 41.686l55.581 37.054a50.102 50.102 0 0 1 22.309 41.686v6.587M83.5 716.012v6.588a50.099 50.099 0 0 0 22.309 41.685l55.581 37.054a50.102 50.102 0 0 1 22.309 41.686v6.587M183.7 584.5v6.587a50.1 50.1 0 0 0 22.31 41.686l55.581 37.054a50.097 50.097 0 0 1 22.309 41.685v6.588M384.101 277.637v6.588a50.1 50.1 0 0 0 22.309 41.685l55.581 37.054a50.1 50.1 0 0 1 22.31 41.686v6.587M384.1 770.288v6.587a50.1 50.1 0 0 1-22.309 41.686l-55.581 37.054A50.099 50.099 0 0 0 283.9 897.3v6.588"
          stroke="#334155"
        />
        <path
          d="M384.1 770.288v6.587a50.1 50.1 0 0 1-22.309 41.686l-55.581 37.054A50.099 50.099 0 0 0 283.9 897.3v6.588M484.3 594.937v6.587a50.1 50.1 0 0 1-22.31 41.686l-55.581 37.054A50.1 50.1 0 0 0 384.1 721.95v6.587M484.3 872.575v6.587a50.1 50.1 0 0 1-22.31 41.686l-55.581 37.054a50.098 50.098 0 0 0-22.309 41.686v6.582M584.501 663.824v39.988a50.099 50.099 0 0 1-22.31 41.685l-55.581 37.054a50.102 50.102 0 0 0-22.309 41.686v6.587M283.899 945.637v6.588a50.1 50.1 0 0 1-22.309 41.685l-55.581 37.05a50.12 50.12 0 0 0-22.31 41.69v6.59M384.1 277.637c0 19.946 12.763 37.655 31.686 43.962l137.028 45.676c18.923 6.308 31.686 24.016 31.686 43.962M183.7 463.425v30.69c0 21.564 13.799 40.709 34.257 47.529l134.457 44.819c18.922 6.307 31.686 24.016 31.686 43.962M83.5 102.288c0 19.515 13.554 36.412 32.604 40.645l235.391 52.309c19.05 4.234 32.605 21.13 32.605 40.646M83.5 463.425v-58.45M183.699 542.75V396.625M283.9 1068.8V945.637M83.5 363.225v-141.95M83.5 179.524v-77.237M83.5 60.537V0M384.1 630.425V277.637M484.301 830.824V594.937M584.5 1068.8V663.825M484.301 555.275V452.988M584.5 622.075V452.988M384.1 728.537v-56.362M384.1 1068.8v-20.88M384.1 1006.17V770.287M283.9 903.888V759.85M183.699 1066.71V891.362M83.5 1068.8V716.012M83.5 674.263V505.175"
          stroke="#334155"
        />
        <circle
          cx="83.5"
          cy="384.1"
          r="10.438"
          transform="rotate(-180 83.5 384.1)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="83.5"
          cy="200.399"
          r="10.438"
          transform="rotate(-180 83.5 200.399)"
          stroke="#334155"
        />
        <circle
          cx="83.5"
          cy="81.412"
          r="10.438"
          transform="rotate(-180 83.5 81.412)"
          stroke="#334155"
        />
        <circle
          cx="183.699"
          cy="375.75"
          r="10.438"
          transform="rotate(-180 183.699 375.75)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="183.699"
          cy="563.625"
          r="10.438"
          transform="rotate(-180 183.699 563.625)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="384.1"
          cy="651.3"
          r="10.438"
          transform="rotate(-180 384.1 651.3)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="484.301"
          cy="574.062"
          r="10.438"
          transform="rotate(-180 484.301 574.062)"
          fill="#0EA5E9"
          fillOpacity=".42"
          stroke="#0EA5E9"
        />
        <circle
          cx="384.1"
          cy="749.412"
          r="10.438"
          transform="rotate(-180 384.1 749.412)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="384.1"
          cy="1027.05"
          r="10.438"
          transform="rotate(-180 384.1 1027.05)"
          stroke="#334155"
        />
        <circle
          cx="283.9"
          cy="924.763"
          r="10.438"
          transform="rotate(-180 283.9 924.763)"
          stroke="#334155"
        />
        <circle
          cx="183.699"
          cy="870.487"
          r="10.438"
          transform="rotate(-180 183.699 870.487)"
          stroke="#334155"
        />
        <circle
          cx="283.9"
          cy="738.975"
          r="10.438"
          transform="rotate(-180 283.9 738.975)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="83.5"
          cy="695.138"
          r="10.438"
          transform="rotate(-180 83.5 695.138)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="83.5"
          cy="484.3"
          r="10.438"
          transform="rotate(-180 83.5 484.3)"
          fill="#0EA5E9"
          fillOpacity=".42"
          stroke="#0EA5E9"
        />
        <circle
          cx="484.301"
          cy="432.112"
          r="10.438"
          transform="rotate(-180 484.301 432.112)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="584.5"
          cy="432.112"
          r="10.438"
          transform="rotate(-180 584.5 432.112)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="584.5"
          cy="642.95"
          r="10.438"
          transform="rotate(-180 584.5 642.95)"
          fill="#1E293B"
          stroke="#334155"
        />
        <circle
          cx="484.301"
          cy="851.699"
          r="10.438"
          transform="rotate(-180 484.301 851.699)"
          stroke="#334155"
        />
        <circle
          cx="384.1"
          cy="256.763"
          r="10.438"
          transform="rotate(-180 384.1 256.763)"
          stroke="#334155"
        />
      </g>
    </svg>
  )
}
',
    'hero',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-syntax", "component_type": "hero", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/HeroBackground.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Mobilenavigation - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Mobilenavigation - Marketing',
    'Marketing/Landing page component from Tailwind Plus Syntax template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { Suspense, useCallback, useEffect, useState } from ''react''
import Link from ''next/link''
import { usePathname, useSearchParams } from ''next/navigation''
import { Dialog, DialogPanel } from ''@headlessui/react''

import { Logomark } from ''@/components/Logo''
import { Navigation } from ''@/components/Navigation''

function MenuIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth="2"
      strokeLinecap="round"
      {...props}
    >
      <path d="M4 7h16M4 12h16M4 17h16" />
    </svg>
  )
}

function CloseIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      fill="none"
      strokeWidth="2"
      strokeLinecap="round"
      {...props}
    >
      <path d="M5 5l14 14M19 5l-14 14" />
    </svg>
  )
}

function CloseOnNavigation({ close }: { close: () => void }) {
  let pathname = usePathname()
  let searchParams = useSearchParams()

  useEffect(() => {
    close()
  }, [pathname, searchParams, close])

  return null
}

export function MobileNavigation() {
  let [isOpen, setIsOpen] = useState(false)
  let close = useCallback(() => setIsOpen(false), [setIsOpen])

  function onLinkClick(event: React.MouseEvent<HTMLAnchorElement>) {
    let link = event.currentTarget
    if (
      link.pathname + link.search + link.hash ===
      window.location.pathname + window.location.search + window.location.hash
    ) {
      close()
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setIsOpen(true)}
        className="relative"
        aria-label="Open navigation"
      >
        <MenuIcon className="h-6 w-6 stroke-slate-500" />
      </button>
      <Suspense fallback={null}>
        <CloseOnNavigation close={close} />
      </Suspense>
      <Dialog
        open={isOpen}
        onClose={() => close()}
        className="fixed inset-0 z-50 flex items-start overflow-y-auto bg-slate-900/50 pr-10 backdrop-blur-sm lg:hidden"
        aria-label="Navigation"
      >
        <DialogPanel className="min-h-full w-full max-w-xs bg-white px-4 pt-5 pb-12 sm:px-6 dark:bg-slate-900">
          <div className="flex items-center">
            <button
              type="button"
              onClick={() => close()}
              aria-label="Close navigation"
            >
              <CloseIcon className="h-6 w-6 stroke-slate-500" />
            </button>
            <Link href="/" className="ml-6" aria-label="Home page">
              <Logomark className="h-9 w-9" />
            </Link>
          </div>
          <Navigation className="mt-5 px-1" onLinkClick={onLinkClick} />
        </DialogPanel>
      </Dialog>
    </>
  )
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["next/link", "next/navigation", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-syntax", "component_type": "navigation", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/MobileNavigation.tsx", "uses_components": ["Dialog"], "dependencies": ["next/link", "next/navigation", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Site Navigation - Syntax
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Site Navigation - Syntax',
    'Marketing/Landing page component from Tailwind Plus Syntax template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import Link from ''next/link''
import { usePathname } from ''next/navigation''
import clsx from ''clsx''

import { navigation } from ''@/lib/navigation''

export function Navigation({
  className,
  onLinkClick,
}: {
  className?: string
  onLinkClick?: React.MouseEventHandler<HTMLAnchorElement>
}) {
  let pathname = usePathname()

  return (
    <nav className={clsx(''text-base lg:text-sm'', className)}>
      <ul role="list" className="space-y-9">
        {navigation.map((section) => (
          <li key={section.title}>
            <h2 className="font-display font-medium text-slate-900 dark:text-white">
              {section.title}
            </h2>
            <ul
              role="list"
              className="mt-2 space-y-2 border-l-2 border-slate-100 lg:mt-4 lg:space-y-4 lg:border-slate-200 dark:border-slate-800"
            >
              {section.links.map((link) => (
                <li key={link.href} className="relative">
                  <Link
                    href={link.href}
                    onClick={onLinkClick}
                    className={clsx(
                      ''block w-full pl-3.5 before:pointer-events-none before:absolute before:top-1/2 before:-left-1 before:h-1.5 before:w-1.5 before:-translate-y-1/2 before:rounded-full'',
                      link.href === pathname
                        ? ''font-semibold text-sky-500 before:bg-sky-500''
                        : ''text-slate-500 before:hidden before:bg-slate-300 hover:text-slate-600 hover:before:block dark:text-slate-400 dark:before:bg-slate-700 dark:hover:text-slate-300'',
                    )}
                  >
                    {link.title}
                  </Link>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </nav>
  )
}
',
    'navigation',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "next/navigation", "clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-syntax", "component_type": "navigation", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/Navigation.tsx", "uses_components": [], "dependencies": ["next/link", "next/navigation", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Forms - Search - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Forms - Search - Marketing',
    'Marketing/Landing page component from Tailwind Plus Syntax template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import {
  forwardRef,
  Fragment,
  Suspense,
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
} from ''react''
import Highlighter from ''react-highlight-words''
import { usePathname, useRouter, useSearchParams } from ''next/navigation''
import {
  type AutocompleteApi,
  type AutocompleteCollection,
  type AutocompleteState,
  createAutocomplete,
} from ''@algolia/autocomplete-core''
import { Dialog, DialogPanel } from ''@headlessui/react''
import clsx from ''clsx''

import { navigation } from ''@/lib/navigation''
import { type Result } from ''@/markdoc/search.mjs''

type EmptyObject = Record<string, never>

type Autocomplete = AutocompleteApi<
  Result,
  React.SyntheticEvent,
  React.MouseEvent,
  React.KeyboardEvent
>

function SearchIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  return (
    <svg aria-hidden="true" viewBox="0 0 20 20" {...props}>
      <path d="M16.293 17.707a1 1 0 0 0 1.414-1.414l-1.414 1.414ZM9 14a5 5 0 0 1-5-5H2a7 7 0 0 0 7 7v-2ZM4 9a5 5 0 0 1 5-5V2a7 7 0 0 0-7 7h2Zm5-5a5 5 0 0 1 5 5h2a7 7 0 0 0-7-7v2Zm8.707 12.293-3.757-3.757-1.414 1.414 3.757 3.757 1.414-1.414ZM14 9a4.98 4.98 0 0 1-1.464 3.536l1.414 1.414A6.98 6.98 0 0 0 16 9h-2Zm-1.464 3.536A4.98 4.98 0 0 1 9 14v2a6.98 6.98 0 0 0 4.95-2.05l-1.414-1.414Z" />
    </svg>
  )
}

function useAutocomplete({
  close,
}: {
  close: (autocomplete: Autocomplete) => void
}) {
  let id = useId()
  let router = useRouter()
  let [autocompleteState, setAutocompleteState] = useState<
    AutocompleteState<Result> | EmptyObject
  >({})

  function navigate({ itemUrl }: { itemUrl?: string }) {
    if (!itemUrl) {
      return
    }

    router.push(itemUrl)

    if (
      itemUrl ===
      window.location.pathname + window.location.search + window.location.hash
    ) {
      close(autocomplete)
    }
  }

  let [autocomplete] = useState<Autocomplete>(() =>
    createAutocomplete<
      Result,
      React.SyntheticEvent,
      React.MouseEvent,
      React.KeyboardEvent
    >({
      id,
      placeholder: ''Find something...'',
      defaultActiveItemId: 0,
      onStateChange({ state }) {
        setAutocompleteState(state)
      },
      shouldPanelOpen({ state }) {
        return state.query !== ''''
      },
      navigator: {
        navigate,
      },
      getSources({ query }) {
        return import(''@/markdoc/search.mjs'').then(({ search }) => {
          return [
            {
              sourceId: ''documentation'',
              getItems() {
                return search(query, { limit: 5 })
              },
              getItemUrl({ item }) {
                return item.url
              },
              onSelect: navigate,
            },
          ]
        })
      },
    }),
  )

  return { autocomplete, autocompleteState }
}

function LoadingIcon(props: React.ComponentPropsWithoutRef<''svg''>) {
  let id = useId()

  return (
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" {...props}>
      <circle cx="10" cy="10" r="5.5" strokeLinejoin="round" />
      <path
        stroke={`url(#${id})`}
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15.5 10a5.5 5.5 0 1 0-5.5 5.5"
      />
      <defs>
        <linearGradient
          id={id}
          x1="13"
          x2="9.5"
          y1="9"
          y2="15"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="currentColor" />
          <stop offset="1" stopColor="currentColor" stopOpacity="0" />
        </linearGradient>
      </defs>
    </svg>
  )
}

function HighlightQuery({ text, query }: { text: string; query: string }) {
  return (
    <Highlighter
      highlightClassName="group-aria-selected:underline bg-transparent text-sky-600 dark:text-sky-400"
      searchWords={[query]}
      autoEscape={true}
      textToHighlight={text}
    />
  )
}

function SearchResult({
  result,
  autocomplete,
  collection,
  query,
}: {
  result: Result
  autocomplete: Autocomplete
  collection: AutocompleteCollection<Result>
  query: string
}) {
  let id = useId()

  let sectionTitle = navigation.find((section) =>
    section.links.find((link) => link.href === result.url.split(''#'')[0]),
  )?.title
  let hierarchy = [sectionTitle, result.pageTitle].filter(
    (x): x is string => typeof x === ''string'',
  )

  return (
    <li
      className="group block cursor-default rounded-lg px-3 py-2 aria-selected:bg-slate-100 dark:aria-selected:bg-slate-700/30"
      aria-labelledby={`${id}-hierarchy ${id}-title`}
      {...autocomplete.getItemProps({
        item: result,
        source: collection.source,
      })}
    >
      <div
        id={`${id}-title`}
        aria-hidden="true"
        className="text-sm text-slate-700 group-aria-selected:text-sky-600 dark:text-slate-300 dark:group-aria-selected:text-sky-400"
      >
        <HighlightQuery text={result.title} query={query} />
      </div>
      {hierarchy.length > 0 && (
        <div
          id={`${id}-hierarchy`}
          aria-hidden="true"
          className="mt-0.5 truncate text-xs whitespace-nowrap text-slate-500 dark:text-slate-400"
        >
          {hierarchy.map((item, itemIndex, items) => (
            <Fragment key={itemIndex}>
              <HighlightQuery text={item} query={query} />
              <span
                className={
                  itemIndex === items.length - 1
                    ? ''sr-only''
                    : ''mx-2 text-slate-300 dark:text-slate-700''
                }
              >
                /
              </span>
            </Fragment>
          ))}
        </div>
      )}
    </li>
  )
}

function SearchResults({
  autocomplete,
  query,
  collection,
}: {
  autocomplete: Autocomplete
  query: string
  collection: AutocompleteCollection<Result>
}) {
  if (collection.items.length === 0) {
    return (
      <p className="px-4 py-8 text-center text-sm text-slate-700 dark:text-slate-400">
        No results for &ldquo;
        <span className="break-words text-slate-900 dark:text-white">
          {query}
        </span>
        &rdquo;
      </p>
    )
  }

  return (
    <ul {...autocomplete.getListProps()}>
      {collection.items.map((result) => (
        <SearchResult
          key={result.url}
          result={result}
          autocomplete={autocomplete}
          collection={collection}
          query={query}
        />
      ))}
    </ul>
  )
}

const SearchInput = forwardRef<
  React.ElementRef<''input''>,
  {
    autocomplete: Autocomplete
    autocompleteState: AutocompleteState<Result> | EmptyObject
    onClose: () => void
  }
>(function SearchInput({ autocomplete, autocompleteState, onClose }, inputRef) {
  let inputProps = autocomplete.getInputProps({ inputElement: null })

  return (
    <div className="group relative flex h-12">
      <SearchIcon className="pointer-events-none absolute top-0 left-4 h-full w-5 fill-slate-400 dark:fill-slate-500" />
      <input
        ref={inputRef}
        data-autofocus
        className={clsx(
          ''flex-auto appearance-none bg-transparent pl-12 text-slate-900 outline-hidden placeholder:text-slate-400 focus:w-full focus:flex-none sm:text-sm dark:text-white [&::-webkit-search-cancel-button]:hidden [&::-webkit-search-decoration]:hidden [&::-webkit-search-results-button]:hidden [&::-webkit-search-results-decoration]:hidden'',
          autocompleteState.status === ''stalled'' ? ''pr-11'' : ''pr-4'',
        )}
        {...inputProps}
        onKeyDown={(event) => {
          if (
            event.key === ''Escape'' &&
            !autocompleteState.isOpen &&
            autocompleteState.query === ''''
          ) {
            // In Safari, closing the dialog with the escape key can sometimes cause the scroll position to jump to the
            // bottom of the page. This is a workaround for that until we can figure out a proper fix in Headless UI.
            if (document.activeElement instanceof HTMLElement) {
              document.activeElement.blur()
            }

            onClose()
          } else {
            inputProps.onKeyDown(event)
          }
        }}
      />
      {autocompleteState.status === ''stalled'' && (
        <div className="absolute inset-y-0 right-3 flex items-center">
          <LoadingIcon className="h-6 w-6 animate-spin stroke-slate-200 text-slate-400 dark:stroke-slate-700 dark:text-slate-500" />
        </div>
      )}
    </div>
  )
})

function CloseOnNavigation({
  close,
  autocomplete,
}: {
  close: (autocomplete: Autocomplete) => void
  autocomplete: Autocomplete
}) {
  let pathname = usePathname()
  let searchParams = useSearchParams()

  useEffect(() => {
    close(autocomplete)
  }, [pathname, searchParams, close, autocomplete])

  return null
}

function SearchDialog({
  open,
  setOpen,
  className,
}: {
  open: boolean
  setOpen: (open: boolean) => void
  className?: string
}) {
  let formRef = useRef<React.ElementRef<''form''>>(null)
  let panelRef = useRef<React.ElementRef<''div''>>(null)
  let inputRef = useRef<React.ElementRef<typeof SearchInput>>(null)

  let close = useCallback(
    (autocomplete: Autocomplete) => {
      setOpen(false)
      autocomplete.setQuery('''')
    },
    [setOpen],
  )

  let { autocomplete, autocompleteState } = useAutocomplete({
    close() {
      close(autocomplete)
    },
  })

  useEffect(() => {
    if (open) {
      return
    }

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === ''k'' && (event.metaKey || event.ctrlKey)) {
        event.preventDefault()
        setOpen(true)
      }
    }

    window.addEventListener(''keydown'', onKeyDown)

    return () => {
      window.removeEventListener(''keydown'', onKeyDown)
    }
  }, [open, setOpen])

  return (
    <>
      <Suspense fallback={null}>
        <CloseOnNavigation close={close} autocomplete={autocomplete} />
      </Suspense>
      <Dialog
        open={open}
        onClose={() => close(autocomplete)}
        className={clsx(''fixed inset-0 z-50'', className)}
      >
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm" />

        <div className="fixed inset-0 overflow-y-auto px-4 py-4 sm:px-6 sm:py-20 md:py-32 lg:px-8 lg:py-[15vh]">
          <DialogPanel className="mx-auto transform-gpu overflow-hidden rounded-xl bg-white shadow-xl sm:max-w-xl dark:bg-slate-800 dark:ring-1 dark:ring-slate-700">
            <div {...autocomplete.getRootProps({})}>
              <form
                ref={formRef}
                {...autocomplete.getFormProps({
                  inputElement: inputRef.current,
                })}
              >
                <SearchInput
                  ref={inputRef}
                  autocomplete={autocomplete}
                  autocompleteState={autocompleteState}
                  onClose={() => setOpen(false)}
                />
                <div
                  ref={panelRef}
                  className="border-t border-slate-200 bg-white px-2 py-3 empty:hidden dark:border-slate-400/10 dark:bg-slate-800"
                  {...autocomplete.getPanelProps({})}
                >
                  {autocompleteState.isOpen && (
                    <SearchResults
                      autocomplete={autocomplete}
                      query={autocompleteState.query}
                      collection={autocompleteState.collections[0]}
                    />
                  )}
                </div>
              </form>
            </div>
          </DialogPanel>
        </div>
      </Dialog>
    </>
  )
}

function useSearchProps() {
  let buttonRef = useRef<React.ElementRef<''button''>>(null)
  let [open, setOpen] = useState(false)

  return {
    buttonProps: {
      ref: buttonRef,
      onClick() {
        setOpen(true)
      },
    },
    dialogProps: {
      open,
      setOpen: useCallback((open: boolean) => {
        let { width = 0, height = 0 } =
          buttonRef.current?.getBoundingClientRect() ?? {}
        if (!open || (width !== 0 && height !== 0)) {
          setOpen(open)
        }
      }, []),
    },
  }
}

export function Search() {
  let [modifierKey, setModifierKey] = useState<string>()
  let { buttonProps, dialogProps } = useSearchProps()

  useEffect(() => {
    setModifierKey(
      /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform) ? ''⌘'' : ''Ctrl '',
    )
  }, [])

  return (
    <>
      <button
        type="button"
        className="group flex h-6 w-6 items-center justify-center sm:justify-start md:h-auto md:w-80 md:flex-none md:rounded-lg md:py-2.5 md:pr-3.5 md:pl-4 md:text-sm md:ring-1 md:ring-slate-200 md:hover:ring-slate-300 lg:w-96 dark:md:bg-slate-800/75 dark:md:ring-white/5 dark:md:ring-inset dark:md:hover:bg-slate-700/40 dark:md:hover:ring-slate-500"
        {...buttonProps}
      >
        <SearchIcon className="h-5 w-5 flex-none fill-slate-400 group-hover:fill-slate-500 md:group-hover:fill-slate-400 dark:fill-slate-500" />
        <span className="sr-only md:not-sr-only md:ml-2 md:text-slate-500 md:dark:text-slate-400">
          Search docs
        </span>
        {modifierKey && (
          <kbd className="ml-auto hidden font-medium text-slate-400 md:block dark:text-slate-500">
            <kbd className="font-sans">{modifierKey}</kbd>
            <kbd className="font-sans">K</kbd>
          </kbd>
        )}
      </button>
      <SearchDialog {...dialogProps} />
    </>
  )
}
',
    'forms',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["clsx", "next/navigation", "react-highlight-words", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-syntax", "component_type": "forms", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/Search.tsx", "uses_components": ["Dialog"], "dependencies": ["clsx", "next/navigation", "react-highlight-words", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Team - Aboutsection - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Team - Aboutsection - Marketing',
    'Marketing/Landing page component from Tailwind Plus Transmit template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    '''use client''

import { useState } from ''react''
import clsx from ''clsx''

import { TinyWaveFormIcon } from ''@/components/TinyWaveFormIcon''

export function AboutSection(props: React.ComponentPropsWithoutRef<''section''>) {
  let [isExpanded, setIsExpanded] = useState(false)

  return (
    <section {...props}>
      <h2 className="flex items-center font-mono text-sm/7 font-medium text-slate-900">
        <TinyWaveFormIcon
          colors={[''fill-violet-300'', ''fill-pink-300'']}
          className="h-2.5 w-2.5"
        />
        <span className="ml-2.5">About</span>
      </h2>
      <p
        className={clsx(
          ''mt-2 text-base/7 text-slate-700'',
          !isExpanded && ''lg:line-clamp-4'',
        )}
      >
        In this show, Eric and Wes dig deep to get to the facts with guests who
        have been labeled villains by a society quick to judge, without actually
        getting the full story. Tune in every Thursday to get to the truth with
        another misunderstood outcast as they share the missing context in their
        tragic tale.
      </p>
      {!isExpanded && (
        <button
          type="button"
          className="mt-2 hidden text-sm/6 font-bold text-pink-500 hover:text-pink-700 active:text-pink-900 lg:inline-block"
          onClick={() => setIsExpanded(true)}
        >
          Show more
        </button>
      )}
    </section>
  )
}
',
    'team',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'team', 'transmit', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx"]}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-transmit", "component_type": "team", "file_path": "tailwind-plus-transmit/transmit-ts/src/components/AboutSection.tsx", "uses_components": [], "dependencies": ["clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

-- Forms - Waveform - Marketing
INSERT INTO sections (
    name,
    description,
    category,
    source,
    react_template,
    block_type,
    app_type,
    is_template,
    published,
    tags,
    dependencies,
    props_schema,
    example_props,
    project_id
) VALUES (
    'Forms - Waveform - Marketing',
    'Marketing/Landing page component from Tailwind Plus Transmit template. FOR MARKETING SITES ONLY - not for application UIs. Section extracted from Tailwind_Templates template',
    'marketing-landing',
    'tailwind-plus-marketing',
    'import { useId } from ''react''

function randomBetween(min: number, max: number, seed = 1) {
  return () => {
    let rand = Math.sin(seed++) * 10000
    rand = rand - Math.floor(rand)
    return Math.floor(rand * (max - min + 1) + min)
  }
}

export function Waveform(props: React.ComponentPropsWithoutRef<''svg''>) {
  let id = useId()
  let bars = {
    total: 100,
    width: 2,
    gap: 2,
    minHeight: 40,
    maxHeight: 100,
  }

  let barHeights = Array.from(
    { length: bars.total },
    randomBetween(bars.minHeight, bars.maxHeight),
  )

  return (
    <svg aria-hidden="true" {...props}>
      <defs>
        <linearGradient id={`${id}-fade`} x1="0" x2="0" y1="0" y2="1">
          <stop offset="40%" stopColor="white" />
          <stop offset="100%" stopColor="black" />
        </linearGradient>
        <linearGradient id={`${id}-gradient`}>
          <stop offset="0%" stopColor="#4989E8" />
          <stop offset="50%" stopColor="#6159DA" />
          <stop offset="100%" stopColor="#FF54AD" />
        </linearGradient>
        <mask id={`${id}-mask`}>
          <rect width="100%" height="100%" fill={`url(#${id}-pattern)`} />
        </mask>
        <pattern
          id={`${id}-pattern`}
          width={bars.total * bars.width + bars.total * bars.gap}
          height="100%"
          patternUnits="userSpaceOnUse"
        >
          {Array.from({ length: bars.total }, (_, index) => (
            <rect
              key={index}
              width={bars.width}
              height={`${barHeights[index]}%`}
              x={bars.gap * (index + 1) + bars.width * index}
              fill={`url(#${id}-fade)`}
            />
          ))}
        </pattern>
      </defs>
      <rect
        width="100%"
        height="100%"
        fill={`url(#${id}-gradient)`}
        mask={`url(#${id}-mask)`}
        opacity="0.25"
      />
    </svg>
  )
}
',
    'forms',  -- block_type
    'marketing-site',  -- app_type - clearly marking as marketing
    True,
    True,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'transmit', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,  -- props_schema
    '{"template_name": "tailwind-plus-transmit", "component_type": "forms", "file_path": "tailwind-plus-transmit/transmit-ts/src/components/Waveform.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,  -- example_props (using metadata)
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
) ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
