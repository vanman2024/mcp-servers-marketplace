-- Marketing Sections Batch 2
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
    'error',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'error', 'keynote', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/font/google", "clsx"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-keynote", "component_type": "error", "file_path": "tailwind-plus-keynote/keynote-ts/src/app/layout.tsx", "uses_components": [], "dependencies": ["next/font/google", "clsx"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'auth',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "auth", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/AuthLayout.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'faq',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'faq', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "faq", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Faqs.tsx", "uses_components": [], "dependencies": [], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'footer',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "footer", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Footer.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "framer-motion"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "hero", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "framer-motion"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["clsx", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "hero", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": ["clsx", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'navigation',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'navigation', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "framer-motion"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "navigation", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/NavLinks.tsx", "uses_components": [], "dependencies": ["next/link", "framer-motion"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'pricing',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'pricing', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["clsx", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "pricing", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Pricing.tsx", "uses_components": ["Button"], "dependencies": ["clsx", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'features',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["use-debounce", "clsx", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "features", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/PrimaryFeatures.tsx", "uses_components": [], "dependencies": ["use-debounce", "clsx", "@headlessui/react"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'testimonials',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'testimonials', 'pocket', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["framer-motion", "clsx"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-pocket", "component_type": "testimonials", "file_path": "tailwind-plus-pocket/pocket-ts/src/components/Reviews.tsx", "uses_components": [], "dependencies": ["framer-motion", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

