import { useState, useEffect } from 'react';
import { Activity, Zap, Clock, DollarSign, AlertTriangle, Layers, CheckCircle, XCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { checkSystemHealth } from '../services/systemHealth';
import Skeleton from '../components/ui/Skeleton';
import ErrorState from '../components/ui/ErrorState';

function HealthIndicator({ status }) {
  if (status === 'healthy' || status === 'good' || status === 'pass') return <CheckCircle size={18} className="text-emerald-400" />;
  if (status === 'warning' || status === 'warn') return <AlertCircle size={18} className="text-amber-400" />;
  return <XCircle size={18} className="text-red-400" />;
}

function StatusBadge({ status }) {
  const colors = { healthy: 'bg-emerald-500/20 text-emerald-400', pass: 'bg-emerald-500/20 text-emerald-400', warning: 'bg-amber-500/20 text-amber-400', degraded: 'bg-red-500/20 text-red-400', good: 'bg-emerald-500/20 text-emerald-400' };
  return <span className={`badge ${colors[status] || colors.healthy}`}>{status}</span>;
}

export default function SystemHealth() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = () => {
    setLoading(true);
    setError(null);
    checkSystemHealth()
      .then(setHealth)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  if (loading) return <div className="grid grid-cols-1 sm:grid-cols-2 gap-4"><Skeleton className="h-32" count={4} /></div>;
  if (error) return <ErrorState message={error} onRetry={load} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">System Health</h1>
          <p className="text-sm text-gray-400 mt-1">Real-time system status and metrics</p>
        </div>
        <div className="flex items-center gap-3">
          <StatusBadge status={health?.status || 'unknown'} />
          <button onClick={load} className="btn-ghost"><RefreshCw size={16} /></button>
        </div>
      </div>

      {health && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {health.checks?.map(check => (
              <div key={check.name} className="glass-card">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Activity size={18} className="text-primary-300" />
                    <h3 className="text-sm font-semibold text-white">{check.name}</h3>
                  </div>
                  <HealthIndicator status={check.status} />
                </div>
                <div className="text-sm text-gray-400">{check.detail || check.message || 'OK'}</div>
              </div>
            ))}
            {(!health.checks || health.checks.length === 0) && (
              <div className="glass-card col-span-2">
                <div className="flex items-center gap-2 text-emerald-400">
                  <CheckCircle size={20} />
                  <span className="font-medium">All systems operational</span>
                </div>
                <p className="text-sm text-gray-400 mt-2">API: {health.api_status || 'OK'} · DB: {health.database_status || 'OK'} · Redis: {health.redis_status || 'OK'}</p>
              </div>
            )}
          </div>

          <div className="glass-card">
            <h3 className="text-sm font-semibold text-white mb-3">Response</h3>
            <pre className="text-xs text-gray-400 overflow-auto max-h-60">{JSON.stringify(health, null, 2)}</pre>
          </div>
        </>
      )}
    </div>
  );
}
