export default function Skeleton({ className = '', count = 1 }) {
  const base = 'bg-surface-light/50 animate-pulse rounded-lg';
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className={`${base} ${className}`} />
      ))}
    </>
  );
}
