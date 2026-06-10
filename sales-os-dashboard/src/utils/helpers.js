export function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric',
  });
}

export function formatTime(dateStr) {
  return new Date(dateStr).toLocaleTimeString('en-US', {
    hour: '2-digit', minute: '2-digit',
  });
}

export function statusColor(status) {
  const map = { Hot: 'text-red-400 bg-red-400/10', Warm: 'text-amber-400 bg-amber-400/10', Cold: 'text-gray-400 bg-gray-400/10' };
  return map[status] || map.Cold;
}

export function scoreColor(score) {
  if (score >= 80) return 'text-emerald-400';
  if (score >= 60) return 'text-amber-400';
  return 'text-gray-400';
}

export function stageColor(stage) {
  const map = {
    new: 'bg-gray-500/20 text-gray-300',
    researching: 'bg-blue-500/20 text-blue-300',
    contacted: 'bg-purple-500/20 text-purple-300',
    qualified: 'bg-indigo-500/20 text-indigo-300',
    converted: 'bg-emerald-500/20 text-emerald-300',
  };
  return map[stage] || map.new;
}

export function healthColor(status) {
  const map = { healthy: 'text-emerald-400', warning: 'text-amber-400', degraded: 'text-red-400', good: 'text-emerald-400' };
  return map[status] || map.healthy;
}

export function eventIcon(type) {
  const map = {
    'lead.created': 'UserPlus', 'research.completed': 'Search', 'call.completed': 'Phone',
    'lead.qualified': 'Award', 'follow_up.sent': 'Send', 'lead.updated': 'Edit',
    'call.scheduled': 'Calendar',
  };
  return map[type] || 'Circle';
}
