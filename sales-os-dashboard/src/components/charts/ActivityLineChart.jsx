import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card !p-3 !rounded-lg text-sm">
      <p className="text-white font-medium mb-1">{label}</p>
      {payload.map((p, i) => (
        <p key={i} className="text-gray-400">{p.name}: {p.value}</p>
      ))}
    </div>
  );
};

export default function ActivityLineChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis dataKey="day" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
        <YAxis tick={{ fill: '#9CA3AF', fontSize: 12 }} />
        <Tooltip content={<CustomTooltip />} />
        <Legend wrapperStyle={{ fontSize: 12, color: '#9CA3AF' }} />
        <Line type="monotone" dataKey="leads" stroke="#4F46E5" strokeWidth={2} dot={{ fill: '#4F46E5', r: 4 }} activeDot={{ r: 6 }} />
        <Line type="monotone" dataKey="calls" stroke="#10B981" strokeWidth={2} dot={{ fill: '#10B981', r: 4 }} />
        <Line type="monotone" dataKey="followups" stroke="#8B5CF6" strokeWidth={2} dot={{ fill: '#8B5CF6', r: 4 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}
