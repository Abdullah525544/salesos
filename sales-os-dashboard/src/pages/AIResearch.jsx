import { useState } from 'react';
import { Search, Clock, CheckCircle, RotateCw, MapPin, Globe, User, Phone, Mail, Link as LinkIcon, Loader, ChevronDown, ChevronUp, Sparkles } from 'lucide-react';
import { searchLeads, getLeadFinderStatus } from '../services/leads';
import Badge from '../components/ui/Badge';
import EmptyState from '../components/ui/EmptyState';

const statusVariant = { completed: 'success', in_progress: 'warning', pending: 'default', running: 'warning' };
const statusIcon = { completed: CheckCircle, in_progress: RotateCw, pending: Clock, running: Loader };

export default function AIResearch() {
  const [showForm, setShowForm] = useState(true);
  const [form, setForm] = useState({ niche: '', city: '', country: '', keyword: '', category: '', limit: 25 });
  const [filters, setFilters] = useState({ phone: false, email: false, website: false });
  const [searching, setSearching] = useState(false);
  const [runId, setRunId] = useState(null);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const handleChange = (e) => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!form.niche.trim()) { setError('Niche is required'); return; }
    setSearching(true);
    setError(null);
    setResults(null);
    try {
      const data = await searchLeads(form.niche, {
        city: form.city || undefined,
        country: form.country || undefined,
        keyword: form.keyword || undefined,
        category: form.category || undefined,
        limit: parseInt(form.limit) || 25,
      });
      setRunId(data.run_id);
      setResults(data);
      setHistory(prev => [{ niche: form.niche, city: form.city, run_id: data.run_id, status: 'running', timestamp: new Date().toLocaleString() }, ...prev]);

      // Poll status
      if (data.run_id) {
        const poll = setInterval(async () => {
          try {
            const s = await getLeadFinderStatus(data.run_id);
            setStatus(s);
            if (s.status === 'completed' || s.status === 'failed') {
              clearInterval(poll);
              setHistory(prev => prev.map(h => h.run_id === data.run_id ? { ...h, status: s.status } : h));
            }
          } catch {}
        }, 3000);
        setTimeout(() => clearInterval(poll), 120000);
      }
    } catch (err) {
      setError(err.message);
      setHistory(prev => [{ niche: form.niche, city: form.city, status: 'failed', error: err.message, timestamp: new Date().toLocaleString() }, ...prev]);
    } finally {
      setSearching(false);
    }
  };

  const hasPhoneFilter = filters.phone || form.keyword;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">AI Research</h1>
          <p className="text-sm text-gray-400 mt-1">Find & research leads using Google Places API</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-ghost flex items-center gap-2">
          {showForm ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          {showForm ? 'Hide' : 'Show'} Search Form
        </button>
      </div>

      {/* Search Form */}
      {showForm && (
        <form onSubmit={handleSearch} className="glass-card space-y-5">
          <div className="flex items-center gap-2 text-primary-300">
            <Sparkles size={18} />
            <h2 className="text-sm font-semibold text-white">Find New Leads</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="sm:col-span-2 lg:col-span-1">
              <label className="block text-sm text-gray-300 mb-1">Niche / Industry *</label>
              <div className="relative">
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input name="niche" value={form.niche} onChange={handleChange} required className="input-field pl-10" placeholder="e.g. Dentist, Plumber, Real Estate" />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-300 mb-1">City</label>
              <div className="relative">
                <MapPin size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input name="city" value={form.city} onChange={handleChange} className="input-field pl-10" placeholder="e.g. San Francisco" />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-300 mb-1">Country</label>
              <div className="relative">
                <Globe size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input name="country" value={form.country} onChange={handleChange} className="input-field pl-10" placeholder="e.g. US" />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-300 mb-1">Keyword</label>
              <input name="keyword" value={form.keyword} onChange={handleChange} className="input-field" placeholder="e.g. cosmetic, emergency" />
            </div>
            <div>
              <label className="block text-sm text-gray-300 mb-1">Category</label>
              <input name="category" value={form.category} onChange={handleChange} className="input-field" placeholder="e.g. dental_clinic" />
            </div>
            <div>
              <label className="block text-sm text-gray-300 mb-1">Max Leads</label>
              <select name="limit" value={form.limit} onChange={handleChange} className="input-field">
                <option value={10}>10</option>
                <option value={25}>25</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
                <option value={250}>250</option>
              </select>
            </div>
          </div>

          {/* Data filters */}
          <div>
            <p className="text-sm text-gray-400 mb-2">Collect the following data for each lead:</p>
            <div className="flex flex-wrap gap-4">
              <label className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                <input type="checkbox" checked={filters.phone} onChange={e => setFilters(prev => ({ ...prev, phone: e.target.checked }))} className="rounded border-gray-600 bg-surface-light text-primary focus:ring-primary" />
                <Phone size={14} /> Phone Number
              </label>
              <label className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                <input type="checkbox" checked={filters.email} onChange={e => setFilters(prev => ({ ...prev, email: e.target.checked }))} className="rounded border-gray-600 bg-surface-light text-primary focus:ring-primary" />
                <Mail size={14} /> Email Address
              </label>
              <label className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                <input type="checkbox" checked={filters.website} onChange={e => setFilters(prev => ({ ...prev, website: e.target.checked }))} className="rounded border-gray-600 bg-surface-light text-primary focus:ring-primary" />
                <LinkIcon size={14} /> Website
              </label>
            </div>
          </div>

          {error && <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-sm text-red-400">{error}</div>}

          <div className="flex items-center gap-3 pt-2">
            <button type="submit" disabled={searching} className="btn-primary flex items-center gap-2">
              {searching ? <Loader size={16} className="animate-spin" /> : <Search size={16} />}
              {searching ? 'Searching...' : 'Find Leads via Google Places'}
            </button>
            {runId && status?.status === 'running' && (
              <span className="flex items-center gap-2 text-sm text-amber-400">
                <Loader size={14} className="animate-spin" /> Processing...
              </span>
            )}
          </div>
        </form>
      )}

      {/* Search results */}
      {results && (
        <div className="glass-card">
          <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
            <CheckCircle size={16} className="text-emerald-400" /> Lead Finder Results
          </h3>
          <p className="text-sm text-gray-400 mb-3">
            Run ID: {results.run_id} · Status: {status?.status || 'submitted'} · {results.leads_found ?? results.total ?? '—'} leads discovered
          </p>
          {results.leads_found === 0 && (
            <EmptyState title="No leads found" description="Try adjusting your niche, city, or search terms." icon={Search} />
          )}
        </div>
      )}

      {/* Search History */}
      {history.length > 0 && (
        <div className="glass-card !p-0 overflow-hidden">
          <div className="px-4 py-3 border-b border-white/5">
            <h3 className="text-sm font-semibold text-white">Search History</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-xs text-gray-400 uppercase tracking-wider">
                  <th className="text-left px-4 py-2 font-medium">Niche</th>
                  <th className="text-left px-4 py-2 font-medium">City</th>
                  <th className="text-left px-4 py-2 font-medium">Status</th>
                  <th className="text-left px-4 py-2 font-medium">Run ID</th>
                  <th className="text-left px-4 py-2 font-medium">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {history.map((h, i) => {
                  const StatusIcon = statusIcon[h.status] || Clock;
                  return (
                    <tr key={i} className="hover:bg-white/5 transition-colors text-sm">
                      <td className="px-4 py-2 text-white">{h.niche}</td>
                      <td className="px-4 py-2 text-gray-400">{h.city || '—'}</td>
                      <td className="px-4 py-2">
                        <Badge variant={statusVariant[h.status] || 'default'} className="gap-1">
                          <StatusIcon size={12} /> {h.status}
                        </Badge>
                      </td>
                      <td className="px-4 py-2 text-gray-400 font-mono text-xs">{h.run_id || '—'}</td>
                      <td className="px-4 py-2 text-gray-500">{h.timestamp}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Research history */}
      <div className="glass-card !p-0 overflow-hidden">
        <div className="px-4 py-3 border-b border-white/5">
          <h3 className="text-sm font-semibold text-white">Research History</h3>
        </div>
        <EmptyState title="Research leads first" description="Use the form above to find and research new leads via Google Places API." icon={Sparkles} />
      </div>
    </div>
  );
}
