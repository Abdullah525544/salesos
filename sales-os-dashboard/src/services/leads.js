import api from './api';

export async function fetchLeads(params = {}) {
  const res = await api.get('/leads', { params });
  return res.data;
}

export async function fetchLead(id) {
  const res = await api.get(`/leads/${id}`);
  return res.data;
}

export async function createLead(data) {
  const res = await api.post('/leads', data);
  return res.data;
}

export async function deleteLead(id) {
  await api.delete(`/leads/${id}`);
}

export async function searchLeads(niche, options = {}) {
  const res = await api.post('/lead-finder/search', { niche, ...options });
  return res.data;
}

export async function getLeadFinderStatus(runId) {
  const res = await api.get(`/lead-finder/status/${runId}`);
  return res.data;
}

export async function researchLead(leadId) {
  const res = await api.post(`/research/analyze/${leadId}`);
  return res.data;
}

export async function createCall(data) {
  const res = await api.post('/calls', data);
  return res.data;
}

export async function analyzeCall(callId, data) {
  const res = await api.post(`/calls/${callId}/analyze`, data);
  return res.data;
}

export async function scheduleFollowUp(leadId, data) {
  const res = await api.post(`/leads/${leadId}/follow-up`, data);
  return res.data;
}

export async function dispatchFollowUp(leadId) {
  const res = await api.post(`/leads/${leadId}/follow-up/dispatch`);
  return res.data;
}
