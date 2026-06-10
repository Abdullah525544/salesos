import api from './api';

export async function fetchAnalytics() {
  const res = await api.get('/analytics');
  return res.data;
}
