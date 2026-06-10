import KanbanBoard from '../components/kanban/KanbanBoard';
import { kanbanStages } from '../data/mockData';

export default function Pipeline() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Pipeline</h1>
        <p className="text-sm text-gray-400 mt-1">Drag & drop leads through sales stages</p>
      </div>
      <KanbanBoard stages={kanbanStages} />
    </div>
  );
}
