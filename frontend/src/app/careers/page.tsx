import PageHero from '@/components/PageHero';
import { getJobs, getSiteContent } from '@/lib/api';

export default async function CareersPage() {
  const [site, jobs] = await Promise.all([getSiteContent(), getJobs()]);

  return (
    <>
      <PageHero
        eyebrow={site.careers_page.eyebrow}
        title={site.careers_page.title}
        subtitle={site.careers_page.subtitle}
      />
      <div className="mt-4 grid-cards">
        <div className="card">
          <h3>Benefits</h3>
          <ul className="pl-5">
            {site.careers_page.benefits.map((benefit) => (
              <li key={benefit}>{benefit}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3>Open Roles</h3>
          <ul className="pl-5">
            {jobs.map((job) => (
              <li key={job.id}>{job.title}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="card mt-4">
        <h3>Apply Now</h3>
        <p>
          Send your CV to{' '}
          <a href={`mailto:${site.contact.email_careers}`} className="text-accent">
            {site.contact.email_careers}
          </a>
          .
        </p>
      </div>
    </>
  );
}
