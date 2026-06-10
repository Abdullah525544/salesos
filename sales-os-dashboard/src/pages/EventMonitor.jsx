import { motion } from 'framer-motion';
import { Radio, Activity, Zap, AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import Badge from '../components/ui/Badge';

const events = [
  { id: 'evt_101', type: 'lead.created', status: 'processed', latency: '23ms', timestamp: '2026-06-08T14:32:00Z', handler: 'LeadCreatedHandler' },
  { id: 'evt_102', type: 'research.completed', status: 'processing', latency: '—', timestamp: '2026-06-08T14:31:00Z', handler: 'ResearchCompletedHandler' },
  { id: 'evt_103', type: 'call.completed', status: 'processed', latency: '45ms', timestamp: '2026-06-08T14:30:00Z', handler: 'CallCompletedHandler' },
  { id: 'evt_104', type: 'lead.qualified', status: 'processed', latency: '12ms', timestamp: '2026-06-08T14:28:00Z', handler: 'LeadQualifiedHandler' },
  { id: 'evt_105', type: 'follow_up.sent', status: 'failed', latency: '—', timestamp: '2026-06-08T14:25:00Z', handler: 'FollowUpHandler', error: 'Redis connection timeout' },
  { id: 'evt_106', type: 'lead.created', status: 'processed', latency: '18ms', timestamp: '2026-06-08T14:20:00Z', handler: 'LeadCreatedHandler' },
  { id: 'evt_107', type: 'call.completed', status: 'queued', latency: '—', timestamp: '2026-06-08T14:18:00Z', handler: 'CallCompletedHandler' },
];

const statusIcon = { processed: CheckCircle, processing: Activity, queued: Clock, failed: AlertTriangle };
const statusColor = { processed: 'text-emerald-400', processing: 'text-blue-400', queued: 'text-amber-400', failed: 'text-red-400' };
const statusVariant = { processed: 'success', processing: 'info', queued: 'warning', failed: 'warning' };

export default function EventMonitor() {
  const stats = {
    total: events.length,
    processed: events.filter(e => e.status === 'processed').length,
    failed: events.filter(e => e.status === 'failed').length,
    queued: events.filter(e => e.status === 'queued').length,
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Event Monitor</h1>
        <p className="text-sm text-gray-400 mt-1">Real-time event bus monitoring</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: 'Total Events', value: stats.total, color: 'text-white', bg: 'bg-primary/20' },
          { label: 'Processed', value: stats.processed, color: 'text-emerald-400', bg: 'bg-emerald-500/20' },
          { label: 'Failed', value: stats.failed, color: 'text-red-400', bg: 'bg-red-500/20' },
          { label: 'Queued', value: stats.queued, color: 'text-amber-400', bg: 'bg-amber-500/20' },
        ].map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }} className="glass-card text-center">
            <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
            <p className="text-xs text-gray-400 mt-1">{s.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Live Indicator */}
      <div className="flex items-center gap-2 text-xs text-gray-400">
        <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
        Event bus active · {events.length} events in window
      </div>

      {/* Event list */}
      <div className="glass-card !p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/5 text-xs text-gray-400 uppercase tracking-wider">
                <th className="text-left px-4 py-3 font-medium">Event</th>
                <th className="text-left px-4 py-3 font-medium">Status</th>
                <th className="text-left px-4 py-3 font-medium">Latency</th>
                <th className="text-left px-4 py-3 font-medium">Handler</th>
                <th className="text-right px-4 py-3 font-medium">Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {events.map(evt => {
                const Icon = statusIcon[evt.status] || CheckCircle;
                return (
                  <tr key={evt.id} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3">
                      <p className="text-sm font-medium text-white">{evt.type}</p>
                      <p className="text-xs text-gray-500">{evt.id}</p>
                    </td>
                    <td className="px-4 py-3">
                      <Badge variant={statusVariant[evt.status]} className="gap-1">
                        <Icon size={12} className={statusColor[evt.status]} />
                        {evt.status}
                      </Badge>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-400">{evt.latency}</td>
                    <td className="px-4 py-3 text-sm text-gray-400">{evt.handler}</td>
                    <td className="px-4 py-3 text-sm text-gray-500 text-right">{new Date(evt.timestamp).toLocaleTimeString()}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
