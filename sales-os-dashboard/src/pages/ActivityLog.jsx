import { useState } from 'react';
import { Search, Filter, ChevronDown, ChevronUp, ClipboardList } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { activityLogs } from '../data/mockData';
import Badge from '../components/ui/Badge';

const eventTypes = ['all', 'lead.created', 'research.completed', 'call.completed', 'lead.qualified', 'follow_up.sent', 'lead.updated', 'call.scheduled'];

const typeVariant = {
  'lead.created': 'success', 'research.completed': 'info', 'call.completed': 'primary',
  'lead.qualified': 'purple', 'follow_up.sent': 'purple', 'lead.updated': 'warning', 'call.scheduled': 'info',
};

export default function ActivityLog() {
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [expanded, setExpanded] = useState(null);

  const filtered = activityLogs.filter(log => {
    const matchSearch = log.lead.toLowerCase().includes(search.toLowerCase()) || log.detail.toLowerCase().includes(search.toLowerCase());
    const matchType = typeFilter === 'all' || log.type === typeFilter;
    return matchSearch && matchType;
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Activity Log</h1>
        <p className="text-sm text-gray-400 mt-1">Complete system event history</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="relative flex-1 max-w-xs">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input type="text" placeholder="Search logs..." value={search} onChange={e => setSearch(e.target.value)} className="input-field pl-10" />
        </div>
        <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)} className="input-field w-auto">
          {eventTypes.map(t => (
            <option key={t} value={t}>{t === 'all' ? 'All Events' : t}</option>
          ))}
        </select>
      </div>

      {/* Timeline */}
      <div className="space-y-2">
        {filtered.map(log => (
          <motion.div
            key={log.id}
            layout
            className="glass-card !p-0 overflow-hidden"
          >
            <button onClick={() => setExpanded(expanded === log.id ? null : log.id)} className="w-full flex items-start gap-4 p-4 text-left hover:bg-white/5 transition-colors">
              <div className="w-2 h-2 mt-2 rounded-full bg-primary flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <Badge variant={typeVariant[log.type] || 'default'}>{log.type}</Badge>
                  <span className="text-sm font-medium text-white">{log.lead}</span>
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  {new Date(log.timestamp).toLocaleString()} · {log.user}
                </p>
              </div>
              <div className="flex-shrink-0 text-gray-500">
                {expanded === log.id ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </div>
            </button>
            <AnimatePresence>
              {expanded === log.id && (
                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="border-t border-white/5 px-4 py-3">
                  <p className="text-sm text-gray-400">{log.detail}</p>
                  <p className="text-xs text-gray-500 mt-2">ID: {log.id}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
        {filtered.length === 0 && (
          <div className="glass-card text-center py-12">
            <ClipboardList size={40} className="mx-auto text-gray-600 mb-3" />
            <p className="text-sm text-gray-500">No matching log entries.</p>
          </div>
        )}
      </div>
    </div>
  );
}
