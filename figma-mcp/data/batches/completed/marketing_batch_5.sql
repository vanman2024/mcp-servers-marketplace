-- Marketing Sections Batch 5
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
    'blog',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/navigation", "dayjs", "@heroicons/react/16/solid", "next-sanity"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-radiant", "component_type": "blog", "file_path": "tailwind-plus-radiant/radiant-ts/src/app/blog/[slug]/page.tsx", "uses_components": ["Button"], "dependencies": ["next/navigation", "dayjs", "@heroicons/react/16/solid", "next-sanity"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'auth',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'auth', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Input", "Button"], "dependencies": ["clsx", "@heroicons/react/16/solid", "@headlessui/react"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-radiant", "component_type": "auth", "file_path": "tailwind-plus-radiant/radiant-ts/src/app/login/page.tsx", "uses_components": ["Input", "Button"], "dependencies": ["clsx", "@heroicons/react/16/solid", "@headlessui/react"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'pricing',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'pricing', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["@headlessui/react"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-radiant", "component_type": "pricing", "file_path": "tailwind-plus-radiant/radiant-ts/src/app/pricing/page.tsx", "uses_components": ["Button"], "dependencies": ["@headlessui/react"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'blog',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'radiant', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["node:assert", "feed"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-radiant", "component_type": "blog", "file_path": "tailwind-plus-radiant/radiant-js/src/app/blog/feed.xml/route.js", "uses_components": [], "dependencies": ["node:assert", "feed"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'faq',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'faq', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-salient", "component_type": "faq", "file_path": "tailwind-plus-salient/salient-ts/src/components/Faqs.tsx", "uses_components": [], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'footer',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-salient", "component_type": "footer", "file_path": "tailwind-plus-salient/salient-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'salient', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "clsx"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-salient", "component_type": "hero", "file_path": "tailwind-plus-salient/salient-ts/src/components/Header.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'salient', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-salient", "component_type": "hero", "file_path": "tailwind-plus-salient/salient-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": ["next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'pricing',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'pricing', 'salient', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["clsx"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-salient", "component_type": "pricing", "file_path": "tailwind-plus-salient/salient-ts/src/components/Pricing.tsx", "uses_components": ["Button"], "dependencies": ["clsx"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'features',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'salient', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-salient", "component_type": "features", "file_path": "tailwind-plus-salient/salient-ts/src/components/PrimaryFeatures.tsx", "uses_components": [], "dependencies": ["clsx", "@headlessui/react", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

