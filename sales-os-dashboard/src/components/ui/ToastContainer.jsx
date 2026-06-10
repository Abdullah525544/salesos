import { motion, AnimatePresence } from 'framer-motion';
import { useToastContext } from '../../contexts/ToastContext';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

const icons = {
  success: CheckCircle, error: AlertCircle, info: Info, warning: AlertTriangle,
};

const colors = {
  success: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400',
  error: 'border-red-500/30 bg-red-500/10 text-red-400',
  info: 'border-blue-500/30 bg-blue-500/10 text-blue-400',
  warning: 'border-amber-500/30 bg-amber-500/10 text-amber-400',
};

export default function ToastContainer() {
  const { toasts, removeToast } = useToastContext() || { toasts: [], removeToast: () => {} };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2 max-w-sm">
      <AnimatePresence>
        {toasts.map(t => {
          const Icon = icons[t.type] || Info;
          return (
            <motion.div
              key={t.id}
              initial={{ opacity: 0, x: 100, scale: 0.9 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 100, scale: 0.9 }}
              className={`glass border rounded-xl p-4 flex items-start gap-3 ${colors[t.type] || colors.info}`}
            >
              <Icon size={18} className="flex-shrink-0 mt-0.5" />
              <p className="text-sm flex-1">{t.message}</p>
              <button onClick={() => removeToast(t.id)} className="flex-shrink-0 opacity-60 hover:opacity-100">
                <X size={14} />
              </button>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
