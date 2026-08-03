import Link from 'next/link';

const links = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/services', label: 'Services' },
  { href: '/clients', label: 'Clients' },
  { href: '/careers', label: 'Careers' },
  { href: '/contact', label: 'Contact' },
];

export default function Header() {
  return (
    <header className="sticky top-0 z-20 border-b border-border bg-bg/85 backdrop-blur-sm">
      <div className="container mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-[18px] px-7 py-7">
        <Link href="/" className="flex items-center gap-3 font-bold tracking-[0.3px] no-underline text-text">
          <span className="inline-flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-accent to-[#ff3647] font-extrabold text-white shadow-[0_6px_18px_rgba(225,29,46,0.35)]">
            C
          </span>
          <span>Camp Security</span>
        </Link>
        <nav className="flex flex-wrap gap-3">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="relative rounded-lg border border-transparent px-3 py-2.5 text-text no-underline after:absolute after:bottom-1.5 after:left-3 after:right-3 after:h-0.5 after:origin-center after:scale-x-0 after:bg-gradient-to-r after:from-transparent after:via-accent after:to-transparent after:transition-transform hover:after:scale-x-100"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
