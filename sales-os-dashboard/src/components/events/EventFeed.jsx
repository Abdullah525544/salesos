import { motion } from 'framer-motion';
import { UserPlus, Search, Phone, Award, Send, Radio } from 'lucide-react';

const iconMap = {
  UserPlus, Search, Phone, Award, Send, Radio,
};

const colorMap = {
  green: 'bg-emerald-500/20 text-emerald-400',
  blue: 'bg-blue-500/20 text-blue-400',
  indigo: 'bg-indigo-500/20 text-indigo-400',
  emerald: 'bg-emerald-500/20 text-emerald-400',
  purple: 'bg-purple-500/20 text-purple-400',
};

export default function EventFeed({ events = [] }) {
  return (
    <div className="space-y-2">
      {events.map((evt, i) => {
        const Icon = iconMap[evt.icon] || Radio;
        return (
          <motion.div
            key={evt.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="flex items-center gap-3 p-3 rounded-lg hover:bg-white/5 transition-colors"
          >
            <div className={`p-2 rounded-lg ${colorMap[evt.color] || colorMap.green}`}>
              <Icon size={14} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white truncate">{evt.lead}</p>
              <p className="text-xs text-gray-400">{evt.type}</p>
            </div>
            <span className="text-xs text-gray-500 flex-shrink-0">{evt.time}</span>
          </motion.div>
        );
      })}
    </div>
  );
}
