-- Marketing Sections Batch 4
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "@headlessui/react", "clsx"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "hero", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "@headlessui/react", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "hero", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/HeroPattern.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'navigation',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["framer-motion", "zustand"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "navigation", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/MobileNavigation.tsx", "uses_components": ["Dialog"], "dependencies": ["framer-motion", "zustand"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'navigation',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "clsx", "@headlessui/react", "next/navigation"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "navigation", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Navigation.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "framer-motion", "clsx", "@headlessui/react", "next/navigation"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'cta',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'cta', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "cta", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Resources.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'ecommerce',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'ecommerce', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "ecommerce", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/icons/CartIcon.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'forms',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "forms", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Feedback.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'forms',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'forms', 'protocol', 'not-for-apps']::text[],
    '{"uses_components": ["Dialog"], "dependencies": ["clsx", "next/navigation", "@headlessui/react", "react-highlight-words"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-protocol", "component_type": "forms", "file_path": "tailwind-plus-protocol/protocol-ts/src/components/Search.tsx", "uses_components": ["Dialog"], "dependencies": ["clsx", "next/navigation", "@headlessui/react", "react-highlight-words"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'footer',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-radiant", "component_type": "footer", "file_path": "tailwind-plus-radiant/radiant-ts/src/components/footer.tsx", "uses_components": ["Button"], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'navigation',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["framer-motion", "@heroicons/react/24/solid"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-radiant", "component_type": "navigation", "file_path": "tailwind-plus-radiant/radiant-ts/src/components/navbar.tsx", "uses_components": [], "dependencies": ["framer-motion", "@heroicons/react/24/solid"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

