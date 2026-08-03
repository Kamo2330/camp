interface CardGridProps {
  items: { title: string; description: string }[];
}

export default function CardGrid({ items }: CardGridProps) {
  return (
    <section className="grid-cards">
      {items.map((item) => (
        <div key={item.title} className="card">
          <h3 className="mt-0">{item.title}</h3>
          <p className="muted">{item.description}</p>
        </div>
      ))}
    </section>
  );
}
