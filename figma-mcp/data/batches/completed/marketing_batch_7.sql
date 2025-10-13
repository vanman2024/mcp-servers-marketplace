-- Marketing Sections Batch 7
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
    'footer',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'footer', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "footer", "file_path": "tailwind-plus-studio/studio-ts/src/components/Footer.tsx", "uses_components": [], "dependencies": ["next/link"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'features',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'features', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "features", "file_path": "tailwind-plus-studio/studio-ts/src/app/page.tsx", "uses_components": [], "dependencies": ["next/link", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'team',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'team', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "team", "file_path": "tailwind-plus-studio/studio-ts/src/app/about/page.tsx", "uses_components": [], "dependencies": ["next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'blog',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'studio', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "blog", "file_path": "tailwind-plus-studio/studio-ts/src/app/blog/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'blog',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'blog', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "blog", "file_path": "tailwind-plus-studio/studio-ts/src/app/blog/wrapper.tsx", "uses_components": [], "dependencies": [], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'cta',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'cta', 'studio', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "cta", "file_path": "tailwind-plus-studio/studio-ts/src/app/contact/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'portfolio',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'portfolio', 'studio', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["next/link", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "portfolio", "file_path": "tailwind-plus-studio/studio-ts/src/app/work/page.tsx", "uses_components": ["Button"], "dependencies": ["next/link", "next/image"], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'portfolio',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'portfolio', 'studio', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": []}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-studio", "component_type": "portfolio", "file_path": "tailwind-plus-studio/studio-ts/src/app/work/wrapper.tsx", "uses_components": [], "dependencies": [], "is_page": true, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": [], "dependencies": ["next/navigation"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-syntax", "component_type": "hero", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/DocsHeader.tsx", "uses_components": [], "dependencies": ["next/navigation"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
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
    'hero',
    'marketing-site',
    true,
    true,
    ARRAY['marketing', 'landing-page', 'tailwind-plus', 'hero', 'syntax', 'not-for-apps']::text[],
    '{"uses_components": ["Button"], "dependencies": ["prism-react-renderer", "clsx", "next/image"]}'::jsonb,
    '{}'::jsonb,
    '{"template_name": "tailwind-plus-syntax", "component_type": "hero", "file_path": "tailwind-plus-syntax/syntax-ts/src/components/Hero.tsx", "uses_components": ["Button"], "dependencies": ["prism-react-renderer", "clsx", "next/image"], "is_page": false, "warning": "This is a marketing/landing page component. For application UIs, use app-specific sections."}'::jsonb,
    (SELECT id FROM project_specifications WHERE name = 'Default Project' LIMIT 1)
)
ON CONFLICT (name, project_id) DO UPDATE SET
    description = EXCLUDED.description,
    react_template = EXCLUDED.react_template,
    tags = EXCLUDED.tags,
    updated_at = NOW();

