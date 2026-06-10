import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, UserCheck, Flame, Phone, Send, HeartPulse } from 'lucide-react';
import KPICard from '../components/ui/KPICard';
import FunnelChart from '../components/charts/FunnelChart';
import ActivityLineChart from '../components/charts/ActivityLineChart';
import EventFeed from '../components/events/EventFeed';
import Skeleton from '../components/ui/Skeleton';
import { fetchAnalytics } from '../services/analytics';
import { fetchLeads } from '../services/leads';
import { kpiData as mockKpi, pipelineFunnel, dailyActivity, recentEvents } from '../data/mockData';

export default function Dashboard() {
  const [kpiValues, setKpiValues] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchAnalytics().catch(() => null),
      fetchLeads().catch(() => null),
    ]).then(([a, l]) => {
      if (a || l) {
        setKpiValues({
          totalLeads: a?.total_leads ?? l?.total ?? mockKpi.totalLeads.value,
          activeLeads: a ? (a.total_leads - a.cold_leads) : mockKpi.activeLeads.value,
          hotLeads: a?.hot_leads ?? mockKpi.hotLeads.value,
          callsMade: a?.calls_made ?? mockKpi.callsMade.value,
          followupsSent: mockKpi.followupsSent.value,
          conversion: a ? `${a.conversion_rate}%` : '—',
        });
      } else {
        setKpiValues({
          totalLeads: mockKpi.totalLeads.value,
          activeLeads: mockKpi.activeLeads.value,
          hotLeads: mockKpi.hotLeads.value,
          callsMade: mockKpi.callsMade.value,
          followupsSent: mockKpi.followupsSent.value,
          conversion: `${mockKpi.systemHealth.value}%`,
        });
      }
    }).finally(() => setLoading(false));
  }, []);

  const kpiConfig = kpiValues ? [
    { label: 'Total Leads', value: kpiValues.totalLeads, change: 0, icon: Users, color: 'primary' },
    { label: 'Active Leads', value: kpiValues.activeLeads, change: 0, icon: UserCheck, color: 'blue' },
    { label: 'Hot Leads', value: kpiValues.hotLeads, change: 0, icon: Flame, color: 'red' },
    { label: 'Calls Made', value: kpiValues.callsMade, change: 0, icon: Phone, color: 'green' },
    { label: 'Follow-ups Sent', value: kpiValues.followupsSent, change: 0, icon: Send, color: 'purple' },
    { label: 'Conversion', value: kpiValues.conversion, change: 0, icon: HeartPulse, color: 'green' },
  ] : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-sm text-gray-400 mt-1">AI-powered Sales OS overview</p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="h-28" />)}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          {kpiConfig.map((kpi, i) => (
            <motion.div key={kpi.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <KPICard {...kpi} />
            </motion.div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card">
          <h3 className="text-sm font-semibold text-white mb-4">Pipeline Overview</h3>
          <FunnelChart data={pipelineFunnel} />
        </div>
        <div className="glass-card">
          <h3 className="text-sm font-semibold text-white mb-4">Lead Activity (7 days)</h3>
          <ActivityLineChart data={dailyActivity} />
        </div>
      </div>

      <div className="glass-card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-white">Real-time Event Feed</h3>
          <span className="flex items-center gap-2 text-xs text-gray-400">
            <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
            Live
          </span>
        </div>
        <EventFeed events={recentEvents} />
      </div>
    </div>
  );
}
