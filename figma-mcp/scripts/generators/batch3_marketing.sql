-- Batch 3
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
