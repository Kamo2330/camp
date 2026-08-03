import Link from 'next/link';
import CardGrid from '@/components/CardGrid';
import PageHero from '@/components/PageHero';
import { getSiteContent } from '@/lib/api';

export default async function HomePage() {
  const site = await getSiteContent();

  return (
    <>
      <PageHero
        eyebrow={site.home.eyebrow}
        title={site.home.title}
        subtitle={site.home.subtitle}
      >
        <Link href="/contact" className="btn">
          Request a Quote
        </Link>
        <Link href="/careers" className="btn btn-ghost">
          Join Our Team
        </Link>
      </PageHero>
      <CardGrid
        items={site.home.featured_services.map((s) => ({
          title: s.title,
          description: s.description,
        }))}
      />
    </>
  );
}
