import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, MapPin, Globe, Star, Building2, TrendingUp } from 'lucide-react';
import { fetchLead } from '../services/leads';
import { leadDetail as mockLead, leads as mockLeads } from '../data/mockData';
import Badge from '../components/ui/Badge';
import Skeleton from '../components/ui/Skeleton';
import EmptyState from '../components/ui/EmptyState';

export default function LeadDetail() {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchLead(id)
      .then(setLead)
      .catch(() => {
        // Fall back to mock data
        const found = mockLeads.find(l => l.id === parseInt(id));
        setLead(found || (parseInt(id) === 1 ? mockLead : null));
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="space-y-6"><Skeleton className="h-48" /><Skeleton className="h-64" /></div>;
  if (!lead) return <EmptyState title="Lead not found" description="This lead does not exist." />;

  const name = lead.business_name || lead.name;
  const contact = lead.contact_name || lead.company;
  const email = lead.email;
  const phone = lead.phone_number || lead.phone;
  const website = lead.website;
  const city = lead.city;
  const country = lead.country;
  const niche = lead.niche || lead.industry;
  const rating = lead.google_rating || lead.rating;
  const source = lead.lead_source || lead.source || 'manual';
  const score = lead.quality_score ?? lead.score ?? 0;
  const classification = (lead.classification || lead.status || 'cold').toLowerCase();
  const stage = lead.pipeline_stage || 'new_lead';
  const qualScore = lead.qualification_score;
  const nextAction = lead.next_action || 'Review';
  const researchStatus = lead.research_status || 'pending';
  const createdAt = lead.created_at;
  const ai = lead.aiInsights;

  return (
    <div className="space-y-6">
      <Link to="/leads" className="inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors">
        <ArrowLeft size={16} /> Back to Leads
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <div className="glass-card">
            <div className="flex items-start gap-4">
              <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center text-xl font-bold text-primary-300 flex-shrink-0">
                {(name || '?').split(' ').map(n => n[0]).join('').slice(0, 2)}
              </div>
              <div>
                <h2 className="text-lg font-bold text-white">{name}</h2>
                <p className="text-sm text-gray-400">{contact || 'No contact'}</p>
                <div className="flex items-center gap-2 mt-2">
                  <Badge variant={classification}>{classification}</Badge>
                  <span className="text-sm font-semibold text-emerald-400">{score}/100</span>
                </div>
              </div>
            </div>
          </div>

          <div className="glass-card space-y-4">
            <h3 className="text-sm font-semibold text-white">Contact Info</h3>
            <div className="space-y-3 text-sm">
              {city && <div className="flex items-center gap-3 text-gray-400"><MapPin size={16} /><span>{city}{country ? `, ${country}` : ''}</span></div>}
              {niche && <div className="flex items-center gap-3 text-gray-400"><Building2 size={16} /><span>{niche}</span></div>}
              {website && <div className="flex items-center gap-3 text-gray-400"><Globe size={16} /><a href={website} className="text-primary-300 hover:underline truncate">{website}</a></div>}
              {rating && <div className="flex items-center gap-3 text-gray-400"><Star size={16} className="text-amber-400" /><span>{rating}/5</span></div>}
              {email && <p className="text-gray-300">{email}</p>}
              {phone && <p className="text-gray-300">{phone}</p>}
            </div>
            <div className="pt-3 border-t border-white/5">
              <p className="text-xs text-gray-500">Source: <span className="text-gray-300">{source}</span></p>
              <p className="text-xs text-gray-500 mt-1">Stage: <span className="text-gray-300">{stage.replace(/_/g, ' ')}</span></p>
              {createdAt && <p className="text-xs text-gray-500 mt-1">Created: <span className="text-gray-300">{new Date(createdAt).toLocaleDateString()}</span></p>}
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <div className="glass-card">
            <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
              <TrendingUp size={16} className="text-primary-300" /> AI Insights
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
              <div className="text-center p-4 rounded-lg bg-surface-light/30">
                <p className="text-2xl font-bold text-emerald-400">{qualScore ?? '—'}/100</p>
                <p className="text-xs text-gray-400 mt-1">Qualification Score</p>
              </div>
              <div className="text-center p-4 rounded-lg bg-surface-light/30">
                <p className="text-2xl font-bold text-primary-300">{nextAction}</p>
                <p className="text-xs text-gray-400 mt-1">Next Action</p>
              </div>
              <div className="text-center p-4 rounded-lg bg-surface-light/30">
                <p className="text-2xl font-bold text-amber-400">{researchStatus}</p>
                <p className="text-xs text-gray-400 mt-1">Research Status</p>
              </div>
            </div>
            {ai && (
              <div className="space-y-3">
                <p className="text-sm text-gray-400"><strong className="text-gray-300">Sentiment:</strong> {ai.sentiment}/10</p>
                <p className="text-sm text-gray-400"><strong className="text-gray-300">Suggested:</strong> {ai.suggestedAction}</p>
                <p className="text-sm text-gray-400"><strong className="text-gray-300">Pain Points:</strong> {ai.painPoints?.join(', ') || 'None'}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
