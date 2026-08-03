import { getSiteContent } from '@/lib/api';
import ContactPageClient from './ContactPageClient';

export default async function ContactPage() {
  const site = await getSiteContent();
  return <ContactPageClient site={site} />;
}
