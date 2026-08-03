import PageHero from '@/components/PageHero';
import CardGrid from '@/components/CardGrid';
import { getSiteContent } from '@/lib/api';

export default async function AboutPage() {
  const site = await getSiteContent();

  return (
    <>
      <PageHero
        eyebrow={site.about.eyebrow}
        title={site.about.title}
        subtitle={site.about.subtitle}
      />
      <div className="mt-4">
        <CardGrid items={site.about.sections} />
      </div>
    </>
  );
}
