-- Marketing Sections Batch 1
-- 10 sections in this batch


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
    'forms',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'commit', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-commit", "component_type": "forms", "file_path": "tailwind-plus-commit/commit-ts/src/components/SignUpForm.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
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
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
}

function SiteNavigation() {
  let [mobileMenuOpen, setMobileMenuOpen] = useState(false)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

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
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
}
',
    'navigation',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'compass', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["next/link", "clsx"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-compass", "component_type": "navigation", "file_path": "tailwind-plus-compass/compass-ts/src/components/navbar.tsx", "uses_components": ["Dialog"], "dependencies": ["next/link", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
}
',
    'auth',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'compass', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-compass", "component_type": "auth", "file_path": "tailwind-plus-compass/compass-ts/src/app/(auth)/layout.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
}
',
    'auth',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'compass', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-compass", "component_type": "auth", "file_path": "tailwind-plus-compass/compass-ts/src/app/(auth)/otp/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
}

export function BreadcrumbHome() {
  return (
    <Link href="/" className="min-w-0 shrink-0 text-gray-950 dark:text-white">
      Compass
    </Link>
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
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
    )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
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
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
}

export function BreadcrumbSeparator({ className }: { className?: string }) {
  return (
    <span className={clsx(className, "text-gray-950/25 dark:text-white/25")}>
      /
    </span>
  )
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();
}
',
    'navigation',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'compass', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "clsx"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-compass", "component_type": "navigation", "file_path": "tailwind-plus-compass/compass-ts/src/components/breadcrumbs.tsx", "uses_components": [], "dependencies": ["next/link", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
    'footer',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-keynote", "component_type": "footer", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-keynote", "component_type": "hero", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-keynote", "component_type": "hero", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
    'forms',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-keynote", "component_type": "forms", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Newsletter.tsx", "uses_components": ["Button"], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();


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
    'ecommerce',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'ecommerce', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-keynote", "component_type": "ecommerce", "file_path": "tailwind-plus-keynote/keynote-ts/src/components/Speakers.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

