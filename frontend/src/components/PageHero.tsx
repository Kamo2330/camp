interface PageHeroProps {
  eyebrow: string;
  title: string;
  subtitle: string;
  children?: React.ReactNode;
}

export default function PageHero({ eyebrow, title, subtitle, children }: PageHeroProps) {
  return (
    <section className="pb-5 pt-11">
      <div className="card card-inset min-w-[280px] flex-1">
        <div className="eyebrow">{eyebrow}</div>
        <h1 className="title">{title}</h1>
        <p className="muted">{subtitle}</p>
        {children && <div className="mt-4 flex flex-wrap gap-2.5">{children}</div>}
      </div>
    </section>
  );
}
