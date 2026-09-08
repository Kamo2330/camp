const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface Service {
  id: number;
  title: string;
  description: string;
  featured: boolean;
  order: number;
}

export interface Industry {
  id: number;
  title: string;
  description: string;
  order: number;
}

export interface JobOpening {
  id: number;
  title: string;
  order: number;
}

export interface AboutSection {
  title: string;
  description: string;
}

export interface SiteContent {
  brand: string;
  home: {
    eyebrow: string;
    title: string;
    subtitle: string;
    featured_services: Service[];
  };
  about: {
    eyebrow: string;
    title: string;
    subtitle: string;
    sections: AboutSection[];
  };
  services_page: {
    eyebrow: string;
    title: string;
    subtitle: string;
  };
  clients_page: {
    eyebrow: string;
    title: string;
    subtitle: string;
    testimonial: string;
  };
  careers_page: {
    eyebrow: string;
    title: string;
    subtitle: string;
    benefits: string[];
  };
  contact_page: {
    eyebrow: string;
    title: string;
    subtitle: string;
  };
  contact: {
    phone_emergency: string;
    phone_office: string;
    email_info: string;
    email_sales: string;
    email_careers: string;
    address: string;
  };
}

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      next: { revalidate: 60 },
    });
  } catch {
    throw new Error(
      `Could not connect to API at ${API_URL}. Is the Django backend running?`
    );
  }
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}

export function getSiteContent(): Promise<SiteContent> {
  return fetchApi<SiteContent>('/site/');
}

export function getServices(): Promise<Service[]> {
  return fetchApi<Service[]>('/services/');
}

export function getIndustries(): Promise<Industry[]> {
  return fetchApi<Industry[]>('/industries/');
}

export function getJobs(): Promise<JobOpening[]> {
  return fetchApi<JobOpening[]>('/jobs/');
}

export async function submitContact(data: {
  name: string;
  email: string;
  message: string;
}): Promise<void> {
  const res = await fetch(`${API_URL}/contact/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.message || 'Failed to submit inquiry');
  }
}

export type ChatResponse = { reply: string; mode: string };

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
  } catch {
    throw new Error(
      `Could not connect to API at ${API_URL}. Is the Django backend running?`
    );
  }
  if (!res.ok) {
    throw new Error(`Chat API error: ${res.status}`);
  }
  return res.json();
}
