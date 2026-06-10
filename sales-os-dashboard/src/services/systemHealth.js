import api from './api';

export async function checkSystemHealth() {
  const res = await api.get('/health', { baseURL: 'http://localhost:8000/api/v1' });
  return res.data;
}
