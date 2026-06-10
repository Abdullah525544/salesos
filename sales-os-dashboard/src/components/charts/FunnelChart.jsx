import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LabelList } from 'recharts';

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="glass-card !p-3 !rounded-lg text-sm">
      <p className="text-white font-medium">{d.name}</p>
      <p className="text-gray-400 mt-1">{d.value} leads</p>
      <p className="text-xs text-gray-500 mt-0.5">{d.fill}</p>
    </div>
  );
};

export default function FunnelChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={data} layout="vertical" margin={{ left: 20, right: 40, top: 10, bottom: 10 }}>
        <XAxis type="number" hide />
        <YAxis type="category" dataKey="name" tick={{ fill: '#9CA3AF', fontSize: 12 }} width={100} />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
        <Bar dataKey="value" radius={[0, 8, 8, 0]} barSize={36}>
          {data.map((entry, i) => (
            <rect key={i} fill={entry.fill} />
          ))}
          <LabelList dataKey="value" position="right" fill="#9CA3AF" fontSize={12} fontWeight={600} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
