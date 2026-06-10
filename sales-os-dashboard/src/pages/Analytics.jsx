import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend, Cell } from 'recharts';
import { fetchAnalytics } from '../services/analytics';
import FunnelChart from '../components/charts/FunnelChart';
import CustomPieChart from '../components/charts/PieChart';
import Skeleton from '../components/ui/Skeleton';
import ErrorState from '../components/ui/ErrorState';
import { pipelineFunnel } from '../data/mockData';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card !p-3 !rounded-lg text-sm">
      <p className="text-white font-medium mb-1">{label}</p>
      {payload.map((p, i) => (
        <p key={i} className="text-gray-400">{p.name}: {p.value}{p.name === 'rate' || p.name === 'Conversion Rate' ? '%' : ''}</p>
      ))}
    </div>
  );
};

export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (error) return <ErrorState message={error} onRetry={() => window.location.reload()} />;

  const qualityDistribution = data ? [
    { name: 'Hot', value: data.hot_leads || 0, fill: '#EF4444' },
    { name: 'Warm', value: data.warm_leads || 0, fill: '#F59E0B' },
    { name: 'Cold', value: data.cold_leads || 0, fill: '#6B7280' },
  ] : [];

  const conversionData = data ? [
    { month: 'Current', rate: data.conversion_rate || 0 },
  ] : [];

  return (
    <div className="space-y-6">
      <div><h1 className="text-2xl font-bold text-white">Analytics</h1><p className="text-sm text-gray-400 mt-1">Performance metrics and AI efficiency</p></div>

      {loading ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-72" />)}
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {data && (
            <>
              <div className="glass-card">
                <h3 className="text-sm font-semibold text-white mb-4">Conversion Rate</h3>
                <p className="text-4xl font-bold text-emerald-400 mb-2">{data.conversion_rate}%</p>
                <p className="text-sm text-gray-400">Overall lead-to-meeting conversion</p>
              </div>
              <div className="glass-card">
                <h3 className="text-sm font-semibold text-white mb-4">Lead Quality Distribution</h3>
                <CustomPieChart data={qualityDistribution} />
              </div>
              <div className="glass-card">
                <h3 className="text-sm font-semibold text-white mb-4">Key Metrics</h3>
                <div className="grid grid-cols-2 gap-4">
                  {[
                    { label: 'Total Leads', value: data.total_leads },
                    { label: 'Calls Made', value: data.calls_made },
                    { label: 'Connected Calls', value: data.connected_calls },
                    { label: 'Interested Leads', value: data.interested_leads },
                    { label: 'Meetings Booked', value: data.meetings_booked },
                    { label: 'Revenue', value: `$${data.revenue_generated?.toLocaleString() || 0}` },
                  ].map(m => (
                    <div key={m.label} className="p-3 rounded-lg bg-surface-light/30 text-center">
                      <p className="text-lg font-bold text-white">{m.value}</p>
                      <p className="text-xs text-gray-400 mt-1">{m.label}</p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="glass-card">
                <h3 className="text-sm font-semibold text-white mb-4">Pipeline Funnel</h3>
                <FunnelChart data={pipelineFunnel} />
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
