import PageHero from '@/components/PageHero';
import CardGrid from '@/components/CardGrid';
import { getIndustries, getSiteContent } from '@/lib/api';

export default async function ClientsPage() {
  const [industries, site] = await Promise.all([getIndustries(), getSiteContent()]);

  return (
    <>
      <PageHero
        eyebrow={site.clients_page.eyebrow}
        title={site.clients_page.title}
        subtitle={site.clients_page.subtitle}
      />
      <div className="mt-4">
        <CardGrid
          items={industries.map((i) => ({ title: i.title, description: i.description }))}
        />
      </div>
      <div className="card mt-4">
        <h3>What Clients Say</h3>
        <p>
          <em>&ldquo;{site.clients_page.testimonial}&rdquo;</em>
        </p>
      </div>
    </>
  );
}
