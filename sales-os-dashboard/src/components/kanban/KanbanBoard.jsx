import { useState } from 'react';
import { motion } from 'framer-motion';
import Badge from '../ui/Badge';

export default function KanbanBoard({ stages }) {
  const [items, setItems] = useState(stages);
  const [draggedItem, setDraggedItem] = useState(null);

  const handleDragStart = (item, stageId) => {
    setDraggedItem({ ...item, fromStage: stageId });
  };

  const handleDrop = (toStageId) => {
    if (!draggedItem || draggedItem.fromStage === toStageId) {
      setDraggedItem(null);
      return;
    }
    setItems(prev => {
      const next = prev.map(stage => {
        if (stage.id === draggedItem.fromStage) {
          return { ...stage, items: stage.items.filter(i => i.id !== draggedItem.id) };
        }
        if (stage.id === toStageId) {
          return { ...stage, items: [...stage.items, { ...draggedItem, id: `${draggedItem.id}_${Date.now()}` }] };
        }
        return stage;
      });
      return next;
    });
    setDraggedItem(null);
  };

  const priorityVariant = { high: 'high', medium: 'medium', low: 'low' };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 overflow-x-auto pb-4">
      {items.map(stage => (
        <div
          key={stage.id}
          onDragOver={e => e.preventDefault()}
          onDrop={() => handleDrop(stage.id)}
          className="bg-surface-light/30 rounded-xl p-3 min-w-[220px]"
        >
          <div className="flex items-center justify-between mb-3 px-1">
            <h3 className="text-sm font-semibold text-gray-300">{stage.title}</h3>
            <span className="text-xs text-gray-500 bg-white/5 px-2 py-0.5 rounded-full">{stage.items.length}</span>
          </div>
          <div className="space-y-2 min-h-[100px]">
            {stage.items.map(item => (
              <motion.div
                key={item.id}
                layout
                draggable
                onDragStart={() => handleDragStart(item, stage.id)}
                className="glass-card !p-3 cursor-grab active:cursor-grabbing hover:border-primary/30 transition-colors"
              >
                <p className="text-sm font-medium text-white truncate">{item.title}</p>
                <div className="flex items-center justify-between mt-2">
                  <Badge variant={priorityVariant[item.priority]}>{item.priority}</Badge>
                  <span className="text-xs text-gray-500">{item.score}</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">{item.assignee}</p>
              </motion.div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
