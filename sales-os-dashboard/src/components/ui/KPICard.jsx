import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function KPICard({ label, value, change, icon: Icon, color = 'primary' }) {
  const colorMap = {
    primary: 'bg-primary/20 text-primary-300',
    green: 'bg-emerald-500/20 text-emerald-400',
    blue: 'bg-blue-500/20 text-blue-400',
    amber: 'bg-amber-500/20 text-amber-400',
    purple: 'bg-purple-500/20 text-purple-400',
    red: 'bg-red-500/20 text-red-400',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card flex items-start gap-4"
    >
      <div className={`p-3 rounded-xl ${colorMap[color] || colorMap.primary}`}>
        {Icon && <Icon size={24} />}
      </div>
      <div className="flex-1">
        <p className="stat-label">{label}</p>
        <p className="stat-value mt-1">{value}</p>
        <div className="flex items-center gap-1 mt-1">
          {change >= 0 ? (
            <TrendingUp size={14} className="text-emerald-400" />
          ) : (
            <TrendingDown size={14} className="text-red-400" />
          )}
          <span className={`text-xs font-medium ${change >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {Math.abs(change)}%
          </span>
          <span className="text-xs text-gray-500">vs last month</span>
        </div>
      </div>
    </motion.div>
  );
}
