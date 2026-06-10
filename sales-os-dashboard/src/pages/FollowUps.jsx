import { Send, Clock, CheckCircle, FileEdit } from 'lucide-react';
import { followups } from '../data/mockData';
import Badge from '../components/ui/Badge';
import { formatDate } from '../utils/helpers';

const statusVariant = { pending: 'warning', scheduled: 'info', draft: 'default', completed: 'success' };
const statusIcon = { pending: Clock, scheduled: Clock, draft: FileEdit, completed: CheckCircle };
const priorityVariant = { high: 'high', medium: 'medium', low: 'low' };

export default function FollowUps() {
  const now = new Date();
  const overdue = followups.filter(f => f.status === 'pending' && new Date(f.due) < now);
  const upcoming = followups.filter(f => f.status !== 'completed');

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Follow-ups</h1>
          <p className="text-sm text-gray-400 mt-1">
            {overdue.length > 0 ? (
              <span className="text-red-400">{overdue.length} overdue</span>
            ) : 'All caught up'}
            {' · '}{upcoming.length} pending
          </p>
        </div>
        <button className="btn-primary"><Send size={16} className="mr-2 inline" /> New Follow-up</button>
      </div>

      <div className="space-y-3">
        {followups.map(fu => {
          const StatusIcon = statusIcon[fu.status] || Clock;
          const isOverdue = fu.status === 'pending' && new Date(fu.due) < now;
          return (
            <div key={fu.id} className={`glass-card !p-4 flex items-start gap-4 ${isOverdue ? 'border-red-500/20' : ''}`}>
              <div className={`p-2 rounded-lg ${isOverdue ? 'bg-red-500/20 text-red-400' : 'bg-primary/20 text-primary-300'}`}>
                <StatusIcon size={18} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white">{fu.lead}</p>
                <p className="text-sm text-gray-400 mt-0.5">{fu.type}</p>
                <div className="flex items-center gap-3 mt-2">
                  <Badge variant={priorityVariant[fu.priority]}>{fu.priority}</Badge>
                  <Badge variant={statusVariant[fu.status]}>{fu.status}</Badge>
                  {isOverdue && <span className="text-xs text-red-400 font-medium">Overdue</span>}
                </div>
              </div>
              <div className="text-right flex-shrink-0">
                <p className="text-xs text-gray-400">{formatDate(fu.due)}</p>
                <p className="text-xs text-gray-500">{new Date(fu.due).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
