import { Inbox } from 'lucide-react';

export default function EmptyState({ title = 'No data yet', description = 'Items will appear here once available.', icon: Icon = Inbox }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <Icon size={48} className="text-gray-600 mb-4" />
      <h3 className="text-lg font-medium text-gray-300">{title}</h3>
      <p className="text-sm text-gray-500 mt-1 max-w-sm">{description}</p>
    </div>
  );
}
