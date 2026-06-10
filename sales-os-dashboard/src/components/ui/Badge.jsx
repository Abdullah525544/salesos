export default function Badge({ children, variant = 'default', className = '' }) {
  const variants = {
    default: 'bg-gray-500/20 text-gray-300',
    hot: 'bg-red-500/20 text-red-400',
    warm: 'bg-amber-500/20 text-amber-400',
    cold: 'bg-gray-500/20 text-gray-400',
    success: 'bg-emerald-500/20 text-emerald-400',
    warning: 'bg-amber-500/20 text-amber-400',
    info: 'bg-blue-500/20 text-blue-400',
    primary: 'bg-primary/20 text-primary-300',
    purple: 'bg-purple-500/20 text-purple-400',
    high: 'bg-red-500/20 text-red-400',
    medium: 'bg-amber-500/20 text-amber-400',
    low: 'bg-gray-500/20 text-gray-400',
  };

  return (
    <span className={`badge ${variants[variant] || variants.default} ${className}`}>
      {children}
    </span>
  );
}
