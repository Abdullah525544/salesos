import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Plus } from 'lucide-react';
import { createLead } from '../services/leads';

export default function LeadCreate() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    business_name: '', contact_name: '', email: '', phone_number: '',
    website: '', address: '', city: '', country: '', niche: '',
    google_rating: '', lead_source: 'manual',
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.business_name.trim()) { setError('Business name is required'); return; }
    setSaving(true);
    setError(null);
    try {
      const lead = await createLead({
        ...form,
        google_rating: form.google_rating ? parseFloat(form.google_rating) : undefined,
      });
      navigate(`/leads/${lead.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Link to="/leads" className="inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors">
        <ArrowLeft size={16} /> Back to Leads
      </Link>

      <div>
        <h1 className="text-2xl font-bold text-white">Add Lead</h1>
        <p className="text-sm text-gray-400 mt-1">Create a new lead manually</p>
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-sm text-red-400">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="glass-card space-y-5">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="sm:col-span-2">
            <label className="block text-sm text-gray-300 mb-1">Business Name *</label>
            <input name="business_name" value={form.business_name} onChange={handleChange} required className="input-field" placeholder="e.g. BrightStar Dental" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Contact Name</label>
            <input name="contact_name" value={form.contact_name} onChange={handleChange} className="input-field" placeholder="Dr. Sarah Chen" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Email</label>
            <input name="email" type="email" value={form.email} onChange={handleChange} className="input-field" placeholder="sarah@example.com" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Phone</label>
            <input name="phone_number" value={form.phone_number} onChange={handleChange} className="input-field" placeholder="+1 (415) 555-0101" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Website</label>
            <input name="website" value={form.website} onChange={handleChange} className="input-field" placeholder="https://brightstardental.com" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Niche / Industry</label>
            <input name="niche" value={form.niche} onChange={handleChange} className="input-field" placeholder="Dentist" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">City</label>
            <input name="city" value={form.city} onChange={handleChange} className="input-field" placeholder="San Francisco" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Country</label>
            <input name="country" value={form.country} onChange={handleChange} className="input-field" placeholder="US" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Google Rating</label>
            <input name="google_rating" type="number" step="0.1" min="0" max="5" value={form.google_rating} onChange={handleChange} className="input-field" placeholder="4.5" />
          </div>
          <div>
            <label className="block text-sm text-gray-300 mb-1">Source</label>
            <select name="lead_source" value={form.lead_source} onChange={handleChange} className="input-field">
              <option value="manual">Manual</option>
              <option value="google_places">Google Places</option>
              <option value="referral">Referral</option>
              <option value="website">Website</option>
              <option value="linkedin">LinkedIn</option>
              <option value="conference">Conference</option>
            </select>
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm text-gray-300 mb-1">Address</label>
            <input name="address" value={form.address} onChange={handleChange} className="input-field" placeholder="123 Market St, San Francisco, CA" />
          </div>
        </div>

        <div className="flex items-center gap-3 pt-4 border-t border-white/5">
          <button type="submit" disabled={saving} className="btn-primary flex items-center gap-2">
            <Plus size={16} /> {saving ? 'Saving...' : 'Create Lead'}
          </button>
          <Link to="/leads" className="btn-ghost">Cancel</Link>
        </div>
      </form>
    </div>
  );
}
