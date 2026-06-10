import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Phone, Search as SearchIcon, Eye, RefreshCw } from 'lucide-react';
import { fetchLeads } from '../services/leads';
import { leads as mockLeads } from '../data/mockData';
import Badge from '../components/ui/Badge';
import Skeleton from '../components/ui/Skeleton';
import EmptyState from '../components/ui/EmptyState';
import { scoreColor } from '../utils/helpers';

export default function Leads() {
  const [leads, setLeads] = useState([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [usingMock, setUsingMock] = useState(false);

  const load = () => {
    setLoading(true);
    fetchLeads({ search: search || undefined, classification: statusFilter !== 'all' ? statusFilter : undefined })
      .then(data => { setLeads(data.leads || []); setTotal(data.total || 0); setUsingMock(false); })
      .catch(() => {
        // Fall back to mock data
        let filtered = [...mockLeads];
        if (search) filtered = filtered.filter(l => l.name.toLowerCase().includes(search.toLowerCase()) || l.company.toLowerCase().includes(search.toLowerCase()));
        if (statusFilter !== 'all') filtered = filtered.filter(l => l.status.toLowerCase() === statusFilter);
        setLeads(filtered);
        setTotal(filtered.length);
        setUsingMock(true);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [search, statusFilter]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Leads</h1>
          <p className="text-sm text-gray-400 mt-1">{total} total leads{usingMock ? ' (offline mode)' : ''}</p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={load} className="btn-ghost"><RefreshCw size={16} /></button>
          <Link to="/leads/create" className="btn-primary">+ Add Lead</Link>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <div className="relative flex-1 max-w-xs">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input type="text" placeholder="Search leads..." value={search} onChange={e => setSearch(e.target.value)} className="input-field pl-10" />
        </div>
        <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} className="input-field w-auto">
          <option value="all">All Status</option>
          <option value="hot">Hot</option>
          <option value="warm">Warm</option>
          <option value="cold">Cold</option>
        </select>
      </div>

      {loading ? (
        <div className="space-y-2"><Skeleton className="h-12" count={5} /></div>
      ) : leads.length === 0 ? (
        <EmptyState title="No leads found" description="Leads will appear here once discovered or imported." />
      ) : (
        <div className="glass-card !p-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/5 text-xs text-gray-400 uppercase tracking-wider">
                  <th className="text-left px-4 py-3 font-medium">Name / Company</th>
                  <th className="text-left px-4 py-3 font-medium">Contact</th>
                  <th className="text-left px-4 py-3 font-medium">Score</th>
                  <th className="text-left px-4 py-3 font-medium">Status</th>
                  <th className="text-left px-4 py-3 font-medium">{usingMock ? 'Last Activity' : 'Stage'}</th>
                  <th className="text-right px-4 py-3 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {leads.map((lead, i) => {
                  const name = lead.business_name || lead.name;
                  const company = lead.contact_name || lead.company;
                  const score = lead.quality_score ?? lead.score ?? 0;
                  const status = lead.classification || lead.status || 'Cold';
                  const stage = lead.pipeline_stage || lead.lastActivity || '—';
                  return (
                    <tr key={lead.id || i} className="hover:bg-white/5 transition-colors">
                      <td className="px-4 py-3">
                        <Link to={`/leads/${lead.id || i + 1}`} className="text-sm font-medium text-white hover:text-primary-300 transition-colors">{name}</Link>
                        <p className="text-xs text-gray-400">{company || '—'}</p>
                      </td>
                      <td className="px-4 py-3">
                        <p className="text-sm text-gray-300">{lead.email || '—'}</p>
                        <p className="text-xs text-gray-500">{lead.phone_number || lead.phone || '—'}</p>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`text-sm font-semibold ${scoreColor(score)}`}>{score}</span>
                      </td>
                      <td className="px-4 py-3">
                        <Badge variant={status.toLowerCase()}>{status}</Badge>
                      </td>
                      <td className="px-4 py-3 text-xs text-gray-400">{stage}</td>
                      <td className="px-4 py-3 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Link to={`/leads/${lead.id || i + 1}`} className="btn-ghost p-1.5"><Eye size={16} /></Link>
                          <button className="btn-ghost p-1.5"><Phone size={16} /></button>
                          <button className="btn-ghost p-1.5"><SearchIcon size={16} /></button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
