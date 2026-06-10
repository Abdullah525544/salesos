import { AlertTriangle } from 'lucide-react';

export default function ErrorState({ message = 'Something went wrong.', onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <AlertTriangle size={48} className="text-red-400 mb-4" />
      <h3 className="text-lg font-medium text-gray-300">Error</h3>
      <p className="text-sm text-gray-500 mt-1">{message}</p>
      {onRetry && (
        <button onClick={onRetry} className="btn-primary mt-4">
          Retry
        </button>
      )}
    </div>
  );
}
