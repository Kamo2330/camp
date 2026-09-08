import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ChatWidget from '@/components/ChatWidget';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Camp Security',
  description: 'Trusted security services for your people, property, and peace of mind.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen text-text`}>
        <Header />
        <main className="container mx-auto max-w-6xl px-7 py-7">{children}</main>
        <Footer />
        <ChatWidget />
      </body>
    </html>
  );
}
