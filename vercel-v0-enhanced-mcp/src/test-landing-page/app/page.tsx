import HeroSection from '@/components/hero-section'
import FeaturesSection from '@/components/features-section'
import ContactForm from '@/components/contact-form'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-white">
      <HeroSection />
      <FeaturesSection />
      <ContactForm />
    </main>
  )
}