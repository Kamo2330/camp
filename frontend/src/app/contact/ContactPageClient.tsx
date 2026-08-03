'use client';

import { FormEvent, useState } from 'react';
import PageHero from '@/components/PageHero';
import { submitContact, type SiteContent } from '@/lib/api';

interface ContactPageProps {
  site: SiteContent;
}

export default function ContactPageClient({ site }: ContactPageProps) {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [error, setError] = useState('');

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus('loading');
    setError('');
    const form = e.currentTarget;
    const data = new FormData(form);
    try {
      await submitContact({
        name: String(data.get('name')),
        email: String(data.get('email')),
        message: String(data.get('message')),
      });
      setStatus('success');
      form.reset();
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'Something went wrong');
    }
  }

  return (
    <>
      <PageHero
        eyebrow={site.contact_page.eyebrow}
        title={site.contact_page.title}
        subtitle={site.contact_page.subtitle}
      />
      <div className="mt-4 grid-cards">
        <div className="card">
          <h3>Phone</h3>
          <p>
            Emergency: {site.contact.phone_emergency}
            <br />
            Office: {site.contact.phone_office}
          </p>
        </div>
        <div className="card">
          <h3>Email</h3>
          <p>
            {site.contact.email_info}
            <br />
            {site.contact.email_sales}
          </p>
        </div>
        <div className="card">
          <h3>Address</h3>
          <p>{site.contact.address}</p>
        </div>
      </div>
      <div className="card mt-4">
        <h3>Request a Quote</h3>
        <p className="muted">Tell us about your needs and we&apos;ll tailor a solution for you.</p>
        <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-3">
          <input
            name="name"
            required
            placeholder="Your name"
            className="rounded-lg border border-soft-border bg-surface px-3 py-2 text-text"
          />
          <input
            name="email"
            type="email"
            required
            placeholder="Email address"
            className="rounded-lg border border-soft-border bg-surface px-3 py-2 text-text"
          />
          <textarea
            name="message"
            required
            minLength={10}
            rows={4}
            placeholder="How can we help?"
            className="rounded-lg border border-soft-border bg-surface px-3 py-2 text-text"
          />
          <button type="submit" className="btn w-fit" disabled={status === 'loading'}>
            {status === 'loading' ? 'Sending…' : 'Submit Inquiry'}
          </button>
          {status === 'success' && (
            <p className="text-green-400">Thanks! We&apos;ll be in touch soon.</p>
          )}
          {status === 'error' && <p className="text-accent">{error}</p>}
        </form>
      </div>
    </>
  );
}
