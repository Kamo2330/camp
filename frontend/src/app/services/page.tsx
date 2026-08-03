import PageHero from '@/components/PageHero';
import CardGrid from '@/components/CardGrid';
import { getServices, getSiteContent } from '@/lib/api';

export default async function ServicesPage() {
  const [site, services] = await Promise.all([getSiteContent(), getServices()]);

  return (
    <>
      <PageHero
        eyebrow={site.services_page.eyebrow}
        title={site.services_page.title}
        subtitle={site.services_page.subtitle}
      />
      <div className="mt-4">
        <CardGrid
          items={services.map((s) => ({ title: s.title, description: s.description }))}
        />
      </div>
    </>
  );
}
