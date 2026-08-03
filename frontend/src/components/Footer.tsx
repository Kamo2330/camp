export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <div className="container mx-auto max-w-6xl border-t border-border px-7 py-[18px] text-sm text-muted">
      © {year} Camp Security. All rights reserved.
    </div>
  );
}
