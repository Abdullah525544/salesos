import { useState } from 'react';
import { Phone, ThumbsUp, AlertTriangle, Lightbulb, CheckCircle, XCircle } from 'lucide-react';
import { callIntelligence } from '../data/mockData';
import Badge from '../components/ui/Badge';

const bantLabels = { budget: 'Budget', authority: 'Authority', need: 'Need', timeline: 'Timeline' };

export default function CallIntelligence() {
  const [selected, setSelected] = useState(callIntelligence[0]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Call Intelligence</h1>
        <p className="text-sm text-gray-400 mt-1">AI-analyzed call transcripts and insights</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Call list */}
        <div className="lg:col-span-1 space-y-2">
          {callIntelligence.map(call => (
            <button key={call.id} onClick={() => setSelected(call)} className={`w-full text-left glass-card !p-4 transition-colors ${selected?.id === call.id ? 'border-primary/50' : ''}`}>
              <p className="text-sm font-medium text-white">{call.lead}</p>
              <div className="flex items-center gap-3 mt-2 text-xs text-gray-400">
                <span>{call.date}</span>
                <span>{call.duration}</span>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-emerald-400 text-sm font-semibold">{call.sentiment}/10</span>
                <div className="flex-1 h-1.5 bg-surface-light rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${call.sentiment * 10}%` }} />
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* Detail */}
        <div className="lg:col-span-2 space-y-6">
          {selected && (
            <>
              {/* BANT */}
              <div className="glass-card">
                <h3 className="text-sm font-semibold text-white mb-4">BANT Scoring</h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {Object.entries(selected.bant).map(([key, val]) => (
                    <div key={key} className={`p-3 rounded-lg text-center ${val ? 'bg-emerald-500/10 border border-emerald-500/20' : 'bg-red-500/10 border border-red-500/20'}`}>
                      <div className="flex justify-center mb-1">
                        {val ? <CheckCircle size={18} className="text-emerald-400" /> : <XCircle size={18} className="text-red-400" />}
                      </div>
                      <p className={`text-xs font-medium ${val ? 'text-emerald-300' : 'text-red-300'}`}>{bantLabels[key]}</p>
                      <p className={`text-xs ${val ? 'text-emerald-400' : 'text-red-400'}`}>{val ? 'Confirmed' : 'Missing'}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Sentiment & Objections */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="glass-card">
                  <div className="flex items-center gap-2 mb-3">
                    <ThumbsUp size={16} className="text-emerald-400" />
                    <h3 className="text-sm font-semibold text-white">Sentiment Analysis</h3>
                  </div>
                  <p className="text-3xl font-bold text-emerald-400">{selected.sentiment}/10</p>
                  <div className="mt-2 h-2 bg-surface-light rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${selected.sentiment * 10}%` }} />
                  </div>
                </div>
                <div className="glass-card">
                  <div className="flex items-center gap-2 mb-3">
                    <AlertTriangle size={16} className="text-amber-400" />
                    <h3 className="text-sm font-semibold text-white">Objections</h3>
                  </div>
                  {selected.objections.length > 0 ? (
                    <ul className="space-y-1">
                      {selected.objections.map((o, i) => (
                        <li key={i} className="text-sm text-gray-400">• {o}</li>
                      ))}
                    </ul>
                  ) : <p className="text-sm text-emerald-400">No objections raised</p>}
                </div>
              </div>

              {/* Transcript */}
              <div className="glass-card">
                <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
                  <Phone size={16} className="text-primary-300" /> Transcript
                </h3>
                <div className="bg-surface-light/30 rounded-lg p-4">
                  <pre className="text-sm text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">{selected.transcript}</pre>
                </div>
              </div>

              {/* Recommendations */}
              <div className="glass-card">
                <div className="flex items-center gap-2 mb-3">
                  <Lightbulb size={16} className="text-amber-400" />
                  <h3 className="text-sm font-semibold text-white">AI Recommendations</h3>
                </div>
                <div className="space-y-2">
                  {selected.recommendations.map((rec, i) => (
                    <div key={i} className="flex items-center gap-3 p-3 rounded-lg bg-surface-light/30">
                      <Badge variant="primary">{i + 1}</Badge>
                      <p className="text-sm text-gray-300">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
